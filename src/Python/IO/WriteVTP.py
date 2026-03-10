#!/usr/bin/env python

# Read GPS track points from a CSV file, build a vtkPolyData point
# cloud, write it to a VTP file using vtkXMLPolyDataWriter, read it
# back, and render the result colored by elevation.

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
from vtkmodules.vtkIOXML import (
    vtkXMLPolyDataReader,
    vtkXMLPolyDataWriter,
)
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
vtp_path = os.path.join(tempfile.gettempdir(), "WriteVTP_output.vtp")

# Reader: load GPS track data from CSV
csv_reader = vtkDelimitedTextReader()
csv_reader.SetFileName(str(data_dir / "LakeGininderra.csv"))
csv_reader.DetectNumericColumnsOn()
csv_reader.SetFieldDelimiterCharacters(",")
csv_reader.SetHaveHeaders(True)
csv_reader.Update()

# Build polydata from table columns
table = csv_reader.GetOutput()
n_rows = table.GetNumberOfRows()
easting = table.GetColumnByName("Easting(m)")
northing = table.GetColumnByName("Northing(m)")
elevation = table.GetColumnByName("Elevation(m)")

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

# Writer: save polydata to a VTP file
vtp_writer = vtkXMLPolyDataWriter()
vtp_writer.SetFileName(vtp_path)
vtp_writer.SetInputData(polydata)
vtp_writer.Write()
print(f"Wrote: {vtp_path}")

# Reader: read back the written VTP file for verification
vtp_reader = vtkXMLPolyDataReader()
vtp_reader.SetFileName(vtp_path)
vtp_reader.Update()

# Mapper: map point data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(vtp_reader.GetOutputPort())
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
render_window.SetWindowName("WriteVTP")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
