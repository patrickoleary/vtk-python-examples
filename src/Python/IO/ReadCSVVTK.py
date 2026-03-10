#!/usr/bin/env python

# Read ECEF coordinates from a CSV file using vtkDelimitedTextReader and
# overlay the original track (black) with a centroid-translated and rotated
# version (diverging color map) in a single renderer. The centroid translation
# brings the data to the origin so the ECEF-to-local rotation is visible.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import csv
import os
from pathlib import Path

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyLine,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import (
    vtkTableToPolyData,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkIOInfovis import vtkDelimitedTextReader
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
paraview_bkg_rgb = (0.322, 0.341, 0.431)
black_rgb = (0.0, 0.0, 0.0)

# Data file: set VPE_DATA_DIR env var to override, otherwise look next to this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "LakeGininderra.csv")

# Compute the latitude mid-point for the ECEF rotation.
# We need this before building the VTK pipeline.
latitudes = []
with open(file_name, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            latitudes.append(float(row["Latitude"]))
        except (ValueError, KeyError):
            continue
lat_mid_pt = (min(latitudes) + max(latitudes)) / 2.0

# Reader: use vtkDelimitedTextReader to read the CSV directly into a vtkTable
points_reader = vtkDelimitedTextReader()
points_reader.SetFileName(file_name)
points_reader.DetectNumericColumnsOn()
points_reader.SetFieldDelimiterCharacters(",")
points_reader.SetHaveHeaders(True)

# TableToPolyData: convert the table into polydata using ECEF columns
table_to_poly = vtkTableToPolyData()
table_to_poly.SetInputConnection(points_reader.GetOutputPort())
table_to_poly.SetXColumn("X(m)")
table_to_poly.SetYColumn("Y(m)")
table_to_poly.SetZColumn("Z(m)")
table_to_poly.Update()

# Set elevation as the active scalar for coloring
poly_data = table_to_poly.GetOutput()
poly_data.GetPointData().SetActiveScalars("Elevation(m)")
elev_range = poly_data.GetPointData().GetScalars().GetRange()

# PolyLine: connect all points in order
num_pts = poly_data.GetNumberOfPoints()
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(num_pts)
for i in range(num_pts):
    poly_line.GetPointIds().SetId(i, i)

cells = vtkCellArray()
cells.InsertNextCell(poly_line)
poly_data.SetLines(cells)
poly_data.Modified()

# Compute the centroid of the ECEF points so we can translate to the origin
# before rotating. Without this step, the rotation pivots around the Earth
# center (~6.3 million meters away) and has no visible effect on the track.
bounds = poly_data.GetBounds()
centroid_x = (bounds[0] + bounds[1]) / 2.0
centroid_y = (bounds[2] + bounds[3]) / 2.0
centroid_z = (bounds[4] + bounds[5]) / 2.0

# Original transform: translate to origin only (no rotation)
translate_only = vtkTransform()
translate_only.Translate(-centroid_x, -centroid_y, -centroid_z)

original_filter = vtkTransformPolyDataFilter()
original_filter.SetInputData(poly_data)
original_filter.SetTransform(translate_only)
original_filter.Update()

# Rotated transform: translate to origin, then rotate ECEF → local
# (vtkTransform applies operations in reverse order, so Translate is applied
# first, then RotateZ, then RotateX)
rotate_transform = vtkTransform()
rotate_transform.RotateX(-(90.0 - lat_mid_pt))
rotate_transform.RotateZ(90.0 - lat_mid_pt)
rotate_transform.Translate(-centroid_x, -centroid_y, -centroid_z)

rotated_filter = vtkTransformPolyDataFilter()
rotated_filter.SetInputData(poly_data)
rotated_filter.SetTransform(rotate_transform)
rotated_filter.Update()

# Diverging lookup table: cool (blue) → white → warm (red)
# See: Diverging Color Maps for Scientific Visualization (Kenneth Moreland)
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.230, 0.299, 0.754)
ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(1.0, 0.706, 0.016, 0.150)

table_size = 256
lut = vtkLookupTable()
lut.SetTableRange(elev_range)
lut.SetNumberOfTableValues(table_size)
lut.Build()
for i in range(table_size):
    rgb = ctf.GetColor(float(i) / table_size)
    lut.SetTableValue(i, rgb[0], rgb[1], rgb[2], 1.0)

# Original actor: centroid-translated only, black, no scalar coloring
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(original_filter.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(black_rgb)
original_actor.GetProperty().SetLineWidth(2)

# Rotated actor: centroid-translated + rotated, diverging LUT
rotated_mapper = vtkPolyDataMapper()
rotated_mapper.SetInputConnection(rotated_filter.GetOutputPort())
rotated_mapper.SetScalarRange(elev_range)
rotated_mapper.SetLookupTable(lut)
rotated_mapper.ScalarVisibilityOn()

rotated_actor = vtkActor()
rotated_actor.SetMapper(rotated_mapper)
rotated_actor.GetProperty().SetLineWidth(2)

# Scalar bar: display the elevation color legend
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Elevation (m)")
scalar_bar.UnconstrainedFontSizeOff()
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetMaximumWidthInPixels(128)
scalar_bar.SetMaximumHeightInPixels(400)
scalar_bar.SetPosition(0.87, 0.1)

# Renderer: both actors overlaid in one scene
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(rotated_actor)
renderer.AddActor(scalar_bar)
renderer.SetBackground(paraview_bkg_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1024, 768)
render_window.SetWindowName("ReadCSVVTK")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
