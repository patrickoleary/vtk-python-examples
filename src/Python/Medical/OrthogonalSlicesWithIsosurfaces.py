#!/usr/bin/env python

# Display three orthogonal image planes (sagittal, axial, coronal) together
# with skin and bone isosurfaces from a CT head dataset.  Each plane uses a
# different lookup table to illustrate different color-mapping strategies.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D, vtkStripper
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
skin_color_rgb = (0.941, 0.722, 0.627)
ivory_rgb = (1.0, 1.0, 0.941)
black_rgb = (0.0, 0.0, 0.0)
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

skin_stripper = vtkStripper()
skin_stripper.SetInputConnection(skin_extractor.GetOutputPort())

skin_mapper = vtkPolyDataMapper()
skin_mapper.SetInputConnection(skin_stripper.GetOutputPort())
skin_mapper.ScalarVisibilityOff()

skin_actor = vtkActor()
skin_actor.SetMapper(skin_mapper)
skin_actor.GetProperty().SetDiffuseColor(skin_color_rgb)
skin_actor.GetProperty().SetSpecular(0.3)
skin_actor.GetProperty().SetSpecularPower(20)
skin_actor.GetProperty().SetOpacity(0.5)

# Bone: extract the bone isosurface at contour value 1150
bone_extractor = vtkFlyingEdges3D()
bone_extractor.SetInputConnection(reader.GetOutputPort())
bone_extractor.SetValue(0, 1150)

bone_stripper = vtkStripper()
bone_stripper.SetInputConnection(bone_extractor.GetOutputPort())

bone_mapper = vtkPolyDataMapper()
bone_mapper.SetInputConnection(bone_stripper.GetOutputPort())
bone_mapper.ScalarVisibilityOff()

bone_actor = vtkActor()
bone_actor.SetMapper(bone_mapper)
bone_actor.GetProperty().SetDiffuseColor(ivory_rgb)
bone_actor.VisibilityOff()

# Outline: provide spatial context around the volume
outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# LookupTable: black-and-white for the sagittal plane
bw_lut = vtkLookupTable()
bw_lut.SetTableRange(0, 2000)
bw_lut.SetSaturationRange(0, 0)
bw_lut.SetHueRange(0, 0)
bw_lut.SetValueRange(0, 1)
bw_lut.Build()

# LookupTable: full hue circle for the axial plane
hue_lut = vtkLookupTable()
hue_lut.SetTableRange(0, 2000)
hue_lut.SetHueRange(0, 1)
hue_lut.SetSaturationRange(1, 1)
hue_lut.SetValueRange(1, 1)
hue_lut.Build()

# LookupTable: single-hue saturation ramp for the coronal plane
sat_lut = vtkLookupTable()
sat_lut.SetTableRange(0, 2000)
sat_lut.SetHueRange(0.6, 0.6)
sat_lut.SetSaturationRange(0, 1)
sat_lut.SetValueRange(1, 1)
sat_lut.Build()

# Sagittal plane: black-and-white color mapping
sagittal_colors = vtkImageMapToColors()
sagittal_colors.SetInputConnection(reader.GetOutputPort())
sagittal_colors.SetLookupTable(bw_lut)
sagittal_colors.Update()

sagittal_actor = vtkImageActor()
sagittal_actor.GetMapper().SetInputConnection(sagittal_colors.GetOutputPort())
sagittal_actor.SetDisplayExtent(128, 128, 0, 255, 0, 92)
sagittal_actor.ForceOpaqueOn()

# Axial plane: full-hue color mapping
axial_colors = vtkImageMapToColors()
axial_colors.SetInputConnection(reader.GetOutputPort())
axial_colors.SetLookupTable(hue_lut)
axial_colors.Update()

axial_actor = vtkImageActor()
axial_actor.GetMapper().SetInputConnection(axial_colors.GetOutputPort())
axial_actor.SetDisplayExtent(0, 255, 0, 255, 46, 46)
axial_actor.ForceOpaqueOn()

# Coronal plane: saturation-ramp color mapping
coronal_colors = vtkImageMapToColors()
coronal_colors.SetInputConnection(reader.GetOutputPort())
coronal_colors.SetLookupTable(sat_lut)
coronal_colors.Update()

coronal_actor = vtkImageActor()
coronal_actor.GetMapper().SetInputConnection(coronal_colors.GetOutputPort())
coronal_actor.SetDisplayExtent(0, 255, 128, 128, 0, 92)
coronal_actor.ForceOpaqueOn()

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
renderer.AddActor(outline_actor)
renderer.AddActor(sagittal_actor)
renderer.AddActor(axial_actor)
renderer.AddActor(coronal_actor)
renderer.AddActor(skin_actor)
renderer.AddActor(bone_actor)
renderer.SetActiveCamera(camera)
renderer.SetBackground(bkg_color_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("OrthogonalSlicesWithIsosurfaces")
render_window.Render()

renderer.ResetCamera()
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Initialize()
interactor.Start()
