#!/usr/bin/env python

# Elevation banded contours with normal glyphs on a parametric RandomHills surface.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricRandomHills
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkVariant,
    vtkVariantArray,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkParametricFunctionSource,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
paraview_bkg = (0.322, 0.341, 0.431)
black = (0.000, 0.000, 0.000)
alice_blue = (0.941, 0.973, 1.000)

# Source: generate a parametric RandomHills surface
fn = vtkParametricRandomHills()
fn.AllowRandomGenerationOn()
fn.SetRandomSeed(1)
fn.SetNumberOfHills(30)

source = vtkParametricFunctionSource()
source.SetParametricFunction(fn)
source.SetUResolution(50)
source.SetVResolution(50)
source.SetScalarModeToZ()
source.Update()
source.GetOutput().GetPointData().GetScalars().SetName("Elevation")

# Transform: rotate so Y is up
transform = vtkTransform()
transform.Translate(0.0, 5.0, 15.0)
transform.RotateX(-90.0)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(source.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()

surface = transform_filter.GetOutput()
surface.GetPointData().SetActiveScalars("Elevation")
scalar_range = surface.GetPointData().GetScalars("Elevation").GetRange()

# Lookup table: categorical (Brewer Qualitative Set3)
color_series = vtkColorSeries()
color_series.SetColorScheme(color_series.BREWER_QUALITATIVE_SET3)

lut = vtkLookupTable()
color_series.BuildLookupTable(lut, color_series.CATEGORICAL)
lut.SetNanColor(0, 0, 0, 1)

# Lookup table: ordinal (for glyphs)
lut_ordinal = vtkLookupTable()
color_series.BuildLookupTable(lut_ordinal, color_series.ORDINAL)
lut_ordinal.SetNanColor(0, 0, 0, 1)

# Bands: custom integer-spaced elevation bands for RandomHills
my_bands = [
    [0, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 4.0],
    [4.0, 5.0], [5.0, 6.0], [6.0, 7.0], [7.0, 8.0],
]

bands = dict()
idx_min = 0
for idx in range(len(my_bands)):
    if my_bands[idx][1] > scalar_range[0] >= my_bands[idx][0]:
        idx_min = idx
        break
idx_max = len(my_bands) - 1
for idx in range(len(my_bands) - 1, -1, -1):
    if my_bands[idx][1] > scalar_range[1] >= my_bands[idx][0]:
        idx_max = idx
        break
my_bands[idx_min][0] = scalar_range[0]
my_bands[idx_max][1] = scalar_range[1]
trimmed = my_bands[idx_min: idx_max + 1]
for idx, e in enumerate(trimmed):
    bands[idx] = [e[0], e[0] + (e[1] - e[0]) / 2, e[1]]

adj_scalar_range = (bands[0][0], bands[len(bands) - 1][2])
lut.SetTableRange(adj_scalar_range)
lut.SetNumberOfTableValues(len(bands))
lut_ordinal.SetTableRange(adj_scalar_range)
lut_ordinal.SetNumberOfTableValues(len(bands))

# Annotate the LUT with band midpoints
values = vtkVariantArray()
for k in bands:
    values.InsertNextValue(vtkVariant("{:4.2f}".format(bands[k][1])))
for i in range(values.GetNumberOfTuples()):
    lut.SetAnnotation(i, values.GetValue(i).ToString())

# Reversed LUT for the scalar bar (highest value at top)
lutr = vtkLookupTable()
lutr.DeepCopy(lut)
t_max = lut.GetNumberOfTableValues() - 1
for i in reversed(range(t_max + 1)):
    rgba = [0.0] * 3
    lut.GetColor(float(i), rgba)
    rgba.append(lut.GetOpacity(float(i)))
    lutr.SetTableValue(t_max - i, rgba)
for i in reversed(range(lut.GetNumberOfAnnotatedValues())):
    lutr.SetAnnotation(lut.GetNumberOfAnnotatedValues() - 1 - i, lut.GetAnnotation(i))

# Filter: create banded elevation contours
bcf = vtkBandedPolyDataContourFilter()
bcf.SetInputData(surface)
for k in bands:
    bcf.SetValue(k, bands[k][2])
bcf.SetScalarModeToIndex()
bcf.GenerateContourEdgesOn()

# Glyph: arrow glyphs showing surface normals colored by elevation
mask_pts = vtkMaskPoints()
mask_pts.SetOnRatio(5)
mask_pts.RandomModeOn()
mask_pts.SetInputData(surface)

arrow = vtkArrowSource()
arrow.SetTipResolution(16)
arrow.SetTipLength(0.3)
arrow.SetTipRadius(0.1)

glyph = vtkGlyph3D()
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetInputConnection(mask_pts.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleFactor(1.0)
glyph.SetColorModeToColorByVector()
glyph.SetScaleModeToScaleByVector()
glyph.OrientOn()
glyph.Update()

# Mapper: map the banded surface to graphics primitives
src_mapper = vtkPolyDataMapper()
src_mapper.SetInputConnection(bcf.GetOutputPort())
src_mapper.SetScalarRange(adj_scalar_range)
src_mapper.SetLookupTable(lut)
src_mapper.SetScalarModeToUseCellData()

# Actor: display the banded elevation surface
src_actor = vtkActor()
src_actor.SetMapper(src_mapper)

# Mapper: map the contour edges
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputData(bcf.GetContourEdgesOutput())
edge_mapper.SetResolveCoincidentTopologyToPolygonOffset()

# Actor: display the contour edge lines
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(black)

# Mapper: map the normal glyphs
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.SetScalarModeToUsePointFieldData()
glyph_mapper.SetColorModeToMapScalars()
glyph_mapper.ScalarVisibilityOn()
glyph_mapper.SelectColorArray("Elevation")
glyph_mapper.SetLookupTable(lut_ordinal)
glyph_mapper.SetScalarRange(adj_scalar_range)

# Actor: display the normal glyphs
glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Scalar bar: elevation legend
window_width = 800
window_height = 800

scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lutr)
scalar_bar.SetTitle("Elevation")
scalar_bar.GetTitleTextProperty().SetColor(alice_blue)
scalar_bar.GetLabelTextProperty().SetColor(alice_blue)
scalar_bar.GetAnnotationTextProperty().SetColor(alice_blue)
scalar_bar.UnconstrainedFontSizeOn()
scalar_bar.SetMaximumWidthInPixels(window_width // 8)
scalar_bar.SetMaximumHeightInPixels(window_height // 3)
scalar_bar.SetPosition(0.85, 0.05)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddViewProp(src_actor)
renderer.AddViewProp(edge_actor)
renderer.AddViewProp(glyph_actor)
renderer.AddViewProp(scalar_bar)
renderer.SetBackground(paraview_bkg)
cam = renderer.GetActiveCamera()
cam.SetPosition(10.9299, 59.1505, 24.9823)
cam.SetFocalPoint(2.21692, 7.97545, 7.75135)
cam.SetViewUp(-0.230136, 0.345504, -0.909761)
cam.SetDistance(54.6966)
cam.SetClippingRange(36.3006, 77.9852)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ElevationBandsWithGlyphs")
render_window.SetSize(window_width, window_height)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
