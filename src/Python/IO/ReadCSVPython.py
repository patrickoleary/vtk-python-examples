#!/usr/bin/env python

# Read UTM coordinates from a CSV file, build a polyline colored by
# elevation, and render it with a simple hue-based lookup table.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import csv
import os
from pathlib import Path

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkInteractionWidgets import vtkCameraOrientationWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
paraview_bkg_rgb = (0.322, 0.341, 0.431)

# Data file: set VPE_DATA_DIR env var to override, otherwise look next to this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "LakeGininderra.csv")

# CSV column indices for UTM coordinates and elevation
EASTING_COL = "Easting(m)"
NORTHING_COL = "Northing(m)"
ELEVATION_COL = "Elevation(m)"

# Read the CSV file and extract UTM coordinates + elevation
eastings = []
northings = []
elevations = []

with open(file_name, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            e = float(row[EASTING_COL])
            n = float(row[NORTHING_COL])
            el = float(row[ELEVATION_COL])
        except (ValueError, KeyError):
            continue
        eastings.append(e)
        northings.append(n)
        elevations.append(el)

num_pts = len(eastings)

# Points: insert UTM coordinates as XYZ (Easting=X, Northing=Y, Elevation=Z)
points = vtkPoints()
for i in range(num_pts):
    points.InsertNextPoint(eastings[i], northings[i], elevations[i])

# Scalars: elevation values for coloring
elevation_scalars = vtkFloatArray()
elevation_scalars.SetName("Elevation(m)")
elevation_scalars.SetNumberOfTuples(num_pts)
for i in range(num_pts):
    elevation_scalars.SetValue(i, elevations[i])

# PolyLine: connect all points in order
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(num_pts)
for i in range(num_pts):
    poly_line.GetPointIds().SetId(i, i)

cells = vtkCellArray()
cells.InsertNextCell(poly_line)

# PolyData: assemble points, scalars, and line cells
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.GetPointData().SetScalars(elevation_scalars)
poly_data.SetLines(cells)

# Lookup table: simple hue ramp from blue (low) to red (high)
elev_range = elevation_scalars.GetRange()
lut = vtkLookupTable()
lut.SetTableRange(elev_range)
lut.SetHueRange(0.667, 0.0)
lut.Build()

# Mapper: map polydata to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)
mapper.SetScalarRange(elev_range)
mapper.SetLookupTable(lut)
mapper.ScalarVisibilityOn()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Scalar bar: display the elevation color legend
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Elevation (m)")
scalar_bar.UnconstrainedFontSizeOff()
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetMaximumWidthInPixels(128)
scalar_bar.SetMaximumHeightInPixels(400)
scalar_bar.SetPosition(0.87, 0.1)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(scalar_bar)
renderer.SetBackground(paraview_bkg_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1024, 768)
render_window.SetWindowName("ReadCSVPython")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Camera orientation widget: interactive gizmo in the corner
cam_orient_widget = vtkCameraOrientationWidget()
cam_orient_widget.SetParentRenderer(renderer)
cam_orient_widget.On()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
