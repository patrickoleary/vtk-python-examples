#!/usr/bin/env python
# Demonstrate vtkColorSeries by rendering swatches of all built-in color palettes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

palettes = vtkColorSeries()

# Find total number of color schemes and maximum palette size.
num_schemes = palettes.GetNumberOfColorSchemes()
max_palette_size = 0
for p in range(num_schemes):
    palettes.SetColorScheme(p)
    num_colors = palettes.GetNumberOfColors()
    if num_colors > max_palette_size:
        max_palette_size = num_colors

# Create image data for swatch display.
image_data = vtkImageData()
pixel_array = vtkUnsignedCharArray()
pixel_array.SetNumberOfComponents(3)
pixel_array.SetNumberOfTuples(num_schemes * 5 * max_palette_size * 5)
pixel_array.FillComponent(0, 255)
pixel_array.FillComponent(1, 255)
pixel_array.FillComponent(2, 255)
image_data.SetExtent(0, max_palette_size * 5 - 1, 0, num_schemes * 5 - 1, 0, 0)
image_data.GetPointData().SetScalars(pixel_array)

# Fill swatches for each palette.
for p in range(num_schemes):
    palettes.SetColorScheme(p)
    num_colors = palettes.GetNumberOfColors()
    yoff = (num_schemes - p - 1) * 5
    for c in range(num_colors):
        color = palettes.GetColorRepeating(c)
        for i in range(1, 4):
            for j in range(1, 4):
                coord = (((yoff + i) * max_palette_size + c) * 5 + j) * 3
                pixel_array.SetValue(coord, color.GetRed())
                pixel_array.SetValue(coord + 1, color.GetGreen())
                pixel_array.SetValue(coord + 2, color.GetBlue())

# Display using standard image rendering pipeline.
producer = vtkTrivialProducer()
producer.SetOutput(image_data)

image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(producer.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

render_window = vtkRenderWindow()
render_window.SetSize(400, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("color series")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
