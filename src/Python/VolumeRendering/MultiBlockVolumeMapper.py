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

for i in range(8):
    img = vtkImageData()
    img.SetDimensions(*dim)
    img.SetSpacing(*spc)
    img.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
    ofs = (i % 2, (i // 2) % 2, i // 4)
    img.SetOrigin(
        ofs[0] * (dim[0] - 1) * spc[0],
        ofs[1] * (dim[1] - 1) * spc[1],
        ofs[2] * (dim[2] - 1) * spc[2],
    )
    col = color_series.GetColor(i)
    for x in range(dim[0]):
        for y in range(dim[1]):
            for z in range(dim[2]):
                for c in range(3):
                    img.SetScalarComponentFromDouble(x, y, z, c, col[c])
                img.SetScalarComponentFromDouble(x, y, z, 3, 255)
    mb.SetBlock(i, img)

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
render_window.SetSize(640, 480)
render_window.SetWindowName("MultiBlockVolumeMapper")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Camera: adjust the view
render_window.Render()
camera = renderer.GetActiveCamera()
camera.Elevation(30)
camera.Azimuth(45)
renderer.ResetCamera()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
