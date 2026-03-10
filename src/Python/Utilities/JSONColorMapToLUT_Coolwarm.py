#!/usr/bin/env python

# Build a color transfer function from an inline Coolwarm JSON colormap.

import json

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricTorus
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# JSON colormap: the "Cool to Warm" diverging colormap embedded inline.
# Designed by Kenneth Moreland for scientific visualization. Blue at
# the low end diverges through white to red at the high end.
# Format matches ParaView export.
COLORMAP_JSON = json.loads("""
[
  {
    "ColorSpace": "Diverging",
    "Creator": "Kenneth Moreland",
    "Name": "Cool to Warm",
    "NanColor": [1.0, 1.0, 0.0],
    "RGBPoints": [
      0.0,   0.23137, 0.29804, 0.75294,
      0.125, 0.32549, 0.47843, 0.88627,
      0.25,  0.48235, 0.65882, 0.96078,
      0.375, 0.67451, 0.81176, 0.97647,
      0.5,   0.86275, 0.86275, 0.86275,
      0.625, 0.95686, 0.76471, 0.63137,
      0.75,  0.93333, 0.55294, 0.38039,
      0.875, 0.82745, 0.30196, 0.20392,
      1.0,   0.70588, 0.01569, 0.14902
    ]
  }
]
""")

# Parse the JSON colormap into a vtkDiscretizableColorTransferFunction
cm = COLORMAP_JSON[0]

ctf = vtkDiscretizableColorTransferFunction()

interp_space = cm.get("ColorSpace", "RGB").lower()
if interp_space == "lab":
    ctf.SetColorSpaceToLab()
elif interp_space == "hsv":
    ctf.SetColorSpaceToHSV()
elif interp_space == "diverging":
    ctf.SetColorSpaceToDiverging()
else:
    ctf.SetColorSpaceToRGB()

ctf.SetScaleToLinear()

if "NanColor" in cm:
    ctf.SetNanColor(*cm["NanColor"])

points = cm["RGBPoints"]
n_points = len(points) // 4
for i in range(n_points):
    x = points[i * 4]
    r = points[i * 4 + 1]
    g = points[i * 4 + 2]
    b = points[i * 4 + 3]
    ctf.AddRGBPoint(x, r, g, b)

ctf.SetNumberOfValues(n_points)
ctf.DiscretizeOff()

# Source: a torus to show the diverging colormap wrapping around geometry
torus_func = vtkParametricTorus()
torus_func.SetRingRadius(1.0)
torus_func.SetCrossSectionRadius(0.4)

torus = vtkParametricFunctionSource()
torus.SetParametricFunction(torus_func)
torus.SetUResolution(60)
torus.SetVResolution(30)
torus.Update()
bounds = torus.GetOutput().GetBounds()

# ElevationFilter: map vertical height to scalar range [0, 1]
elevation = vtkElevationFilter()
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)
elevation.SetInputConnection(torus.GetOutputPort())

# Mapper: map elevation scalars through the Coolwarm color transfer function
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation.GetOutputPort())
mapper.SetLookupTable(ctf)
mapper.SetColorModeToMapScalars()
mapper.InterpolateScalarsBeforeMappingOn()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.15)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("JSONColorMapToLUT_Coolwarm")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
