#!/usr/bin/env python

# Display a poly data model as an orientation marker in the viewport corner.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
silver_rgb = (0.753, 0.753, 0.753)
slate_gray_rgb = (0.439, 0.502, 0.565)
wheat_rgb = (0.961, 0.871, 0.702)
carrot_rgb = (0.930, 0.569, 0.129)
white_rgb = (1.0, 1.0, 1.0)

# Data: read Bunny.vtp for the orientation marker icon
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "Bunny.vtp"

# Reader: load XML poly data for the icon
reader = vtkXMLPolyDataReader()
reader.SetFileName(str(file_path))

# Mapper: map the icon poly data
icon_mapper = vtkDataSetMapper()
icon_mapper.SetInputConnection(reader.GetOutputPort())

# Actor: the icon actor for the orientation marker
icon_actor = vtkActor()
icon_actor.SetMapper(icon_mapper)
icon_actor.GetProperty().SetColor(silver_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetWindowName("OrientationMarkerWidget1")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# OrientationMarkerWidget: display the bunny icon in the viewport corner
om_widget = vtkOrientationMarkerWidget()
om_widget.SetOrientationMarker(icon_actor)
om_widget.SetInteractor(render_window_interactor)
om_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
om_widget.SetOutlineColor(*wheat_rgb)
om_widget.SetEnabled(1)
om_widget.InteractiveOn()

# Source: generate a superquadric as the main scene object
superquadric_source = vtkSuperquadricSource()
superquadric_source.SetPhiRoundness(0.2)
superquadric_source.SetThetaRoundness(0.8)

# Mapper: map superquadric polygon data
superquadric_mapper = vtkPolyDataMapper()
superquadric_mapper.SetInputConnection(superquadric_source.GetOutputPort())

# Actor: assign the superquadric geometry
superquadric_actor = vtkActor()
superquadric_actor.SetMapper(superquadric_mapper)
superquadric_actor.GetProperty().SetInterpolationToFlat()
superquadric_actor.GetProperty().SetDiffuseColor(carrot_rgb)
superquadric_actor.GetProperty().SetSpecularColor(white_rgb)
superquadric_actor.GetProperty().SetDiffuse(0.6)
superquadric_actor.GetProperty().SetSpecular(0.5)
superquadric_actor.GetProperty().SetSpecularPower(5.0)

renderer.AddActor(superquadric_actor)
renderer.ResetCamera()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Initialize()
render_window_interactor.Start()
