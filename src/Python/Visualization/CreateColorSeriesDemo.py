#!/usr/bin/env python

# Create custom vtkColorSeries from VTK named colors and display them on a plane.


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

# Color series definitions: scheme name → list of VTK named color strings
COLOR_SERIES = {
    "Blue": ("VTKBlueColors", [
        "alice_blue", "blue", "blue_light", "blue_medium", "cadet", "cobalt",
        "cornflower", "cerulean", "dodger_blue", "indigo", "manganese_blue",
        "midnight_blue", "navy", "peacock", "powder_blue", "royal_blue",
        "slate_blue", "slate_blue_dark", "slate_blue_light", "slate_blue_medium",
        "sky_blue", "sky_blue_deep", "sky_blue_light", "steel_blue",
        "steel_blue_light", "turquoise_blue", "ultramarine",
    ]),
    "Brown": ("VTKBrownColors", [
        "beige", "brown", "brown_madder", "brown_ochre", "burlywood",
        "burnt_sienna", "burnt_umber", "chocolate", "deep_ochre", "flesh",
        "flesh_ochre", "gold_ochre", "greenish_umber", "khaki", "khaki_dark",
        "light_beige", "peru", "rosy_brown", "raw_sienna", "raw_umber",
        "sepia", "sienna", "saddle_brown", "sandy_brown", "tan", "van_dyke_brown",
    ]),
    "Red": ("VTKRedColors", [
        "alizarin_crimson", "brick", "cadmium_red_deep", "coral", "coral_light",
        "deep_pink", "english_red", "firebrick", "geranium_lake", "hot_pink",
        "indian_red", "light_salmon", "madder_lake_deep", "maroon", "pink",
        "pink_light", "raspberry", "red", "rose_madder", "salmon", "tomato",
        "venetian_red",
    ]),
    "Orange": ("VTKOrangeColors", [
        "cadmium_orange", "cadmium_red_light", "carrot", "dark_orange",
        "mars_orange", "mars_yellow", "orange", "orange_red", "yellow_ochre",
    ]),
    "White": ("VTKWhiteColors", [
        "antique_white", "azure", "bisque", "blanched_almond", "cornsilk",
        "eggshell", "floral_white", "gainsboro", "ghost_white", "honeydew",
        "ivory", "lavender", "lavender_blush", "lemon_chiffon", "linen",
        "mint_cream", "misty_rose", "moccasin", "navajo_white", "old_lace",
        "papaya_whip", "peach_puff", "seashell", "snow", "thistle",
        "titanium_white", "wheat", "white", "white_smoke", "zinc_white",
    ]),
    "Grey": ("VTKGreyColors", [
        "cold_grey", "dim_grey", "grey", "light_grey", "slate_grey",
        "slate_grey_dark", "slate_grey_light", "warm_grey",
    ]),
    "Magenta": ("VTKMagentaColors", [
        "blue_violet", "cobalt_violet_deep", "magenta", "orchid", "orchid_dark",
        "orchid_medium", "permanent_red_violet", "plum", "purple",
        "purple_medium", "ultramarine_violet", "violet", "violet_dark",
        "violet_red", "violet_red_medium", "violet_red_pale",
    ]),
    "Cyan": ("VTKCyanColors", [
        "aquamarine", "aquamarine_medium", "cyan", "cyan_white", "turquoise",
        "turquoise_dark", "turquoise_medium", "turquoise_pale",
    ]),
    "Yellow": ("VTKYellowColors", [
        "aureoline_yellow", "banana", "cadmium_lemon", "cadmium_yellow",
        "cadmium_yellow_light", "gold", "goldenrod", "goldenrod_dark",
        "goldenrod_light", "goldenrod_pale", "light_goldenrod", "melon",
        "naples_yellow_deep", "yellow", "yellow_light",
    ]),
    "Green": ("VTKGreenColors", [
        "chartreuse", "chrome_oxide_green", "cinnabar_green", "cobalt_green",
        "emerald_green", "forest_green", "green", "green_dark", "green_pale",
        "green_yellow", "lawn_green", "lime_green", "mint", "olive",
        "olive_drab", "olive_green_dark", "permanent_green", "sap_green",
        "sea_green", "sea_green_dark", "sea_green_medium", "sea_green_light",
        "spring_green", "spring_green_medium", "terre_verte", "viridian_light",
        "yellow_green",
    ]),
}

# Select the color series
series_name = "Red"

nc = vtkNamedColors()
scheme_name, color_names = COLOR_SERIES[series_name]

# Build the vtkColorSeries from named colors
color_series = vtkColorSeries()
color_series.SetColorSchemeByName(scheme_name)
for name in color_names:
    color_series.AddColor(nc.GetColor3ub(name))

num_colors = color_series.GetNumberOfColors()
print(f"Number of colors: {num_colors}")

# Source: generate a 6×6 plane
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
render_window.SetWindowName("CreateColorSeriesDemo")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
