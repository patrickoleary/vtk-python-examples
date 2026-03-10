#!/usr/bin/env python

# Render a stippled (dashed) line by creating a 1-D texture from a
# 16-bit pattern and applying it to a vtkLineSource via texture coords.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
banana = (0.890, 0.812, 0.341)
background = (0.439, 0.502, 0.565)

# Stipple parameters
stipple_pattern = 0xA1A1
stipple_repeat = 2

# Source: generate a line from origin to (1,1,0)
line = vtkLineSource()
line.SetPoint1(0, 0, 0)
line.SetPoint2(1, 1, 0)
line.Update()

# Texture: build a 1-D RGBA image from the 16-bit stipple pattern
dimension = 16 * stipple_repeat
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(4)
canvas.SetExtent(0, dimension - 1, 0, 0, 0, 0)
canvas.SetDrawColor(0, 0, 0, 0)
canvas.FillBox(0, dimension - 1, 0, 0)
canvas.SetDrawColor(255, 255, 255, 255)
for i in range(16):
    if (stipple_pattern & (1 << i)) != 0:
        for j in range(stipple_repeat):
            canvas.DrawPoint(i * stipple_repeat + j, 0)
canvas.Update()

texture = vtkTexture()
texture.SetInputConnection(canvas.GetOutputPort())
texture.InterpolateOff()
texture.RepeatOn()

# Texture coordinates: assign along the line so the pattern tiles
poly_data = line.GetOutput()
tcoords = vtkDoubleArray()
tcoords.SetNumberOfComponents(2)
tcoords.SetNumberOfTuples(poly_data.GetNumberOfPoints())
for i in range(poly_data.GetNumberOfPoints()):
    value = float(i) * 0.5 / (poly_data.GetNumberOfPoints() - 1)
    tcoords.SetComponent(i, 0, value)
    tcoords.SetComponent(i, 1, 0.0)
poly_data.GetPointData().SetTCoords(tcoords)

# Mapper: map line polygon data
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(line.GetOutputPort())

# Actor: stippled line with texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(5)
actor.GetProperty().SetColor(banana)
actor.SetTexture(texture)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("StippledLine")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
