#!/usr/bin/env python

# Test vtkHedgeHog on cow with vtkCleanPolyData PointMergingOff.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkCleanPolyData,
    vtkHedgeHog,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read cow data
wavefront = vtkOBJReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

wavefront.SetFileName(os.path.join(data_dir, "Viewpoint", "cow.obj"))
wavefront.Update()

cone = vtkConeSource()
cone.SetResolution(6)
cone.SetRadius(0.1)

transform = vtkTransform()
transform.Translate(0.5, 0.0, 0.0)
transform_f = vtkTransformPolyDataFilter()
transform_f.SetInputConnection(cone.GetOutputPort())
transform_f.SetTransform(transform)

# Clean normals with merging off
clean = vtkCleanPolyData()
clean.SetInputConnection(wavefront.GetOutputPort())
clean.PointMergingOff()

glyph = vtkHedgeHog()
glyph.SetInputConnection(clean.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleFactor(0.4)

hair_mapper = vtkPolyDataMapper()
hair_mapper.SetInputConnection(glyph.GetOutputPort())

hair_actor = vtkActor()
hair_actor.SetMapper(hair_mapper)

cow_mapper = vtkPolyDataMapper()
cow_mapper.SetInputConnection(wavefront.GetOutputPort())

cow_actor = vtkActor()
cow_actor.SetMapper(cow_mapper)

# Colors
saddle_brown_rgb = (0.545, 0.271, 0.075)
thistle_rgb = (0.847, 0.749, 0.847)

hair_actor.GetProperty().SetDiffuseColor(saddle_brown_rgb)
hair_actor.GetProperty().SetAmbientColor(thistle_rgb)
hair_actor.GetProperty().SetAmbient(0.3)

cow_actor.GetProperty().SetDiffuseColor(163 / 255.0, 148 / 255.0, 128 / 255.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cow_actor)
renderer.AddActor(hair_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hedge hog cow")
render_window.SetMultiSamples(0)
render_window.SetSize(320, 240)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(2)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
