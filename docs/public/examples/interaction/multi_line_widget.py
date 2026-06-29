#!/usr/bin/env python
# Demonstrate vtkMultiLineWidget with directional line representation.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkMultiLineRepresentation, vtkMultiLineWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
sphere = vtkSphereSource()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multi line widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
multi_line_rep = vtkMultiLineRepresentation()
multi_line_rep.GetEndPointProperty().SetColor(1, 0, 1)
multi_line_rep.GetEndPoint2Property().SetColor(1, 0, 1)
multi_line_rep.GetLineProperty().SetColor(1, 1, 0)
multi_line_rep.SetDirectionalLine(True)

multi_line_widget = vtkMultiLineWidget()
multi_line_widget.CreateDefaultRepresentation()
multi_line_widget.SetInteractor(interactor)
multi_line_widget.SetRepresentation(multi_line_rep)
multi_line_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
