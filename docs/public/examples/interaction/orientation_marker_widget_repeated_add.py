#!/usr/bin/env python
# Demonstrate vtkOrientationMarkerWidget with repeated add/remove cycle.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
axes = vtkAxesActor()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("orientation marker widget repeated add")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget: first widget (add then remove)
widget_1 = vtkOrientationMarkerWidget()
widget_1.SetOrientationMarker(axes)
widget_1.SetInteractor(interactor)
widget_1.SetViewport(0, 0, 0.2, 0.2)
widget_1.EnabledOn()
widget_1.InteractiveOn()
widget_1.EnabledOff()

print("After first widget removed")

# Widget: second widget (add and keep)
widget_2 = vtkOrientationMarkerWidget()
widget_2.SetOrientationMarker(axes)
widget_2.SetInteractor(interactor)
widget_2.SetViewport(0, 0, 0.2, 0.2)
widget_2.EnabledOn()
widget_2.InteractiveOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
print("After second widget removed")
