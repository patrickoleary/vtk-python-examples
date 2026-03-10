#!/usr/bin/env python

# Point data subdivision comparison: original, linear, and butterfly on a Boy surface.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricBoy
from vtkmodules.vtkCommonDataModel import vtkColor3ub
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersModeling import (
    vtkButterflySubdivisionFilter,
    vtkLinearSubdivisionFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkParametricFunctionSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
    vtkTextProperty,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
gold = (1.000, 0.843, 0.000)

# Source: generate a Boy surface with Z-based scalars
boy = vtkParametricBoy()
boy.JoinUOff()

boy_source = vtkParametricFunctionSource()
boy_source.SetParametricFunction(boy)
boy_source.SetScalarModeToZ()
boy_source.Update()
boy_source.GetOutput().GetPointData().GetScalars().SetName("Elevation")

scalar_range = boy_source.GetOutput().GetScalarRange()
bounds = boy_source.GetOutput().GetBounds()
scale_factor = min(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]) * 0.2
glyph_points = 50

# Lookup table: Brewer Qualitative Set3 color transfer function
color_series = vtkColorSeries()
color_series.SetColorScheme(61)
lut = vtkColorTransferFunction()
lut.SetColorSpaceToHSV()
num_colors = color_series.GetNumberOfColors()
for i in range(num_colors):
    c3 = vtkColor3ub(color_series.GetColor(i))
    r, g, b = c3[0] / 255.0, c3[1] / 255.0, c3[2] / 255.0
    t = scalar_range[0] + (scalar_range[1] - scalar_range[0]) / (num_colors - 1) * i
    lut.AddRGBPoint(t, r, g, b)

# Filter: butterfly subdivision (3 levels)
butterfly = vtkButterflySubdivisionFilter()
butterfly.SetInputConnection(boy_source.GetOutputPort())
butterfly.SetNumberOfSubdivisions(3)
butterfly.Update()

# Filter: linear subdivision (3 levels)
linear = vtkLinearSubdivisionFilter()
linear.SetInputConnection(boy_source.GetOutputPort())
linear.SetNumberOfSubdivisions(3)
linear.Update()

# Sources and labels for three viewports: original (left), linear (center), butterfly (right)
sources = [boy_source, linear, butterfly]
labels = ["Original", "Linear Subdivision", "Butterfly Subdivision"]
viewports = [(0.0, 0.0, 1.0 / 3.0, 1.0),
             (1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0),
             (2.0 / 3.0, 0.0, 1.0, 1.0)]

ren_win_x = 1200
ren_win_y = ren_win_x // 3
min_dim = min(ren_win_x, ren_win_y)

renderers = []
for i in range(3):
    src = sources[i]

    # ---- Mapper: map the subdivided surface ----
    surf_mapper = vtkPolyDataMapper()
    surf_mapper.SetInputConnection(src.GetOutputPort())
    surf_mapper.SetLookupTable(lut)
    surf_mapper.SetScalarRange(scalar_range)
    surf_mapper.SetColorModeToMapScalars()
    surf_mapper.ScalarVisibilityOn()

    # ---- Actor: display the surface with Gouraud interpolation ----
    surf_actor = vtkActor()
    surf_actor.SetMapper(surf_mapper)
    surf_actor.GetProperty().SetInterpolationToGouraud()

    # ---- Glyph: arrow glyphs showing surface normals ----
    arrow = vtkArrowSource()

    mask = vtkMaskPoints()
    mask.SetInputConnection(src.GetOutputPort())
    mask.SetOnRatio(src.GetOutput().GetNumberOfPoints() // glyph_points)
    mask.SetRandomMode(1)

    glyph = vtkGlyph3D()
    glyph.SetScaleFactor(scale_factor)
    glyph.SetVectorModeToUseNormal()
    glyph.SetColorModeToColorByScalar()
    glyph.SetScaleModeToScaleByVector()
    glyph.OrientOn()
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.SetInputConnection(mask.GetOutputPort())
    glyph.Update()

    glyph_mapper = vtkDataSetMapper()
    glyph_mapper.SetScalarRange(scalar_range)
    glyph_mapper.SetColorModeToMapScalars()
    glyph_mapper.ScalarVisibilityOn()
    glyph_mapper.SetLookupTable(lut)
    glyph_mapper.SetInputConnection(glyph.GetOutputPort())

    glyph_actor = vtkActor()
    glyph_actor.SetMapper(glyph_mapper)

    # ---- Label: text overlay identifying the subdivision method ----
    text_prop = vtkTextProperty()
    text_prop.SetJustificationToCentered()
    text_prop.SetFontSize(int(min_dim / 20))

    text_mapper = vtkTextMapper()
    text_mapper.SetInput(labels[i])
    text_mapper.SetTextProperty(text_prop)

    label_actor = vtkActor2D()
    label_actor.SetMapper(text_mapper)
    label_actor.SetPosition(min_dim / 2.0, 16)
    label_actor.GetProperty().SetColor(gold)

    # ---- Renderer: one viewport per subdivision method ----
    ren = vtkRenderer()
    ren.SetViewport(viewports[i])
    ren.AddActor(surf_actor)
    ren.AddActor(glyph_actor)
    ren.AddActor(label_actor)
    ren.SetBackground(slate_gray)
    ren.ResetCamera()
    renderers.append(ren)

# Window: display the three-panel comparison
render_window = vtkRenderWindow()
for ren in renderers:
    render_window.AddRenderer(ren)
render_window.SetWindowName("PointDataSubdivision")
render_window.SetSize(ren_win_x, ren_win_y)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
