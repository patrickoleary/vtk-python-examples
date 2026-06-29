#!/usr/bin/env python

# Demonstrate vtkSynchronizedTemplates3D on clips of a structured points
# dataset (ironProt.vtk), casting each clip to different scalar types and
# generating isosurfaces at value 30, colored with named colors.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkSynchronizedTemplates3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageClip
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
named_colors = vtkNamedColors()

# Read structured points data
reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(data_dir, "ironProt.vtk"))

# Clips — one slab per scalar type
clip_0 = vtkImageClip()
clip_0.SetInputConnection(reader.GetOutputPort())
clip_0.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 1, 6)

clip_1 = vtkImageClip()
clip_1.SetInputConnection(reader.GetOutputPort())
clip_1.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 6, 11)

clip_2 = vtkImageClip()
clip_2.SetInputConnection(reader.GetOutputPort())
clip_2.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 11, 16)

clip_3 = vtkImageClip()
clip_3.SetInputConnection(reader.GetOutputPort())
clip_3.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 16, 21)

clip_4 = vtkImageClip()
clip_4.SetInputConnection(reader.GetOutputPort())
clip_4.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 21, 26)

clip_5 = vtkImageClip()
clip_5.SetInputConnection(reader.GetOutputPort())
clip_5.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 26, 31)

clip_6 = vtkImageClip()
clip_6.SetInputConnection(reader.GetOutputPort())
clip_6.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 31, 36)

clip_7 = vtkImageClip()
clip_7.SetInputConnection(reader.GetOutputPort())
clip_7.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 36, 41)

clip_8 = vtkImageClip()
clip_8.SetInputConnection(reader.GetOutputPort())
clip_8.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 41, 46)

clip_9 = vtkImageClip()
clip_9.SetInputConnection(reader.GetOutputPort())
clip_9.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 46, 51)

# Casts — each clip to a different scalar type
cast_0 = vtkImageCast()
cast_0.SetOutputScalarTypeToUnsignedChar()
cast_0.SetInputConnection(clip_0.GetOutputPort())
cast_0.ClampOverflowOn()

cast_1 = vtkImageCast()
cast_1.SetOutputScalarTypeToChar()
cast_1.SetInputConnection(clip_1.GetOutputPort())
cast_1.ClampOverflowOn()

cast_2 = vtkImageCast()
cast_2.SetOutputScalarTypeToShort()
cast_2.SetInputConnection(clip_2.GetOutputPort())
cast_2.ClampOverflowOn()

cast_3 = vtkImageCast()
cast_3.SetOutputScalarTypeToUnsignedShort()
cast_3.SetInputConnection(clip_3.GetOutputPort())
cast_3.ClampOverflowOn()

cast_4 = vtkImageCast()
cast_4.SetOutputScalarTypeToInt()
cast_4.SetInputConnection(clip_4.GetOutputPort())
cast_4.ClampOverflowOn()

cast_5 = vtkImageCast()
cast_5.SetOutputScalarTypeToUnsignedInt()
cast_5.SetInputConnection(clip_5.GetOutputPort())
cast_5.ClampOverflowOn()

cast_6 = vtkImageCast()
cast_6.SetOutputScalarTypeToLong()
cast_6.SetInputConnection(clip_6.GetOutputPort())
cast_6.ClampOverflowOn()

cast_7 = vtkImageCast()
cast_7.SetOutputScalarTypeToUnsignedLong()
cast_7.SetInputConnection(clip_7.GetOutputPort())
cast_7.ClampOverflowOn()

cast_8 = vtkImageCast()
cast_8.SetOutputScalarTypeToFloat()
cast_8.SetInputConnection(clip_8.GetOutputPort())
cast_8.ClampOverflowOn()

cast_9 = vtkImageCast()
cast_9.SetOutputScalarTypeToDouble()
cast_9.SetInputConnection(clip_9.GetOutputPort())
cast_9.ClampOverflowOn()

# Synchronized templates 3D isosurfaces at value 30
sync_0 = vtkSynchronizedTemplates3D()
sync_0.SetInputConnection(cast_0.GetOutputPort())
sync_0.GenerateValues(1, 30, 30)

sync_1 = vtkSynchronizedTemplates3D()
sync_1.SetInputConnection(cast_1.GetOutputPort())
sync_1.GenerateValues(1, 30, 30)

sync_2 = vtkSynchronizedTemplates3D()
sync_2.SetInputConnection(cast_2.GetOutputPort())
sync_2.GenerateValues(1, 30, 30)

sync_3 = vtkSynchronizedTemplates3D()
sync_3.SetInputConnection(cast_3.GetOutputPort())
sync_3.GenerateValues(1, 30, 30)

sync_4 = vtkSynchronizedTemplates3D()
sync_4.SetInputConnection(cast_4.GetOutputPort())
sync_4.GenerateValues(1, 30, 30)

sync_5 = vtkSynchronizedTemplates3D()
sync_5.SetInputConnection(cast_5.GetOutputPort())
sync_5.GenerateValues(1, 30, 30)

sync_6 = vtkSynchronizedTemplates3D()
sync_6.SetInputConnection(cast_6.GetOutputPort())
sync_6.GenerateValues(1, 30, 30)

sync_7 = vtkSynchronizedTemplates3D()
sync_7.SetInputConnection(cast_7.GetOutputPort())
sync_7.GenerateValues(1, 30, 30)

sync_8 = vtkSynchronizedTemplates3D()
sync_8.SetInputConnection(cast_8.GetOutputPort())
sync_8.GenerateValues(1, 30, 30)

sync_9 = vtkSynchronizedTemplates3D()
sync_9.SetInputConnection(cast_9.GetOutputPort())
sync_9.GenerateValues(1, 30, 30)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

# Mapper and actor pairs with named colors
flesh_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("flesh", flesh_rgb)
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sync_0.GetOutputPort())
mapper_0.ScalarVisibilityOff()
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(flesh_rgb)
actor_0.GetProperty().SetSpecularPower(30)
actor_0.GetProperty().SetDiffuse(0.7)
actor_0.GetProperty().SetSpecular(0.5)

banana_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("banana", banana_rgb)
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(sync_1.GetOutputPort())
mapper_1.ScalarVisibilityOff()
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(banana_rgb)
actor_1.GetProperty().SetSpecularPower(30)
actor_1.GetProperty().SetDiffuse(0.7)
actor_1.GetProperty().SetSpecular(0.5)

grey_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("grey", grey_rgb)
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(sync_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(grey_rgb)
actor_2.GetProperty().SetSpecularPower(30)
actor_2.GetProperty().SetDiffuse(0.7)
actor_2.GetProperty().SetSpecular(0.5)

pink_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("pink", pink_rgb)
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(sync_3.GetOutputPort())
mapper_3.ScalarVisibilityOff()
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetDiffuseColor(pink_rgb)
actor_3.GetProperty().SetSpecularPower(30)
actor_3.GetProperty().SetDiffuse(0.7)
actor_3.GetProperty().SetSpecular(0.5)

carrot_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("carrot", carrot_rgb)
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(sync_4.GetOutputPort())
mapper_4.ScalarVisibilityOff()
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetDiffuseColor(carrot_rgb)
actor_4.GetProperty().SetSpecularPower(30)
actor_4.GetProperty().SetDiffuse(0.7)
actor_4.GetProperty().SetSpecular(0.5)

gainsboro_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("gainsboro", gainsboro_rgb)
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(sync_5.GetOutputPort())
mapper_5.ScalarVisibilityOff()
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetDiffuseColor(gainsboro_rgb)
actor_5.GetProperty().SetSpecularPower(30)
actor_5.GetProperty().SetDiffuse(0.7)
actor_5.GetProperty().SetSpecular(0.5)

tomato_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", tomato_rgb)
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(sync_6.GetOutputPort())
mapper_6.ScalarVisibilityOff()
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetDiffuseColor(tomato_rgb)
actor_6.GetProperty().SetSpecularPower(30)
actor_6.GetProperty().SetDiffuse(0.7)
actor_6.GetProperty().SetSpecular(0.5)

gold_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("gold", gold_rgb)
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(sync_7.GetOutputPort())
mapper_7.ScalarVisibilityOff()
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetDiffuseColor(gold_rgb)
actor_7.GetProperty().SetSpecularPower(30)
actor_7.GetProperty().SetDiffuse(0.7)
actor_7.GetProperty().SetSpecular(0.5)

thistle_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("thistle", thistle_rgb)
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(sync_8.GetOutputPort())
mapper_8.ScalarVisibilityOff()
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetDiffuseColor(thistle_rgb)
actor_8.GetProperty().SetSpecularPower(30)
actor_8.GetProperty().SetDiffuse(0.7)
actor_8.GetProperty().SetSpecular(0.5)

chocolate_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("chocolate", chocolate_rgb)
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(sync_9.GetOutputPort())
mapper_9.ScalarVisibilityOff()
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetDiffuseColor(chocolate_rgb)
actor_9.GetProperty().SetSpecularPower(30)
actor_9.GetProperty().SetDiffuse(0.7)
actor_9.GetProperty().SetSpecular(0.5)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.VisibilityOff()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(actor_8)
renderer.AddActor(actor_9)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.9, 0.9, 0.9)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("sync3d all")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(20)
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
