#!/usr/bin/env python

# Blow-molding simulation showing ten time steps of parison deformation.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkConnectivityFilter,
    vtkContourFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
ivory_black = (0.161, 0.141, 0.129)
alice_blue = (0.941, 0.973, 1.000)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "blow.vtk")

# Lookup table: color the parison by thickness
lut = vtkLookupTable()
lut.SetHueRange(0.0, 0.66667)

# Grid layout: 2 columns x 5 rows = 10 frames
grid_cols = 2
grid_rows = 5
renderer_size_x = 750
renderer_size_y = 400
scale = 0.5

renderers = []
for i in range(10):
    thickness_name = "thickness" + str(i)
    displacement_name = "displacement" + str(i)

    # ---- Reader: load data with per-frame scalars and vectors ----
    reader = vtkDataSetReader()
    reader.SetFileName(file_name)
    reader.SetScalarsName(thickness_name)
    reader.SetVectorsName(displacement_name)
    reader.Update()

    # ---- Filter: warp the mesh by displacement vectors ----
    warp = vtkWarpVector()
    warp.SetInputData(reader.GetUnstructuredGridOutput())

    # ---- Filter: extract the mold (regions 0 and 1) ----
    mold_connect = vtkConnectivityFilter()
    mold_connect.SetInputConnection(warp.GetOutputPort())
    mold_connect.SetExtractionModeToSpecifiedRegions()
    mold_connect.AddSpecifiedRegion(0)
    mold_connect.AddSpecifiedRegion(1)

    mold_geom = vtkGeometryFilter()
    mold_geom.SetInputConnection(mold_connect.GetOutputPort())

    mold_mapper = vtkDataSetMapper()
    mold_mapper.SetInputConnection(mold_geom.GetOutputPort())
    mold_mapper.ScalarVisibilityOff()

    mold_actor = vtkActor()
    mold_actor.SetMapper(mold_mapper)
    mold_actor.GetProperty().SetColor(ivory_black)
    mold_actor.GetProperty().SetRepresentationToWireframe()

    # ---- Filter: extract the parison (region 2) ----
    parison_connect = vtkConnectivityFilter()
    parison_connect.SetInputConnection(warp.GetOutputPort())
    parison_connect.SetExtractionModeToSpecifiedRegions()
    parison_connect.AddSpecifiedRegion(2)

    parison_geom = vtkGeometryFilter()
    parison_geom.SetInputConnection(parison_connect.GetOutputPort())

    parison_normals = vtkPolyDataNormals()
    parison_normals.SetInputConnection(parison_geom.GetOutputPort())
    parison_normals.SetFeatureAngle(60)

    parison_mapper = vtkPolyDataMapper()
    parison_mapper.SetInputConnection(parison_normals.GetOutputPort())
    parison_mapper.SetLookupTable(lut)
    parison_mapper.SetScalarRange(0.12, 1.0)

    parison_actor = vtkActor()
    parison_actor.SetMapper(parison_mapper)

    # ---- Filter: thickness contour at 0.5 ----
    contour = vtkContourFilter()
    contour.SetInputConnection(parison_connect.GetOutputPort())
    contour.SetValue(0, 0.5)

    contour_mapper = vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contour.GetOutputPort())

    contour_actor = vtkActor()
    contour_actor.SetMapper(contour_mapper)

    # ---- Renderer: assemble one frame ----
    ren = vtkRenderer()
    ren.AddActor(mold_actor)
    ren.AddActor(parison_actor)
    ren.AddActor(contour_actor)
    ren.SetBackground(alice_blue)
    ren.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
    ren.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
    ren.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
    ren.GetActiveCamera().SetClippingRange(36.640827, 78.614680)

    row = i // grid_cols
    col = i % grid_cols
    x0 = col / grid_cols
    y0 = (grid_rows - row - 1) / grid_rows
    x1 = (col + 1) / grid_cols
    y1 = (grid_rows - row) / grid_rows
    ren.SetViewport(x0, y0, x1, y1)
    renderers.append(ren)

# Window: display all ten frames in a 2x5 grid
render_window = vtkRenderWindow()
for ren in renderers:
    render_window.AddRenderer(ren)
render_window.SetWindowName("Blow")
render_window.SetSize(
    int(renderer_size_x * grid_cols * scale),
    int(renderer_size_y * grid_rows * scale),
)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
