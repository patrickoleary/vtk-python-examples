#!/usr/bin/env python

# Demonstrate vtkExtractArray by extracting individual sparse arrays from
# a vtkArrayData and visualizing the extracted values as colored bars.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkSparseArray
from vtkmodules.vtkCommonDataModel import vtkArrayData
from vtkmodules.vtkFiltersGeneral import vtkExtractArray
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Create two sparse arrays
sparse_array_a = vtkSparseArray['float64']()
sparse_array_a.Resize(3)
sparse_array_a.AddValue(0, 1.0)
sparse_array_a.AddValue(1, 2.0)
sparse_array_a.AddValue(2, 3.0)

sparse_array_b = vtkSparseArray['float64']()
sparse_array_b.Resize(3)
sparse_array_b.AddValue(0, 4.0)
sparse_array_b.AddValue(1, 5.0)
sparse_array_b.AddValue(2, 6.0)

# Pack into vtkArrayData
factored = vtkArrayData()
factored.AddArray(sparse_array_a)
factored.AddArray(sparse_array_b)

# Extract array 0
extract_0 = vtkExtractArray()
extract_0.SetInputData(factored)
extract_0.SetIndex(0)
extract_0.Update()
arr_a = extract_0.GetOutput().GetArray(0)

# Extract array 1
extract_1 = vtkExtractArray()
extract_1.SetInputData(factored)
extract_1.SetIndex(1)
extract_1.Update()
arr_b = extract_1.GetOutput().GetArray(0)

# Visualize the extracted values as colored bars
# Array A values: 1.0, 2.0, 3.0  Array B values: 4.0, 5.0, 6.0

# Array A bar 0: val=1.0
bar_a_0 = vtkPlaneSource()
bar_a_0.SetOrigin(0.0, 0, 0)
bar_a_0.SetPoint1(1.0, 0, 0)
bar_a_0.SetPoint2(0.0, 1.0, 0)

bar_a_mapper_0 = vtkPolyDataMapper()
bar_a_mapper_0.SetInputConnection(bar_a_0.GetOutputPort())

bar_a_actor_0 = vtkActor()
bar_a_actor_0.SetMapper(bar_a_mapper_0)
bar_a_actor_0.GetProperty().SetColor(1.0, 0.3, 0.3)

# Array A bar 1: val=2.0
bar_a_1 = vtkPlaneSource()
bar_a_1.SetOrigin(1.5, 0, 0)
bar_a_1.SetPoint1(2.5, 0, 0)
bar_a_1.SetPoint2(1.5, 2.0, 0)

bar_a_mapper_1 = vtkPolyDataMapper()
bar_a_mapper_1.SetInputConnection(bar_a_1.GetOutputPort())

bar_a_actor_1 = vtkActor()
bar_a_actor_1.SetMapper(bar_a_mapper_1)
bar_a_actor_1.GetProperty().SetColor(1.0, 0.3, 0.3)

# Array A bar 2: val=3.0
bar_a_2 = vtkPlaneSource()
bar_a_2.SetOrigin(3.0, 0, 0)
bar_a_2.SetPoint1(4.0, 0, 0)
bar_a_2.SetPoint2(3.0, 3.0, 0)

bar_a_mapper_2 = vtkPolyDataMapper()
bar_a_mapper_2.SetInputConnection(bar_a_2.GetOutputPort())

bar_a_actor_2 = vtkActor()
bar_a_actor_2.SetMapper(bar_a_mapper_2)
bar_a_actor_2.GetProperty().SetColor(1.0, 0.3, 0.3)

# Array B bar 0: val=4.0
bar_b_0 = vtkPlaneSource()
bar_b_0.SetOrigin(5.5, 0, 0)
bar_b_0.SetPoint1(6.5, 0, 0)
bar_b_0.SetPoint2(5.5, 4.0, 0)

bar_b_mapper_0 = vtkPolyDataMapper()
bar_b_mapper_0.SetInputConnection(bar_b_0.GetOutputPort())

bar_b_actor_0 = vtkActor()
bar_b_actor_0.SetMapper(bar_b_mapper_0)
bar_b_actor_0.GetProperty().SetColor(0.3, 0.3, 1.0)

# Array B bar 1: val=5.0
bar_b_1 = vtkPlaneSource()
bar_b_1.SetOrigin(7.0, 0, 0)
bar_b_1.SetPoint1(8.0, 0, 0)
bar_b_1.SetPoint2(7.0, 5.0, 0)

bar_b_mapper_1 = vtkPolyDataMapper()
bar_b_mapper_1.SetInputConnection(bar_b_1.GetOutputPort())

bar_b_actor_1 = vtkActor()
bar_b_actor_1.SetMapper(bar_b_mapper_1)
bar_b_actor_1.GetProperty().SetColor(0.3, 0.3, 1.0)

# Array B bar 2: val=6.0
bar_b_2 = vtkPlaneSource()
bar_b_2.SetOrigin(8.5, 0, 0)
bar_b_2.SetPoint1(9.5, 0, 0)
bar_b_2.SetPoint2(8.5, 6.0, 0)

bar_b_mapper_2 = vtkPolyDataMapper()
bar_b_mapper_2.SetInputConnection(bar_b_2.GetOutputPort())

bar_b_actor_2 = vtkActor()
bar_b_actor_2.SetMapper(bar_b_mapper_2)
bar_b_actor_2.GetProperty().SetColor(0.3, 0.3, 1.0)

# Label
label = vtkTextActor()
label.SetInput("ExtractArray: Array A (red) / Array B (blue)")
label.GetTextProperty().SetFontSize(14)
label.GetTextProperty().SetColor(1, 1, 1)
label.SetPosition(10, 10)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(bar_a_actor_0)
renderer.AddActor(bar_a_actor_1)
renderer.AddActor(bar_a_actor_2)
renderer.AddActor(bar_b_actor_0)
renderer.AddActor(bar_b_actor_1)
renderer.AddActor(bar_b_actor_2)
renderer.AddViewProp(label)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("array extract factored array")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
