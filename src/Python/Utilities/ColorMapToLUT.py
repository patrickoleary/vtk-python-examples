#!/usr/bin/env python

# Apply a custom color transfer function to elevation-mapped geometry.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: a cone oriented vertically
cone = vtkConeSource()
cone.SetResolution(6)
cone.SetDirection(0, 1, 0)
cone.SetHeight(1)
cone.Update()
bounds = cone.GetOutput().GetBounds()

# ElevationFilter: map vertical height to a scalar range [0, 1]
elevation = vtkElevationFilter()
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)
elevation.SetInputConnection(cone.GetOutputPort())

# ColorTransferFunction: the "Fast" colormap by Francesca Samsel and
# Alan W. Scott, interpolated in Lab color space.
ctf = vtkDiscretizableColorTransferFunction()
ctf.SetColorSpaceToLab()
ctf.SetScaleToLinear()
ctf.SetNanColor(0.0, 1.0, 0.0)
ctf.AddRGBPoint(0.0, 0.0564, 0.0564, 0.47)
ctf.AddRGBPoint(0.1716, 0.243, 0.4604, 0.81)
ctf.AddRGBPoint(0.2985, 0.3568, 0.7450, 0.9544)
ctf.AddRGBPoint(0.4321, 0.6882, 0.93, 0.9179)
ctf.AddRGBPoint(0.5, 0.8995, 0.9446, 0.7687)
ctf.AddRGBPoint(0.5882, 0.9571, 0.8338, 0.5089)
ctf.AddRGBPoint(0.7061, 0.9275, 0.6214, 0.3154)
ctf.AddRGBPoint(0.8476, 0.8, 0.352, 0.16)
ctf.AddRGBPoint(1.0, 0.59, 0.0767, 0.1195)
ctf.SetNumberOfValues(9)
ctf.DiscretizeOff()

# Mapper: map elevation scalars through the color transfer function
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
render_window.SetWindowName("ColorMapToLUT")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
