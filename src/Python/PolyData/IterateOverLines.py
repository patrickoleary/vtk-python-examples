#!/usr/bin/env python

# Build a polydata with line cells, iterate over them printing connectivity, and render.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
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

# Source: five points connected by four line segments
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 2.0)
points.InsertNextPoint(1.0, 2.0, 3.0)

lines = vtkCellArray()
line0 = vtkLine()
line0.GetPointIds().SetId(0, 0)
line0.GetPointIds().SetId(1, 1)
lines.InsertNextCell(line0)

line1 = vtkLine()
line1.GetPointIds().SetId(0, 1)
line1.GetPointIds().SetId(1, 2)
lines.InsertNextCell(line1)

line2 = vtkLine()
line2.GetPointIds().SetId(0, 2)
line2.GetPointIds().SetId(1, 3)
lines.InsertNextCell(line2)

line3 = vtkLine()
line3.GetPointIds().SetId(0, 3)
line3.GetPointIds().SetId(1, 4)
lines.InsertNextCell(line3)

lines_polydata = vtkPolyData()
lines_polydata.SetPoints(points)
lines_polydata.SetLines(lines)

print(f"There are {lines_polydata.GetNumberOfLines()} lines.")

# Iterate over each line cell and print its point connectivity
lines_polydata.GetLines().InitTraversal()
id_list = vtkIdList()
line_count = 0
while lines_polydata.GetLines().GetNextCell(id_list):
    print(f"Line {line_count} has {id_list.GetNumberOfIds()} points")
    for i in range(id_list.GetNumberOfIds() - 1):
        print(f"  {id_list.GetId(i)} -> {id_list.GetId(i + 1)}")
    line_count += 1

# Mapper: map line cells to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(lines_polydata)

# Actor: render the lines with visible width
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetLineWidth(3)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("IterateOverLines")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
