#!/usr/bin/env python

# Build a color transfer function from an inline Viridis JSON colormap.

import json

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# JSON colormap: the "Viridis" colormap embedded inline.
# This perceptually uniform sequential colormap is widely used
# for scientific visualization. Format matches ParaView export.
COLORMAP_JSON = json.loads("""
[
  {
    "ColorSpace": "Lab",
    "Creator": "Matplotlib",
    "Name": "Viridis (matplotlib)",
    "NanColor": [1.0, 0.0, 0.0],
    "RGBPoints": [
      0.0,    0.267004, 0.004874, 0.329415,
      0.1,    0.282327, 0.140926, 0.457517,
      0.2,    0.229739, 0.322361, 0.545706,
      0.3,    0.172719, 0.498103, 0.557937,
      0.4,    0.127568, 0.566949, 0.550556,
      0.5,    0.190631, 0.632739, 0.510488,
      0.6,    0.342890, 0.693840, 0.432390,
      0.7,    0.536553, 0.741509, 0.314060,
      0.8,    0.741388, 0.772852, 0.165530,
      0.9,    0.925937, 0.808720, 0.097855,
      1.0,    0.993248, 0.906157, 0.143936
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

# Source: a cylinder oriented vertically for clear elevation mapping
cylinder = vtkCylinderSource()
cylinder.SetResolution(32)
cylinder.SetHeight(2.0)
cylinder.Update()
bounds = cylinder.GetOutput().GetBounds()

# ElevationFilter: map vertical height to scalar range [0, 1]
elevation = vtkElevationFilter()
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)
elevation.SetInputConnection(cylinder.GetOutputPort())

# Mapper: map elevation scalars through the Viridis color transfer function
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
render_window.SetWindowName("JSONColorMapToLUT_Viridis")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
