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
    vtkActor2D,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
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

for curvature_type, curv_name in [("gaussian", "Gauss_Curvature"), ("mean", "Mean_Curvature")]:
    cc = vtkCurvatures()
    cc.SetInputData(source)
    if curvature_type == "gaussian":
        cc.SetCurvatureTypeToGaussian()
    else:
        cc.SetCurvatureTypeToMean()
    cc.Update()
    curv_output = cc.GetOutput()

    # Adjust edge curvatures
    curv_output.GetPointData().SetActiveScalars(curv_name)
    np_src = dsa.WrapDataObject(curv_output)
    curvatures_arr = np_src.PointData[curv_name]

    generate_ids = vtkGenerateIds()
    generate_ids.SetInputData(curv_output)
    generate_ids.SetPointIds(True)
    generate_ids.SetCellIds(False)
    generate_ids.SetPointIdsArrayName("ids")
    generate_ids.SetCellIdsArrayName("ids")
    generate_ids.Update()

    edges = vtkFeatureEdges()
    edges.SetInputConnection(generate_ids.GetOutputPort())
    edges.BoundaryEdgesOn()
    edges.ManifoldEdgesOff()
    edges.NonManifoldEdgesOff()
    edges.FeatureEdgesOff()
    edges.Update()

    edge_array = edges.GetOutput().GetPointData().GetArray("ids")
    boundary_ids = []
    for i in range(edges.GetOutput().GetNumberOfPoints()):
        boundary_ids.append(edge_array.GetValue(i))
    boundary_set = set(boundary_ids)

    for p_id in boundary_ids:
        cell_ids = vtkIdList()
        curv_output.GetPointCells(p_id, cell_ids)
        neighbours = set()
        for ci in range(cell_ids.GetNumberOfIds()):
            cell_point_ids = vtkIdList()
            curv_output.GetCellPoints(cell_ids.GetId(ci), cell_point_ids)
            for cpi in range(cell_point_ids.GetNumberOfIds()):
                neighbours.add(cell_point_ids.GetId(cpi))
        neighbours -= boundary_set
        curvs = np.array([curvatures_arr[n] for n in neighbours])
        dists = np.array([
            np.linalg.norm(
                np.array(curv_output.GetPoint(n)) - np.array(curv_output.GetPoint(p_id))
            )
            for n in neighbours
        ])
        curvs = curvs[dists > 0]
        dists = dists[dists > 0]
        if len(curvs) > 0:
            weights = 1.0 / dists
            weights /= weights.sum()
            curvatures_arr[p_id] = np.dot(curvs, weights)
        else:
            curvatures_arr[p_id] = 0.0

    curvatures_arr = np.where(np.abs(curvatures_arr) < epsilon, 0, curvatures_arr)
    curv_vtk = numpy_support.numpy_to_vtk(
        num_array=curvatures_arr.ravel(), deep=True, array_type=VTK_DOUBLE
    )
    curv_vtk.SetName(curv_name)
    curv_output.GetPointData().RemoveArray(curv_name)
    curv_output.GetPointData().AddArray(curv_vtk)
    curv_output.GetPointData().SetActiveScalars(curv_name)

    source.GetPointData().AddArray(
        curv_output.GetPointData().GetAbstractArray(curv_name)
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

render_window = vtkRenderWindow()
render_window.SetSize(window_width, window_height)
render_window.SetWindowName("CurvaturesAdjustEdges")

render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

cam_orient = vtkCameraOrientationWidget()

camera = None
curvature_names = ["Gauss_Curvature", "Mean_Curvature"]
viewports = [(0.0, 0.0, 0.5, 1.0), (0.5, 0.0, 1.0, 1.0)]

for idx, curv_name in enumerate(curvature_names):
    source.GetPointData().SetActiveScalars(curv_name)
    scalar_range = source.GetPointData().GetScalars(curv_name).GetRange()

    mapper = vtkPolyDataMapper()
    mapper.SetInputData(source)
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SelectColorArray(curv_name)
    mapper.SetScalarRange(scalar_range)
    mapper.SetLookupTable(lut)

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())
    scalar_bar.SetTitle(curv_name.replace("_", "\n"))
    scalar_bar.UnconstrainedFontSizeOn()
    scalar_bar.SetNumberOfLabels(5)
    scalar_bar.SetMaximumWidthInPixels(window_width // 8)
    scalar_bar.SetMaximumHeightInPixels(window_height // 3)
    scalar_bar.SetBarRatio(scalar_bar.GetBarRatio() * 0.5)
    scalar_bar.SetPosition(0.85, 0.1)

    text_mapper = vtkTextMapper()
    text_mapper.SetInput(curv_name.replace("_", "\n"))
    text_mapper.SetTextProperty(text_property)

    text_actor = vtkActor2D()
    text_actor.SetMapper(text_mapper)
    text_actor.SetPosition(250, 16)

    renderer = vtkRenderer()
    renderer.SetBackground(paraview_bkg_rgb)
    renderer.AddActor(actor)
    renderer.AddActor(text_actor)
    renderer.AddActor(scalar_bar)
    renderer.SetViewport(viewports[idx])

    if idx == 0:
        cam_orient.SetParentRenderer(renderer)
        camera = renderer.GetActiveCamera()
        camera.Elevation(60)
    else:
        renderer.SetActiveCamera(camera)

    renderer.ResetCamera()
    render_window.AddRenderer(renderer)

cam_orient.On()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
