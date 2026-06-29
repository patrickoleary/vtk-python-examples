#!/usr/bin/env python

# Volume render a Gaussian cube file with atoms, bonds, contours, and an outline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkGlyph3D,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOChemistry import vtkGaussianCubeReader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the Gaussian cube data
reader = vtkGaussianCubeReader()
reader.SetFileName(os.path.join(data_dir, "m4_TotalDensity.cube"))
reader.SetHBScale(1.1)
reader.SetBScale(10)
reader.Update()

scalar_range = reader.GetGridOutput().GetPointData().GetScalars().GetRange()
min_val = scalar_range[0]
max_val = scalar_range[1]

# Shift and scale to unsigned char
reader_ss = vtkImageShiftScale()
reader_ss.SetInputData(reader.GetGridOutput())
reader_ss.SetShift(min_val * -1)
reader_ss.SetScale(255 / (max_val - min_val))
reader_ss.SetOutputScalarTypeToUnsignedChar()

# Outline
bounds = vtkOutlineFilter()
bounds.SetInputData(reader.GetGridOutput())

bounds_mapper = vtkPolyDataMapper()
bounds_mapper.SetInputConnection(bounds.GetOutputPort())

bounds_actor = vtkActor()
bounds_actor.SetMapper(bounds_mapper)
bounds_actor.GetProperty().SetColor(0, 0, 0)

# Contour
contour = vtkContourFilter()
contour.SetInputData(reader.GetGridOutput())
contour.GenerateValues(5, 0, 0.05)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(0, 0.1)
contour_mapper.GetLookupTable().SetHueRange(0.32, 0)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetOpacity(0.5)

# Opacity transfer function
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(0, 0.01)
opacity_transfer_function.AddPoint(255, 0.35)
opacity_transfer_function.ClampingOn()

# Color transfer function
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddHSVPoint(0.0, 0.66, 1.0, 1.0)
color_transfer_function.AddHSVPoint(50.0, 0.33, 1.0, 1.0)
color_transfer_function.AddHSVPoint(100.0, 0.00, 1.0, 1.0)

# Volume property
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)
volume_property.SetInterpolationTypeToLinear()

# Volume mapper
volume_mapper = vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader_ss.GetOutputPort())

# Volume
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Atom glyphs
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1)
sphere.SetThetaResolution(16)
sphere.SetStartTheta(0)
sphere.SetEndTheta(360)
sphere.SetPhiResolution(16)
sphere.SetStartPhi(0)
sphere.SetEndPhi(180)

glyph = vtkGlyph3D()
glyph.SetInputConnection(reader.GetOutputPort())
glyph.SetOrient(1)
glyph.SetColorMode(1)
glyph.SetScaleMode(2)
glyph.SetScaleFactor(0.6)
glyph.SetSourceConnection(sphere.GetOutputPort())

atoms_mapper = vtkPolyDataMapper()
atoms_mapper.SetInputConnection(glyph.GetOutputPort())
atoms_mapper.UseLookupTableScalarRangeOff()
atoms_mapper.SetScalarVisibility(1)
atoms_mapper.SetScalarModeToDefault()

atoms_actor = vtkActor()
atoms_actor.SetMapper(atoms_mapper)
atoms_actor.GetProperty().SetRepresentationToSurface()
atoms_actor.GetProperty().SetInterpolationToGouraud()
atoms_actor.GetProperty().SetAmbient(0.15)
atoms_actor.GetProperty().SetDiffuse(0.85)
atoms_actor.GetProperty().SetSpecular(0.1)
atoms_actor.GetProperty().SetSpecularPower(100)
atoms_actor.GetProperty().SetSpecularColor(1, 1, 1)
atoms_actor.GetProperty().SetColor(1, 1, 1)

# Bond tubes
tube = vtkTubeFilter()
tube.SetInputConnection(reader.GetOutputPort())
tube.SetNumberOfSides(16)
tube.SetCapping(0)
tube.SetRadius(0.2)
tube.SetVaryRadius(0)
tube.SetRadiusFactor(10)

bonds_mapper = vtkPolyDataMapper()
bonds_mapper.SetInputConnection(tube.GetOutputPort())
bonds_mapper.UseLookupTableScalarRangeOff()
bonds_mapper.SetScalarVisibility(1)
bonds_mapper.SetScalarModeToDefault()

bonds_actor = vtkActor()
bonds_actor.SetMapper(bonds_mapper)
bonds_actor.GetProperty().SetRepresentationToSurface()
bonds_actor.GetProperty().SetInterpolationToGouraud()
bonds_actor.GetProperty().SetAmbient(0.15)
bonds_actor.GetProperty().SetDiffuse(0.85)
bonds_actor.GetProperty().SetSpecular(0.1)
bonds_actor.GetProperty().SetSpecularPower(100)
bonds_actor.GetProperty().SetSpecularColor(1, 1, 1)
bonds_actor.GetProperty().SetColor(1, 1, 1)

renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(bounds_actor)
renderer.AddActor(atoms_actor)
renderer.AddActor(bonds_actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("gaussian")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().SetFocalPoint(12, 10.5, 15)
renderer.GetActiveCamera().SetPosition(-70, 15, 34)
renderer.GetActiveCamera().ComputeViewPlaneNormal()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
