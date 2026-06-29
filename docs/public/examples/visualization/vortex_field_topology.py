#!/usr/bin/env python

# Demonstrate vtkVectorFieldTopology computing critical points,
# separating lines, separating surfaces, and boundary switch features
# from a computed vector field on a wavelet source.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersFlowPaths import vtkVectorFieldTopology
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)

# Compute vector field
calc = vtkArrayCalculator()
calc.AddCoordinateScalarVariable("coordsX", 0)
calc.AddCoordinateScalarVariable("coordsY", 1)
calc.AddCoordinateScalarVariable("coordsZ", 2)
calc.SetFunction(
    "coordsY*iHat - coordsX*jHat + coordsZ*kHat")
calc.SetInputConnection(wavelet.GetOutputPort())
calc.Update()

# Vector field topology
topology = vtkVectorFieldTopology()
topology.SetInputData(calc.GetOutput())
topology.SetIntegrationStepUnit(1)
topology.SetSeparatrixDistance(1)
topology.SetIntegrationStepSize(1)
topology.SetMaxNumSteps(1000)
topology.SetComputeSurfaces(True)
topology.SetUseBoundarySwitchPoints(True)
topology.SetUseIterativeSeeding(True)
topology.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "resultArray")
topology.Update()

# Bounding box
wavelet_mapper = vtkDataSetMapper()
wavelet_mapper.SetInputConnection(wavelet.GetOutputPort())

wavelet_actor = vtkActor()
wavelet_actor.SetMapper(wavelet_mapper)
wavelet_actor.GetProperty().SetColor(0.4, 0.4, 0.4)
wavelet_actor.GetProperty().SetOpacity(0.1)
wavelet_actor.GetProperty().SetRepresentationToSurface()

# Critical points
point_mapper = vtkDataSetMapper()
point_mapper.SetInputConnection(topology.GetOutputPort(0))

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetColor(0.1, 0.1, 0.1)
point_actor.GetProperty().SetPointSize(20.0)
point_actor.GetProperty().SetRenderPointsAsSpheres(True)

# Separating lines
line_mapper = vtkDataSetMapper()
line_mapper.SetInputConnection(topology.GetOutputPort(1))

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
line_actor.GetProperty().SetLineWidth(10.0)
line_actor.GetProperty().SetRenderLinesAsTubes(True)

# Separating surfaces
surface_mapper = vtkDataSetMapper()
surface_mapper.SetInputConnection(topology.GetOutputPort(2))

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetColor(0.1, 0.1, 0.1)
surface_actor.GetProperty().SetRepresentationToWireframe()

# Boundary switch lines
line_mapper_2 = vtkDataSetMapper()
line_mapper_2.SetInputConnection(topology.GetOutputPort(3))

line_actor_2 = vtkActor()
line_actor_2.SetMapper(line_mapper_2)
line_actor_2.GetProperty().SetColor(0.2, 0.2, 0.2)
line_actor_2.GetProperty().SetLineWidth(10.0)
line_actor_2.GetProperty().SetRenderLinesAsTubes(True)

# Boundary switch surfaces
surface_mapper_2 = vtkDataSetMapper()
surface_mapper_2.SetInputConnection(topology.GetOutputPort(4))

surface_actor_2 = vtkActor()
surface_actor_2.SetMapper(surface_mapper_2)
surface_actor_2.GetProperty().SetColor(0.1, 0.1, 0.1)
surface_actor_2.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(wavelet_actor)
renderer.AddActor(point_actor)
renderer.AddActor(line_actor)
renderer.AddActor(surface_actor)
renderer.AddActor(line_actor_2)
renderer.AddActor(surface_actor_2)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.SetWindowName("vortex field topology")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene - position camera based on bounds
renderer.ResetCamera()
bounds = renderer.ComputeVisiblePropBounds()
center = [(bounds[0] + bounds[1])/2, (bounds[2] + bounds[3])/2, (bounds[4] + bounds[5])/2]
max_dim = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
distance = max_dim * 1.5

camera = renderer.GetActiveCamera()
camera.SetPosition(center[0] + distance, center[1] + distance, center[2] + distance)
camera.SetFocalPoint(center[0], center[1], center[2])
camera.SetViewUp(0, 0, 1)

interactor.Initialize()
interactor.Start()
