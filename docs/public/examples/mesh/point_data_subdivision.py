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
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
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

ren_win_x = 1200
ren_win_y = ren_win_x // 3
min_dim = min(ren_win_x, ren_win_y)

# --- Viewport 0: original ---
surf_mapper_0 = vtkPolyDataMapper()
surf_mapper_0.SetInputConnection(boy_source.GetOutputPort())
surf_mapper_0.SetLookupTable(lut)
surf_mapper_0.SetScalarRange(scalar_range)
surf_mapper_0.SetColorModeToMapScalars()
surf_mapper_0.ScalarVisibilityOn()

surf_actor_0 = vtkActor()
surf_actor_0.SetMapper(surf_mapper_0)
surf_actor_0.GetProperty().SetInterpolationToGouraud()

arrow_0 = vtkArrowSource()

mask_0 = vtkMaskPoints()
mask_0.SetInputConnection(boy_source.GetOutputPort())
mask_0.SetOnRatio(boy_source.GetOutput().GetNumberOfPoints() // glyph_points)
mask_0.SetRandomMode(1)

glyph_0 = vtkGlyph3D()
glyph_0.SetScaleFactor(scale_factor)
glyph_0.SetVectorModeToUseNormal()
glyph_0.SetColorModeToColorByScalar()
glyph_0.SetScaleModeToScaleByVector()
glyph_0.OrientOn()
glyph_0.SetSourceConnection(arrow_0.GetOutputPort())
glyph_0.SetInputConnection(mask_0.GetOutputPort())
glyph_0.Update()

glyph_mapper_0 = vtkDataSetMapper()
glyph_mapper_0.SetScalarRange(scalar_range)
glyph_mapper_0.SetColorModeToMapScalars()
glyph_mapper_0.ScalarVisibilityOn()
glyph_mapper_0.SetLookupTable(lut)
glyph_mapper_0.SetInputConnection(glyph_0.GetOutputPort())

glyph_actor_0 = vtkActor()
glyph_actor_0.SetMapper(glyph_mapper_0)

text_prop_0 = vtkTextProperty()
text_prop_0.SetJustificationToCentered()
text_prop_0.SetFontSize(int(min_dim / 20))

label_actor_0 = vtkTextActor()
label_actor_0.SetInput("Original")
label_actor_0.SetPosition(min_dim / 2.0, 16)
label_actor_0.GetTextProperty().ShallowCopy(text_prop_0)
label_actor_0.GetTextProperty().SetColor(gold)

ren_0 = vtkRenderer()
ren_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0)
ren_0.AddActor(surf_actor_0)
ren_0.AddActor(glyph_actor_0)
ren_0.AddActor(label_actor_0)
ren_0.SetBackground(slate_gray)
ren_0.ResetCamera()

# --- Viewport 1: linear subdivision ---
surf_mapper_1 = vtkPolyDataMapper()
surf_mapper_1.SetInputConnection(linear.GetOutputPort())
surf_mapper_1.SetLookupTable(lut)
surf_mapper_1.SetScalarRange(scalar_range)
surf_mapper_1.SetColorModeToMapScalars()
surf_mapper_1.ScalarVisibilityOn()

surf_actor_1 = vtkActor()
surf_actor_1.SetMapper(surf_mapper_1)
surf_actor_1.GetProperty().SetInterpolationToGouraud()

arrow_1 = vtkArrowSource()

mask_1 = vtkMaskPoints()
mask_1.SetInputConnection(linear.GetOutputPort())
mask_1.SetOnRatio(linear.GetOutput().GetNumberOfPoints() // glyph_points)
mask_1.SetRandomMode(1)

glyph_1 = vtkGlyph3D()
glyph_1.SetScaleFactor(scale_factor)
glyph_1.SetVectorModeToUseNormal()
glyph_1.SetColorModeToColorByScalar()
glyph_1.SetScaleModeToScaleByVector()
glyph_1.OrientOn()
glyph_1.SetSourceConnection(arrow_1.GetOutputPort())
glyph_1.SetInputConnection(mask_1.GetOutputPort())
glyph_1.Update()

glyph_mapper_1 = vtkDataSetMapper()
glyph_mapper_1.SetScalarRange(scalar_range)
glyph_mapper_1.SetColorModeToMapScalars()
glyph_mapper_1.ScalarVisibilityOn()
glyph_mapper_1.SetLookupTable(lut)
glyph_mapper_1.SetInputConnection(glyph_1.GetOutputPort())

glyph_actor_1 = vtkActor()
glyph_actor_1.SetMapper(glyph_mapper_1)

text_prop_1 = vtkTextProperty()
text_prop_1.SetJustificationToCentered()
text_prop_1.SetFontSize(int(min_dim / 20))

label_actor_1 = vtkTextActor()
label_actor_1.SetInput("Linear Subdivision")
label_actor_1.SetPosition(min_dim / 2.0, 16)
label_actor_1.GetTextProperty().ShallowCopy(text_prop_1)
label_actor_1.GetTextProperty().SetColor(gold)

ren_1 = vtkRenderer()
ren_1.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0)
ren_1.AddActor(surf_actor_1)
ren_1.AddActor(glyph_actor_1)
ren_1.AddActor(label_actor_1)
ren_1.SetBackground(slate_gray)
ren_1.ResetCamera()

# --- Viewport 2: butterfly subdivision ---
surf_mapper_2 = vtkPolyDataMapper()
surf_mapper_2.SetInputConnection(butterfly.GetOutputPort())
surf_mapper_2.SetLookupTable(lut)
surf_mapper_2.SetScalarRange(scalar_range)
surf_mapper_2.SetColorModeToMapScalars()
surf_mapper_2.ScalarVisibilityOn()

surf_actor_2 = vtkActor()
surf_actor_2.SetMapper(surf_mapper_2)
surf_actor_2.GetProperty().SetInterpolationToGouraud()

arrow_2 = vtkArrowSource()

mask_2 = vtkMaskPoints()
mask_2.SetInputConnection(butterfly.GetOutputPort())
mask_2.SetOnRatio(butterfly.GetOutput().GetNumberOfPoints() // glyph_points)
mask_2.SetRandomMode(1)

glyph_2 = vtkGlyph3D()
glyph_2.SetScaleFactor(scale_factor)
glyph_2.SetVectorModeToUseNormal()
glyph_2.SetColorModeToColorByScalar()
glyph_2.SetScaleModeToScaleByVector()
glyph_2.OrientOn()
glyph_2.SetSourceConnection(arrow_2.GetOutputPort())
glyph_2.SetInputConnection(mask_2.GetOutputPort())
glyph_2.Update()

glyph_mapper_2 = vtkDataSetMapper()
glyph_mapper_2.SetScalarRange(scalar_range)
glyph_mapper_2.SetColorModeToMapScalars()
glyph_mapper_2.ScalarVisibilityOn()
glyph_mapper_2.SetLookupTable(lut)
glyph_mapper_2.SetInputConnection(glyph_2.GetOutputPort())

glyph_actor_2 = vtkActor()
glyph_actor_2.SetMapper(glyph_mapper_2)

text_prop_2 = vtkTextProperty()
text_prop_2.SetJustificationToCentered()
text_prop_2.SetFontSize(int(min_dim / 20))

label_actor_2 = vtkTextActor()
label_actor_2.SetInput("Butterfly Subdivision")
label_actor_2.SetPosition(min_dim / 2.0, 16)
label_actor_2.GetTextProperty().ShallowCopy(text_prop_2)
label_actor_2.GetTextProperty().SetColor(gold)

ren_2 = vtkRenderer()
ren_2.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0)
ren_2.AddActor(surf_actor_2)
ren_2.AddActor(glyph_actor_2)
ren_2.AddActor(label_actor_2)
ren_2.SetBackground(slate_gray)
ren_2.ResetCamera()

# Window: display the three-panel comparison
render_window = vtkRenderWindow()
render_window.AddRenderer(ren_0)
render_window.AddRenderer(ren_1)
render_window.AddRenderer(ren_2)
render_window.SetWindowName("point data subdivision")
render_window.SetMultiSamples(0)
render_window.SetSize(ren_win_x, ren_win_y)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
