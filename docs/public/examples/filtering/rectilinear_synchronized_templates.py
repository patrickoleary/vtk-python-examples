#!/usr/bin/env python

# Contour a rectilinear grid using vtkRectilinearSynchronizedTemplates.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkRectilinearSynchronizedTemplates
from vtkmodules.vtkIOLegacy import vtkRectilinearGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load rectilinear grid
reader = vtkRectilinearGridReader()
reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
reader.Update()

# Contour
contour = vtkRectilinearSynchronizedTemplates()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0, 1)
contour.ComputeScalarsOff()
contour.ComputeNormalsOn()
contour.ComputeGradientsOn()

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(contour_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("rectilinear synchronized templates")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
