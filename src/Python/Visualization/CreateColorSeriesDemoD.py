#!/usr/bin/env python

# Create custom vtkColorSeries from VTK named colors (White) and display them on a plane.


# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import (
    vtkColorSeries,
    vtkNamedColors,
)
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)

# Color series definitions: scheme name and list of VTK named color strings
COLOR_SERIES = {
    "White": ("VTKWhiteColors", [
        "antique_white", "azure", "bisque", "blanched_almond", "cornsilk",
        "eggshell", "floral_white", "gainsboro", "ghost_white", "honeydew",
        "ivory", "lavender", "lavender_blush", "lemon_chiffon", "linen",
        "mint_cream", "misty_rose", "moccasin", "navajo_white", "old_lace",
        "papaya_whip", "peach_puff", "seashell", "snow", "thistle",
        "titanium_white", "wheat", "white", "white_smoke", "zinc_white",
    ]),
}

# Select the color series
series_name = "White"

nc = vtkNamedColors()
scheme_name, color_names = COLOR_SERIES[series_name]

# Build the vtkColorSeries from named colors
color_series = vtkColorSeries()
color_series.SetColorSchemeByName(scheme_name)
for name in color_names:
    color_series.AddColor(nc.GetColor3ub(name))

num_colors = color_series.GetNumberOfColors()
print(f"Number of colors: {num_colors}")

# Source: generate a 6x6 plane
x_res, y_res = 6, 6
plane = vtkPlaneSource()
plane.SetXResolution(x_res)
plane.SetYResolution(y_res)
table_size = x_res * y_res + 1

# Cell data: assign increasing scalar values
cell_data = vtkFloatArray()
for i in range(x_res * y_res):
    cell_data.InsertNextValue(i)
plane.Update()
plane.GetOutput().GetCellData().SetScalars(cell_data)

# Lookup table: populate from the color series
lut = vtkLookupTable()
lut.SetNumberOfTableValues(table_size)
lut.SetTableRange(0, table_size)
for i in range(table_size):
    color = color_series.GetColorRepeating(i)
    lut.SetTableValue(i, color.GetRed() / 255.0, color.GetGreen() / 255.0,
                      color.GetBlue() / 255.0, 1.0)

# Mapper: map cell scalars through the lookup table
mapper = vtkPolyDataMapper()
mapper.SetLookupTable(lut)
mapper.SetInputConnection(plane.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SetScalarRange(0, table_size)

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CreateColorSeriesDemoD")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
