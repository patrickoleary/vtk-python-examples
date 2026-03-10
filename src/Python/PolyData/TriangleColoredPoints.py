#!/usr/bin/env python

# Create three coloured vertex cells at triangle corners, write to a .vtp file, and render.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: three points as individual vertex cells
points = vtkPoints()
vertices = vtkCellArray()

pid = points.InsertNextPoint(1.0, 0.0, 0.0)
vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid)

pid = points.InsertNextPoint(0.0, 0.0, 0.0)
vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid)

pid = points.InsertNextPoint(0.0, 1.0, 0.0)
vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid)

# Per-vertex colours (unsigned char RGB)
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName("Colors")
colors.InsertNextTuple3(255, 0, 0)
colors.InsertNextTuple3(50, 205, 50)
colors.InsertNextTuple3(0, 0, 255)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(vertices)
polydata.GetPointData().SetScalars(colors)

# Writer: save to VTP
writer = vtkXMLPolyDataWriter()
writer.SetFileName("TriangleColoredPoints.vtp")
writer.SetInputData(polydata)
writer.Write()

# Mapper: map vertex cells to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)

# Actor: render the coloured vertices with visible point size
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(10)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TriangleColoredPoints")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
