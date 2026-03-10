#!/usr/bin/env python

# Demonstrate vtkCellQuality to compute a quality metric for each cell
# of a Delaunay triangulation and color the mesh by quality.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersVerdict import vtkCellQuality
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: random points in a disk
point_source = vtkPointSource()
point_source.SetNumberOfPoints(100)
point_source.SetRadius(1.0)
point_source.SetCenter(0, 0, 0)
point_source.Update()

# Flatten to 2D by zeroing Z
flat_points = vtkPoints()
for i in range(point_source.GetOutput().GetNumberOfPoints()):
    pt = point_source.GetOutput().GetPoint(i)
    flat_points.InsertNextPoint(pt[0], pt[1], 0)

flat_poly = vtkPolyData()
flat_poly.SetPoints(flat_points)

# Filter: Delaunay triangulation
delaunay = vtkDelaunay2D()
delaunay.SetInputData(flat_poly)

# Filter: compute cell quality (aspect ratio)
quality = vtkCellQuality()
quality.SetInputConnection(delaunay.GetOutputPort())
quality.SetQualityMeasureToAspectRatio()
quality.Update()

# Mapper: map the mesh to graphics primitives with quality coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(quality.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SelectColorArray("CellQuality")
mapper.SetScalarRange(quality.GetOutput().GetCellData().GetArray("CellQuality").GetRange())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CellQuality")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
