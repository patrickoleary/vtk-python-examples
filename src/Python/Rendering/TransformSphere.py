#!/usr/bin/env python

# Scale a sphere non-uniformly with vtkTransformFilter and colour it by
# elevation through a blue-to-red lookup table.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background = (0.439, 0.502, 0.565)

# Source: generate a sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(12)
sphere.SetPhiResolution(12)

# Transform: scale non-uniformly (1x, 1.5x, 2x)
transform = vtkTransform()
transform.Scale(1, 1.5, 2)

# Filter: apply the transform to the sphere geometry
transform_filter = vtkTransformFilter()
transform_filter.SetInputConnection(sphere.GetOutputPort())
transform_filter.SetTransform(transform)

# Filter: assign scalar values based on elevation (z-axis)
elevation = vtkElevationFilter()
elevation.SetInputConnection(transform_filter.GetOutputPort())
elevation.SetLowPoint(0, 0, -1)
elevation.SetHighPoint(0, 0, 1)

# Lookup table: blue-to-red colour ramp
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.SetSaturationRange(1, 1)
lut.SetValueRange(1, 1)

# Mapper: map the elevation scalars through the lookup table
mapper = vtkDataSetMapper()
mapper.SetLookupTable(lut)
mapper.SetInputConnection(elevation.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TransformSphere")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
