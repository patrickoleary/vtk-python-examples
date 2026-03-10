#!/usr/bin/env python

# Frog slice: photo (upper-left), segmentation (upper-right), composite (bottom).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageConstantPad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
    vtkWindowLevelLookupTable,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data: locate frog and frogtissue volumes
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
frog_file = str(data_dir / "Frog" / "frog.mhd")
tissue_file = str(data_dir / "Frog" / "frogtissue.mhd")
slice_number = 39

# Transform: head-first superior-to-inferior (hfsi) orientation
# Combines a 180° y-rotation (head-first) with a superior-to-inferior permutation.
hf_mat = vtkMatrix4x4()
hf_mat.Zero()
hf_mat.SetElement(0, 0, -1)
hf_mat.SetElement(1, 1, 1)
hf_mat.SetElement(2, 2, -1)
hf_mat.SetElement(3, 3, 1)

si_mat = vtkMatrix4x4()
si_mat.Zero()
si_mat.SetElement(0, 0, 1)
si_mat.SetElement(1, 2, 1)
si_mat.SetElement(2, 1, -1)
si_mat.SetElement(3, 3, 1)

hfsi_transform = vtkTransform()
hfsi_transform.Concatenate(hf_mat)
hfsi_transform.Concatenate(si_mat)

# LookupTable: tissue segmentation colors (16 labels)
lut = vtkLookupTable()
lut.SetNumberOfColors(16)
lut.SetTableRange(0, 15)
lut.Build()
lut.SetTableValue(0, 0.0, 0.0, 0.0, 1.0)          # Black
lut.SetTableValue(1, 0.980, 0.502, 0.447, 1.0)      # Salmon
lut.SetTableValue(2, 0.961, 0.961, 0.863, 1.0)      # Beige
lut.SetTableValue(3, 1.0, 0.647, 0.0, 1.0)          # Orange
lut.SetTableValue(4, 1.0, 0.894, 0.882, 1.0)        # MistyRose
lut.SetTableValue(5, 1.0, 1.0, 1.0, 1.0)            # White
lut.SetTableValue(6, 1.0, 0.388, 0.278, 1.0)        # Tomato
lut.SetTableValue(7, 0.529, 0.149, 0.341, 1.0)      # Raspberry
lut.SetTableValue(8, 0.890, 0.812, 0.341, 1.0)      # Banana
lut.SetTableValue(9, 0.804, 0.522, 0.247, 1.0)      # Peru
lut.SetTableValue(10, 1.0, 0.753, 0.796, 1.0)       # Pink
lut.SetTableValue(11, 0.690, 0.878, 0.902, 1.0)     # PowderBlue
lut.SetTableValue(12, 0.930, 0.569, 0.129, 1.0)     # Carrot
lut.SetTableValue(13, 0.961, 0.871, 0.702, 1.0)     # Wheat
lut.SetTableValue(14, 0.933, 0.510, 0.933, 1.0)     # Violet
lut.SetTableValue(15, 0.867, 0.627, 0.867, 1.0)     # Plum

# ---------- Greyscale photograph slice ----------

# Reader: load the photographic frog volume
grey_reader = vtkMetaImageReader()
grey_reader.SetFileName(frog_file)
grey_reader.Update()

# ImageConstantPad: extract a single slice
grey_padder = vtkImageConstantPad()
grey_padder.SetInputConnection(grey_reader.GetOutputPort())
grey_padder.SetOutputWholeExtent(0, 511, 0, 511, slice_number, slice_number)
grey_padder.SetConstant(0)

# PlaneSource: geometry for the textured quad
grey_plane = vtkPlaneSource()

# TransformPolyDataFilter: orient the plane with hfsi transform
grey_transform = vtkTransformPolyDataFilter()
grey_transform.SetTransform(hfsi_transform)
grey_transform.SetInputConnection(grey_plane.GetOutputPort())

# PolyDataNormals: ensure correct normal direction
grey_normals = vtkPolyDataNormals()
grey_normals.SetInputConnection(grey_transform.GetOutputPort())
grey_normals.FlipNormalsOff()

# WindowLevelLookupTable: map greyscale values
wllut = vtkWindowLevelLookupTable()
wllut.SetWindow(255)
wllut.SetLevel(128)
wllut.SetTableRange(0, 255)
wllut.Build()

# Mapper: map the plane geometry
grey_mapper = vtkPolyDataMapper()
grey_mapper.SetInputConnection(grey_plane.GetOutputPort())

# Texture: apply the greyscale slice as a texture
grey_texture = vtkTexture()
grey_texture.SetInputConnection(grey_padder.GetOutputPort())
grey_texture.SetLookupTable(wllut)
grey_texture.SetColorModeToMapScalars()
grey_texture.InterpolateOn()

# Actor: textured greyscale plane
grey_actor = vtkActor()
grey_actor.SetMapper(grey_mapper)
grey_actor.SetTexture(grey_texture)

# ---------- Segmented tissue slice ----------

# Reader: load the segmented frog tissue volume
segment_reader = vtkMetaImageReader()
segment_reader.SetFileName(tissue_file)
segment_reader.Update()

# ImageConstantPad: extract a single slice
segment_padder = vtkImageConstantPad()
segment_padder.SetInputConnection(segment_reader.GetOutputPort())
segment_padder.SetOutputWholeExtent(0, 511, 0, 511, slice_number, slice_number)
segment_padder.SetConstant(0)

# PlaneSource: geometry for the textured quad
segment_plane = vtkPlaneSource()

# TransformPolyDataFilter: orient the plane with hfsi transform
segment_transform = vtkTransformPolyDataFilter()
segment_transform.SetTransform(hfsi_transform)
segment_transform.SetInputConnection(segment_plane.GetOutputPort())

# PolyDataNormals: ensure correct normal direction
segment_normals = vtkPolyDataNormals()
segment_normals.SetInputConnection(segment_transform.GetOutputPort())
segment_normals.FlipNormalsOn()

# Mapper: map the plane geometry
segment_mapper = vtkPolyDataMapper()
segment_mapper.SetInputConnection(segment_plane.GetOutputPort())

# Texture: apply the tissue labels as a color texture
segment_texture = vtkTexture()
segment_texture.SetInputConnection(segment_padder.GetOutputPort())
segment_texture.SetLookupTable(lut)
segment_texture.SetColorModeToMapScalars()
segment_texture.InterpolateOff()

# Actor: textured segmented plane
segment_actor = vtkActor()
segment_actor.SetMapper(segment_mapper)
segment_actor.SetTexture(segment_texture)

# Actor: semi-transparent overlay of segmentation on photograph
segment_overlay_actor = vtkActor()
segment_overlay_actor.SetMapper(segment_mapper)
segment_overlay_actor.SetTexture(segment_texture)
segment_overlay_actor.GetProperty().SetOpacity(0.5)

# ---------- Renderers and window ----------

# Camera: shared across all three viewports
cam1 = vtkCamera()
cam1.SetViewUp(0, -1, 0)
cam1.SetPosition(0, 0, -1)

# Renderer: greyscale photograph (upper-left)
ren1 = vtkRenderer()
ren1.SetViewport(0, 0.5, 0.5, 1)
ren1.AddActor(grey_actor)
ren1.SetBackground(slate_gray_rgb)
ren1.SetActiveCamera(cam1)
ren1.ResetCamera()
cam1.SetViewUp(0, -1, 0)
cam1.SetPosition(0.0554068, -0.0596001, -0.491383)
cam1.SetFocalPoint(0.0554068, -0.0596001, 0)
ren1.ResetCameraClippingRange()

# Renderer: segmented tissue (upper-right)
ren2 = vtkRenderer()
ren2.SetViewport(0.5, 0.5, 1, 1)
ren2.AddActor(segment_actor)
ren2.SetBackground(slate_gray_rgb)
ren2.SetActiveCamera(ren1.GetActiveCamera())

# Renderer: composite overlay (bottom)
ren3 = vtkRenderer()
ren3.SetViewport(0, 0, 1, 0.5)
ren3.AddActor(grey_actor)
ren3.AddActor(segment_overlay_actor)
segment_overlay_actor.SetPosition(0, 0, -0.01)
ren3.SetBackground(slate_gray_rgb)
ren3.SetActiveCamera(ren1.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("FrogSlice")
render_window.AddRenderer(ren1)
render_window.AddRenderer(ren2)
render_window.AddRenderer(ren3)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
