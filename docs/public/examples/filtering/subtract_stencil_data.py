#!/usr/bin/env python

# Test vtkImageStencilData Subtract operation with two box stencils.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR, vtkPoints
from vtkmodules.vtkCommonDataModel import VTK_QUAD, vtkImageData, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkMatrixToLinearTransform
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkPolyDataToImageStencil,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Z-shift matrix for extrusion
shift_matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, -0.5, 0, 0, 0, 1]

# --- Build box stencil 1 (10, 30) ---
poly_data_1 = vtkPolyData()
poly_data_1.AllocateEstimate(1, 4)
points_1 = vtkPoints()
points_1.InsertNextPoint(10, 10, 0.0)
points_1.InsertNextPoint(30, 10, 0.0)
points_1.InsertNextPoint(30, 30, 0.0)
points_1.InsertNextPoint(10, 30, 0.0)
poly_data_1.SetPoints(points_1)
poly_data_1.InsertNextCell(VTK_QUAD, 4, [0, 1, 2, 3])

extrude_1 = vtkLinearExtrusionFilter()
extrude_1.SetInputData(poly_data_1)
extrude_1.SetScaleFactor(1)
extrude_1.SetExtrusionTypeToNormalExtrusion()
extrude_1.SetVector(0, 0, 1)
extrude_1.Update()

matrix_1 = vtkMatrix4x4()
matrix_1.DeepCopy(shift_matrix)
transform_1 = vtkMatrixToLinearTransform()
transform_1.SetInput(matrix_1)
transform_poly_data_1 = vtkTransformPolyDataFilter()
transform_poly_data_1.SetInputConnection(extrude_1.GetOutputPort())
transform_poly_data_1.SetTransform(transform_1)
transform_poly_data_1.Update()

convert_stencil_1 = vtkPolyDataToImageStencil()
convert_stencil_1.SetInputConnection(transform_poly_data_1.GetOutputPort())

dummy_1 = vtkImageData()
dummy_1.SetSpacing(1.0, 1.0, 1.0)
dummy_1.SetOrigin(0.0, 0.0, 0.0)
dummy_1.SetExtent(8, 32, 8, 32, 0, 0)
dummy_1.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

stencil_op_1 = vtkImageStencil()
stencil_op_1.SetInputData(dummy_1)
stencil_op_1.SetStencilConnection(convert_stencil_1.GetOutputPort())
stencil_op_1.SetBackgroundValue(0)
stencil_op_1.Update()
stencil_data_1 = convert_stencil_1.GetOutput()

# --- Build box stencil 2 (20, 40) ---
poly_data_2 = vtkPolyData()
poly_data_2.AllocateEstimate(1, 4)
points_2 = vtkPoints()
points_2.InsertNextPoint(20, 20, 0.0)
points_2.InsertNextPoint(40, 20, 0.0)
points_2.InsertNextPoint(40, 40, 0.0)
points_2.InsertNextPoint(20, 40, 0.0)
poly_data_2.SetPoints(points_2)
poly_data_2.InsertNextCell(VTK_QUAD, 4, [0, 1, 2, 3])

extrude_2 = vtkLinearExtrusionFilter()
extrude_2.SetInputData(poly_data_2)
extrude_2.SetScaleFactor(1)
extrude_2.SetExtrusionTypeToNormalExtrusion()
extrude_2.SetVector(0, 0, 1)
extrude_2.Update()

matrix_2 = vtkMatrix4x4()
matrix_2.DeepCopy(shift_matrix)
transform_2 = vtkMatrixToLinearTransform()
transform_2.SetInput(matrix_2)
transform_poly_data_2 = vtkTransformPolyDataFilter()
transform_poly_data_2.SetInputConnection(extrude_2.GetOutputPort())
transform_poly_data_2.SetTransform(transform_2)
transform_poly_data_2.Update()

convert_stencil_2 = vtkPolyDataToImageStencil()
convert_stencil_2.SetInputConnection(transform_poly_data_2.GetOutputPort())

dummy_2 = vtkImageData()
dummy_2.SetSpacing(1.0, 1.0, 1.0)
dummy_2.SetOrigin(0.0, 0.0, 0.0)
dummy_2.SetExtent(18, 42, 18, 42, 0, 0)
dummy_2.AllocateScalars(VTK_UNSIGNED_CHAR, 1)

stencil_op_2 = vtkImageStencil()
stencil_op_2.SetInputData(dummy_2)
stencil_op_2.SetStencilConnection(convert_stencil_2.GetOutputPort())
stencil_op_2.SetBackgroundValue(0)
stencil_op_2.Update()
stencil_data_2 = convert_stencil_2.GetOutput()

# Subtract stencil 2 from stencil 1
stencil_data_1.Subtract(stencil_data_2)

# Apply combined stencil to a white image to visualize
white_image = vtkImageData()
white_image.SetExtent(0, 50, 0, 50, 0, 0)
white_image.AllocateScalars(VTK_UNSIGNED_CHAR, 3)
white_image.GetPointData().GetScalars().Fill(255)

black_image = vtkImageData()
black_image.SetExtent(0, 50, 0, 50, 0, 0)
black_image.AllocateScalars(VTK_UNSIGNED_CHAR, 3)
black_image.GetPointData().GetScalars().Fill(0)

stencil_producer = vtkTrivialProducer()
stencil_producer.SetOutput(stencil_data_1)

result_stencil = vtkImageStencil()
result_stencil.SetInputData(white_image)
result_stencil.SetBackgroundInputData(black_image)
result_stencil.SetStencilConnection(stencil_producer.GetOutputPort())
result_stencil.Update()

# Display
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(result_stencil.GetOutputPort())

renderer = vtkRenderer()
renderer.AddViewProp(image_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("subtract stencil data")

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
