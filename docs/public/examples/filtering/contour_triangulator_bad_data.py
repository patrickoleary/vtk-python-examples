#!/usr/bin/env python

# Demonstrate vtkContourTriangulator handling bad data gracefully by
# reading a VTK dataset with problematic contours and verifying the
# triangulator terminates without infinite recursion.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read bad contour data
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "TriangulatorBadData.vtk"))
reader.Update()

# Triangulate the bad data (should terminate without infinite loop)
triangulator = vtkContourTriangulator()
triangulator.SetInputConnection(reader.GetOutputPort())
triangulator.Update()

# Display the triangulation result
contour_mapper = vtkDataSetMapper()
contour_mapper.SetInputConnection(triangulator.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(contour_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contour triangulator bad data")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-90)

interactor.Initialize()
interactor.Start()
