#!/usr/bin/env python

# Map a procedural checkerboard texture onto a warped plane using
# vtkTextureMapToPlane to generate planar texture coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToPlane
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
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
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a high-resolution plane and warp it with a scalar field
plane = vtkPlaneSource()
plane.SetResolution(50, 50)
plane.SetOrigin(-1.0, -1.0, 0.0)
plane.SetPoint1(1.0, -1.0, 0.0)
plane.SetPoint2(-1.0, 1.0, 0.0)
plane.Update()

# Add a scalar field for warping: distance from center
import math
from vtkmodules.vtkCommonCore import vtkFloatArray
scalars = vtkFloatArray()
scalars.SetName("Elevation")
output = plane.GetOutput()
for i in range(output.GetNumberOfPoints()):
    x, y, _ = output.GetPoint(i)
    r = math.sqrt(x * x + y * y)
    scalars.InsertNextValue(0.3 * math.cos(3.0 * r))
output.GetPointData().SetScalars(scalars)

# Warp: displace points along the normal by the scalar field
warp = vtkWarpScalar()
warp.SetInputData(output)
warp.SetScaleFactor(1.0)

# Texture image: procedural checkerboard pattern
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetExtent(0, 127, 0, 127, 0, 0)
canvas.SetDrawColor(255, 255, 255)
canvas.FillBox(0, 127, 0, 127)
canvas.SetDrawColor(70, 130, 180)
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            canvas.FillBox(col * 16, col * 16 + 15, row * 16, row * 16 + 15)
canvas.Update()

texture = vtkTexture()
texture.SetInputConnection(canvas.GetOutputPort())
texture.InterpolateOn()

# TextureMapToPlane: generate planar (s, t) texture coordinates
texture_map = vtkTextureMapToPlane()
texture_map.SetInputConnection(warp.GetOutputPort())

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(texture_map.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry with the texture
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-30)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextureMapToPlane")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
