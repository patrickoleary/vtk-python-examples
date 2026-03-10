#!/usr/bin/env python

# Read GPS track points from a CSV file using vtkDelimitedTextReader,
# build a vtkPolyData point cloud from the table columns, render it
# colored by elevation, and write three selected columns back to a
# new CSV file using Python's csv module.

import csv
import os
import tempfile
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkIOInfovis import vtkDelimitedTextReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Output path: write to a temporary file
csv_out_path = os.path.join(tempfile.gettempdir(), "WriteCSV_output.csv")

# Reader: load GPS track data from CSV
reader = vtkDelimitedTextReader()
reader.SetFileName(str(data_dir / "LakeGininderra.csv"))
reader.DetectNumericColumnsOn()
reader.SetFieldDelimiterCharacters(",")
reader.SetHaveHeaders(True)
reader.Update()

# Extract columns from the table
table = reader.GetOutput()
n_rows = table.GetNumberOfRows()
easting = table.GetColumnByName("Easting(m)")
northing = table.GetColumnByName("Northing(m)")
elevation = table.GetColumnByName("Elevation(m)")

# Writer: write selected columns back to a new CSV file
with open(csv_out_path, "w", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Easting(m)", "Northing(m)", "Elevation(m)"])
    for i in range(n_rows):
        csv_writer.writerow([easting.GetValue(i), northing.GetValue(i), elevation.GetValue(i)])
print(f"Wrote: {csv_out_path}")

points = vtkPoints()
points.SetNumberOfPoints(n_rows)
scalars = vtkFloatArray()
scalars.SetName("Elevation(m)")
scalars.SetNumberOfTuples(n_rows)

for i in range(n_rows):
    points.SetPoint(i, easting.GetValue(i), northing.GetValue(i), elevation.GetValue(i))
    scalars.SetValue(i, elevation.GetValue(i))

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().SetScalars(scalars)

# Create vertex cells so the points are visible
verts = vtkCellArray()
for i in range(n_rows):
    verts.InsertNextCell(1)
    verts.InsertCellPoint(i)
polydata.SetVerts(verts)

# Mapper: map point data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetScalarRange(scalars.GetRange())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(4.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1024, 768)
render_window.SetWindowName("WriteCSV")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
