#!/usr/bin/env python

# Demonstrate vtkProgrammableDataObjectSource with vtkRearrangeFields,
# vtkArrayCalculator, and vtkAssignAttribute to manipulate financial data
# fields, then visualize with Gaussian splatting and labeled axes.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkFieldData
from vtkmodules.vtkFiltersCore import (
    vtkArrayCalculator,
    vtkAssignAttribute,
    vtkContourFilter,
    vtkDataObjectToDataSetFilter,
    vtkRearrangeFields,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkFiltersSources import vtkProgrammableDataObjectSource
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkFollower,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Field names
x_axis = "INTEREST_RATE"
y_axis = "MONTHLY_PAYMENT"
z_axis = "MONTHLY_INCOME"
scalar = "TIME_LATE"

# Programmable data object source — parses financial.txt
data_source = vtkProgrammableDataObjectSource()

def parse_file():
    f = open(os.path.join(data_dir, "financial.txt"), "r")

    line = f.readline().split()
    num_pts = int(line[1])
    num_lines = (num_pts - 1) // 8 + 1

    field = vtkFieldData()
    field.AllocateArrays(4)

    # TIME_LATE - dependent variable
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    time_late = vtkFloatArray()
    time_late.SetName(line[0])
    for i in range(num_lines):
        line = f.readline().split()
        for j in line:
            time_late.InsertNextValue(float(j))
    field.AddArray(time_late)

    # MONTHLY_PAYMENT - independent variable
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    monthly_payment = vtkFloatArray()
    monthly_payment.SetName(line[0])
    for i in range(num_lines):
        line = f.readline().split()
        for j in line:
            monthly_payment.InsertNextValue(float(j))
    field.AddArray(monthly_payment)

    # UNPAID_PRINCIPLE - skip
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    for i in range(num_lines):
        line = f.readline()

    # LOAN_AMOUNT - skip
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    for i in range(num_lines):
        line = f.readline()

    # INTEREST_RATE - independent variable
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    interest_rate = vtkFloatArray()
    interest_rate.SetName(line[0])
    for i in range(num_lines):
        line = f.readline().split()
        for j in line:
            interest_rate.InsertNextValue(float(j))
    field.AddArray(interest_rate)

    # MONTHLY_INCOME - independent variable
    while True:
        line = f.readline().split()
        if len(line) > 0:
            break
    monthly_income = vtkFloatArray()
    monthly_income.SetName(line[0])
    for i in range(num_lines):
        line = f.readline().split()
        for j in line:
            monthly_income.InsertNextValue(float(j))
    field.AddArray(monthly_income)

    data_source.GetOutput().SetFieldData(field)

data_source.SetExecuteMethod(parse_file)

# Convert field to polydata points
data_to_dataset = vtkDataObjectToDataSetFilter()
data_to_dataset.SetInputConnection(data_source.GetOutputPort())
data_to_dataset.SetDataSetTypeToPolyData()
data_to_dataset.DefaultNormalizeOn()
data_to_dataset.SetPointComponent(0, x_axis, 0)
data_to_dataset.SetPointComponent(1, y_axis, 0)
data_to_dataset.SetPointComponent(2, z_axis, 0)
data_to_dataset.Update()

# Move TIME_LATE from data object to point data using vtkRearrangeFields
rearrange_fields = vtkRearrangeFields()
rearrange_fields.SetInputConnection(data_to_dataset.GetOutputPort())
rearrange_fields.AddOperation("MOVE", scalar, "DATA_OBJECT", "POINT_DATA")
rearrange_fields.RemoveOperation("MOVE", scalar, "DATA_OBJECT", "POINT_DATA")
rearrange_fields.AddOperation("MOVE", scalar, "DATA_OBJECT", "POINT_DATA")
rearrange_fields.RemoveAllOperations()
rearrange_fields.AddOperation("MOVE", scalar, "DATA_OBJECT", "POINT_DATA")
rearrange_fields.Update()
max_val = rearrange_fields.GetOutput().GetPointData().GetArray(scalar).GetRange(0)[1]

# Normalize the scalar using vtkArrayCalculator
calc = vtkArrayCalculator()
calc.SetInputConnection(rearrange_fields.GetOutputPort())
calc.SetAttributeTypeToPointData()
calc.SetFunction("s / %f" % max_val)
calc.AddScalarVariable("s", scalar, 0)
calc.SetResultArrayName("resArray")

# Assign the result as the active scalar
assign_attribute = vtkAssignAttribute()
assign_attribute.SetInputConnection(calc.GetOutputPort())
assign_attribute.Assign("resArray", "SCALARS", "POINT_DATA")
assign_attribute.Update()

# Copy scalars back to data object field
rearrange_fields_2 = vtkRearrangeFields()
rearrange_fields_2.SetInputConnection(assign_attribute.GetOutputPort())
rearrange_fields_2.AddOperation("COPY", "SCALARS", "POINT_DATA", "DATA_OBJECT")

# Pipeline for original population (translucent gray)
pop_splatter = vtkGaussianSplatter()
pop_splatter.SetInputConnection(rearrange_fields_2.GetOutputPort())
pop_splatter.SetSampleDimensions(50, 50, 50)
pop_splatter.SetRadius(0.05)
pop_splatter.ScalarWarpingOff()

pop_surface = vtkContourFilter()
pop_surface.SetInputConnection(pop_splatter.GetOutputPort())
pop_surface.SetValue(0, 0.01)

pop_mapper = vtkPolyDataMapper()
pop_mapper.SetInputConnection(pop_surface.GetOutputPort())
pop_mapper.ScalarVisibilityOff()

pop_actor = vtkActor()
pop_actor.SetMapper(pop_mapper)
pop_actor.GetProperty().SetOpacity(0.3)
pop_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

# Pipeline for delinquent population (red)
late_splatter = vtkGaussianSplatter()
late_splatter.SetInputConnection(assign_attribute.GetOutputPort())
late_splatter.SetSampleDimensions(50, 50, 50)
late_splatter.SetRadius(0.05)
late_splatter.SetScaleFactor(0.05)

late_surface = vtkContourFilter()
late_surface.SetInputConnection(late_splatter.GetOutputPort())
late_surface.SetValue(0, 0.01)

late_mapper = vtkPolyDataMapper()
late_mapper.SetInputConnection(late_surface.GetOutputPort())
late_mapper.ScalarVisibilityOff()

late_actor = vtkActor()
late_actor.SetMapper(late_mapper)
late_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Create axes
pop_splatter.Update()
bounds = pop_splatter.GetOutput().GetBounds()

axes = vtkAxes()
axes.SetOrigin(bounds[0], bounds[2], bounds[4])
axes.SetScaleFactor(pop_splatter.GetOutput().GetLength() / 5.0)

axes_tubes = vtkTubeFilter()
axes_tubes.SetInputConnection(axes.GetOutputPort())
axes_tubes.SetRadius(axes.GetScaleFactor() / 25.0)
axes_tubes.SetNumberOfSides(6)

axes_mapper = vtkPolyDataMapper()
axes_mapper.SetInputConnection(axes_tubes.GetOutputPort())

axes_actor = vtkActor()
axes_actor.SetMapper(axes_mapper)

# X-axis label
x_text = vtkVectorText()
x_text.SetText(x_axis)
x_text_mapper = vtkPolyDataMapper()
x_text_mapper.SetInputConnection(x_text.GetOutputPort())
x_label = vtkFollower()
x_label.SetMapper(x_text_mapper)
x_label.SetScale(0.02, 0.02, 0.02)
x_label.SetPosition(0.35, -0.05, -0.05)
x_label.GetProperty().SetColor(0, 0, 0)

# Y-axis label
y_text = vtkVectorText()
y_text.SetText(y_axis)
y_text_mapper = vtkPolyDataMapper()
y_text_mapper.SetInputConnection(y_text.GetOutputPort())
y_label = vtkFollower()
y_label.SetMapper(y_text_mapper)
y_label.SetScale(0.02, 0.02, 0.02)
y_label.SetPosition(-0.05, 0.35, -0.05)
y_label.GetProperty().SetColor(0, 0, 0)

# Z-axis label
z_text = vtkVectorText()
z_text.SetText(z_axis)
z_text_mapper = vtkPolyDataMapper()
z_text_mapper.SetInputConnection(z_text.GetOutputPort())
z_label = vtkFollower()
z_label.SetMapper(z_text_mapper)
z_label.SetScale(0.02, 0.02, 0.02)
z_label.SetPosition(-0.05, -0.05, 0.35)
z_label.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(axes_actor)
renderer.AddActor(late_actor)
renderer.AddActor(x_label)
renderer.AddActor(y_label)
renderer.AddActor(z_label)
renderer.AddActor(pop_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("financial field rearrange calc")

# Scene
camera = vtkCamera()
camera.SetClippingRange(0.274, 13.72)
camera.SetFocalPoint(0.433816, 0.333131, 0.449)
camera.SetPosition(-1.96987, 1.15145, 1.49053)
camera.SetViewUp(0.378927, 0.911821, 0.158107)
renderer.SetActiveCamera(camera)
x_label.SetCamera(camera)
y_label.SetCamera(camera)
z_label.SetCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
