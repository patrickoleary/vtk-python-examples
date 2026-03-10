#!/usr/bin/env python

# Render a quadratic hexahedron with tessellation and node glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkQuadraticHexahedron,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkTessellatorFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
ivory_black_rgb = (0.161, 0.141, 0.129)
banana_rgb = (0.890, 0.812, 0.341)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Data: build a quadratic hexahedron with slightly perturbed node positions
hex_cell = vtkQuadraticHexahedron()
points = vtkPoints()
pcoords = hex_cell.GetParametricCoords()
rng = vtkMinimalStandardRandomSequence()
points.SetNumberOfPoints(hex_cell.GetNumberOfPoints())
rng.SetSeed(5070)
for i in range(hex_cell.GetNumberOfPoints()):
    perturbation = [0.0] * 3
    for j in range(3):
        rng.Next()
        perturbation[j] = rng.GetRangeValue(-0.1, 0.1)
    hex_cell.GetPointIds().SetId(i, i)
    points.SetPoint(i, pcoords[3 * i] + perturbation[0],
                    pcoords[3 * i + 1] + perturbation[1],
                    pcoords[3 * i + 2] + perturbation[2])

unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.SetPoints(points)
unstructured_grid.InsertNextCell(hex_cell.GetCellType(), hex_cell.GetPointIds())

# Filter: tessellate the quadratic cell into linear elements for rendering
tessellate = vtkTessellatorFilter()
tessellate.SetInputData(unstructured_grid)
tessellate.SetMaximumNumberOfSubdivisions(2)

# Mapper and actor: tessellated hexahedron with edges
hex_mapper = vtkDataSetMapper()
hex_mapper.SetInputConnection(tessellate.GetOutputPort())
hex_mapper.ScalarVisibilityOff()

hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)
hex_actor.GetProperty().SetDiffuseColor(tomato_rgb)
hex_actor.GetProperty().SetEdgeColor(ivory_black_rgb)
hex_actor.GetProperty().EdgeVisibilityOn()

# Source: small spheres to mark quadratic node positions
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.02)

# Filter: place a sphere glyph at each node
glyph_3d = vtkGlyph3D()
glyph_3d.SetInputData(unstructured_grid)
glyph_3d.SetSourceConnection(sphere_source.GetOutputPort())
glyph_3d.ScalingOff()
glyph_3d.Update()

glyph_mapper = vtkDataSetMapper()
glyph_mapper.SetInputConnection(glyph_3d.GetOutputPort())
glyph_mapper.ScalarVisibilityOff()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(banana_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(hex_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(slate_gray_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("QuadraticHexahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
