#!/usr/bin/env python

# Gaussian curvature banded contours with normal glyphs on a parametric RandomHills surface.

import numpy as np
from vtk.util import numpy_support
from vtkmodules.numpy_interface import dataset_adapter as dsa

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricRandomHills
from vtkmodules.vtkCommonCore import (
    VTK_DOUBLE,
    vtkIdList,
    vtkLookupTable,
    vtkVariant,
    vtkVariantArray,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkFeatureEdges,
    vtkGenerateIds,
    vtkGlyph3D,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkCurvatures,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkParametricFunctionSource,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
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

param_source = vtkParametricFunctionSource()
param_source.SetParametricFunction(fn)
param_source.SetUResolution(50)
param_source.SetVResolution(50)
param_source.SetScalarModeToZ()
param_source.Update()
param_source.GetOutput().GetPointData().GetScalars().SetName("Elevation")

# Transform: rotate so Y is up
transform = vtkTransform()
transform.Translate(0.0, 5.0, 15.0)
transform.RotateX(-90.0)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(param_source.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()

surface = transform_filter.GetOutput()

# Curvature: compute Gaussian curvature
curvature_name = "Gauss_Curvature"
cc = vtkCurvatures()
cc.SetInputData(surface)
cc.SetCurvatureTypeToGaussian()
cc.Update()

# Adjust edge curvatures: replace boundary point curvatures with
# weighted average of interior neighbours
curv_output = cc.GetOutput()
curv_output.GetPointData().SetActiveScalars(curvature_name)
np_source = dsa.WrapDataObject(curv_output)
curvatures = np_source.PointData[curvature_name]

array_name = "ids"
id_filter = vtkGenerateIds()
id_filter.SetInputData(curv_output)
id_filter.SetPointIds(True)
id_filter.SetCellIds(False)
id_filter.SetPointIdsArrayName(array_name)
id_filter.SetCellIdsArrayName(array_name)
id_filter.Update()

edges = vtkFeatureEdges()
edges.SetInputConnection(id_filter.GetOutputPort())
edges.BoundaryEdgesOn()
edges.ManifoldEdgesOff()
edges.NonManifoldEdgesOff()
edges.FeatureEdgesOff()
edges.Update()

edge_array = edges.GetOutput().GetPointData().GetArray(array_name)
boundary_ids = []
for i in range(edges.GetOutput().GetNumberOfPoints()):
    boundary_ids.append(edge_array.GetValue(i))
p_ids_set = set(boundary_ids)

for p_id in boundary_ids:
    cell_ids = vtkIdList()
    curv_output.GetPointCells(p_id, cell_ids)
    neighbour = set()
    for cell_idx in range(cell_ids.GetNumberOfIds()):
        cell_id = cell_ids.GetId(cell_idx)
        cell_point_ids = vtkIdList()
        curv_output.GetCellPoints(cell_id, cell_point_ids)
        for cell_pt_idx in range(cell_point_ids.GetNumberOfIds()):
            neighbour.add(cell_point_ids.GetId(cell_pt_idx))
    neighbour -= p_ids_set
    curvs = [curvatures[n] for n in neighbour]
    dists = [np.linalg.norm(np.array(curv_output.GetPoint(n)) - np.array(curv_output.GetPoint(p_id))) for n in neighbour]
    curvs = np.array(curvs)
    dists = np.array(dists)
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        curvatures[p_id] = np.dot(curvs, weights)
    else:
        curvatures[p_id] = 0.0

epsilon = 1.0e-08
curvatures = np.where(abs(curvatures) < epsilon, 0, curvatures)
curv_arr = numpy_support.numpy_to_vtk(num_array=curvatures.ravel(), deep=True, array_type=VTK_DOUBLE)
curv_arr.SetName(curvature_name)
curv_output.GetPointData().RemoveArray(curvature_name)
curv_output.GetPointData().AddArray(curv_arr)
curv_output.GetPointData().SetActiveScalars(curvature_name)

scalar_range_curvatures = curv_output.GetPointData().GetScalars(curvature_name).GetRange()
scalar_range_elevation = curv_output.GetPointData().GetScalars("Elevation").GetRange()

# Lookup table: categorical (Brewer Qualitative Set3) for curvature bands
color_series = vtkColorSeries()
color_series.SetColorScheme(color_series.BREWER_QUALITATIVE_SET3)

lut = vtkLookupTable()
color_series.BuildLookupTable(lut, color_series.CATEGORICAL)
lut.SetNanColor(0, 0, 0, 1)

# Lookup table: diverging green-to-red for elevation on glyphs
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(1.0, 0.758, 0.214, 0.233)

lut_elev = vtkLookupTable()
lut_elev.SetNumberOfTableValues(256)
lut_elev.Build()
for i in range(256):
    rgba = list(ctf.GetColor(float(i) / 256))
    rgba.append(1)
    lut_elev.SetTableValue(i, rgba)
lut_elev.SetTableRange(scalar_range_elevation)

# Bands: custom curvature bands for RandomHills
my_bands = [
    [-0.630, -0.190], [-0.190, -0.043], [-0.043, 0.0452], [0.0452, 0.0746],
    [0.0746, 0.104], [0.104, 0.251], [0.251, 1.131],
]

bands = dict()
idx_min = 0
for idx in range(len(my_bands)):
    if my_bands[idx][1] > scalar_range_curvatures[0] >= my_bands[idx][0]:
        idx_min = idx
        break
idx_max = len(my_bands) - 1
for idx in range(len(my_bands) - 1, -1, -1):
    if my_bands[idx][1] > scalar_range_curvatures[1] >= my_bands[idx][0]:
        idx_max = idx
        break
my_bands[idx_min][0] = scalar_range_curvatures[0]
my_bands[idx_max][1] = scalar_range_curvatures[1]
trimmed = my_bands[idx_min: idx_max + 1]
for idx, e in enumerate(trimmed):
    bands[idx] = [e[0], e[0] + (e[1] - e[0]) / 2, e[1]]

# Trim empty leading/trailing bands
freq = dict()
for i in range(len(bands)):
    freq[i] = 0
num_tuples = curv_output.GetPointData().GetScalars().GetNumberOfTuples()
for i in range(num_tuples):
    x = curv_output.GetPointData().GetScalars().GetTuple1(i)
    for j in range(len(bands)):
        if x <= bands[j][2]:
            freq[j] += 1
            break

first = 0
for k, v in freq.items():
    if v != 0:
        first = k
        break
last = max(freq.keys())
for idx in list(freq.keys())[::-1]:
    if freq[idx] != 0:
        last = idx
        break
min_key = min(freq.keys())
max_key = max(freq.keys())
for idx in range(min_key, first):
    freq.pop(idx)
    bands.pop(idx)
for idx in range(last + 1, max_key + 1):
    freq.popitem()
    bands.popitem()
adj_freq = dict()
adj_bands = dict()
for idx, k in enumerate(freq.keys()):
    adj_freq[idx] = freq[k]
    adj_bands[idx] = bands[k]
bands = adj_bands

lut.SetTableRange(scalar_range_curvatures)
lut.SetNumberOfTableValues(len(bands))

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

# Filter: create banded curvature contours
bcf = vtkBandedPolyDataContourFilter()
bcf.SetInputData(curv_output)
for k in bands:
    bcf.SetValue(k, bands[k][2])
bcf.SetScalarModeToIndex()
bcf.GenerateContourEdgesOn()

# Glyph: arrow glyphs showing surface normals colored by elevation
mask_pts = vtkMaskPoints()
mask_pts.SetOnRatio(5)
mask_pts.RandomModeOn()
mask_pts.SetInputData(curv_output)

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

# Mapper: map the banded curvature surface
src_mapper = vtkPolyDataMapper()
src_mapper.SetInputConnection(bcf.GetOutputPort())
src_mapper.SetScalarRange(scalar_range_curvatures)
src_mapper.SetLookupTable(lut)
src_mapper.SetScalarModeToUseCellData()

# Actor: display the banded curvature surface
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
glyph_mapper.SetLookupTable(lut_elev)
glyph_mapper.SetScalarRange(scalar_range_elevation)

# Actor: display the normal glyphs
glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Scalar bar: Gaussian curvature legend
window_width = 800
window_height = 800

scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lutr)
scalar_bar.SetTitle("Gauss\nCurvature")
scalar_bar.GetTitleTextProperty().SetColor(alice_blue)
scalar_bar.GetLabelTextProperty().SetColor(alice_blue)
scalar_bar.GetAnnotationTextProperty().SetColor(alice_blue)
scalar_bar.UnconstrainedFontSizeOn()
scalar_bar.SetMaximumWidthInPixels(window_width // 8)
scalar_bar.SetMaximumHeightInPixels(window_height // 3)
scalar_bar.SetPosition(0.85, 0.05)

# Scalar bar: elevation legend
scalar_bar_elev = vtkScalarBarActor()
scalar_bar_elev.SetLookupTable(lut_elev)
scalar_bar_elev.SetTitle("Elevation")
scalar_bar_elev.GetTitleTextProperty().SetColor(alice_blue)
scalar_bar_elev.GetLabelTextProperty().SetColor(alice_blue)
scalar_bar_elev.GetAnnotationTextProperty().SetColor(alice_blue)
scalar_bar_elev.UnconstrainedFontSizeOn()
scalar_bar_elev.SetNumberOfLabels(5)
scalar_bar_elev.SetMaximumWidthInPixels(window_width // 8)
scalar_bar_elev.SetMaximumHeightInPixels(window_height // 3)
scalar_bar_elev.SetPosition(0.85, 0.4)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddViewProp(src_actor)
renderer.AddViewProp(edge_actor)
renderer.AddViewProp(glyph_actor)
renderer.AddViewProp(scalar_bar)
renderer.AddViewProp(scalar_bar_elev)
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
render_window.SetWindowName("CurvatureBandsWithGlyphs")
render_window.SetSize(window_width, window_height)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
