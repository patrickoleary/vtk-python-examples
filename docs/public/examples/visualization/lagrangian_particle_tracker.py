#!/usr/bin/env python

# Demonstrate vtkLagrangianParticleTracker tracking particles through
# a wavelet flow field with bounce, pass, and termination surfaces,
# using the Matida integration model.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersFlowPaths import (
    vtkLagrangianBasicIntegrationModel,
    vtkLagrangianMatidaIntegrationModel,
    vtkLagrangianParticleTracker,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkImageDataToPointSet,
    vtkMultiBlockDataGroupFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkPointSource,
    vtkSphereSource,
)
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkCommonMath import vtkRungeKutta2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create seed points
seeds = vtkPointSource()
seeds.SetNumberOfPoints(10)
seeds.SetRadius(4)
seeds.Update()
seed_pd = seeds.GetOutput()
seed_data = seed_pd.GetPointData()

# Seed particle data arrays
part_vel = vtkDoubleArray()
part_vel.SetNumberOfComponents(3)
part_vel.SetNumberOfTuples(seed_pd.GetNumberOfPoints())
part_vel.SetName("InitialVelocity")
part_vel.FillComponent(0, 2)
part_vel.FillComponent(1, 5)
part_vel.FillComponent(2, 1)

part_dens = vtkDoubleArray()
part_dens.SetNumberOfComponents(1)
part_dens.SetNumberOfTuples(seed_pd.GetNumberOfPoints())
part_dens.SetName("ParticleDensity")
part_dens.FillComponent(0, 1920)

part_diam = vtkDoubleArray()
part_diam.SetNumberOfComponents(1)
part_diam.SetNumberOfTuples(seed_pd.GetNumberOfPoints())
part_diam.SetName("ParticleDiameter")
part_diam.FillComponent(0, 0.1)

seed_data.AddArray(part_vel)
seed_data.AddArray(part_dens)
seed_data.AddArray(part_diam)

# Create wavelet flow field
wavelet = vtkRTAnalyticSource()
wavelet.Update()
wavelet_img = wavelet.GetOutput()
cell_data = wavelet_img.GetCellData()

flow_vel = vtkDoubleArray()
flow_vel.SetNumberOfComponents(3)
flow_vel.SetNumberOfTuples(wavelet_img.GetNumberOfCells())
flow_vel.SetName("FlowVelocity")
flow_vel.FillComponent(0, -0.3)
flow_vel.FillComponent(1, -0.3)
flow_vel.FillComponent(2, -0.3)

flow_dens = vtkDoubleArray()
flow_dens.SetNumberOfComponents(1)
flow_dens.SetNumberOfTuples(wavelet_img.GetNumberOfCells())
flow_dens.SetName("FlowDensity")
flow_dens.FillComponent(0, 1000)

flow_dyn_visc = vtkDoubleArray()
flow_dyn_visc.SetNumberOfComponents(1)
flow_dyn_visc.SetNumberOfTuples(wavelet_img.GetNumberOfCells())
flow_dyn_visc.SetName("FlowDynamicViscosity")
flow_dyn_visc.FillComponent(0, 0.894)

cell_data.AddArray(flow_vel)
cell_data.AddArray(flow_dens)
cell_data.AddArray(flow_dyn_visc)

# Termination surface from wavelet boundary
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(wavelet.GetOutputPort())
surface.Update()
surface_pd = surface.GetOutput()

surface_type_term = vtkDoubleArray()
surface_type_term.SetNumberOfComponents(1)
surface_type_term.SetName("SurfaceType")
surface_type_term.SetNumberOfTuples(surface_pd.GetNumberOfCells())
surface_type_term.FillComponent(
    0, vtkLagrangianBasicIntegrationModel.SURFACE_TYPE_TERM)
surface_pd.GetCellData().AddArray(surface_type_term)

# Pass-through plane
surface_pass = vtkPlaneSource()
surface_pass.SetOrigin(-10, -10, 0)
surface_pass.SetPoint1(10, -10, 0)
surface_pass.SetPoint2(-10, 10, 0)
surface_pass.Update()
pass_pd = surface_pass.GetOutput()

surface_type_pass = vtkDoubleArray()
surface_type_pass.SetNumberOfComponents(1)
surface_type_pass.SetName("SurfaceType")
surface_type_pass.SetNumberOfTuples(pass_pd.GetNumberOfCells())
surface_type_pass.FillComponent(
    0, vtkLagrangianBasicIntegrationModel.SURFACE_TYPE_PASS)
pass_pd.GetCellData().AddArray(surface_type_pass)

# Bounce plane
surface_bounce = vtkPlaneSource()
surface_bounce.SetOrigin(-2, -2, -2)
surface_bounce.SetPoint1(5, -2, -2)
surface_bounce.SetPoint2(-2, 5, -2)
surface_bounce.Update()
bounce_pd = surface_bounce.GetOutput()

surface_type_bounce = vtkDoubleArray()
surface_type_bounce.SetNumberOfComponents(1)
surface_type_bounce.SetName("SurfaceType")
surface_type_bounce.SetNumberOfTuples(bounce_pd.GetNumberOfCells())
surface_type_bounce.FillComponent(
    0, vtkLagrangianBasicIntegrationModel.SURFACE_TYPE_BOUNCE)
bounce_pd.GetCellData().AddArray(surface_type_bounce)

# Group surfaces
group_surface = vtkMultiBlockDataGroupFilter()
group_surface.AddInputDataObject(surface_pd)
group_surface.AddInputDataObject(pass_pd)
group_surface.AddInputDataObject(bounce_pd)

# Convert image data to point set for tracker
ug_flow = vtkImageDataToPointSet()
ug_flow.AddInputData(wavelet_img)

# Integration model
integrator = vtkRungeKutta2()

integration_model = vtkLagrangianMatidaIntegrationModel()
integration_model.SetInputArrayToProcess(
    0, 1, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "InitialVelocity")
integration_model.SetInputArrayToProcess(
    2, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "SurfaceType")
integration_model.SetInputArrayToProcess(
    3, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "FlowVelocity")
integration_model.SetInputArrayToProcess(
    4, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "FlowDensity")
integration_model.SetInputArrayToProcess(
    5, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "FlowDynamicViscosity")
integration_model.SetInputArrayToProcess(
    6, 1, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "ParticleDiameter")
integration_model.SetInputArrayToProcess(
    7, 1, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "ParticleDensity")
integration_model.SetNumberOfTrackedUserData(13)

# Particle tracker
tracker = vtkLagrangianParticleTracker()
tracker.SetIntegrator(integrator)
tracker.SetIntegrationModel(integration_model)
tracker.SetInputData(wavelet_img)
tracker.SetSourceData(seed_pd)
tracker.SetSurfaceConnection(group_surface.GetOutputPort())
tracker.SetStepFactor(0.1)
tracker.SetStepFactorMin(0.1)
tracker.SetStepFactorMax(0.1)
tracker.SetMaximumNumberOfSteps(300)
tracker.SetCellLengthComputationMode(
    vtkLagrangianParticleTracker.STEP_CUR_CELL_VEL_DIR)
tracker.AdaptiveStepReintegrationOff()
tracker.ForcePManualShiftOn()
tracker.Update()

streams = tracker.GetOutput()
mb_inter = tracker.GetOutputDataObject(1)

# Glyph for interaction points
sphere_glyph = vtkSphereSource()
sphere_glyph.SetRadius(0.1)

glyph = vtkGlyph3D()
glyph.SetSourceConnection(sphere_glyph.GetOutputPort())
glyph.SetInputData(mb_inter.GetBlock(1))

# Stream paths mapper
mapper = vtkPolyDataMapper()
mapper.SetInputData(streams)

actor = vtkActor()
actor.SetMapper(mapper)

# Bounce surface
bounce_mapper = vtkPolyDataMapper()
bounce_mapper.SetInputConnection(surface_bounce.GetOutputPort())

bounce_actor = vtkActor()
bounce_actor.SetMapper(bounce_mapper)

# Pass surface
pass_mapper = vtkPolyDataMapper()
pass_mapper.SetInputConnection(surface_pass.GetOutputPort())

pass_actor = vtkActor()
pass_actor.SetMapper(pass_mapper)

# Glyph for interaction points
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(bounce_actor)
renderer.AddActor(pass_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.1, 0.5, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrangian particle tracker")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, -1)
camera.SetViewUp(0, 0, 1)
camera.SetPosition(0, -40, 0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
