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
panels = []
for i in range(4):
    cc = vtkCurvatures()
    if i < 2:
        cc.SetInputConnection(cleaner.GetOutputPort())
    else:
        cc.SetInputConnection(rh_fn_src.GetOutputPort())
    if i % 2 == 0:
        cc.SetCurvatureTypeToGaussian()
        curv_name = "Gauss_Curvature"
    else:
        cc.SetCurvatureTypeToMean()
        curv_name = "Mean_Curvature"
    cc.Update()
    curv_output = cc.GetOutput()

    # Adjust edge curvatures inline
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
    for bi in range(edges.GetOutput().GetNumberOfPoints()):
        boundary_ids.append(edge_array.GetValue(bi))
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

    panels.append((curv_output, curv_name))

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

render_window = vtkRenderWindow()
render_window.SetSize(window_width, window_height)
render_window.SetWindowName("CurvaturesApp")

# Viewport layout: row 0 = top (torus), row 1 = bottom (hills)
# col 0 = left (Gauss), col 1 = right (Mean)
for row in range(2):
    for col in range(2):
        idx = row * 2 + col
        panel_source, panel_curv_name = panels[idx]

        panel_source.GetPointData().SetActiveScalars(panel_curv_name)
        scalar_range = panel_source.GetPointData().GetScalars(panel_curv_name).GetRange()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(panel_source)
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SelectColorArray(panel_curv_name)
        mapper.SetScalarRange(scalar_range)
        mapper.SetLookupTable(lut)

        actor = vtkActor()
        actor.SetMapper(mapper)

        curv_title = panel_curv_name.replace("_", "\n")

        scalar_bar = vtkScalarBarActor()
        scalar_bar.SetLookupTable(mapper.GetLookupTable())
        scalar_bar.SetTitle(curv_title)
        scalar_bar.UnconstrainedFontSizeOn()
        scalar_bar.SetNumberOfLabels(5)
        scalar_bar.SetMaximumWidthInPixels(window_width // 8)
        scalar_bar.SetMaximumHeightInPixels(window_height // 3)
        scalar_bar.SetBarRatio(scalar_bar.GetBarRatio() * 0.5)
        scalar_bar.SetPosition(0.85, 0.1)

        text_mapper = vtkTextMapper()
        text_mapper.SetInput(curv_title)
        text_mapper.SetTextProperty(text_property)

        text_actor = vtkActor2D()
        text_actor.SetMapper(text_mapper)
        text_actor.SetPosition(250, 16)

        xmin = float(col) / 2
        xmax = float(col + 1) / 2
        ymin = float(1 - row) / 2
        ymax = float(2 - row) / 2

        renderer = vtkRenderer()
        renderer.SetViewport(xmin, ymin, xmax, ymax)
        renderer.SetBackground(slate_gray_rgb)
        renderer.AddActor(actor)
        renderer.AddActor(text_actor)
        renderer.AddActor(scalar_bar)

        render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
