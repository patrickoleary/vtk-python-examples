#!/usr/bin/env python

# Compute Gaussian and mean curvatures on a superquadric torus using
# vtkCurvatures and display them side by side with lookup tables.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkFiltersGeneral import vtkCurvatures
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a superquadric torus
torus = vtkSuperquadricSource()
torus.SetCenter(0.0, 0.0, 0.0)
torus.SetScale(1.0, 1.0, 1.0)
torus.SetPhiResolution(64)
torus.SetThetaResolution(64)
torus.SetPhiRoundness(1.0)
torus.SetThetaRoundness(1.0)
torus.SetThickness(0.5)
torus.SetSize(0.5)
torus.SetToroidal(1)

# Clean coincident points
cleaner = vtkCleanPolyData()
cleaner.SetInputConnection(torus.GetOutputPort())
cleaner.SetTolerance(0.005)

# Gaussian curvature
curve_gauss = vtkCurvatures()
curve_gauss.SetInputConnection(cleaner.GetOutputPort())
curve_gauss.SetCurvatureTypeToGaussian()

# Mean curvature
curve_mean = vtkCurvatures()
curve_mean.SetInputConnection(cleaner.GetOutputPort())
curve_mean.SetCurvatureTypeToMean()

# Lookup table for Gaussian curvature
lut_gauss = vtkLookupTable()
lut_gauss.SetNumberOfColors(256)
lut_gauss.SetHueRange(0.15, 1.0)
lut_gauss.SetSaturationRange(1.0, 1.0)
lut_gauss.SetValueRange(1.0, 1.0)
lut_gauss.SetAlphaRange(1.0, 1.0)
lut_gauss.SetRange(-20, 20)

# Lookup table for mean curvature
lut_mean = vtkLookupTable()
lut_mean.SetNumberOfColors(256)
lut_mean.SetHueRange(0.15, 1.0)
lut_mean.SetSaturationRange(1.0, 1.0)
lut_mean.SetValueRange(1.0, 1.0)
lut_mean.SetAlphaRange(1.0, 1.0)
lut_mean.SetRange(0, 4)

# Gaussian curvature mapper and actor
gauss_mapper = vtkPolyDataMapper()
gauss_mapper.SetInputConnection(curve_gauss.GetOutputPort())
gauss_mapper.SetLookupTable(lut_gauss)
gauss_mapper.SetUseLookupTableScalarRange(1)

gauss_actor = vtkActor()
gauss_actor.SetMapper(gauss_mapper)
gauss_actor.SetPosition(-0.5, 0.0, 0.0)

# Mean curvature mapper and actor
mean_mapper = vtkPolyDataMapper()
mean_mapper.SetInputConnection(curve_mean.GetOutputPort())
mean_mapper.SetLookupTable(lut_mean)
mean_mapper.SetUseLookupTableScalarRange(1)

mean_actor = vtkActor()
mean_actor.SetMapper(mean_mapper)
mean_actor.SetPosition(0.5, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(gauss_actor)
renderer.AddActor(mean_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 200)
render_window.SetWindowName("curvatures")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetPosition(0.0, 2.0, 2.1)
camera.SetFocalPoint(0.0, 0.0, 0.0)
camera.SetViewAngle(30)
renderer.SetActiveCamera(camera)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
