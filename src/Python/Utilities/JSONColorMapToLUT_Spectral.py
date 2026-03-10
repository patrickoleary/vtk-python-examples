#!/usr/bin/env python

# Build a color transfer function from an inline Spectral JSON colormap.

import json

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSuperEllipsoid
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# JSON colormap: the "Spectral" diverging colormap embedded inline.
# Based on the ColorBrewer Spectral scheme — red through yellow to blue.
# Commonly used for showing data that diverges around a central value.
# Format matches ParaView export.
COLORMAP_JSON = json.loads("""
[
  {
    "ColorSpace": "Lab",
    "Creator": "ColorBrewer",
    "Name": "Spectral",
    "NanColor": [0.5, 0.5, 0.5],
    "RGBPoints": [
      0.0,    0.61961, 0.00392, 0.25882,
      0.1,    0.83529, 0.24314, 0.30980,
      0.2,    0.95686, 0.42745, 0.26275,
      0.3,    0.99216, 0.68235, 0.38039,
      0.4,    0.99608, 0.87843, 0.54510,
      0.5,    1.00000, 1.00000, 0.74902,
      0.6,    0.90196, 0.96078, 0.59608,
      0.7,    0.67059, 0.86667, 0.64314,
      0.8,    0.40000, 0.76078, 0.64706,
      0.9,    0.19608, 0.53333, 0.74118,
      1.0,    0.36863, 0.30980, 0.63529
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

# Source: a super-ellipsoid for an interesting shape that shows
# the full spectral range across its surface
superellipsoid = vtkParametricSuperEllipsoid()
superellipsoid.SetN1(0.5)
superellipsoid.SetN2(0.5)

source = vtkParametricFunctionSource()
source.SetParametricFunction(superellipsoid)
source.SetUResolution(60)
source.SetVResolution(30)
source.Update()
bounds = source.GetOutput().GetBounds()

# ElevationFilter: map vertical height to scalar range [0, 1]
elevation = vtkElevationFilter()
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)
elevation.SetInputConnection(source.GetOutputPort())

# Mapper: map elevation scalars through the Spectral color transfer function
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
render_window.SetWindowName("JSONColorMapToLUT_Spectral")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
