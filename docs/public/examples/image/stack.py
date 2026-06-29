#!/usr/bin/env python

# Test vtkImageStack for image layering with checkerboard and lookup table overlays.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkImageProperty,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingImage import (
    vtkImageResliceMapper,
    vtkImageStack,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read headsq data
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.Update()

# Red lookup table with alpha ramp
lookup_table = vtkLookupTable()
lookup_table.SetValueRange(0.0, 1.0)
lookup_table.SetSaturationRange(1.0, 1.0)
lookup_table.SetHueRange(0.0, 0.0)
lookup_table.SetAlphaRange(0.0, 1.0)
lookup_table.SetRampToLinear()
lookup_table.Build()

# --- Viewport 0: vtkImageSliceMapper, checkerboard overlay ---

base_property_0 = vtkImageProperty()
base_property_0.SetColorWindow(2000)
base_property_0.SetColorLevel(1000)
base_property_0.SetAmbient(0.0)
base_property_0.SetDiffuse(1.0)
base_property_0.SetInterpolationTypeToLinear()
base_property_0.SetLayerNumber(0)

overlay_property_0 = vtkImageProperty()
overlay_property_0.SetColorWindow(2000)
overlay_property_0.SetColorLevel(1000)
overlay_property_0.SetAmbient(0.0)
overlay_property_0.SetDiffuse(1.0)
overlay_property_0.SetLookupTable(lookup_table)
overlay_property_0.SetInterpolationTypeToLinear()
overlay_property_0.SetLayerNumber(1)
overlay_property_0.BackingOn()
overlay_property_0.CheckerboardOn()
overlay_property_0.SetCheckerboardSpacing(25.0, 25.0)

# Slice X
base_mapper_0_x = vtkImageSliceMapper()
base_mapper_0_x.SetInputConnection(reader.GetOutputPort())
base_mapper_0_x.SliceAtFocalPointOn()
base_mapper_0_x.BorderOn()
base_mapper_0_x.SetOrientation(0)

overlay_mapper_0_x = vtkImageSliceMapper()
overlay_mapper_0_x.SetInputConnection(reader.GetOutputPort())
overlay_mapper_0_x.SliceAtFocalPointOn()
overlay_mapper_0_x.BorderOn()
overlay_mapper_0_x.SetOrientation(0)

base_image_0_x = vtkImageSlice()
base_image_0_x.SetProperty(base_property_0)
base_image_0_x.SetMapper(base_mapper_0_x)

overlay_image_0_x = vtkImageSlice()
overlay_image_0_x.SetProperty(overlay_property_0)
overlay_image_0_x.SetMapper(overlay_mapper_0_x)

stack_0_x = vtkImageStack()
stack_0_x.AddImage(overlay_image_0_x)
stack_0_x.AddImage(base_image_0_x)
stack_0_x.SetActiveLayer(1)
stack_0_x.RotateY(-5)
stack_0_x.RotateX(-10)

outline_filter_0_x = vtkOutlineFilter()
outline_filter_0_x.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_x = vtkDataSetMapper()
outline_mapper_0_x.SetInputConnection(outline_filter_0_x.GetOutputPort())

outline_actor_0_x = vtkActor()
outline_actor_0_x.SetMapper(outline_mapper_0_x)
outline_actor_0_x.RotateY(-5)
outline_actor_0_x.RotateX(-10)

# Slice Y
base_mapper_0_y = vtkImageSliceMapper()
base_mapper_0_y.SetInputConnection(reader.GetOutputPort())
base_mapper_0_y.SliceAtFocalPointOn()
base_mapper_0_y.BorderOn()
base_mapper_0_y.SetOrientation(1)

overlay_mapper_0_y = vtkImageSliceMapper()
overlay_mapper_0_y.SetInputConnection(reader.GetOutputPort())
overlay_mapper_0_y.SliceAtFocalPointOn()
overlay_mapper_0_y.BorderOn()
overlay_mapper_0_y.SetOrientation(1)

base_image_0_y = vtkImageSlice()
base_image_0_y.SetProperty(base_property_0)
base_image_0_y.SetMapper(base_mapper_0_y)

overlay_image_0_y = vtkImageSlice()
overlay_image_0_y.SetProperty(overlay_property_0)
overlay_image_0_y.SetMapper(overlay_mapper_0_y)

stack_0_y = vtkImageStack()
stack_0_y.AddImage(overlay_image_0_y)
stack_0_y.AddImage(base_image_0_y)
stack_0_y.SetActiveLayer(1)
stack_0_y.RotateY(-5)
stack_0_y.RotateX(-10)

outline_filter_0_y = vtkOutlineFilter()
outline_filter_0_y.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_y = vtkDataSetMapper()
outline_mapper_0_y.SetInputConnection(outline_filter_0_y.GetOutputPort())

outline_actor_0_y = vtkActor()
outline_actor_0_y.SetMapper(outline_mapper_0_y)
outline_actor_0_y.RotateY(-5)
outline_actor_0_y.RotateX(-10)

# Slice Z
base_mapper_0_z = vtkImageSliceMapper()
base_mapper_0_z.SetInputConnection(reader.GetOutputPort())
base_mapper_0_z.SliceAtFocalPointOn()
base_mapper_0_z.BorderOn()
base_mapper_0_z.SetOrientation(2)

overlay_mapper_0_z = vtkImageSliceMapper()
overlay_mapper_0_z.SetInputConnection(reader.GetOutputPort())
overlay_mapper_0_z.SliceAtFocalPointOn()
overlay_mapper_0_z.BorderOn()
overlay_mapper_0_z.SetOrientation(2)

base_image_0_z = vtkImageSlice()
base_image_0_z.SetProperty(base_property_0)
base_image_0_z.SetMapper(base_mapper_0_z)

overlay_image_0_z = vtkImageSlice()
overlay_image_0_z.SetProperty(overlay_property_0)
overlay_image_0_z.SetMapper(overlay_mapper_0_z)

stack_0_z = vtkImageStack()
stack_0_z.AddImage(overlay_image_0_z)
stack_0_z.AddImage(base_image_0_z)
stack_0_z.SetActiveLayer(1)
stack_0_z.RotateY(-5)
stack_0_z.RotateX(-10)

outline_filter_0_z = vtkOutlineFilter()
outline_filter_0_z.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_z = vtkDataSetMapper()
outline_mapper_0_z.SetInputConnection(outline_filter_0_z.GetOutputPort())

outline_actor_0_z = vtkActor()
outline_actor_0_z.SetMapper(outline_mapper_0_z)
outline_actor_0_z.RotateY(-5)
outline_actor_0_z.RotateX(-10)

# --- Viewport 1: vtkImageResliceMapper, checkerboard overlay ---

base_property_1 = vtkImageProperty()
base_property_1.SetColorWindow(2000)
base_property_1.SetColorLevel(1000)
base_property_1.SetAmbient(0.0)
base_property_1.SetDiffuse(1.0)
base_property_1.SetInterpolationTypeToLinear()
base_property_1.SetLayerNumber(0)

overlay_property_1 = vtkImageProperty()
overlay_property_1.SetColorWindow(2000)
overlay_property_1.SetColorLevel(1000)
overlay_property_1.SetAmbient(0.0)
overlay_property_1.SetDiffuse(1.0)
overlay_property_1.SetLookupTable(lookup_table)
overlay_property_1.SetInterpolationTypeToLinear()
overlay_property_1.SetLayerNumber(1)
overlay_property_1.BackingOn()
overlay_property_1.CheckerboardOn()
overlay_property_1.SetCheckerboardSpacing(25.0, 25.0)

# Slice X
base_reslice_mapper_1_x = vtkImageResliceMapper()
base_reslice_mapper_1_x.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_1_x.SliceAtFocalPointOn()
base_reslice_mapper_1_x.BorderOn()
base_reslice_mapper_1_x.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)

overlay_reslice_mapper_1_x = vtkImageResliceMapper()
overlay_reslice_mapper_1_x.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_1_x.SliceAtFocalPointOn()
overlay_reslice_mapper_1_x.BorderOn()
overlay_reslice_mapper_1_x.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)

base_image_1_x = vtkImageSlice()
base_image_1_x.SetProperty(base_property_1)
base_image_1_x.SetMapper(base_reslice_mapper_1_x)
base_image_1_x.RotateX(10)
base_image_1_x.RotateY(5)

overlay_image_1_x = vtkImageSlice()
overlay_image_1_x.SetProperty(overlay_property_1)
overlay_image_1_x.SetMapper(overlay_reslice_mapper_1_x)

stack_1_x = vtkImageStack()
stack_1_x.AddImage(overlay_image_1_x)
stack_1_x.AddImage(base_image_1_x)
stack_1_x.SetActiveLayer(1)
stack_1_x.RotateY(-5)
stack_1_x.RotateX(-10)

outline_filter_1_x = vtkOutlineFilter()
outline_filter_1_x.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_x = vtkDataSetMapper()
outline_mapper_1_x.SetInputConnection(outline_filter_1_x.GetOutputPort())

outline_actor_1_x = vtkActor()
outline_actor_1_x.SetMapper(outline_mapper_1_x)
outline_actor_1_x.RotateX(10)
outline_actor_1_x.RotateY(5)
outline_actor_1_x.RotateY(-5)
outline_actor_1_x.RotateX(-10)

# Slice Y
base_reslice_mapper_1_y = vtkImageResliceMapper()
base_reslice_mapper_1_y.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_1_y.SliceAtFocalPointOn()
base_reslice_mapper_1_y.BorderOn()
base_reslice_mapper_1_y.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)

overlay_reslice_mapper_1_y = vtkImageResliceMapper()
overlay_reslice_mapper_1_y.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_1_y.SliceAtFocalPointOn()
overlay_reslice_mapper_1_y.BorderOn()
overlay_reslice_mapper_1_y.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)

base_image_1_y = vtkImageSlice()
base_image_1_y.SetProperty(base_property_1)
base_image_1_y.SetMapper(base_reslice_mapper_1_y)
base_image_1_y.RotateX(10)
base_image_1_y.RotateY(5)

overlay_image_1_y = vtkImageSlice()
overlay_image_1_y.SetProperty(overlay_property_1)
overlay_image_1_y.SetMapper(overlay_reslice_mapper_1_y)

stack_1_y = vtkImageStack()
stack_1_y.AddImage(overlay_image_1_y)
stack_1_y.AddImage(base_image_1_y)
stack_1_y.SetActiveLayer(1)
stack_1_y.RotateY(-5)
stack_1_y.RotateX(-10)

outline_filter_1_y = vtkOutlineFilter()
outline_filter_1_y.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_y = vtkDataSetMapper()
outline_mapper_1_y.SetInputConnection(outline_filter_1_y.GetOutputPort())

outline_actor_1_y = vtkActor()
outline_actor_1_y.SetMapper(outline_mapper_1_y)
outline_actor_1_y.RotateX(10)
outline_actor_1_y.RotateY(5)
outline_actor_1_y.RotateY(-5)
outline_actor_1_y.RotateX(-10)

# Slice Z
base_reslice_mapper_1_z = vtkImageResliceMapper()
base_reslice_mapper_1_z.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_1_z.SliceAtFocalPointOn()
base_reslice_mapper_1_z.BorderOn()
base_reslice_mapper_1_z.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)

overlay_reslice_mapper_1_z = vtkImageResliceMapper()
overlay_reslice_mapper_1_z.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_1_z.SliceAtFocalPointOn()
overlay_reslice_mapper_1_z.BorderOn()
overlay_reslice_mapper_1_z.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)

base_image_1_z = vtkImageSlice()
base_image_1_z.SetProperty(base_property_1)
base_image_1_z.SetMapper(base_reslice_mapper_1_z)
base_image_1_z.RotateX(10)
base_image_1_z.RotateY(5)

overlay_image_1_z = vtkImageSlice()
overlay_image_1_z.SetProperty(overlay_property_1)
overlay_image_1_z.SetMapper(overlay_reslice_mapper_1_z)

stack_1_z = vtkImageStack()
stack_1_z.AddImage(overlay_image_1_z)
stack_1_z.AddImage(base_image_1_z)
stack_1_z.SetActiveLayer(1)
stack_1_z.RotateY(-5)
stack_1_z.RotateX(-10)

outline_filter_1_z = vtkOutlineFilter()
outline_filter_1_z.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_z = vtkDataSetMapper()
outline_mapper_1_z.SetInputConnection(outline_filter_1_z.GetOutputPort())

outline_actor_1_z = vtkActor()
outline_actor_1_z.SetMapper(outline_mapper_1_z)
outline_actor_1_z.RotateX(10)
outline_actor_1_z.RotateY(5)
outline_actor_1_z.RotateY(-5)
outline_actor_1_z.RotateX(-10)

# --- Viewport 2: vtkImageSliceMapper, no checkerboard ---

base_property_2 = vtkImageProperty()
base_property_2.SetColorWindow(2000)
base_property_2.SetColorLevel(1000)
base_property_2.SetAmbient(0.0)
base_property_2.SetDiffuse(1.0)
base_property_2.SetInterpolationTypeToLinear()
base_property_2.SetLayerNumber(0)

overlay_property_2 = vtkImageProperty()
overlay_property_2.SetColorWindow(2000)
overlay_property_2.SetColorLevel(1000)
overlay_property_2.SetAmbient(0.0)
overlay_property_2.SetDiffuse(1.0)
overlay_property_2.SetLookupTable(lookup_table)
overlay_property_2.SetInterpolationTypeToLinear()
overlay_property_2.SetLayerNumber(1)
overlay_property_2.BackingOn()

# Slice X
base_mapper_2_x = vtkImageSliceMapper()
base_mapper_2_x.SetInputConnection(reader.GetOutputPort())
base_mapper_2_x.SliceAtFocalPointOn()
base_mapper_2_x.BorderOn()
base_mapper_2_x.SetOrientation(0)

overlay_mapper_2_x = vtkImageSliceMapper()
overlay_mapper_2_x.SetInputConnection(reader.GetOutputPort())
overlay_mapper_2_x.SliceAtFocalPointOn()
overlay_mapper_2_x.BorderOn()
overlay_mapper_2_x.SetOrientation(0)

base_image_2_x = vtkImageSlice()
base_image_2_x.SetProperty(base_property_2)
base_image_2_x.SetMapper(base_mapper_2_x)

overlay_image_2_x = vtkImageSlice()
overlay_image_2_x.SetProperty(overlay_property_2)
overlay_image_2_x.SetMapper(overlay_mapper_2_x)

stack_2_x = vtkImageStack()
stack_2_x.AddImage(overlay_image_2_x)
stack_2_x.AddImage(base_image_2_x)
stack_2_x.SetActiveLayer(1)

outline_filter_2_x = vtkOutlineFilter()
outline_filter_2_x.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_x = vtkDataSetMapper()
outline_mapper_2_x.SetInputConnection(outline_filter_2_x.GetOutputPort())

outline_actor_2_x = vtkActor()
outline_actor_2_x.SetMapper(outline_mapper_2_x)

# Slice Y
base_mapper_2_y = vtkImageSliceMapper()
base_mapper_2_y.SetInputConnection(reader.GetOutputPort())
base_mapper_2_y.SliceAtFocalPointOn()
base_mapper_2_y.BorderOn()
base_mapper_2_y.SetOrientation(1)

overlay_mapper_2_y = vtkImageSliceMapper()
overlay_mapper_2_y.SetInputConnection(reader.GetOutputPort())
overlay_mapper_2_y.SliceAtFocalPointOn()
overlay_mapper_2_y.BorderOn()
overlay_mapper_2_y.SetOrientation(1)

base_image_2_y = vtkImageSlice()
base_image_2_y.SetProperty(base_property_2)
base_image_2_y.SetMapper(base_mapper_2_y)

overlay_image_2_y = vtkImageSlice()
overlay_image_2_y.SetProperty(overlay_property_2)
overlay_image_2_y.SetMapper(overlay_mapper_2_y)

stack_2_y = vtkImageStack()
stack_2_y.AddImage(overlay_image_2_y)
stack_2_y.AddImage(base_image_2_y)
stack_2_y.SetActiveLayer(1)

outline_filter_2_y = vtkOutlineFilter()
outline_filter_2_y.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_y = vtkDataSetMapper()
outline_mapper_2_y.SetInputConnection(outline_filter_2_y.GetOutputPort())

outline_actor_2_y = vtkActor()
outline_actor_2_y.SetMapper(outline_mapper_2_y)

# Slice Z
base_mapper_2_z = vtkImageSliceMapper()
base_mapper_2_z.SetInputConnection(reader.GetOutputPort())
base_mapper_2_z.SliceAtFocalPointOn()
base_mapper_2_z.BorderOn()
base_mapper_2_z.SetOrientation(2)

overlay_mapper_2_z = vtkImageSliceMapper()
overlay_mapper_2_z.SetInputConnection(reader.GetOutputPort())
overlay_mapper_2_z.SliceAtFocalPointOn()
overlay_mapper_2_z.BorderOn()
overlay_mapper_2_z.SetOrientation(2)

base_image_2_z = vtkImageSlice()
base_image_2_z.SetProperty(base_property_2)
base_image_2_z.SetMapper(base_mapper_2_z)

overlay_image_2_z = vtkImageSlice()
overlay_image_2_z.SetProperty(overlay_property_2)
overlay_image_2_z.SetMapper(overlay_mapper_2_z)

stack_2_z = vtkImageStack()
stack_2_z.AddImage(overlay_image_2_z)
stack_2_z.AddImage(base_image_2_z)
stack_2_z.SetActiveLayer(1)

outline_filter_2_z = vtkOutlineFilter()
outline_filter_2_z.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_z = vtkDataSetMapper()
outline_mapper_2_z.SetInputConnection(outline_filter_2_z.GetOutputPort())

outline_actor_2_z = vtkActor()
outline_actor_2_z.SetMapper(outline_mapper_2_z)

# --- Viewport 3: vtkImageResliceMapper, no checkerboard ---

base_property_3 = vtkImageProperty()
base_property_3.SetColorWindow(2000)
base_property_3.SetColorLevel(1000)
base_property_3.SetAmbient(0.0)
base_property_3.SetDiffuse(1.0)
base_property_3.SetInterpolationTypeToLinear()
base_property_3.SetLayerNumber(0)

overlay_property_3 = vtkImageProperty()
overlay_property_3.SetColorWindow(2000)
overlay_property_3.SetColorLevel(1000)
overlay_property_3.SetAmbient(0.0)
overlay_property_3.SetDiffuse(1.0)
overlay_property_3.SetLookupTable(lookup_table)
overlay_property_3.SetInterpolationTypeToLinear()
overlay_property_3.SetLayerNumber(1)
overlay_property_3.BackingOn()

# Slice X
base_reslice_mapper_3_x = vtkImageResliceMapper()
base_reslice_mapper_3_x.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_3_x.SliceAtFocalPointOn()
base_reslice_mapper_3_x.BorderOn()
base_reslice_mapper_3_x.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)

overlay_reslice_mapper_3_x = vtkImageResliceMapper()
overlay_reslice_mapper_3_x.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_3_x.SliceAtFocalPointOn()
overlay_reslice_mapper_3_x.BorderOn()
overlay_reslice_mapper_3_x.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)

base_image_3_x = vtkImageSlice()
base_image_3_x.SetProperty(base_property_3)
base_image_3_x.SetMapper(base_reslice_mapper_3_x)
base_image_3_x.RotateX(10)
base_image_3_x.RotateY(5)

overlay_image_3_x = vtkImageSlice()
overlay_image_3_x.SetProperty(overlay_property_3)
overlay_image_3_x.SetMapper(overlay_reslice_mapper_3_x)

stack_3_x = vtkImageStack()
stack_3_x.AddImage(overlay_image_3_x)
stack_3_x.AddImage(base_image_3_x)
stack_3_x.SetActiveLayer(1)

outline_filter_3_x = vtkOutlineFilter()
outline_filter_3_x.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_x = vtkDataSetMapper()
outline_mapper_3_x.SetInputConnection(outline_filter_3_x.GetOutputPort())

outline_actor_3_x = vtkActor()
outline_actor_3_x.SetMapper(outline_mapper_3_x)
outline_actor_3_x.RotateX(10)
outline_actor_3_x.RotateY(5)

# Slice Y
base_reslice_mapper_3_y = vtkImageResliceMapper()
base_reslice_mapper_3_y.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_3_y.SliceAtFocalPointOn()
base_reslice_mapper_3_y.BorderOn()
base_reslice_mapper_3_y.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)

overlay_reslice_mapper_3_y = vtkImageResliceMapper()
overlay_reslice_mapper_3_y.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_3_y.SliceAtFocalPointOn()
overlay_reslice_mapper_3_y.BorderOn()
overlay_reslice_mapper_3_y.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)

base_image_3_y = vtkImageSlice()
base_image_3_y.SetProperty(base_property_3)
base_image_3_y.SetMapper(base_reslice_mapper_3_y)
base_image_3_y.RotateX(10)
base_image_3_y.RotateY(5)

overlay_image_3_y = vtkImageSlice()
overlay_image_3_y.SetProperty(overlay_property_3)
overlay_image_3_y.SetMapper(overlay_reslice_mapper_3_y)

stack_3_y = vtkImageStack()
stack_3_y.AddImage(overlay_image_3_y)
stack_3_y.AddImage(base_image_3_y)
stack_3_y.SetActiveLayer(1)

outline_filter_3_y = vtkOutlineFilter()
outline_filter_3_y.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_y = vtkDataSetMapper()
outline_mapper_3_y.SetInputConnection(outline_filter_3_y.GetOutputPort())

outline_actor_3_y = vtkActor()
outline_actor_3_y.SetMapper(outline_mapper_3_y)
outline_actor_3_y.RotateX(10)
outline_actor_3_y.RotateY(5)

# Slice Z
base_reslice_mapper_3_z = vtkImageResliceMapper()
base_reslice_mapper_3_z.SetInputConnection(reader.GetOutputPort())
base_reslice_mapper_3_z.SliceAtFocalPointOn()
base_reslice_mapper_3_z.BorderOn()
base_reslice_mapper_3_z.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)

overlay_reslice_mapper_3_z = vtkImageResliceMapper()
overlay_reslice_mapper_3_z.SetInputConnection(reader.GetOutputPort())
overlay_reslice_mapper_3_z.SliceAtFocalPointOn()
overlay_reslice_mapper_3_z.BorderOn()
overlay_reslice_mapper_3_z.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)

base_image_3_z = vtkImageSlice()
base_image_3_z.SetProperty(base_property_3)
base_image_3_z.SetMapper(base_reslice_mapper_3_z)
base_image_3_z.RotateX(10)
base_image_3_z.RotateY(5)

overlay_image_3_z = vtkImageSlice()
overlay_image_3_z.SetProperty(overlay_property_3)
overlay_image_3_z.SetMapper(overlay_reslice_mapper_3_z)

stack_3_z = vtkImageStack()
stack_3_z.AddImage(overlay_image_3_z)
stack_3_z.AddImage(base_image_3_z)
stack_3_z.SetActiveLayer(1)

outline_filter_3_z = vtkOutlineFilter()
outline_filter_3_z.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_z = vtkDataSetMapper()
outline_mapper_3_z.SetInputConnection(outline_filter_3_z.GetOutputPort())

outline_actor_3_z = vtkActor()
outline_actor_3_z.SetMapper(outline_mapper_3_z)
outline_actor_3_z.RotateX(10)
outline_actor_3_z.RotateY(5)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_0.AddViewProp(stack_0_x)
renderer_0.AddViewProp(outline_actor_0_x)
renderer_0.AddViewProp(stack_0_y)
renderer_0.AddViewProp(outline_actor_0_y)
renderer_0.AddViewProp(stack_0_z)
renderer_0.AddViewProp(outline_actor_0_z)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_1.AddViewProp(stack_1_x)
renderer_1.AddViewProp(outline_actor_1_x)
renderer_1.AddViewProp(stack_1_y)
renderer_1.AddViewProp(outline_actor_1_y)
renderer_1.AddViewProp(stack_1_z)
renderer_1.AddViewProp(outline_actor_1_z)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.AddViewProp(stack_2_x)
renderer_2.AddViewProp(outline_actor_2_x)
renderer_2.AddViewProp(stack_2_y)
renderer_2.AddViewProp(outline_actor_2_y)
renderer_2.AddViewProp(stack_2_z)
renderer_2.AddViewProp(outline_actor_2_z)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddViewProp(stack_3_x)
renderer_3.AddViewProp(outline_actor_3_x)
renderer_3.AddViewProp(stack_3_y)
renderer_3.AddViewProp(outline_actor_3_y)
renderer_3.AddViewProp(stack_3_z)
renderer_3.AddViewProp(outline_actor_3_z)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("stack")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.Azimuth(10)
camera_0.Elevation(-120)
renderer_0.ResetCamera()
camera_0.Dolly(1.2)
camera_0.SetParallelScale(125)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.Azimuth(10)
camera_1.Elevation(-120)
renderer_1.ResetCamera()
camera_1.Dolly(1.2)
camera_1.SetParallelScale(125)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
camera_2.Azimuth(10)
camera_2.Elevation(-120)
renderer_2.ResetCamera()
camera_2.Dolly(1.2)
camera_2.SetParallelScale(125)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
camera_3.Azimuth(10)
camera_3.Elevation(-120)
renderer_3.ResetCamera()
camera_3.Dolly(1.2)
camera_3.SetParallelScale(125)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
