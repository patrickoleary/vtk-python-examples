#!/usr/bin/env python

# Demonstrate vtkAnimateModes by reading an Exodus dataset, selecting a
# mode shape, and rendering the displaced surface at a particular time step.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersGeneral import vtkAnimateModes
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOIOSS import vtkIOSSReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Exodus dataset
reader = vtkIOSSReader()
reader.AddFileName(os.path.join(data_dir, "Exodus", "can.e.4", "can.e.4.0"))
reader.ApplyDisplacementsOn()
reader.UpdateInformation()
reader.GetNodeBlockFieldSelection().EnableAllArrays()

# Animate modes
mode_shapes = vtkAnimateModes()
mode_shapes.SetInputConnection(reader.GetOutputPort())
mode_shapes.UpdateInformation()
mode_shapes.SetModeShape(11)
mode_shapes.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "DISPL"
)
mode_shapes.DisplacementPreappliedOn()
mode_shapes.SetDisplacementMagnitude(2.0)
mode_shapes.AnimateVibrationsOn()
mode_shapes.UpdateInformation()
mode_shapes.UpdateTimeStep(0.5)

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputDataObject(mode_shapes.GetOutputDataObject(0))

# Mapper and actor
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("animate modes")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(10.0, 10.0, 5.0)
camera.SetViewUp(0.0, 0.4, 1.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
