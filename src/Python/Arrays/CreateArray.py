#!/usr/bin/env python

# Create a custom scalar array, attach it to a sphere's point data,
# and visualize the result with a color lookup table and scalar bar.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import math

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a sphere
source = vtkSphereSource()
source.SetThetaResolution(40)
source.SetPhiResolution(40)
source.Update()
polydata = source.GetOutput()

# Array: create a custom scalar array based on distance from the XY plane
num_points = polydata.GetNumberOfPoints()
scalars = vtkFloatArray()
scalars.SetName("DistanceFromXY")
scalars.SetNumberOfTuples(num_points)
for i in range(num_points):
    x, y, z = polydata.GetPoint(i)
    scalars.SetValue(i, math.sqrt(x * x + y * y))

# Attach the array to the polydata's point data and set it as active scalars
polydata.GetPointData().AddArray(scalars)
polydata.GetPointData().SetActiveScalars("DistanceFromXY")

# Lookup table: map scalar values to a cool-to-warm color ramp
scalar_range = scalars.GetRange()
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.SetRange(scalar_range)
lut.Build()

# Mapper: map polygon data to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetLookupTable(lut)
mapper.SetScalarRange(scalar_range)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Scalar bar: display the color legend
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Distance")
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetOrientationToVertical()
scalar_bar.SetWidth(0.08)
scalar_bar.SetHeight(0.6)
scalar_bar.SetPosition(0.9, 0.2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(scalar_bar)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CreateArray")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
