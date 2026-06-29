#!/usr/bin/env python

# Demonstrate Gaussian and Mean curvature on two surfaces (superquadric torus
# and RandomHills) in a 2x2 grid with diverging colour map and scalar bars.

import numpy as np
from vtk.util import numpy_support

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricRandomHills
from vtkmodules.vtkCommonCore import (
    VTK_DOUBLE,
    vtkIdList,
    vtkLookupTable,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkCleanPolyData,
    vtkFeatureEdges,
    vtkGenerateIds,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkCurvatures,
    vtkTransformFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkParametricFunctionSource,
    vtkSuperquadricSource,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkTextProperty,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)
midnight_blue_rgb = (0.098, 0.098, 0.439)
gainsboro_rgb = (0.863, 0.863, 0.863)
dark_orange_rgb = (1.000, 0.549, 0.000)

# --- Source 1: superquadric torus ---
torus = vtkSuperquadricSource()
torus.SetCenter(0.0, 0.0, 0.0)
torus.SetScale(1.0, 1.0, 1.0)
torus.SetPhiResolution(64)
torus.SetThetaResolution(64)
torus.SetThetaRoundness(1)
torus.SetThickness(0.5)
torus.SetSize(0.5)
torus.SetToroidal(1)

toroid_transform = vtkTransform()
toroid_transform.RotateX(55)

toroid_transform_filter = vtkTransformFilter()
toroid_transform_filter.SetInputConnection(torus.GetOutputPort())
toroid_transform_filter.SetTransform(toroid_transform)

tri = vtkTriangleFilter()
tri.SetInputConnection(toroid_transform_filter.GetOutputPort())

cleaner = vtkCleanPolyData()
cleaner.SetInputConnection(tri.GetOutputPort())
cleaner.SetTolerance(0.005)
cleaner.Update()

# --- Source 2: parametric RandomHills ---
rh = vtkParametricRandomHills()
rh_fn_src = vtkParametricFunctionSource()
rh_fn_src.SetParametricFunction(rh)
rh_fn_src.Update()

# --- Compute curvatures for all four panels ---
# Panel layout: [torus-Gauss, torus-Mean, hills-Gauss, hills-Mean]
epsilon = 1.0e-08

# --- Panel 0: torus Gaussian curvature ---
torus_gauss_cc = vtkCurvatures()
torus_gauss_cc.SetInputConnection(cleaner.GetOutputPort())
torus_gauss_cc.SetCurvatureTypeToGaussian()
torus_gauss_cc.Update()
torus_gauss_output = torus_gauss_cc.GetOutput()

torus_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")
torus_gauss_np = dsa.WrapDataObject(torus_gauss_output)
torus_gauss_arr = torus_gauss_np.PointData["Gauss_Curvature"]

torus_gauss_gen_ids = vtkGenerateIds()
torus_gauss_gen_ids.SetInputData(torus_gauss_output)
torus_gauss_gen_ids.SetPointIds(True)
torus_gauss_gen_ids.SetCellIds(False)
torus_gauss_gen_ids.SetPointIdsArrayName("ids")
torus_gauss_gen_ids.SetCellIdsArrayName("ids")
torus_gauss_gen_ids.Update()

torus_gauss_edges = vtkFeatureEdges()
torus_gauss_edges.SetInputConnection(torus_gauss_gen_ids.GetOutputPort())
torus_gauss_edges.BoundaryEdgesOn()
torus_gauss_edges.ManifoldEdgesOff()
torus_gauss_edges.NonManifoldEdgesOff()
torus_gauss_edges.FeatureEdgesOff()
torus_gauss_edges.Update()

torus_gauss_edge_array = torus_gauss_edges.GetOutput().GetPointData().GetArray("ids")
torus_gauss_boundary_ids = []
for bi in range(torus_gauss_edges.GetOutput().GetNumberOfPoints()):
    torus_gauss_boundary_ids.append(torus_gauss_edge_array.GetValue(bi))
torus_gauss_boundary_set = set(torus_gauss_boundary_ids)

for p_id in torus_gauss_boundary_ids:
    cell_ids = vtkIdList()
    torus_gauss_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        torus_gauss_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= torus_gauss_boundary_set
    curvs = np.array([torus_gauss_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(torus_gauss_output.GetPoint(n)) - np.array(torus_gauss_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        torus_gauss_arr[p_id] = np.dot(curvs, weights)
    else:
        torus_gauss_arr[p_id] = 0.0

torus_gauss_arr = np.where(np.abs(torus_gauss_arr) < epsilon, 0, torus_gauss_arr)
torus_gauss_vtk = numpy_support.numpy_to_vtk(
    num_array=torus_gauss_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
torus_gauss_vtk.SetName("Gauss_Curvature")
torus_gauss_output.GetPointData().RemoveArray("Gauss_Curvature")
torus_gauss_output.GetPointData().AddArray(torus_gauss_vtk)
torus_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")

# --- Panel 1: torus Mean curvature ---
torus_mean_cc = vtkCurvatures()
torus_mean_cc.SetInputConnection(cleaner.GetOutputPort())
torus_mean_cc.SetCurvatureTypeToMean()
torus_mean_cc.Update()
torus_mean_output = torus_mean_cc.GetOutput()

torus_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")
torus_mean_np = dsa.WrapDataObject(torus_mean_output)
torus_mean_arr = torus_mean_np.PointData["Mean_Curvature"]

torus_mean_gen_ids = vtkGenerateIds()
torus_mean_gen_ids.SetInputData(torus_mean_output)
torus_mean_gen_ids.SetPointIds(True)
torus_mean_gen_ids.SetCellIds(False)
torus_mean_gen_ids.SetPointIdsArrayName("ids")
torus_mean_gen_ids.SetCellIdsArrayName("ids")
torus_mean_gen_ids.Update()

torus_mean_edges = vtkFeatureEdges()
torus_mean_edges.SetInputConnection(torus_mean_gen_ids.GetOutputPort())
torus_mean_edges.BoundaryEdgesOn()
torus_mean_edges.ManifoldEdgesOff()
torus_mean_edges.NonManifoldEdgesOff()
torus_mean_edges.FeatureEdgesOff()
torus_mean_edges.Update()

torus_mean_edge_array = torus_mean_edges.GetOutput().GetPointData().GetArray("ids")
torus_mean_boundary_ids = []
for bi in range(torus_mean_edges.GetOutput().GetNumberOfPoints()):
    torus_mean_boundary_ids.append(torus_mean_edge_array.GetValue(bi))
torus_mean_boundary_set = set(torus_mean_boundary_ids)

for p_id in torus_mean_boundary_ids:
    cell_ids = vtkIdList()
    torus_mean_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        torus_mean_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= torus_mean_boundary_set
    curvs = np.array([torus_mean_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(torus_mean_output.GetPoint(n)) - np.array(torus_mean_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        torus_mean_arr[p_id] = np.dot(curvs, weights)
    else:
        torus_mean_arr[p_id] = 0.0

torus_mean_arr = np.where(np.abs(torus_mean_arr) < epsilon, 0, torus_mean_arr)
torus_mean_vtk = numpy_support.numpy_to_vtk(
    num_array=torus_mean_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
torus_mean_vtk.SetName("Mean_Curvature")
torus_mean_output.GetPointData().RemoveArray("Mean_Curvature")
torus_mean_output.GetPointData().AddArray(torus_mean_vtk)
torus_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")

# --- Panel 2: hills Gaussian curvature ---
hills_gauss_cc = vtkCurvatures()
hills_gauss_cc.SetInputConnection(rh_fn_src.GetOutputPort())
hills_gauss_cc.SetCurvatureTypeToGaussian()
hills_gauss_cc.Update()
hills_gauss_output = hills_gauss_cc.GetOutput()

hills_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")
hills_gauss_np = dsa.WrapDataObject(hills_gauss_output)
hills_gauss_arr = hills_gauss_np.PointData["Gauss_Curvature"]

hills_gauss_gen_ids = vtkGenerateIds()
hills_gauss_gen_ids.SetInputData(hills_gauss_output)
hills_gauss_gen_ids.SetPointIds(True)
hills_gauss_gen_ids.SetCellIds(False)
hills_gauss_gen_ids.SetPointIdsArrayName("ids")
hills_gauss_gen_ids.SetCellIdsArrayName("ids")
hills_gauss_gen_ids.Update()

hills_gauss_edges = vtkFeatureEdges()
hills_gauss_edges.SetInputConnection(hills_gauss_gen_ids.GetOutputPort())
hills_gauss_edges.BoundaryEdgesOn()
hills_gauss_edges.ManifoldEdgesOff()
hills_gauss_edges.NonManifoldEdgesOff()
hills_gauss_edges.FeatureEdgesOff()
hills_gauss_edges.Update()

hills_gauss_edge_array = hills_gauss_edges.GetOutput().GetPointData().GetArray("ids")
hills_gauss_boundary_ids = []
for bi in range(hills_gauss_edges.GetOutput().GetNumberOfPoints()):
    hills_gauss_boundary_ids.append(hills_gauss_edge_array.GetValue(bi))
hills_gauss_boundary_set = set(hills_gauss_boundary_ids)

for p_id in hills_gauss_boundary_ids:
    cell_ids = vtkIdList()
    hills_gauss_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        hills_gauss_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= hills_gauss_boundary_set
    curvs = np.array([hills_gauss_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(hills_gauss_output.GetPoint(n)) - np.array(hills_gauss_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        hills_gauss_arr[p_id] = np.dot(curvs, weights)
    else:
        hills_gauss_arr[p_id] = 0.0

hills_gauss_arr = np.where(np.abs(hills_gauss_arr) < epsilon, 0, hills_gauss_arr)
hills_gauss_vtk = numpy_support.numpy_to_vtk(
    num_array=hills_gauss_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
hills_gauss_vtk.SetName("Gauss_Curvature")
hills_gauss_output.GetPointData().RemoveArray("Gauss_Curvature")
hills_gauss_output.GetPointData().AddArray(hills_gauss_vtk)
hills_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")

# --- Panel 3: hills Mean curvature ---
hills_mean_cc = vtkCurvatures()
hills_mean_cc.SetInputConnection(rh_fn_src.GetOutputPort())
hills_mean_cc.SetCurvatureTypeToMean()
hills_mean_cc.Update()
hills_mean_output = hills_mean_cc.GetOutput()

hills_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")
hills_mean_np = dsa.WrapDataObject(hills_mean_output)
hills_mean_arr = hills_mean_np.PointData["Mean_Curvature"]

hills_mean_gen_ids = vtkGenerateIds()
hills_mean_gen_ids.SetInputData(hills_mean_output)
hills_mean_gen_ids.SetPointIds(True)
hills_mean_gen_ids.SetCellIds(False)
hills_mean_gen_ids.SetPointIdsArrayName("ids")
hills_mean_gen_ids.SetCellIdsArrayName("ids")
hills_mean_gen_ids.Update()

hills_mean_edges = vtkFeatureEdges()
hills_mean_edges.SetInputConnection(hills_mean_gen_ids.GetOutputPort())
hills_mean_edges.BoundaryEdgesOn()
hills_mean_edges.ManifoldEdgesOff()
hills_mean_edges.NonManifoldEdgesOff()
hills_mean_edges.FeatureEdgesOff()
hills_mean_edges.Update()

hills_mean_edge_array = hills_mean_edges.GetOutput().GetPointData().GetArray("ids")
hills_mean_boundary_ids = []
for bi in range(hills_mean_edges.GetOutput().GetNumberOfPoints()):
    hills_mean_boundary_ids.append(hills_mean_edge_array.GetValue(bi))
hills_mean_boundary_set = set(hills_mean_boundary_ids)

for p_id in hills_mean_boundary_ids:
    cell_ids = vtkIdList()
    hills_mean_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        hills_mean_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= hills_mean_boundary_set
    curvs = np.array([hills_mean_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(hills_mean_output.GetPoint(n)) - np.array(hills_mean_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        hills_mean_arr[p_id] = np.dot(curvs, weights)
    else:
        hills_mean_arr[p_id] = 0.0

hills_mean_arr = np.where(np.abs(hills_mean_arr) < epsilon, 0, hills_mean_arr)
hills_mean_vtk = numpy_support.numpy_to_vtk(
    num_array=hills_mean_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
hills_mean_vtk.SetName("Mean_Curvature")
hills_mean_output.GetPointData().RemoveArray("Mean_Curvature")
hills_mean_output.GetPointData().AddArray(hills_mean_vtk)
hills_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")

# --- Diverging LUT (MidnightBlue → Gainsboro → DarkOrange) ---
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, *midnight_blue_rgb)
ctf.AddRGBPoint(0.5, *gainsboro_rgb)
ctf.AddRGBPoint(1.0, *dark_orange_rgb)

lut = vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.Build()
for i in range(256):
    rgba = list(ctf.GetColor(float(i) / 256))
    rgba.append(1)
    lut.SetTableValue(i, rgba)

# --- 2x2 grid visualization ---
renderer_size = 512
window_width = renderer_size * 2
window_height = renderer_size * 2

text_property = vtkTextProperty()
text_property.SetFontSize(24)
text_property.SetJustificationToCentered()

# --- Panel 0 renderer: torus Gaussian (top-left) ---
torus_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")
torus_gauss_scalar_range = torus_gauss_output.GetPointData().GetScalars("Gauss_Curvature").GetRange()

torus_gauss_mapper = vtkPolyDataMapper()
torus_gauss_mapper.SetInputData(torus_gauss_output)
torus_gauss_mapper.SetScalarModeToUsePointFieldData()
torus_gauss_mapper.SelectColorArray("Gauss_Curvature")
torus_gauss_mapper.SetScalarRange(torus_gauss_scalar_range)
torus_gauss_mapper.SetLookupTable(lut)

torus_gauss_actor = vtkActor()
torus_gauss_actor.SetMapper(torus_gauss_mapper)

torus_gauss_scalar_bar = vtkScalarBarActor()
torus_gauss_scalar_bar.SetLookupTable(torus_gauss_mapper.GetLookupTable())
torus_gauss_scalar_bar.SetTitle("Gauss\nCurvature")
torus_gauss_scalar_bar.UnconstrainedFontSizeOn()
torus_gauss_scalar_bar.SetNumberOfLabels(5)
torus_gauss_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
torus_gauss_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
torus_gauss_scalar_bar.SetBarRatio(torus_gauss_scalar_bar.GetBarRatio() * 0.5)
torus_gauss_scalar_bar.SetPosition(0.85, 0.1)

torus_gauss_text_actor = vtkTextActor()
torus_gauss_text_actor.SetInput("Gauss\nCurvature")
torus_gauss_text_actor.SetPosition(250, 16)
torus_gauss_text_actor.GetTextProperty().ShallowCopy(text_property)

torus_gauss_renderer = vtkRenderer()
torus_gauss_renderer.SetViewport(0.0, 0.5, 0.5, 1.0)
torus_gauss_renderer.SetBackground(slate_gray_rgb)
torus_gauss_renderer.AddActor(torus_gauss_actor)
torus_gauss_renderer.AddActor(torus_gauss_text_actor)
torus_gauss_renderer.AddActor(torus_gauss_scalar_bar)

# --- Panel 1 renderer: torus Mean (top-right) ---
torus_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")
torus_mean_scalar_range = torus_mean_output.GetPointData().GetScalars("Mean_Curvature").GetRange()

torus_mean_mapper = vtkPolyDataMapper()
torus_mean_mapper.SetInputData(torus_mean_output)
torus_mean_mapper.SetScalarModeToUsePointFieldData()
torus_mean_mapper.SelectColorArray("Mean_Curvature")
torus_mean_mapper.SetScalarRange(torus_mean_scalar_range)
torus_mean_mapper.SetLookupTable(lut)

torus_mean_actor = vtkActor()
torus_mean_actor.SetMapper(torus_mean_mapper)

torus_mean_scalar_bar = vtkScalarBarActor()
torus_mean_scalar_bar.SetLookupTable(torus_mean_mapper.GetLookupTable())
torus_mean_scalar_bar.SetTitle("Mean\nCurvature")
torus_mean_scalar_bar.UnconstrainedFontSizeOn()
torus_mean_scalar_bar.SetNumberOfLabels(5)
torus_mean_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
torus_mean_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
torus_mean_scalar_bar.SetBarRatio(torus_mean_scalar_bar.GetBarRatio() * 0.5)
torus_mean_scalar_bar.SetPosition(0.85, 0.1)

torus_mean_text_actor = vtkTextActor()
torus_mean_text_actor.SetInput("Mean\nCurvature")
torus_mean_text_actor.SetPosition(250, 16)
torus_mean_text_actor.GetTextProperty().ShallowCopy(text_property)

torus_mean_renderer = vtkRenderer()
torus_mean_renderer.SetViewport(0.5, 0.5, 1.0, 1.0)
torus_mean_renderer.SetBackground(slate_gray_rgb)
torus_mean_renderer.AddActor(torus_mean_actor)
torus_mean_renderer.AddActor(torus_mean_text_actor)
torus_mean_renderer.AddActor(torus_mean_scalar_bar)

# --- Panel 2 renderer: hills Gaussian (bottom-left) ---
hills_gauss_output.GetPointData().SetActiveScalars("Gauss_Curvature")
hills_gauss_scalar_range = hills_gauss_output.GetPointData().GetScalars("Gauss_Curvature").GetRange()

hills_gauss_mapper = vtkPolyDataMapper()
hills_gauss_mapper.SetInputData(hills_gauss_output)
hills_gauss_mapper.SetScalarModeToUsePointFieldData()
hills_gauss_mapper.SelectColorArray("Gauss_Curvature")
hills_gauss_mapper.SetScalarRange(hills_gauss_scalar_range)
hills_gauss_mapper.SetLookupTable(lut)

hills_gauss_actor = vtkActor()
hills_gauss_actor.SetMapper(hills_gauss_mapper)

hills_gauss_scalar_bar = vtkScalarBarActor()
hills_gauss_scalar_bar.SetLookupTable(hills_gauss_mapper.GetLookupTable())
hills_gauss_scalar_bar.SetTitle("Gauss\nCurvature")
hills_gauss_scalar_bar.UnconstrainedFontSizeOn()
hills_gauss_scalar_bar.SetNumberOfLabels(5)
hills_gauss_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
hills_gauss_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
hills_gauss_scalar_bar.SetBarRatio(hills_gauss_scalar_bar.GetBarRatio() * 0.5)
hills_gauss_scalar_bar.SetPosition(0.85, 0.1)

hills_gauss_text_actor = vtkTextActor()
hills_gauss_text_actor.SetInput("Gauss\nCurvature")
hills_gauss_text_actor.SetPosition(250, 16)
hills_gauss_text_actor.GetTextProperty().ShallowCopy(text_property)

hills_gauss_renderer = vtkRenderer()
hills_gauss_renderer.SetViewport(0.0, 0.0, 0.5, 0.5)
hills_gauss_renderer.SetBackground(slate_gray_rgb)
hills_gauss_renderer.AddActor(hills_gauss_actor)
hills_gauss_renderer.AddActor(hills_gauss_text_actor)
hills_gauss_renderer.AddActor(hills_gauss_scalar_bar)

# --- Panel 3 renderer: hills Mean (bottom-right) ---
hills_mean_output.GetPointData().SetActiveScalars("Mean_Curvature")
hills_mean_scalar_range = hills_mean_output.GetPointData().GetScalars("Mean_Curvature").GetRange()

hills_mean_mapper = vtkPolyDataMapper()
hills_mean_mapper.SetInputData(hills_mean_output)
hills_mean_mapper.SetScalarModeToUsePointFieldData()
hills_mean_mapper.SelectColorArray("Mean_Curvature")
hills_mean_mapper.SetScalarRange(hills_mean_scalar_range)
hills_mean_mapper.SetLookupTable(lut)

hills_mean_actor = vtkActor()
hills_mean_actor.SetMapper(hills_mean_mapper)

hills_mean_scalar_bar = vtkScalarBarActor()
hills_mean_scalar_bar.SetLookupTable(hills_mean_mapper.GetLookupTable())
hills_mean_scalar_bar.SetTitle("Mean\nCurvature")
hills_mean_scalar_bar.UnconstrainedFontSizeOn()
hills_mean_scalar_bar.SetNumberOfLabels(5)
hills_mean_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
hills_mean_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
hills_mean_scalar_bar.SetBarRatio(hills_mean_scalar_bar.GetBarRatio() * 0.5)
hills_mean_scalar_bar.SetPosition(0.85, 0.1)

hills_mean_text_actor = vtkTextActor()
hills_mean_text_actor.SetInput("Mean\nCurvature")
hills_mean_text_actor.SetPosition(250, 16)
hills_mean_text_actor.GetTextProperty().ShallowCopy(text_property)

hills_mean_renderer = vtkRenderer()
hills_mean_renderer.SetViewport(0.5, 0.0, 1.0, 0.5)
hills_mean_renderer.SetBackground(slate_gray_rgb)
hills_mean_renderer.AddActor(hills_mean_actor)
hills_mean_renderer.AddActor(hills_mean_text_actor)
hills_mean_renderer.AddActor(hills_mean_scalar_bar)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(torus_gauss_renderer)
render_window.AddRenderer(torus_mean_renderer)
render_window.AddRenderer(hills_gauss_renderer)
render_window.AddRenderer(hills_mean_renderer)
render_window.SetWindowName("curvatures app")
render_window.SetMultiSamples(0)
render_window.SetSize(window_width, window_height)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
