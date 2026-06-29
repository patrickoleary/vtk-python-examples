#!/usr/bin/env python

# Test marching contours on image data cast to various scalar types.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkMarchingContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageClip,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()

# Read structured points
structured_reader = vtkStructuredPointsReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

structured_reader.SetFileName(os.path.join(data_dir, "ironProt.vtk"))

# Clip/Cast/Iso pipeline 0: UnsignedChar
clip_0 = vtkImageClip()
clip_0.SetInputConnection(structured_reader.GetOutputPort())
clip_0.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 1, 6)

cast_0 = vtkImageCast()
cast_0.SetOutputScalarTypeToUnsignedChar()
cast_0.SetInputConnection(clip_0.GetOutputPort())
cast_0.ClampOverflowOn()

iso_0 = vtkMarchingContourFilter()
iso_0.SetInputConnection(cast_0.GetOutputPort())
iso_0.GenerateValues(1, 30, 30)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(iso_0.GetOutputPort())
mapper_0.ScalarVisibilityOff()

rgb_0 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("flesh", rgb_0)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(rgb_0)
actor_0.GetProperty().SetSpecularPower(30)
actor_0.GetProperty().SetDiffuse(.7)
actor_0.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 1: Char
clip_1 = vtkImageClip()
clip_1.SetInputConnection(structured_reader.GetOutputPort())
clip_1.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 6, 11)

cast_1 = vtkImageCast()
cast_1.SetOutputScalarTypeToChar()
cast_1.SetInputConnection(clip_1.GetOutputPort())
cast_1.ClampOverflowOn()

iso_1 = vtkMarchingContourFilter()
iso_1.SetInputConnection(cast_1.GetOutputPort())
iso_1.GenerateValues(1, 30, 30)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(iso_1.GetOutputPort())
mapper_1.ScalarVisibilityOff()

rgb_1 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("banana", rgb_1)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(rgb_1)
actor_1.GetProperty().SetSpecularPower(30)
actor_1.GetProperty().SetDiffuse(.7)
actor_1.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 2: Short
clip_2 = vtkImageClip()
clip_2.SetInputConnection(structured_reader.GetOutputPort())
clip_2.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 11, 16)

cast_2 = vtkImageCast()
cast_2.SetOutputScalarTypeToShort()
cast_2.SetInputConnection(clip_2.GetOutputPort())
cast_2.ClampOverflowOn()

iso_2 = vtkMarchingContourFilter()
iso_2.SetInputConnection(cast_2.GetOutputPort())
iso_2.GenerateValues(1, 30, 30)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(iso_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

rgb_2 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("grey", rgb_2)
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(rgb_2)
actor_2.GetProperty().SetSpecularPower(30)
actor_2.GetProperty().SetDiffuse(.7)
actor_2.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 3: UnsignedShort
clip_3 = vtkImageClip()
clip_3.SetInputConnection(structured_reader.GetOutputPort())
clip_3.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 16, 21)

cast_3 = vtkImageCast()
cast_3.SetOutputScalarTypeToUnsignedShort()
cast_3.SetInputConnection(clip_3.GetOutputPort())
cast_3.ClampOverflowOn()

iso_3 = vtkMarchingContourFilter()
iso_3.SetInputConnection(cast_3.GetOutputPort())
iso_3.GenerateValues(1, 30, 30)

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(iso_3.GetOutputPort())
mapper_3.ScalarVisibilityOff()

rgb_3 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("pink", rgb_3)
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetDiffuseColor(rgb_3)
actor_3.GetProperty().SetSpecularPower(30)
actor_3.GetProperty().SetDiffuse(.7)
actor_3.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 4: Int
clip_4 = vtkImageClip()
clip_4.SetInputConnection(structured_reader.GetOutputPort())
clip_4.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 21, 26)

cast_4 = vtkImageCast()
cast_4.SetOutputScalarTypeToInt()
cast_4.SetInputConnection(clip_4.GetOutputPort())
cast_4.ClampOverflowOn()

iso_4 = vtkMarchingContourFilter()
iso_4.SetInputConnection(cast_4.GetOutputPort())
iso_4.GenerateValues(1, 30, 30)

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(iso_4.GetOutputPort())
mapper_4.ScalarVisibilityOff()

rgb_4 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("carrot", rgb_4)
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetDiffuseColor(rgb_4)
actor_4.GetProperty().SetSpecularPower(30)
actor_4.GetProperty().SetDiffuse(.7)
actor_4.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 5: UnsignedInt
clip_5 = vtkImageClip()
clip_5.SetInputConnection(structured_reader.GetOutputPort())
clip_5.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 26, 31)

cast_5 = vtkImageCast()
cast_5.SetOutputScalarTypeToUnsignedInt()
cast_5.SetInputConnection(clip_5.GetOutputPort())
cast_5.ClampOverflowOn()

iso_5 = vtkMarchingContourFilter()
iso_5.SetInputConnection(cast_5.GetOutputPort())
iso_5.GenerateValues(1, 30, 30)

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(iso_5.GetOutputPort())
mapper_5.ScalarVisibilityOff()

rgb_5 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("gainsboro", rgb_5)
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetDiffuseColor(rgb_5)
actor_5.GetProperty().SetSpecularPower(30)
actor_5.GetProperty().SetDiffuse(.7)
actor_5.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 6: Long
clip_6 = vtkImageClip()
clip_6.SetInputConnection(structured_reader.GetOutputPort())
clip_6.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 31, 36)

cast_6 = vtkImageCast()
cast_6.SetOutputScalarTypeToLong()
cast_6.SetInputConnection(clip_6.GetOutputPort())
cast_6.ClampOverflowOn()

iso_6 = vtkMarchingContourFilter()
iso_6.SetInputConnection(cast_6.GetOutputPort())
iso_6.GenerateValues(1, 30, 30)

mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(iso_6.GetOutputPort())
mapper_6.ScalarVisibilityOff()

rgb_6 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", rgb_6)
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetDiffuseColor(rgb_6)
actor_6.GetProperty().SetSpecularPower(30)
actor_6.GetProperty().SetDiffuse(.7)
actor_6.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 7: UnsignedLong
clip_7 = vtkImageClip()
clip_7.SetInputConnection(structured_reader.GetOutputPort())
clip_7.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 36, 41)

cast_7 = vtkImageCast()
cast_7.SetOutputScalarTypeToUnsignedLong()
cast_7.SetInputConnection(clip_7.GetOutputPort())
cast_7.ClampOverflowOn()

iso_7 = vtkMarchingContourFilter()
iso_7.SetInputConnection(cast_7.GetOutputPort())
iso_7.GenerateValues(1, 30, 30)

mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(iso_7.GetOutputPort())
mapper_7.ScalarVisibilityOff()

rgb_7 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("gold", rgb_7)
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetDiffuseColor(rgb_7)
actor_7.GetProperty().SetSpecularPower(30)
actor_7.GetProperty().SetDiffuse(.7)
actor_7.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 8: Float
clip_8 = vtkImageClip()
clip_8.SetInputConnection(structured_reader.GetOutputPort())
clip_8.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 41, 46)

cast_8 = vtkImageCast()
cast_8.SetOutputScalarTypeToFloat()
cast_8.SetInputConnection(clip_8.GetOutputPort())
cast_8.ClampOverflowOn()

iso_8 = vtkMarchingContourFilter()
iso_8.SetInputConnection(cast_8.GetOutputPort())
iso_8.GenerateValues(1, 30, 30)

mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(iso_8.GetOutputPort())
mapper_8.ScalarVisibilityOff()

rgb_8 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("thistle", rgb_8)
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetDiffuseColor(rgb_8)
actor_8.GetProperty().SetSpecularPower(30)
actor_8.GetProperty().SetDiffuse(.7)
actor_8.GetProperty().SetSpecular(.5)

# Clip/Cast/Iso pipeline 9: Double
clip_9 = vtkImageClip()
clip_9.SetInputConnection(structured_reader.GetOutputPort())
clip_9.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 46, 51)

cast_9 = vtkImageCast()
cast_9.SetOutputScalarTypeToDouble()
cast_9.SetInputConnection(clip_9.GetOutputPort())
cast_9.ClampOverflowOn()

iso_9 = vtkMarchingContourFilter()
iso_9.SetInputConnection(cast_9.GetOutputPort())
iso_9.GenerateValues(1, 30, 30)

mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(iso_9.GetOutputPort())
mapper_9.ScalarVisibilityOff()

rgb_9 = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("chocolate", rgb_9)
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetDiffuseColor(rgb_9)
actor_9.GetProperty().SetSpecularPower(30)
actor_9.GetProperty().SetDiffuse(.7)
actor_9.GetProperty().SetSpecular(.5)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(structured_reader.GetOutputPort())

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
renderer.SetBackground(0.9, .9, .9)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("image mc all")

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
