#!/usr/bin/env python

# Build a triangle with per-vertex colours, write it to a .vtp file, and render it.

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
    vtkTriangle,
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

# Source: three vertices of a triangle
points = vtkPoints()
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)

triangles = vtkCellArray()
triangle = vtkTriangle()
triangle.GetPointIds().SetId(0, 0)
triangle.GetPointIds().SetId(1, 1)
triangle.GetPointIds().SetId(2, 2)
triangles.InsertNextCell(triangle)

# Per-vertex colours (unsigned char RGB)
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName("Colors")
colors.InsertNextTuple3(255, 0, 0)
colors.InsertNextTuple3(0, 255, 0)
colors.InsertNextTuple3(0, 0, 255)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(triangles)
polydata.GetPointData().SetScalars(colors)

# Writer: save to VTP
writer = vtkXMLPolyDataWriter()
writer.SetFileName("ColoredTriangle.vtp")
writer.SetInputData(polydata)
writer.Write()

# Mapper: map triangle to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ColoredTriangle")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
