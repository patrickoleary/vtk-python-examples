#!/usr/bin/env python

# Demonstrate vtkPointSmoothingFilter with six smoothing modes (default,
# geometric, uniform, scalar, tensor, frame field) on points sampled from
# a stress tensor field, rendered in a 3x2 viewport grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPlane,
)
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkGlyph3D,
    vtkProbeFilter,
    vtkTensorGlyph,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractTensorComponents
from vtkmodules.vtkFiltersModeling import (
    vtkOutlineFilter,
    vtkPolyDataPointSampler,
)
from vtkmodules.vtkFiltersPoints import vtkPointSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test resolution
res = 30

# Plane normal (slightly off-axis)
normal = [0.1, 0.1, 1]

# Generate a sizing field from a point load (stress tensors)
pt_load = vtkPointLoad()
pt_load.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
pt_load.SetSampleDimensions(res, res, res)
pt_load.Update()

size_field = pt_load.GetOutput()
bounds = size_field.GetBounds()
center = [(bounds[1] + bounds[0]) / 2.0, (bounds[3] + bounds[2]) / 2.0, (bounds[5] + bounds[4]) / 2.0]

# Cut the data with a plane
plane = vtkPlane()
plane.SetOrigin(center)
plane.SetNormal(normal)

# Create a single voxel
voxel = vtkImageData()
voxel.SetDimensions(2, 2, 2)
voxel.SetOrigin(-0.5, -0.5, -0.5)
voxel.SetSpacing(1, 1, 1)

# Cut the voxel to produce a polygon
cut = vtkCutter()
cut.SetInputData(voxel)
cut.SetCutFunction(plane)
cut.Update()

# Sample points on the polygon
sampler = vtkPolyDataPointSampler()
sampler.SetInputConnection(cut.GetOutputPort())
sampler.SetDistance(0.0175)
sampler.SetPointGenerationModeToRandom()
sampler.GenerateVertexPointsOff()
sampler.GenerateEdgePointsOff()
sampler.GenerateInteriorPointsOn()
sampler.Update()

# Probe for tensor data
probe = vtkProbeFilter()
probe.SetInputConnection(sampler.GetOutputPort())
probe.SetSourceConnection(pt_load.GetOutputPort())
probe.Update()

# Extract tensor information
tensor_extract = vtkExtractTensorComponents()
tensor_extract.SetInputConnection(probe.GetOutputPort())
tensor_extract.ExtractScalarsOn()
tensor_extract.ScalarIsNonNegativeDeterminant()
tensor_extract.PassTensorsToOutputOn()
tensor_extract.Update()

# Glyph source
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.5)
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetThetaResolution(16)
sphere_source.SetPhiResolution(8)
sphere_source.Update()

# --- Default (no smoothing, 0 iterations) ---
smooth_0 = vtkPointSmoothingFilter()
smooth_0.SetInputConnection(tensor_extract.GetOutputPort())
smooth_0.SetNumberOfIterations(0)
smooth_0.SetSmoothingModeToDefault()
smooth_0.Update()

glyph_0 = vtkGlyph3D()
glyph_0.SetInputConnection(smooth_0.GetOutputPort())
glyph_0.SetSourceConnection(sphere_source.GetOutputPort())
glyph_0.SetScaleModeToDataScalingOff()
glyph_0.SetScaleFactor(0.025)

glyph_mapper_0 = vtkPolyDataMapper()
glyph_mapper_0.SetInputConnection(glyph_0.GetOutputPort())
glyph_mapper_0.ScalarVisibilityOff()

glyph_actor_0 = vtkActor()
glyph_actor_0.SetMapper(glyph_mapper_0)
glyph_actor_0.GetProperty().SetColor(1, 1, 1)
glyph_actor_0.GetProperty().SetOpacity(1)

# --- Geometric ---
smooth_1 = vtkPointSmoothingFilter()
smooth_1.SetInputConnection(tensor_extract.GetOutputPort())
smooth_1.SetSmoothingModeToGeometric()
smooth_1.SetNumberOfIterations(20)
smooth_1.SetNumberOfSubIterations(10)
smooth_1.SetPackingFactor(1.0)
smooth_1.SetMaximumStepSize(0.01)
smooth_1.SetNeighborhoodSize(24)
smooth_1.EnableConstraintsOn()
smooth_1.SetFixedAngle(45)
smooth_1.SetBoundaryAngle(110)
smooth_1.GenerateConstraintScalarsOn()
smooth_1.Update()

glyph_1 = vtkGlyph3D()
glyph_1.SetInputConnection(smooth_1.GetOutputPort())
glyph_1.SetSourceConnection(sphere_source.GetOutputPort())
glyph_1.SetScaleModeToDataScalingOff()
glyph_1.SetScaleFactor(0.025)

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
glyph_actor_1.GetProperty().SetOpacity(1)

# --- Uniform ---
smooth_2 = vtkPointSmoothingFilter()
smooth_2.SetInputConnection(tensor_extract.GetOutputPort())
smooth_2.SetSmoothingModeToUniform()
smooth_2.SetNumberOfIterations(40)
smooth_2.SetNumberOfSubIterations(10)
smooth_2.SetMaximumStepSize(0.001)
smooth_2.SetNeighborhoodSize(24)
smooth_2.SetPackingFactor(1.5)
smooth_2.SetAttractionFactor(0.5)
smooth_2.EnableConstraintsOn()
smooth_2.SetFixedAngle(45)
smooth_2.SetBoundaryAngle(105)
smooth_2.GenerateConstraintScalarsOn()
smooth_2.SetMotionConstraintToPlane()
smooth_2.SetPlane(plane)
smooth_2.Update()

glyph_2 = vtkGlyph3D()
glyph_2.SetInputConnection(smooth_2.GetOutputPort())
glyph_2.SetSourceConnection(sphere_source.GetOutputPort())
glyph_2.SetScaleModeToDataScalingOff()
glyph_2.SetScaleFactor(0.025)

glyph_mapper_2 = vtkPolyDataMapper()
glyph_mapper_2.SetInputConnection(glyph_2.GetOutputPort())
glyph_mapper_2.SetColorModeToMapScalars()
glyph_mapper_2.SetScalarModeToUsePointFieldData()
glyph_mapper_2.SetArrayAccessMode(1)
glyph_mapper_2.SetArrayName("Constraint Scalars")
glyph_mapper_2.SetScalarRange(0, 2)

glyph_actor_2 = vtkActor()
glyph_actor_2.SetMapper(glyph_mapper_2)
glyph_actor_2.GetProperty().SetColor(1, 1, 1)
glyph_actor_2.GetProperty().SetOpacity(1)

# --- Scalar ---
smooth_3 = vtkPointSmoothingFilter()
smooth_3.SetInputConnection(tensor_extract.GetOutputPort())
smooth_3.SetSmoothingModeToScalars()
smooth_3.SetNumberOfIterations(100)
smooth_3.SetNumberOfSubIterations(100)
smooth_3.SetMaximumStepSize(0.0001)
smooth_3.SetNeighborhoodSize(40)
smooth_3.SetPackingFactor(1.0)
smooth_3.SetAttractionFactor(0.25)
smooth_3.EnableConstraintsOn()
smooth_3.SetFixedAngle(45)
smooth_3.SetBoundaryAngle(100)
smooth_3.GenerateConstraintScalarsOn()
smooth_3.SetMotionConstraintToPlane()
smooth_3.SetPlane(plane)
smooth_3.Update()

glyph_3 = vtkGlyph3D()
glyph_3.SetInputConnection(smooth_3.GetOutputPort())
glyph_3.SetSourceConnection(sphere_source.GetOutputPort())
glyph_3.SetColorModeToColorByScalar()
glyph_3.SetScaleFactor(1)

lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

glyph_mapper_3 = vtkPolyDataMapper()
glyph_mapper_3.SetInputConnection(glyph_3.GetOutputPort())
glyph_mapper_3.SetScalarRange(smooth_3.GetOutput().GetScalarRange())
glyph_mapper_3.SetLookupTable(lookup_table)

glyph_actor_3 = vtkActor()
glyph_actor_3.SetMapper(glyph_mapper_3)
glyph_actor_3.GetProperty().SetColor(1, 1, 1)
glyph_actor_3.GetProperty().SetOpacity(1)

# --- Tensor ---
smooth_4 = vtkPointSmoothingFilter()
smooth_4.SetInputConnection(tensor_extract.GetOutputPort())
smooth_4.SetSmoothingModeToTensors()
smooth_4.SetNumberOfIterations(80)
smooth_4.SetNumberOfSubIterations(20)
smooth_4.SetMaximumStepSize(0.001)
smooth_4.SetNeighborhoodSize(24)
smooth_4.SetPackingFactor(1)
smooth_4.SetAttractionFactor(0.25)
smooth_4.EnableConstraintsOn()
smooth_4.SetFixedAngle(45)
smooth_4.SetBoundaryAngle(100)
smooth_4.GenerateConstraintScalarsOn()
smooth_4.SetMotionConstraintToPlane()
smooth_4.SetPlane(plane)
smooth_4.Update()

glyph_4 = vtkTensorGlyph()
glyph_4.SetInputConnection(smooth_4.GetOutputPort())
glyph_4.SetSourceConnection(sphere_source.GetOutputPort())
glyph_4.SetScaleFactor(0.1)

glyph_mapper_4 = vtkPolyDataMapper()
glyph_mapper_4.SetInputConnection(glyph_4.GetOutputPort())
glyph_mapper_4.SetScalarRange(smooth_4.GetOutput().GetScalarRange())

glyph_actor_4 = vtkActor()
glyph_actor_4.SetMapper(glyph_mapper_4)
glyph_actor_4.GetProperty().SetColor(1, 1, 1)
glyph_actor_4.GetProperty().SetOpacity(1)

# --- Frame Field (tensor mode, no constraints) ---
smooth_5 = vtkPointSmoothingFilter()
smooth_5.SetInputConnection(tensor_extract.GetOutputPort())
smooth_5.SetSmoothingModeToTensors()
smooth_5.SetNumberOfIterations(80)
smooth_5.SetNumberOfSubIterations(10)
smooth_5.SetMaximumStepSize(0.001)
smooth_5.SetNeighborhoodSize(12)
smooth_5.SetPackingFactor(1.5)
smooth_5.SetAttractionFactor(0.25)
smooth_5.EnableConstraintsOff()
smooth_5.SetFixedAngle(45)
smooth_5.SetBoundaryAngle(105)
smooth_5.SetMotionConstraintToPlane()
smooth_5.SetPlane(plane)
smooth_5.Update()

glyph_5 = vtkTensorGlyph()
glyph_5.SetInputConnection(smooth_5.GetOutputPort())
glyph_5.SetSourceConnection(sphere_source.GetOutputPort())
glyph_5.SetScaleFactor(0.05)

glyph_mapper_5 = vtkPolyDataMapper()
glyph_mapper_5.SetInputConnection(glyph_5.GetOutputPort())

glyph_actor_5 = vtkActor()
glyph_actor_5.SetMapper(glyph_mapper_5)
glyph_actor_5.GetProperty().SetColor(1, 1, 1)
glyph_actor_5.GetProperty().SetOpacity(1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(pt_load.GetOutputPort())

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
render_window.SetWindowName("smoothing filter")

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
