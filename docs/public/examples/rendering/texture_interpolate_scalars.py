#!/usr/bin/env python

# Demonstrate texture with interpolated scalars on a textured sphere using a color transfer function.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkTexturedSphereSource
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Textured sphere with elevation scalars
sphere = vtkTexturedSphereSource()
sphere.SetThetaResolution(64)
sphere.SetPhiResolution(32)

elevation = vtkElevationFilter()
elevation.SetLowPoint(0, 0, -0.5)
elevation.SetHighPoint(0, 0, 0.5)
elevation.SetInputConnection(sphere.GetOutputPort())

# Rainbow Desaturated colormap
ctf = vtkDiscretizableColorTransferFunction()
ctf.AddRGBPoint(0.11, 0.278431, 0.278431, 0.858824)
ctf.AddRGBPoint(0.22, 0, 0, 0.360784)
ctf.AddRGBPoint(0.33, 0, 1, 1)
ctf.AddRGBPoint(0.44, 0, 0.501961, 0)
ctf.AddRGBPoint(0.55, 1, 1, 0)
ctf.AddRGBPoint(0.66, 1, 0.380392, 0)
ctf.AddRGBPoint(0.77, 0.419608, 0, 0)
ctf.AddRGBPoint(0.88, 0.878431, 0.301961, 0.301961)
ctf.DiscretizeOn()
ctf.SetNumberOfValues(8)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation.GetOutputPort())
mapper.SetLookupTable(ctf)
mapper.SetColorModeToMapScalars()
mapper.InterpolateScalarsBeforeMappingOn()

# Clouds texture
reader = vtkJPEGReader()
reader.SetFileName(os.path.join(data_dir, "clouds.jpeg"))

texture = vtkTexture()
texture.InterpolateOn()
texture.SetBlendingMode(1)  # VTK_TEXTURE_BLENDING_MODE_MODULATE
texture.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("texture interpolate scalars")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(80)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
