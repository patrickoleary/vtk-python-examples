#!/usr/bin/env python

# Interactive demo of a quadratic tetrahedron.  A slider adjusts the chord
# error of vtkTessellatorFilter and the text overlay shows the resulting
# cell count in real time.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkCommand,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkQuadraticTetra,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkTessellatorFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
    vtkSliderWidget,
)
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


# Data: build a quadratic tetrahedron with slightly perturbed node positions
tetra_cell = vtkQuadraticTetra()
points = vtkPoints()
pcoords = tetra_cell.GetParametricCoords()
rng = vtkMinimalStandardRandomSequence()
points.SetNumberOfPoints(tetra_cell.GetNumberOfPoints())
rng.SetSeed(5070)
for i in range(tetra_cell.GetNumberOfPoints()):
    perturbation = [0.0] * 3
    for j in range(3):
        rng.Next()
        perturbation[j] = rng.GetRangeValue(-0.2, 0.2)
    tetra_cell.GetPointIds().SetId(i, i)
    points.SetPoint(i, pcoords[3 * i] + perturbation[0],
                    pcoords[3 * i + 1] + perturbation[1],
                    pcoords[3 * i + 2] + perturbation[2])

unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.SetPoints(points)
unstructured_grid.InsertNextCell(tetra_cell.GetCellType(), tetra_cell.GetPointIds())

# Filter: tessellate the quadratic cell into linear elements
tessellate = vtkTessellatorFilter()
tessellate.SetInputData(unstructured_grid)
tessellate.SetChordError(0.035)
tessellate.Update()

# Mapper and actor: tessellated tetrahedron with edges
tetra_mapper = vtkDataSetMapper()
tetra_mapper.SetInputConnection(tessellate.GetOutputPort())
tetra_mapper.ScalarVisibilityOff()

tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.GetProperty().SetDiffuseColor(tomato_rgb)
tetra_actor.GetProperty().SetEdgeColor(ivory_black_rgb)
tetra_actor.GetProperty().EdgeVisibilityOn()

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
renderer.AddActor(tetra_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(slate_gray_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 512)
render_window.SetWindowName("QuadraticTetraApp")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Widget: slider to control chord error
slider_rep = vtkSliderRepresentation2D()
slider_rep.SetMinimumValue(0.0)
slider_rep.SetMaximumValue(0.07)
slider_rep.SetValue(tessellate.GetChordError())
slider_rep.SetTitleText("Chord error")
slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint1Coordinate().SetValue(0.1, 0.1)
slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint2Coordinate().SetValue(0.9, 0.1)
slider_rep.SetTubeWidth(0.008)
slider_rep.SetSliderLength(0.008)
slider_rep.SetTitleHeight(0.04)
slider_rep.SetLabelHeight(0.04)

slider_widget = vtkSliderWidget()
slider_widget.SetInteractor(render_window_interactor)
slider_widget.SetRepresentation(slider_rep)
slider_widget.SetAnimationModeToAnimate()
slider_widget.EnabledOn()
slider_widget.AddObserver(
    vtkCommand.InteractionEvent,
    lambda obj, ev: (
        tessellate.SetChordError(obj.GetRepresentation().GetValue()),
        tessellate.SetMaximumNumberOfSubdivisions(5),
        tessellate.Update(),
    ),
)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
