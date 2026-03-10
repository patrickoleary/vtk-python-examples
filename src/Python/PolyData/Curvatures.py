#!/usr/bin/env python

# Compute Mean curvature on a cowHead mesh, adjust edge curvatures, and
# display the result with a color-mapped scalar bar.

import os
from pathlib import Path

import numpy as np
from vtk.util import numpy_support

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import (
    VTK_DOUBLE,
    vtkIdList,
)
from vtkmodules.vtkFiltersCore import (
    vtkFeatureEdges,
    vtkGenerateIds,
)
from vtkmodules.vtkFiltersGeneral import vtkCurvatures
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
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
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
cow_head_file = str(data_dir / "cowHead.vtp")

curvature_name = "Mean_Curvature"

# Reader: load cowHead mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(cow_head_file)
reader.Update()
source = reader.GetOutput()

# Filter: compute Mean curvature
curvatures_filter = vtkCurvatures()
curvatures_filter.SetInputData(source)
curvatures_filter.SetCurvatureTypeToMean()
curvatures_filter.Update()
curv_output = curvatures_filter.GetOutput()

# --- Adjust edge curvatures (inline) ---
epsilon = 1.0e-08
curv_output.GetPointData().SetActiveScalars(curvature_name)
np_source = dsa.WrapDataObject(curv_output)
curvatures_array = np_source.PointData[curvature_name]

# Find boundary point IDs
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

# Replace boundary curvatures with distance-weighted average of interior neighbors
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
    curvs = np.array([curvatures_array[n] for n in neighbours])
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
        curvatures_array[p_id] = np.dot(curvs, weights)
    else:
        curvatures_array[p_id] = 0.0

# Zero out tiny values
curvatures_array = np.where(np.abs(curvatures_array) < epsilon, 0, curvatures_array)
curv_vtk = numpy_support.numpy_to_vtk(
    num_array=curvatures_array.ravel(), deep=True, array_type=VTK_DOUBLE
)
curv_vtk.SetName(curvature_name)
curv_output.GetPointData().RemoveArray(curvature_name)
curv_output.GetPointData().AddArray(curv_vtk)
curv_output.GetPointData().SetActiveScalars(curvature_name)

# Copy adjusted curvature back to source
source.GetPointData().AddArray(curv_output.GetPointData().GetAbstractArray(curvature_name))
scalar_range = source.GetPointData().GetScalars(curvature_name).GetRange()

# Lookup table from a color series
color_series = vtkColorSeries()
color_series.SetColorScheme(16)

lut = vtkColorTransferFunction()
lut.SetColorSpaceToHSV()
num_colors = color_series.GetNumberOfColors()
for i in range(num_colors):
    color = color_series.GetColor(i)
    r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
    t = scalar_range[0] + (scalar_range[1] - scalar_range[0]) / (num_colors - 1) * i
    lut.AddRGBPoint(t, r, g, b)

# Mapper & Actor: map curvature-coloured surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(source)
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray(curvature_name)
mapper.SetScalarRange(scalar_range)
mapper.SetLookupTable(lut)

actor = vtkActor()
actor.SetMapper(mapper)

# Scalar bar
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(mapper.GetLookupTable())
scalar_bar.SetTitle(curvature_name.replace("_", "\n"))
scalar_bar.UnconstrainedFontSizeOn()
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetMaximumWidthInPixels(100)
scalar_bar.SetMaximumHeightInPixels(260)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(scalar_bar)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)
render_window.SetWindowName("Curvatures")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Camera orientation widget
cam_orient = vtkCameraOrientationWidget()
cam_orient.SetParentRenderer(renderer)
cam_orient.On()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
