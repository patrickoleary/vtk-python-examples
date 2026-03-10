#!/usr/bin/env python

# Create a "tissue lens" effect on a CT head dataset.  The skin isosurface
# is clipped by a sphere, and a probe filter samples the volume inside the
# sphere to reveal internal tissue intensities on the spherical surface.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D, vtkProbeFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
skin_color_rgb = (0.941, 0.722, 0.627)
backface_color_rgb = (1.0, 0.898, 0.784)
bkg_color_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Skin: extract the skin isosurface at contour value 500
skin_extractor = vtkFlyingEdges3D()
skin_extractor.SetInputConnection(reader.GetOutputPort())
skin_extractor.SetValue(0, 500)

# ClipFunction: define a spherical region for the lens
clip_function = vtkSphere()
clip_function.SetRadius(50)
clip_function.SetCenter(73, 52, 15)

# ClipDataSet: clip the skin isosurface with the sphere
skin_clip = vtkClipDataSet()
skin_clip.SetInputConnection(skin_extractor.GetOutputPort())
skin_clip.SetClipFunction(clip_function)
skin_clip.SetValue(0)
skin_clip.GenerateClipScalarsOn()
skin_clip.Update()

# Mapper: map the clipped skin surface
skin_mapper = vtkDataSetMapper()
skin_mapper.SetInputConnection(skin_clip.GetOutputPort())
skin_mapper.ScalarVisibilityOff()

# Actor: assign the clipped skin geometry with backface color
skin_actor = vtkActor()
skin_actor.SetMapper(skin_mapper)
skin_actor.GetProperty().SetDiffuseColor(skin_color_rgb)

back_property = vtkProperty()
back_property.SetDiffuseColor(backface_color_rgb)
skin_actor.SetBackfaceProperty(back_property)

# LensSource: generate a sphere matching the clip region
lens_source = vtkSphereSource()
lens_source.SetRadius(50)
lens_source.SetCenter(73, 52, 15)
lens_source.SetPhiResolution(201)
lens_source.SetThetaResolution(101)

# ProbeFilter: sample the volume onto the sphere surface
lens_probe = vtkProbeFilter()
lens_probe.SetInputConnection(lens_source.GetOutputPort())
lens_probe.SetSourceConnection(reader.GetOutputPort())

# ClipDataSet: clip the probed sphere at the skin contour value
lens_clip = vtkClipDataSet()
lens_clip.SetInputConnection(lens_probe.GetOutputPort())
lens_clip.SetValue(500)
lens_clip.GenerateClipScalarsOff()
lens_clip.Update()

# LookupTable: grayscale mapping for tissue intensities
bw_lut = vtkLookupTable()
bw_lut.SetTableRange(0, 2048)
bw_lut.SetSaturationRange(0, 0)
bw_lut.SetHueRange(0, 0)
bw_lut.SetValueRange(0.2, 1)
bw_lut.Build()

# Mapper: map the lens surface with grayscale tissue values
lens_mapper = vtkDataSetMapper()
lens_mapper.SetInputConnection(lens_clip.GetOutputPort())
lens_mapper.SetScalarRange(lens_clip.GetOutput().GetScalarRange())
lens_mapper.SetLookupTable(bw_lut)

# Actor: assign the lens geometry
lens_actor = vtkActor()
lens_actor.SetMapper(lens_mapper)

# Camera: set up an initial view direction
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.ComputeViewPlaneNormal()
camera.Azimuth(30.0)
camera.Elevation(30.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(lens_actor)
renderer.AddActor(skin_actor)
renderer.SetActiveCamera(camera)
renderer.SetBackground(bkg_color_rgb)
renderer.ResetCamera()
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TissueLens")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Initialize()
interactor.Start()
