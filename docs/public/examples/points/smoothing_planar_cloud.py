#!/usr/bin/env python

# Demonstrate vtkPointSmoothingFilter with six smoothing modes on a random
# planar point cloud with synthetic scalars and tensors, rendered in a
# 3x2 viewport grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkTensorGlyph,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractTensorComponents
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import vtkPointSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 1500
math = vtkMath()
math.RandomSeed(31415)

normal = [0, 0, 1]
center = [0, 0, 0]
plane = vtkPlane()
plane.SetOrigin(center)
plane.SetNormal(normal)

# Create random planar point cloud with scalars and tensors
point_positions = vtkPoints()
point_positions.SetNumberOfPoints(n_pts)
verts = vtkCellArray()
scalars = vtkFloatArray()
scalars.SetNumberOfTuples(n_pts)
tensors = vtkFloatArray()
tensors.SetNumberOfComponents(6)
tensors.SetNumberOfTuples(n_pts)

for i in range(0, n_pts):
    point_positions.SetPoint(i, math.Random(-1, 1), math.Random(-1, 1), 0.0)
    verts.InsertNextCell(1, [i])
    scalars.SetTuple1(i, math.Random(2, 5))
    tensors.SetTuple6(i, math.Random(1, 3), math.Random(-1, 1), math.Random(-1, 1),
                      math.Random(1, 3), math.Random(-1, 1), 1)

point_data = vtkPolyData()
point_data.SetPoints(point_positions)
point_data.SetVerts(verts)
point_data.GetPointData().SetScalars(scalars)
point_data.GetPointData().SetTensors(tensors)

# Extract tensor information
tensor_extract = vtkExtractTensorComponents()
tensor_extract.SetInputData(point_data)
tensor_extract.ExtractScalarsOn()
tensor_extract.ScalarIsDeterminant()
tensor_extract.PassTensorsToOutputOn()
tensor_extract.Update()

# Glyph source
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.5)
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetThetaResolution(16)
sphere_source.SetPhiResolution(8)
sphere_source.Update()

# --- Default (no smoothing) ---
smooth_0 = vtkPointSmoothingFilter()
smooth_0.SetInputData(point_data)
smooth_0.SetNumberOfIterations(0)
smooth_0.SetSmoothingModeToDefault()
smooth_0.Update()

glyph_0 = vtkGlyph3D()
glyph_0.SetInputConnection(smooth_0.GetOutputPort())
glyph_0.SetSourceConnection(sphere_source.GetOutputPort())
glyph_0.SetScaleModeToDataScalingOff()
glyph_0.SetScaleFactor(0.1)

glyph_mapper_0 = vtkPolyDataMapper()
glyph_mapper_0.SetInputConnection(glyph_0.GetOutputPort())
glyph_mapper_0.ScalarVisibilityOff()

glyph_actor_0 = vtkActor()
glyph_actor_0.SetMapper(glyph_mapper_0)
glyph_actor_0.GetProperty().SetColor(1, 1, 1)

# --- Geometric ---
smooth_1 = vtkPointSmoothingFilter()
smooth_1.SetInputData(point_data)
smooth_1.SetSmoothingModeToGeometric()
smooth_1.SetNumberOfIterations(20)
smooth_1.SetNumberOfSubIterations(100)
smooth_1.SetMaximumStepSize(0.01)
smooth_1.SetNeighborhoodSize(24)
smooth_1.EnableConstraintsOff()
smooth_1.SetFixedAngle(50)
smooth_1.SetBoundaryAngle(100)
smooth_1.GenerateConstraintScalarsOn()
smooth_1.Update()

glyph_1 = vtkGlyph3D()
glyph_1.SetInputConnection(smooth_1.GetOutputPort())
glyph_1.SetSourceConnection(sphere_source.GetOutputPort())
glyph_1.SetScaleModeToDataScalingOff()
glyph_1.SetScaleFactor(0.1)

glyph_mapper_1 = vtkPolyDataMapper()
glyph_mapper_1.SetInputConnection(glyph_1.GetOutputPort())
glyph_mapper_1.SetColorModeToMapScalars()
glyph_mapper_1.SetScalarModeToUsePointFieldData()
glyph_mapper_1.SetArrayAccessMode(1)
glyph_mapper_1.SetArrayName("Constraint Scalars")
glyph_mapper_1.SetScalarRange(0, 2)

glyph_actor_1 = vtkActor()
glyph_actor_1.SetMapper(glyph_mapper_1)
glyph_actor_1.GetProperty().SetColor(1, 1, 1)

# --- Uniform ---
smooth_2 = vtkPointSmoothingFilter()
smooth_2.SetInputData(point_data)
smooth_2.SetSmoothingModeToUniform()
smooth_2.SetNumberOfIterations(80)
smooth_2.SetNumberOfSubIterations(10)
smooth_2.EnableConstraintsOn()
smooth_2.SetMaximumStepSize(0.01)
smooth_2.SetNeighborhoodSize(20)
smooth_2.GenerateConstraintScalarsOn()
smooth_2.SetPackingFactor(1.5)
smooth_2.Update()

glyph_2 = vtkGlyph3D()
glyph_2.SetInputConnection(smooth_2.GetOutputPort())
glyph_2.SetSourceConnection(sphere_source.GetOutputPort())
glyph_2.SetScaleModeToDataScalingOff()
glyph_2.SetScaleFactor(0.1)
glyph_2.Update()

glyph_mapper_2 = vtkPolyDataMapper()
glyph_mapper_2.SetInputConnection(glyph_2.GetOutputPort())
glyph_mapper_2.SetScalarModeToUsePointFieldData()
glyph_mapper_2.SetArrayAccessMode(1)
glyph_mapper_2.SetArrayName("Constraint Scalars")
glyph_mapper_2.SetScalarRange(0, 2)

glyph_actor_2 = vtkActor()
glyph_actor_2.SetMapper(glyph_mapper_2)
glyph_actor_2.GetProperty().SetColor(1, 1, 1)

# --- Scalar ---
smooth_3 = vtkPointSmoothingFilter()
smooth_3.SetInputData(point_data)
smooth_3.SetSmoothingModeToScalars()
smooth_3.SetNumberOfIterations(80)
smooth_3.SetNumberOfSubIterations(20)
smooth_3.SetMaximumStepSize(0.01)
smooth_3.SetNeighborhoodSize(18)
smooth_3.EnableConstraintsOff()
smooth_3.SetFixedAngle(50)
smooth_3.SetBoundaryAngle(100)
smooth_3.GenerateConstraintScalarsOn()
smooth_3.SetPackingFactor(1.5)
smooth_3.Update()

glyph_3 = vtkGlyph3D()
glyph_3.SetInputConnection(smooth_3.GetOutputPort())
glyph_3.SetSourceConnection(sphere_source.GetOutputPort())
glyph_3.SetScaleFactor(0.01)

glyph_mapper_3 = vtkPolyDataMapper()
glyph_mapper_3.SetInputConnection(glyph_3.GetOutputPort())
glyph_mapper_3.SetScalarRange(2, 5)

glyph_actor_3 = vtkActor()
glyph_actor_3.SetMapper(glyph_mapper_3)
glyph_actor_3.GetProperty().SetColor(1, 1, 1)

# --- Frame Field (first) ---
smooth_4 = vtkPointSmoothingFilter()
smooth_4.SetInputData(point_data)
smooth_4.SetSmoothingModeToFrameField()
smooth_4.SetNumberOfIterations(40)
smooth_4.SetNumberOfSubIterations(10)
smooth_4.SetMaximumStepSize(0.01)
smooth_4.SetNeighborhoodSize(18)
smooth_4.SetPackingFactor(0.75)
smooth_4.SetMotionConstraintToPlane()
smooth_4.SetPlane(plane)
smooth_4.Update()

glyph_4 = vtkTensorGlyph()
glyph_4.SetInputConnection(smooth_4.GetOutputPort())
glyph_4.SetSourceConnection(sphere_source.GetOutputPort())
glyph_4.SetScaleFactor(0.025)

glyph_mapper_4 = vtkPolyDataMapper()
glyph_mapper_4.SetInputConnection(glyph_4.GetOutputPort())
glyph_mapper_4.SetScalarRange(2, 5)

glyph_actor_4 = vtkActor()
glyph_actor_4.SetMapper(glyph_mapper_4)
glyph_actor_4.GetProperty().SetColor(1, 1, 1)

# --- Frame Field (second, more iterations) ---
smooth_5 = vtkPointSmoothingFilter()
smooth_5.SetInputData(point_data)
smooth_5.SetSmoothingModeToFrameField()
smooth_5.SetFrameFieldArray(tensors)
smooth_5.SetNumberOfIterations(5000)
smooth_5.SetNumberOfSubIterations(100)
smooth_5.SetMaximumStepSize(0.00001)
smooth_5.SetNeighborhoodSize(40)
smooth_5.SetPackingFactor(0.25)
smooth_5.SetAttractionFactor(0.25)
smooth_5.SetMotionConstraintToPlane()
smooth_5.SetPlane(plane)
smooth_5.Update()

glyph_5 = vtkTensorGlyph()
glyph_5.SetInputConnection(smooth_5.GetOutputPort())
glyph_5.SetSourceConnection(sphere_source.GetOutputPort())
glyph_5.SetScaleFactor(0.025)

glyph_mapper_5 = vtkPolyDataMapper()
glyph_mapper_5.SetInputConnection(glyph_5.GetOutputPort())
glyph_mapper_5.SetScalarRange(2, 5)

glyph_actor_5 = vtkActor()
glyph_actor_5.SetMapper(glyph_mapper_5)
glyph_actor_5.GetProperty().SetColor(1, 1, 1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(point_data)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1, 1, 1)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 0.5)
renderer_0.AddActor(glyph_actor_0)
renderer_0.AddActor(outline_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.667, 0.5)
renderer_1.AddActor(glyph_actor_1)
renderer_1.AddActor(outline_actor)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.667, 0, 1, 0.5)
renderer_2.AddActor(glyph_actor_2)
renderer_2.AddActor(outline_actor)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0, 0.5, 0.333, 1)
renderer_3.AddActor(glyph_actor_3)
renderer_3.AddActor(outline_actor)
renderer_3.SetBackground(0, 0, 0)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.333, 0.5, 0.667, 1)
renderer_4.AddActor(glyph_actor_4)
renderer_4.AddActor(outline_actor)
renderer_4.SetBackground(0, 0, 0)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.667, 0.5, 1, 1)
renderer_5.AddActor(glyph_actor_5)
renderer_5.AddActor(outline_actor)
renderer_5.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(600, 400)
render_window.SetWindowName("smoothing planar cloud")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(normal)

renderer_0.SetActiveCamera(camera)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)
renderer_4.SetActiveCamera(camera)
renderer_5.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
