#!/usr/bin/env python

# Demonstrate vtkNamedColors by contouring a cone with primary additive and subtractive colors.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black = (0.000, 0.000, 0.000)
misty_rose = (1.000, 0.894, 0.882)
royal_blue = (0.255, 0.412, 0.882)

nc = vtkNamedColors()

# Print all available color names and synonyms
color_names = nc.GetColorNames().split("\n")
print(f"There are {len(color_names)} colors:")
max_len = len(max(color_names, key=len))
line = ""
for i, name in enumerate(color_names, 1):
    line += f"{name.ljust(max_len)} " if i % 5 != 0 else f"{name}\n"
print(line.strip() + "\n")

syn_groups = nc.GetSynonyms().split("\n\n")
print(f"There are {len(syn_groups)} synonyms:")
for group in syn_groups:
    print("  ".join(group.split("\n")))

# Source: generate cone polygon data
cone_source = vtkConeSource()
cone_source.SetCenter(0.0, 0.0, 0.0)
cone_source.SetRadius(5.0)
cone_source.SetHeight(10)
cone_source.SetDirection(0, 1, 0)
cone_source.SetResolution(6)
cone_source.Update()

bounds = [0.0] * 6
cone_source.GetOutput().GetBounds(bounds)

# Filter: compute scalar elevation values
elevation = vtkElevationFilter()
elevation.SetInputConnection(cone_source.GetOutputPort())
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)

# Filter: generate banded contours from elevation scalars
bcf = vtkBandedPolyDataContourFilter()
bcf.SetInputConnection(elevation.GetOutputPort())
bcf.SetScalarModeToValue()
bcf.GenerateContourEdgesOn()
bcf.GenerateValues(7, elevation.GetScalarRange())

# Lookup table: primary additive and subtractive colors
lut = vtkLookupTable()
lut.SetNumberOfTableValues(7)
lut.SetTableValue(0, 1.0, 0.0, 0.0, 0.5)   # Red (semi-transparent)
lut.SetTableValue(1, 0.0, 1.0, 0.0, 0.3)   # Lime (semi-transparent)
lut.SetTableValue(2, 0.0, 0.0, 1.0, 1.0)   # Blue
lut.SetTableValue(3, 0.0, 1.0, 1.0, 1.0)   # Cyan
lut.SetTableValue(4, 1.0, 0.0, 1.0, 1.0)   # Magenta
lut.SetTableValue(5, 1.0, 1.0, 0.0, 1.0)   # Yellow
lut.SetTableValue(6, 1.0, 1.0, 1.0, 1.0)   # White
lut.SetTableRange(elevation.GetScalarRange())
lut.Build()

# Mapper: map banded contour data using the lookup table
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(bcf.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarModeToUseCellData()

# Mapper: map the contour edge lines
contour_line_mapper = vtkPolyDataMapper()
contour_line_mapper.SetInputData(bcf.GetContourEdgesOutput())
contour_line_mapper.SetScalarRange(elevation.GetScalarRange())
contour_line_mapper.SetResolveCoincidentTopologyToPolygonOffset()

# Actor: assign the banded contour surface
actor = vtkActor()
actor.SetMapper(mapper)

# Actor: assign the contour edge lines
contour_line_actor = vtkActor()
contour_line_actor.SetMapper(contour_line_mapper)
contour_line_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(contour_line_actor)
renderer.SetBackground(misty_rose)
renderer.SetBackground2(royal_blue)
renderer.GradientBackgroundOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("NamedColors")
render_window.SetSize(640, 640)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
