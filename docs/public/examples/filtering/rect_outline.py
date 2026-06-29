#!/usr/bin/env python

# Demonstrate vtkRectilinearGridOutlineFilter on a rectilinear grid
# read from an XML file, rendering piece 1 of 2.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersParallel import vtkRectilinearGridOutlineFilter
from vtkmodules.vtkIOXML import vtkXMLRectilinearGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read rectilinear grid
reader = vtkXMLRectilinearGridReader()
reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtr"))

# Outline filter
outline = vtkRectilinearGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_mapper.SetNumberOfPieces(2)
outline_mapper.SetPiece(1)

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("rect outline")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.76213, 10.712)
camera.SetFocalPoint(-0.0842503, -0.136905, 0.610234)
camera.SetPosition(2.53813, 2.2678, -5.22172)
camera.SetViewUp(-0.241047, 0.930635, 0.275343)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
