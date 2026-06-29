#!/usr/bin/env python

# Demonstrate multi-texturing on a textured sphere with two texture layers.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersSources import vtkTexturedSphereSource
from vtkmodules.vtkIOImage import vtkJPEGReader, vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Textured sphere
sphere = vtkTexturedSphereSource()
sphere.SetThetaResolution(64)
sphere.SetPhiResolution(32)
sphere.Update()
pd = sphere.GetOutput()

# Create second texture coordinate array with modified V
tcoord = pd.GetPointData().GetTCoords()
tcoord2 = vtkFloatArray()
tcoord2.SetNumberOfComponents(2)
tcoord2.SetNumberOfTuples(tcoord.GetNumberOfTuples())
for i in range(tcoord.GetNumberOfTuples()):
    u, v = tcoord.GetTuple2(i)
    tcoord2.SetTuple2(i, u, v * 2.0)
tcoord2.SetName("tcoord2")
pd.GetPointData().AddArray(tcoord2)

mapper = vtkPolyDataMapper()
mapper.SetInputData(pd)

actor = vtkActor()
actor.SetMapper(mapper)

# Earth color texture from TIFF
reader_1 = vtkTIFFReader()
reader_1.SetFileName(os.path.join(data_dir, "GIS", "raster.tif"))
tex_1 = vtkTexture()
tex_1.InterpolateOn()
tex_1.SetInputConnection(reader_1.GetOutputPort())
actor.GetProperty().SetTexture("earth_color", tex_1)

# Cloud texture from JPEG with additive blending
reader_2 = vtkJPEGReader()
reader_2.SetFileName(os.path.join(data_dir, "clouds.jpeg"))
tex_2 = vtkTexture()
tex_2.InterpolateOn()
tex_2.SetBlendingMode(4)  # VTK_TEXTURE_BLENDING_MODE_ADD
tex_2.SetInputConnection(reader_2.GetOutputPort())
actor.GetProperty().SetTexture("skyclouds", tex_2)

# Map second tcoord array to skyclouds texture unit
mapper.MapDataArrayToMultiTextureAttribute(
    "skyclouds", "tcoord2", vtkDataObject.FIELD_ASSOCIATION_POINTS
)

# Rendering pipeline
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("multi texturing")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-45)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
