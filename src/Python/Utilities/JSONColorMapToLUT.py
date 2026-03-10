#!/usr/bin/env python

# Build a color transfer function from an inline JSON colormap definition.

import json

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# JSON colormap: the "Inferno" colormap embedded inline.
# This is the same format exported by ParaView.
COLORMAP_JSON = json.loads("""
[
  {
    "ColorSpace": "Lab",
    "Creator": "Matplotlib",
    "Name": "Inferno (matplotlib)",
    "NanColor": [0.0, 1.0, 0.0],
    "RGBPoints": [
      0.0,    0.001462, 0.000466, 0.013866,
      0.125,  0.087411, 0.044556, 0.224813,
      0.25,   0.258234, 0.038571, 0.406485,
      0.375,  0.416331, 0.090834, 0.432943,
      0.5,    0.578040, 0.148039, 0.404411,
      0.625,  0.735683, 0.215906, 0.329917,
      0.75,   0.865006, 0.316822, 0.226055,
      0.875,  0.954506, 0.468744, 0.099874,
      1.0,    0.988362, 0.998364, 0.644924
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

# Source: a sphere with high resolution for smooth color mapping
sphere = vtkSphereSource()
sphere.SetThetaResolution(64)
sphere.SetPhiResolution(32)
sphere.Update()
bounds = sphere.GetOutput().GetBounds()

# ElevationFilter: map vertical height to scalar range [0, 1]
elevation = vtkElevationFilter()
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)
elevation.SetInputConnection(sphere.GetOutputPort())

# Mapper: map elevation scalars through the JSON-derived color transfer function
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
renderer.SetBackground(0.322, 0.341, 0.431)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("JSONColorMapToLUT")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
