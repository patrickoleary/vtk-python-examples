#!/usr/bin/env python

# Demonstrate vtkMatricizeArray by creating a 2x2x2 sparse array,
# matricizing along dimension 0, and visualizing the result as a
# heatmap of colored quads.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkSparseArray
from vtkmodules.vtkCommonDataModel import vtkArrayData
from vtkmodules.vtkFiltersGeneral import vtkMatricizeArray
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Create a 2x2x2 sparse array with values 0..7
array = vtkSparseArray['float64']()
array.Resize(2, 2, 2)
value = 0.0
for i in range(2):
    for j in range(2):
        for k in range(2):
            array.AddValue(i, j, k, value)
            value += 1.0

# Pack into vtkArrayData
array_data = vtkArrayData()
array_data.AddArray(array)

# Matricize along dimension 0
matricize = vtkMatricizeArray()
matricize.SetInputData(array_data)
matricize.SetSliceDimension(0)
matricize.Update()

matricized = matricize.GetOutput().GetArray(0)

# The result is a 2x4 matrix; visualize as colored quads
# rows=2, cols=4, max_val=7.0
# Row 0 (y=1): values 0,1,2,3  Row 1 (y=0): values 4,5,6,7

# Row 0, Col 0: val=0.0, norm=0.0/7.0
cell_0_0 = vtkPlaneSource()
cell_0_0.SetOrigin(0, 1, 0)
cell_0_0.SetPoint1(0.9, 1, 0)
cell_0_0.SetPoint2(0, 1.9, 0)

cell_mapper_0_0 = vtkPolyDataMapper()
cell_mapper_0_0.SetInputConnection(cell_0_0.GetOutputPort())

cell_actor_0_0 = vtkActor()
cell_actor_0_0.SetMapper(cell_mapper_0_0)
cell_actor_0_0.GetProperty().SetColor(0.0, 0.2, 1.0)

# Row 0, Col 1: val=1.0, norm=1.0/7.0
cell_0_1 = vtkPlaneSource()
cell_0_1.SetOrigin(1, 1, 0)
cell_0_1.SetPoint1(1.9, 1, 0)
cell_0_1.SetPoint2(1, 1.9, 0)

cell_mapper_0_1 = vtkPolyDataMapper()
cell_mapper_0_1.SetInputConnection(cell_0_1.GetOutputPort())

cell_actor_0_1 = vtkActor()
cell_actor_0_1.SetMapper(cell_mapper_0_1)
cell_actor_0_1.GetProperty().SetColor(1.0 / 7.0, 0.2, 6.0 / 7.0)

# Row 0, Col 2: val=2.0, norm=2.0/7.0
cell_0_2 = vtkPlaneSource()
cell_0_2.SetOrigin(2, 1, 0)
cell_0_2.SetPoint1(2.9, 1, 0)
cell_0_2.SetPoint2(2, 1.9, 0)

cell_mapper_0_2 = vtkPolyDataMapper()
cell_mapper_0_2.SetInputConnection(cell_0_2.GetOutputPort())

cell_actor_0_2 = vtkActor()
cell_actor_0_2.SetMapper(cell_mapper_0_2)
cell_actor_0_2.GetProperty().SetColor(2.0 / 7.0, 0.2, 5.0 / 7.0)

# Row 0, Col 3: val=3.0, norm=3.0/7.0
cell_0_3 = vtkPlaneSource()
cell_0_3.SetOrigin(3, 1, 0)
cell_0_3.SetPoint1(3.9, 1, 0)
cell_0_3.SetPoint2(3, 1.9, 0)

cell_mapper_0_3 = vtkPolyDataMapper()
cell_mapper_0_3.SetInputConnection(cell_0_3.GetOutputPort())

cell_actor_0_3 = vtkActor()
cell_actor_0_3.SetMapper(cell_mapper_0_3)
cell_actor_0_3.GetProperty().SetColor(3.0 / 7.0, 0.2, 4.0 / 7.0)

# Row 1, Col 0: val=4.0, norm=4.0/7.0
cell_1_0 = vtkPlaneSource()
cell_1_0.SetOrigin(0, 0, 0)
cell_1_0.SetPoint1(0.9, 0, 0)
cell_1_0.SetPoint2(0, 0.9, 0)

cell_mapper_1_0 = vtkPolyDataMapper()
cell_mapper_1_0.SetInputConnection(cell_1_0.GetOutputPort())

cell_actor_1_0 = vtkActor()
cell_actor_1_0.SetMapper(cell_mapper_1_0)
cell_actor_1_0.GetProperty().SetColor(4.0 / 7.0, 0.2, 3.0 / 7.0)

# Row 1, Col 1: val=5.0, norm=5.0/7.0
cell_1_1 = vtkPlaneSource()
cell_1_1.SetOrigin(1, 0, 0)
cell_1_1.SetPoint1(1.9, 0, 0)
cell_1_1.SetPoint2(1, 0.9, 0)

cell_mapper_1_1 = vtkPolyDataMapper()
cell_mapper_1_1.SetInputConnection(cell_1_1.GetOutputPort())

cell_actor_1_1 = vtkActor()
cell_actor_1_1.SetMapper(cell_mapper_1_1)
cell_actor_1_1.GetProperty().SetColor(5.0 / 7.0, 0.2, 2.0 / 7.0)

# Row 1, Col 2: val=6.0, norm=6.0/7.0
cell_1_2 = vtkPlaneSource()
cell_1_2.SetOrigin(2, 0, 0)
cell_1_2.SetPoint1(2.9, 0, 0)
cell_1_2.SetPoint2(2, 0.9, 0)

cell_mapper_1_2 = vtkPolyDataMapper()
cell_mapper_1_2.SetInputConnection(cell_1_2.GetOutputPort())

cell_actor_1_2 = vtkActor()
cell_actor_1_2.SetMapper(cell_mapper_1_2)
cell_actor_1_2.GetProperty().SetColor(6.0 / 7.0, 0.2, 1.0 / 7.0)

# Row 1, Col 3: val=7.0, norm=7.0/7.0
cell_1_3 = vtkPlaneSource()
cell_1_3.SetOrigin(3, 0, 0)
cell_1_3.SetPoint1(3.9, 0, 0)
cell_1_3.SetPoint2(3, 0.9, 0)

cell_mapper_1_3 = vtkPolyDataMapper()
cell_mapper_1_3.SetInputConnection(cell_1_3.GetOutputPort())

cell_actor_1_3 = vtkActor()
cell_actor_1_3.SetMapper(cell_mapper_1_3)
cell_actor_1_3.GetProperty().SetColor(1.0, 0.2, 0.0)

# Label
label = vtkTextActor()
label.SetInput("MatricizeArray: 2x2x2 -> 2x4 matrix")
label.GetTextProperty().SetFontSize(14)
label.GetTextProperty().SetColor(1, 1, 1)
label.SetPosition(10, 10)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cell_actor_0_0)
renderer.AddActor(cell_actor_0_1)
renderer.AddActor(cell_actor_0_2)
renderer.AddActor(cell_actor_0_3)
renderer.AddActor(cell_actor_1_0)
renderer.AddActor(cell_actor_1_1)
renderer.AddActor(cell_actor_1_2)
renderer.AddActor(cell_actor_1_3)
renderer.AddViewProp(label)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("array matricize array")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
