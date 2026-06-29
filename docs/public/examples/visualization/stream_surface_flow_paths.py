#!/usr/bin/env python

# Demonstrate vtkStreamSurface generating a stream surface from a
# computed vector field on a wavelet source using a circular seed.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersFlowPaths import vtkStreamSurface
from vtkmodules.vtkFiltersSources import (
    vtkRegularPolygonSource,
)
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

# Compute vector field using array calculator
calc = vtkArrayCalculator()
calc.AddCoordinateScalarVariable("coordsX", 0)
calc.AddCoordinateScalarVariable("coordsY", 1)
calc.AddCoordinateScalarVariable("coordsZ", 2)
calc.SetFunction(
    "coordsX*iHat + coordsY*jHat + 0.5*(coordsZ^2+coordsX+coordsY)*kHat")
calc.SetInputConnection(wavelet.GetOutputPort())
calc.Update()

# Circular seed with extra closing point
circle = vtkRegularPolygonSource()
circle.SetNumberOfSides(6)
circle.SetRadius(1)
circle.SetCenter(0, 0, 0)
circle.SetNormal(0, 0, 1)
circle.Update()
circle.GetOutput().GetPoints().InsertNextPoint(circle.GetOutput().GetPoint(0))

# Stream surface
stream = vtkStreamSurface()
stream.SetMaximumPropagation(100)
stream.SetMaximumNumberOfSteps(100)
stream.SetInputConnection(0, calc.GetOutputPort())
stream.SetInputConnection(1, circle.GetOutputPort())
stream.SetInitialIntegrationStep(1)
stream.SetIntegrationStepUnit(1)
stream.SetIntegratorTypeToRungeKutta4()
stream.SetUseIterativeSeeding(True)

# Stream surface mapper
stream_mapper = vtkDataSetMapper()
stream_mapper.SetInputConnection(stream.GetOutputPort())

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)
stream_actor.GetProperty().SetColor(0.1, 0.1, 0.1)
stream_actor.GetProperty().SetRepresentationToWireframe()

# Wavelet bounding box
wavelet_mapper = vtkDataSetMapper()
wavelet_mapper.SetInputConnection(wavelet.GetOutputPort())

wavelet_actor = vtkActor()
wavelet_actor.SetMapper(wavelet_mapper)
wavelet_actor.GetProperty().SetColor(0.4, 0.4, 0.4)
wavelet_actor.GetProperty().SetOpacity(0.1)
wavelet_actor.GetProperty().SetRepresentationToSurface()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(wavelet_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.SetWindowName("stream surface flow paths")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
