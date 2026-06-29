#!/usr/bin/env python

# Compute Gaussian and Mean curvatures on a RandomHills parametric surface,
# adjust edge curvatures, and display side-by-side with a cool-to-warm LUT.

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
    vtkFeatureEdges,
    vtkGenerateIds,
    vtkPolyDataTangents,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkCurvatures,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
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
paraview_bkg_rgb = (0.322, 0.341, 0.431)

# --- Source: RandomHills parametric surface ---
hills = vtkParametricRandomHills()
hills.SetRandomSeed(1)
hills.SetNumberOfHills(30)

hills_source = vtkParametricFunctionSource()
hills_source.SetUResolution(51)
hills_source.SetVResolution(51)
hills_source.GenerateTextureCoordinatesOn()
hills_source.SetParametricFunction(hills)
hills_source.Update()

tangents = vtkPolyDataTangents()
tangents.SetInputConnection(hills_source.GetOutputPort())
tangents.Update()

transform = vtkTransform()
transform.Translate(0.0, 5.0, 15.0)
transform.RotateX(-90.0)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(tangents.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()
source = transform_filter.GetOutput()

# --- Helper: adjust edge curvatures inline ---
epsilon = 1.0e-08

# --- Gaussian curvature: compute and adjust edges ---
gauss_cc = vtkCurvatures()
gauss_cc.SetInputData(source)
gauss_cc.SetCurvatureTypeToGaussian()
gauss_cc.Update()
gauss_curv_output = gauss_cc.GetOutput()

gauss_curv_output.GetPointData().SetActiveScalars("Gauss_Curvature")
gauss_np_src = dsa.WrapDataObject(gauss_curv_output)
gauss_curvatures_arr = gauss_np_src.PointData["Gauss_Curvature"]

gauss_generate_ids = vtkGenerateIds()
gauss_generate_ids.SetInputData(gauss_curv_output)
gauss_generate_ids.SetPointIds(True)
gauss_generate_ids.SetCellIds(False)
gauss_generate_ids.SetPointIdsArrayName("ids")
gauss_generate_ids.SetCellIdsArrayName("ids")
gauss_generate_ids.Update()

gauss_edges = vtkFeatureEdges()
gauss_edges.SetInputConnection(gauss_generate_ids.GetOutputPort())
gauss_edges.BoundaryEdgesOn()
gauss_edges.ManifoldEdgesOff()
gauss_edges.NonManifoldEdgesOff()
gauss_edges.FeatureEdgesOff()
gauss_edges.Update()

gauss_edge_array = gauss_edges.GetOutput().GetPointData().GetArray("ids")
gauss_boundary_ids = []
for i in range(gauss_edges.GetOutput().GetNumberOfPoints()):
    gauss_boundary_ids.append(gauss_edge_array.GetValue(i))
gauss_boundary_set = set(gauss_boundary_ids)

for p_id in gauss_boundary_ids:
    cell_ids = vtkIdList()
    gauss_curv_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        gauss_curv_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= gauss_boundary_set
    curvs = np.array([gauss_curvatures_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(gauss_curv_output.GetPoint(n)) - np.array(gauss_curv_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        gauss_curvatures_arr[p_id] = np.dot(curvs, weights)
    else:
        gauss_curvatures_arr[p_id] = 0.0

gauss_curvatures_arr = np.where(np.abs(gauss_curvatures_arr) < epsilon, 0, gauss_curvatures_arr)
gauss_curv_vtk = numpy_support.numpy_to_vtk(
    num_array=gauss_curvatures_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
gauss_curv_vtk.SetName("Gauss_Curvature")
gauss_curv_output.GetPointData().RemoveArray("Gauss_Curvature")
gauss_curv_output.GetPointData().AddArray(gauss_curv_vtk)
gauss_curv_output.GetPointData().SetActiveScalars("Gauss_Curvature")

source.GetPointData().AddArray(
    gauss_curv_output.GetPointData().GetAbstractArray("Gauss_Curvature")
)

# --- Mean curvature: compute and adjust edges ---
mean_cc = vtkCurvatures()
mean_cc.SetInputData(source)
mean_cc.SetCurvatureTypeToMean()
mean_cc.Update()
mean_curv_output = mean_cc.GetOutput()

mean_curv_output.GetPointData().SetActiveScalars("Mean_Curvature")
mean_np_src = dsa.WrapDataObject(mean_curv_output)
mean_curvatures_arr = mean_np_src.PointData["Mean_Curvature"]

mean_generate_ids = vtkGenerateIds()
mean_generate_ids.SetInputData(mean_curv_output)
mean_generate_ids.SetPointIds(True)
mean_generate_ids.SetCellIds(False)
mean_generate_ids.SetPointIdsArrayName("ids")
mean_generate_ids.SetCellIdsArrayName("ids")
mean_generate_ids.Update()

mean_edges = vtkFeatureEdges()
mean_edges.SetInputConnection(mean_generate_ids.GetOutputPort())
mean_edges.BoundaryEdgesOn()
mean_edges.ManifoldEdgesOff()
mean_edges.NonManifoldEdgesOff()
mean_edges.FeatureEdgesOff()
mean_edges.Update()

mean_edge_array = mean_edges.GetOutput().GetPointData().GetArray("ids")
mean_boundary_ids = []
for i in range(mean_edges.GetOutput().GetNumberOfPoints()):
    mean_boundary_ids.append(mean_edge_array.GetValue(i))
mean_boundary_set = set(mean_boundary_ids)

for p_id in mean_boundary_ids:
    cell_ids = vtkIdList()
    mean_curv_output.GetPointCells(p_id, cell_ids)
    neighbours = set()
    for ci in range(cell_ids.GetNumberOfIds()):
        cell_point_ids = vtkIdList()
        mean_curv_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
        for cpi in range(cell_point_ids.GetNumberOfIds()):
            neighbours.add(cell_point_ids.GetId(cpi))
    neighbours -= mean_boundary_set
    curvs = np.array([mean_curvatures_arr[n] for n in neighbours])
    dists = np.array([
        np.linalg.norm(
            np.array(mean_curv_output.GetPoint(n)) - np.array(mean_curv_output.GetPoint(p_id))
        )
        for n in neighbours
    ])
    curvs = curvs[dists > 0]
    dists = dists[dists > 0]
    if len(curvs) > 0:
        weights = 1.0 / dists
        weights /= weights.sum()
        mean_curvatures_arr[p_id] = np.dot(curvs, weights)
    else:
        mean_curvatures_arr[p_id] = 0.0

mean_curvatures_arr = np.where(np.abs(mean_curvatures_arr) < epsilon, 0, mean_curvatures_arr)
mean_curv_vtk = numpy_support.numpy_to_vtk(
    num_array=mean_curvatures_arr.ravel(), deep=True, array_type=VTK_DOUBLE
)
mean_curv_vtk.SetName("Mean_Curvature")
mean_curv_output.GetPointData().RemoveArray("Mean_Curvature")
mean_curv_output.GetPointData().AddArray(mean_curv_vtk)
mean_curv_output.GetPointData().SetActiveScalars("Mean_Curvature")

source.GetPointData().AddArray(
    mean_curv_output.GetPointData().GetAbstractArray("Mean_Curvature")
)

# --- Diverging LUT (cool-to-warm) ---
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.230, 0.299, 0.754)
ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(1.0, 0.706, 0.016, 0.150)

lut = vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.Build()
for i in range(256):
    rgba = list(ctf.GetColor(float(i) / 256))
    rgba.append(1)
    lut.SetTableValue(i, rgba)

# --- Visualization: side-by-side viewports ---
window_width = 1024
window_height = 512

text_property = vtkTextProperty()
text_property.SetFontSize(24)
text_property.SetJustificationToCentered()

# --- Gauss viewport ---
source.GetPointData().SetActiveScalars("Gauss_Curvature")
gauss_scalar_range = source.GetPointData().GetScalars("Gauss_Curvature").GetRange()

gauss_mapper = vtkPolyDataMapper()
gauss_mapper.SetInputData(source)
gauss_mapper.SetScalarModeToUsePointFieldData()
gauss_mapper.SelectColorArray("Gauss_Curvature")
gauss_mapper.SetScalarRange(gauss_scalar_range)
gauss_mapper.SetLookupTable(lut)

gauss_actor = vtkActor()
gauss_actor.SetMapper(gauss_mapper)

gauss_scalar_bar = vtkScalarBarActor()
gauss_scalar_bar.SetLookupTable(gauss_mapper.GetLookupTable())
gauss_scalar_bar.SetTitle("Gauss\nCurvature")
gauss_scalar_bar.UnconstrainedFontSizeOn()
gauss_scalar_bar.SetNumberOfLabels(5)
gauss_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
gauss_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
gauss_scalar_bar.SetBarRatio(gauss_scalar_bar.GetBarRatio() * 0.5)
gauss_scalar_bar.SetPosition(0.85, 0.1)

gauss_text_actor = vtkTextActor()
gauss_text_actor.SetInput("Gauss\nCurvature")
gauss_text_actor.SetPosition(250, 16)
gauss_text_actor.GetTextProperty().ShallowCopy(text_property)

gauss_renderer = vtkRenderer()
gauss_renderer.SetBackground(paraview_bkg_rgb)
gauss_renderer.AddActor(gauss_actor)
gauss_renderer.AddActor(gauss_text_actor)
gauss_renderer.AddActor(gauss_scalar_bar)
gauss_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)

# --- Mean viewport ---
source.GetPointData().SetActiveScalars("Mean_Curvature")
mean_scalar_range = source.GetPointData().GetScalars("Mean_Curvature").GetRange()

mean_mapper = vtkPolyDataMapper()
mean_mapper.SetInputData(source)
mean_mapper.SetScalarModeToUsePointFieldData()
mean_mapper.SelectColorArray("Mean_Curvature")
mean_mapper.SetScalarRange(mean_scalar_range)
mean_mapper.SetLookupTable(lut)

mean_actor = vtkActor()
mean_actor.SetMapper(mean_mapper)

mean_scalar_bar = vtkScalarBarActor()
mean_scalar_bar.SetLookupTable(mean_mapper.GetLookupTable())
mean_scalar_bar.SetTitle("Mean\nCurvature")
mean_scalar_bar.UnconstrainedFontSizeOn()
mean_scalar_bar.SetNumberOfLabels(5)
mean_scalar_bar.SetMaximumWidthInPixels(window_width // 8)
mean_scalar_bar.SetMaximumHeightInPixels(window_height // 3)
mean_scalar_bar.SetBarRatio(mean_scalar_bar.GetBarRatio() * 0.5)
mean_scalar_bar.SetPosition(0.85, 0.1)

mean_text_actor = vtkTextActor()
mean_text_actor.SetInput("Mean\nCurvature")
mean_text_actor.SetPosition(250, 16)
mean_text_actor.GetTextProperty().ShallowCopy(text_property)

mean_renderer = vtkRenderer()
mean_renderer.SetBackground(paraview_bkg_rgb)
mean_renderer.AddActor(mean_actor)
mean_renderer.AddActor(mean_text_actor)
mean_renderer.AddActor(mean_scalar_bar)
mean_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(gauss_renderer)
render_window.AddRenderer(mean_renderer)
render_window.SetWindowName("curvatures adjust edges")
render_window.SetMultiSamples(0)
render_window.SetSize(window_width, window_height)

# Scene: configure the camera
cam_orient = vtkCameraOrientationWidget()
cam_orient.SetParentRenderer(gauss_renderer)
cam_orient.On()
camera = gauss_renderer.GetActiveCamera()
camera.Elevation(60)
mean_renderer.SetActiveCamera(camera)
gauss_renderer.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
