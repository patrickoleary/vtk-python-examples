#!/usr/bin/env python

# Read UTM coordinates from a CSV file using pandas and numpy, build a
# polyline colored by elevation, and render it with a simple lookup table.
# This example demonstrates interoperability between pandas, numpy, and VTK.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import os
from pathlib import Path

import numpy as np
import pandas as pd
from vtk.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAxesActor,
    vtkScalarBarActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
paraview_bkg_rgb = (0.322, 0.341, 0.431)
carrot_rgb = (0.933, 0.569, 0.129)

# Data file: set VPE_DATA_DIR env var to override, otherwise look next to this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "LakeGininderra.csv")

# Read the CSV with pandas and select UTM columns
df = pd.read_csv(file_name)
df = df[["Easting(m)", "Northing(m)", "Elevation(m)"]].dropna()

# Extract numpy arrays for coordinates and elevation
xyz = df[["Easting(m)", "Northing(m)", "Elevation(m)"]].to_numpy(dtype=np.float64)
elevation = df["Elevation(m)"].to_numpy(dtype=np.float64)

num_pts = len(xyz)

# Points: convert the numpy XYZ array directly into vtkPoints
vtk_points_array = numpy_to_vtk(xyz, deep=True)
points = vtkPoints()
points.SetData(vtk_points_array)

# Scalars: convert the elevation numpy array into a VTK array for coloring
elevation_vtk = numpy_to_vtk(elevation, deep=True)
elevation_vtk.SetName("Elevation(m)")

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
poly_data.GetPointData().SetScalars(elevation_vtk)
poly_data.SetLines(cells)

# Lookup table: simple hue ramp from blue (low) to red (high)
elev_range = elevation_vtk.GetRange()
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
render_window.SetWindowName("ReadCSVPandas")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Orientation marker: labeled axes in the lower-left corner
axes_actor = vtkAxesActor()
axes_actor.SetXAxisLabelText("East")
axes_actor.SetYAxisLabelText("North")
axes_actor.SetZAxisLabelText("Zenith")

orientation_widget = vtkOrientationMarkerWidget()
orientation_widget.SetOutlineColor(carrot_rgb[0], carrot_rgb[1], carrot_rgb[2])
orientation_widget.SetOrientationMarker(axes_actor)
orientation_widget.SetInteractor(render_window_interactor)
orientation_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
orientation_widget.EnabledOn()
orientation_widget.InteractiveOn()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
