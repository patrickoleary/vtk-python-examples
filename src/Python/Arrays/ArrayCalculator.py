#!/usr/bin/env python

# Use vtkArrayCalculator to derive a new scalar array from existing
# point coordinates and visualize the result on a warped plane.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkArrayCalculator, vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersSources import vtkPlaneSource
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

# Source: generate a high-resolution plane
source = vtkPlaneSource()
source.SetXResolution(60)
source.SetYResolution(60)
source.SetOrigin(-1.0, -1.0, 0.0)
source.SetPoint1(1.0, -1.0, 0.0)
source.SetPoint2(-1.0, 1.0, 0.0)

# Elevation filter: create an initial scalar from the Y coordinate
elevation = vtkElevationFilter()
elevation.SetInputConnection(source.GetOutputPort())
elevation.SetLowPoint(-1.0, -1.0, 0.0)
elevation.SetHighPoint(1.0, 1.0, 0.0)
elevation.SetScalarRange(0.0, 1.0)

# Array calculator: derive a new scalar using a mathematical expression
# The expression computes a radial sinusoidal pattern from coordinates
calculator = vtkArrayCalculator()
calculator.SetInputConnection(elevation.GetOutputPort())
calculator.AddCoordinateScalarVariable("x", 0)
calculator.AddCoordinateScalarVariable("y", 1)
calculator.SetFunction("sin(3.14159 * x) * cos(3.14159 * y)")
calculator.SetResultArrayName("SinCos")
calculator.SetResultArrayType(10)  # VTK_FLOAT

# Warp: displace the plane along its normal by the computed scalar
warp = vtkWarpScalar()
warp.SetInputConnection(calculator.GetOutputPort())
warp.SetInputArrayToProcess(0, 0, 0, 0, "SinCos")
warp.SetScaleFactor(0.25)

# Lookup table: map scalar values to a diverging color ramp
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.SetRange(-1.0, 1.0)
lut.Build()

# Mapper: map polygon data to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarRange(-1.0, 1.0)
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("SinCos")

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Scalar bar: display the color legend
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("sin(pi*x)*cos(pi*y)")
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
renderer.GetActiveCamera().Elevation(-30)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ArrayCalculator")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
