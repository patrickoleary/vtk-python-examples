#!/usr/bin/env python

# Demonstrate vtkContourFilter on 2D slices of a volume dataset (nut.slc),
# casting each slice to different scalar types and generating contours
# at value 30, with an outline around the volume.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageClip
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read volume data
reader = vtkSLCReader()
reader.SetFileName(os.path.join(data_dir, "nut.slc"))
reader.Update()

# Clips — one 2D slice per scalar type
clip_0 = vtkImageClip()
clip_0.SetInputConnection(reader.GetOutputPort())
clip_0.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 3, 3)

clip_1 = vtkImageClip()
clip_1.SetInputConnection(reader.GetOutputPort())
clip_1.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 5, 5)

clip_2 = vtkImageClip()
clip_2.SetInputConnection(reader.GetOutputPort())
clip_2.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 7, 7)

clip_3 = vtkImageClip()
clip_3.SetInputConnection(reader.GetOutputPort())
clip_3.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 9, 9)

clip_4 = vtkImageClip()
clip_4.SetInputConnection(reader.GetOutputPort())
clip_4.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 11, 11)

clip_5 = vtkImageClip()
clip_5.SetInputConnection(reader.GetOutputPort())
clip_5.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 13, 13)

clip_6 = vtkImageClip()
clip_6.SetInputConnection(reader.GetOutputPort())
clip_6.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 15, 15)

clip_7 = vtkImageClip()
clip_7.SetInputConnection(reader.GetOutputPort())
clip_7.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 17, 17)

clip_8 = vtkImageClip()
clip_8.SetInputConnection(reader.GetOutputPort())
clip_8.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 19, 19)

clip_9 = vtkImageClip()
clip_9.SetInputConnection(reader.GetOutputPort())
clip_9.SetOutputWholeExtent(-1000, 1000, -1000, 1000, 21, 21)

# Casts — each clip to a different scalar type
cast_0 = vtkImageCast()
cast_0.SetOutputScalarTypeToChar()
cast_0.SetInputConnection(clip_0.GetOutputPort())
cast_0.ClampOverflowOn()

cast_1 = vtkImageCast()
cast_1.SetOutputScalarTypeToUnsignedChar()
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

# Contours at value 30
contour_0 = vtkContourFilter()
contour_0.SetInputConnection(cast_0.GetOutputPort())
contour_0.GenerateValues(1, 30, 30)

contour_1 = vtkContourFilter()
contour_1.SetInputConnection(cast_1.GetOutputPort())
contour_1.GenerateValues(1, 30, 30)

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(cast_2.GetOutputPort())
contour_2.GenerateValues(1, 30, 30)

contour_3 = vtkContourFilter()
contour_3.SetInputConnection(cast_3.GetOutputPort())
contour_3.GenerateValues(1, 30, 30)

contour_4 = vtkContourFilter()
contour_4.SetInputConnection(cast_4.GetOutputPort())
contour_4.GenerateValues(1, 30, 30)

contour_5 = vtkContourFilter()
contour_5.SetInputConnection(cast_5.GetOutputPort())
contour_5.GenerateValues(1, 30, 30)

contour_6 = vtkContourFilter()
contour_6.SetInputConnection(cast_6.GetOutputPort())
contour_6.GenerateValues(1, 30, 30)

contour_7 = vtkContourFilter()
contour_7.SetInputConnection(cast_7.GetOutputPort())
contour_7.GenerateValues(1, 30, 30)

contour_8 = vtkContourFilter()
contour_8.SetInputConnection(cast_8.GetOutputPort())
contour_8.GenerateValues(1, 30, 30)

contour_9 = vtkContourFilter()
contour_9.SetInputConnection(cast_9.GetOutputPort())
contour_9.GenerateValues(1, 30, 30)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

# Mapper and actor pairs
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(contour_0.GetOutputPort())
mapper_0.SetColorModeToMapScalars()
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(contour_1.GetOutputPort())
mapper_1.SetColorModeToMapScalars()
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(contour_2.GetOutputPort())
mapper_2.SetColorModeToMapScalars()
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(contour_3.GetOutputPort())
mapper_3.SetColorModeToMapScalars()
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(contour_4.GetOutputPort())
mapper_4.SetColorModeToMapScalars()
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(contour_5.GetOutputPort())
mapper_5.SetColorModeToMapScalars()
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)

mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(contour_6.GetOutputPort())
mapper_6.SetColorModeToMapScalars()
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)

mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(contour_7.GetOutputPort())
mapper_7.SetColorModeToMapScalars()
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)

mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(contour_8.GetOutputPort())
mapper_8.SetColorModeToMapScalars()
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)

mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(contour_9.GetOutputPort())
mapper_9.SetColorModeToMapScalars()
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)

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
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("contour2d all")

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
