#!/usr/bin/env python

# Cut a surface model using scalar-based contours.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
banana = (0.890, 0.812, 0.341)
flesh = (1.000, 0.490, 0.251)
burlywood = (0.871, 0.722, 0.529)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "Torso.vtp")
number_of_cuts = 20

# Reader: load the polygonal surface model
reader = vtkXMLPolyDataReader()
reader.SetFileName(file_name)
reader.Update()

bounds = reader.GetOutput().GetBounds()

# Implicit function: define a plane for scalar evaluation
plane = vtkPlane()
plane.SetOrigin(
    (bounds[1] + bounds[0]) / 2.0,
    (bounds[3] + bounds[2]) / 2.0,
    (bounds[5] + bounds[4]) / 2.0,
)
plane.SetNormal(0, 0, 1)

# Compute scalar distance from the plane for each point
scalars = vtkDoubleArray()
number_of_points = reader.GetOutput().GetNumberOfPoints()
scalars.SetNumberOfTuples(number_of_points)
pts = reader.GetOutput().GetPoints()
for i in range(number_of_points):
    point = pts.GetPoint(i)
    scalars.SetTuple1(i, plane.EvaluateFunction(point))
reader.GetOutput().GetPointData().SetScalars(scalars)

scalar_range = reader.GetOutput().GetPointData().GetScalars().GetRange()

# Filter: extract contour lines from the scalar field
cutter = vtkContourFilter()
cutter.SetInputConnection(reader.GetOutputPort())
cutter.ComputeScalarsOff()
cutter.ComputeNormalsOff()
cutter.GenerateValues(number_of_cuts, 0.99 * scalar_range[0], 0.99 * scalar_range[1])

# Mapper: map cut lines to graphics primitives
cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())
cutter_mapper.ScalarVisibilityOff()

# Actor: display the cut lines
cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(banana)
cutter_actor.GetProperty().SetLineWidth(2)

# Mapper: map the original model surface
model_mapper = vtkPolyDataMapper()
model_mapper.SetInputConnection(reader.GetOutputPort())
model_mapper.ScalarVisibilityOff()

# Actor: display the model surface
model_actor = vtkActor()
model_actor.SetMapper(model_mapper)
model_actor.GetProperty().SetColor(flesh)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cutter_actor)
renderer.AddActor(model_actor)
renderer.SetBackground(burlywood)
renderer.GetActiveCamera().SetPosition(0, -1, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CutWithScalars")
render_window.SetSize(600, 600)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
