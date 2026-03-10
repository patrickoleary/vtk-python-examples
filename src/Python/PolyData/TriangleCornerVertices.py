#!/usr/bin/env python

# Create vertex cells at triangle corner positions, write to a .vtp file, and render.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
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
tomato_rgb = (1.000, 0.388, 0.278)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: three points stored as individual vertex cells
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

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(vertices)

# Writer: save to VTP
writer = vtkXMLPolyDataWriter()
writer.SetFileName("TriangleCornerVertices.vtp")
writer.SetInputData(polydata)
writer.Write()

# Mapper: map vertex cells to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)

# Actor: render the vertices with visible point size
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetPointSize(10)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TriangleCornerVertices")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
