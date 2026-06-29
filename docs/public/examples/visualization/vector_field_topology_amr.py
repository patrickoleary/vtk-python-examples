#!/usr/bin/env python

# Demonstrate vtkVectorFieldTopology on an AMR dataset from
# vtkAMRGaussianPulseSource with a computed vector field, showing
# critical points, separating lines/surfaces, and boundary features.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersAMR import vtkAMRGaussianPulseSource
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersFlowPaths import vtkVectorFieldTopology
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# AMR Gaussian pulse source
wavelet = vtkAMRGaussianPulseSource()

# Compute vector field
calc = vtkArrayCalculator()
calc.AddCoordinateScalarVariable("coordsX", 0)
calc.AddCoordinateScalarVariable("coordsY", 1)
calc.AddCoordinateScalarVariable("coordsZ", 2)
calc.SetFunction(
    "(coordsX+coordsZ-1)*iHat + coordsY*jHat + (coordsX-coordsZ+1)*kHat")
calc.SetInputConnection(wavelet.GetOutputPort())
calc.Update()

# Vector field topology
topology = vtkVectorFieldTopology()
topology.SetInputData(calc.GetOutput())
topology.SetIntegrationStepUnit(1)
topology.SetSeparatrixDistance(0.2)
topology.SetIntegrationStepSize(0.2)
topology.SetMaxNumSteps(1000)
topology.SetComputeSurfaces(True)
topology.SetUseBoundarySwitchPoints(False)
topology.SetUseIterativeSeeding(True)
topology.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "resultArray")
topology.Update()

# Bounding box via composite geometry filter
geom_filter = vtkCompositeDataGeometryFilter()
geom_filter.SetInputConnection(wavelet.GetOutputPort())
geom_filter.Update()

wavelet_mapper = vtkDataSetMapper()
wavelet_mapper.SetInputConnection(geom_filter.GetOutputPort())

wavelet_actor = vtkActor()
wavelet_actor.SetMapper(wavelet_mapper)
wavelet_actor.GetProperty().SetColor(0.4, 0.4, 1.0)
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
render_window.SetWindowName("vector field topology amr")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
