#!/usr/bin/env python
# Demonstrate vtkSession-based serialization pipeline with contour filter on analytic source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Analytic source.
source = vtkRTAnalyticSource()

# Contour filter.
contour = vtkContourFilter()
contour.SetInputConnection(source.GetOutputPort())
contour.GenerateValues(15, 0, 255)

# Mapper.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.SetScalarRange(0, 255)

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("session")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
