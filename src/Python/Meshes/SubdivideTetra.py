#!/usr/bin/env python

# Subdivide a single tetrahedron into twelve smaller tetrahedra using
# vtkSubdivideTetra, and display the original and subdivided meshes
# side by side as wireframes with shrunk cells for visibility.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersModeling import vtkSubdivideTetra
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: build a single tetrahedron as an unstructured grid
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.5, 1.0, 0.0)
points.InsertNextPoint(0.5, 0.5, 1.0)

cells = vtkCellArray()
cells.InsertNextCell(4, [0, 1, 2, 3])

ug = vtkUnstructuredGrid()
ug.SetPoints(points)
ug.SetCells(10, cells)  # VTK_TETRA = 10

# Filter: subdivide each tetrahedron into twelve smaller tetrahedra
subdivide = vtkSubdivideTetra()
subdivide.SetInputData(ug)

# Shrink: separate cells for visibility (original)
shrink_original = vtkShrinkFilter()
shrink_original.SetInputData(ug)
shrink_original.SetShrinkFactor(0.8)

# Shrink: separate cells for visibility (subdivided)
shrink_subdivided = vtkShrinkFilter()
shrink_subdivided.SetInputConnection(subdivide.GetOutputPort())
shrink_subdivided.SetShrinkFactor(0.8)

# ---- Left viewport: original tetrahedron ----
original_mapper = vtkDataSetMapper()
original_mapper.SetInputConnection(shrink_original.GetOutputPort())

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(tomato_rgb)
original_actor.GetProperty().EdgeVisibilityOn()
original_actor.GetProperty().SetLineWidth(2)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(original_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: subdivided tetrahedra ----
subdivided_mapper = vtkDataSetMapper()
subdivided_mapper.SetInputConnection(shrink_subdivided.GetOutputPort())

subdivided_actor = vtkActor()
subdivided_actor.SetMapper(subdivided_mapper)
subdivided_actor.GetProperty().SetColor(steel_blue_rgb)
subdivided_actor.GetProperty().EdgeVisibilityOn()
subdivided_actor.GetProperty().SetLineWidth(1)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(subdivided_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("SubdivideTetra")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
