#!/usr/bin/env python
# Demonstrate vtkProgressBarWidget with two progress bars showing different configurations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import (
    vtkProgressBarRepresentation,
    vtkProgressBarWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("progress bar widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget 1: 60% progress, green bar with background
progress_rep = vtkProgressBarRepresentation()
progress_rep.SetProgressRate(0.6)
progress_rep.SetPosition(0.1, 0.3)
progress_rep.SetPosition2(0.8, 0.1)
progress_rep.SetProgressBarColor(0, 1, 0)
progress_rep.SetBackgroundColor(1, 1, 1)
progress_rep.SetDrawBackground(True)

progress_widget = vtkProgressBarWidget()
progress_widget.SetInteractor(interactor)
progress_widget.SetRepresentation(progress_rep)
progress_widget.On()

# Widget 2: 30% progress, red bar, no background
progress_rep_2 = vtkProgressBarRepresentation()
progress_rep_2.SetProgressRate(0.3)
progress_rep_2.SetPosition(0.1, 0.5)
progress_rep_2.SetPosition2(0.8, 0.1)
progress_rep_2.SetProgressBarColor(1, 0, 0)
progress_rep_2.SetDrawBackground(False)

progress_widget_2 = vtkProgressBarWidget()
progress_widget_2.SetInteractor(interactor)
progress_widget_2.SetRepresentation(progress_rep_2)
progress_widget_2.On()

interactor.Initialize()
interactor.Start()
