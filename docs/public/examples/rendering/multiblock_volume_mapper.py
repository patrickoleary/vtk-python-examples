#!/usr/bin/env python

# Volume rendering of a procedural multi-block dataset with colored blocks.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkCommonDataModel import vtkImageData, vtkMultiBlockDataSet
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkMultiBlockVolumeMapper

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)
forest_green_rgb = (0.133, 0.545, 0.133)

# Source: build a procedural multi-block dataset of 8 colored blocks
dim = (10, 10, 10)
spc = (0.1, 0.1, 0.1)
mb = vtkMultiBlockDataSet()
color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_SET3)

# Block 0: color (141, 211, 199)
img_0 = vtkImageData()
img_0.SetDimensions(*dim)
img_0.SetSpacing(*spc)
img_0.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_0.SetOrigin(0.0, 0.0, 0.0)
col_0 = color_series.GetColor(0)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_0.SetScalarComponentFromDouble(x, y, z, c, col_0[c])
            img_0.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(0, img_0)

# Block 1: color (255, 255, 179)
img_1 = vtkImageData()
img_1.SetDimensions(*dim)
img_1.SetSpacing(*spc)
img_1.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_1.SetOrigin(0.9, 0.0, 0.0)
col_1 = color_series.GetColor(1)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_1.SetScalarComponentFromDouble(x, y, z, c, col_1[c])
            img_1.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(1, img_1)

# Block 2: color (190, 186, 218)
img_2 = vtkImageData()
img_2.SetDimensions(*dim)
img_2.SetSpacing(*spc)
img_2.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_2.SetOrigin(0.0, 0.9, 0.0)
col_2 = color_series.GetColor(2)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_2.SetScalarComponentFromDouble(x, y, z, c, col_2[c])
            img_2.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(2, img_2)

# Block 3: color (251, 128, 114)
img_3 = vtkImageData()
img_3.SetDimensions(*dim)
img_3.SetSpacing(*spc)
img_3.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_3.SetOrigin(0.9, 0.9, 0.0)
col_3 = color_series.GetColor(3)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_3.SetScalarComponentFromDouble(x, y, z, c, col_3[c])
            img_3.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(3, img_3)

# Block 4: color (128, 177, 211)
img_4 = vtkImageData()
img_4.SetDimensions(*dim)
img_4.SetSpacing(*spc)
img_4.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_4.SetOrigin(0.0, 0.0, 0.9)
col_4 = color_series.GetColor(4)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_4.SetScalarComponentFromDouble(x, y, z, c, col_4[c])
            img_4.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(4, img_4)

# Block 5: color (253, 180, 98)
img_5 = vtkImageData()
img_5.SetDimensions(*dim)
img_5.SetSpacing(*spc)
img_5.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_5.SetOrigin(0.9, 0.0, 0.9)
col_5 = color_series.GetColor(5)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_5.SetScalarComponentFromDouble(x, y, z, c, col_5[c])
            img_5.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(5, img_5)

# Block 6: color (179, 222, 105)
img_6 = vtkImageData()
img_6.SetDimensions(*dim)
img_6.SetSpacing(*spc)
img_6.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_6.SetOrigin(0.0, 0.9, 0.9)
col_6 = color_series.GetColor(6)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_6.SetScalarComponentFromDouble(x, y, z, c, col_6[c])
            img_6.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(6, img_6)

# Block 7: color (252, 205, 229)
img_7 = vtkImageData()
img_7.SetDimensions(*dim)
img_7.SetSpacing(*spc)
img_7.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
img_7.SetOrigin(0.9, 0.9, 0.9)
col_7 = color_series.GetColor(7)
for x in range(dim[0]):
    for y in range(dim[1]):
        for z in range(dim[2]):
            for c in range(3):
                img_7.SetScalarComponentFromDouble(x, y, z, c, col_7[c])
            img_7.SetScalarComponentFromDouble(x, y, z, 3, 255)
mb.SetBlock(7, img_7)

# VolumeMapper: multi-block volume mapper
volume_mapper = vtkMultiBlockVolumeMapper()
volume_mapper.SetInputDataObject(mb)

# VolumeProperty: RGBA data (not independent components)
volume_property = vtkVolumeProperty()
volume_property.SetIndependentComponents(False)

# Volume: holds the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Outline: bounding box around the multi-block dataset
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(mb)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(outline_actor)
renderer.SetBackground(forest_green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multiblock volume mapper")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: camera configuration
render_window.Render()
camera = renderer.GetActiveCamera()
camera.Elevation(30)
camera.Azimuth(45)
renderer.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
