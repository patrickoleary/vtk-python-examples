#!/usr/bin/env python

# Read a .slc volume file, extract an isosurface with marching cubes,
# and render it with specular lighting.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load SLC volume data from file
reader = vtkSLCReader()
reader.SetFileName(str(data_dir / "vw_knee.slc"))
reader.Update()

# Contour filter: extract an isosurface at value 72 using marching cubes
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(reader.GetOutputPort())
contour_filter.SetValue(0, 72.0)

# Mapper: map the isosurface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour_filter.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry with specular lighting
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.GetProperty().SetDiffuse(0.8)
actor.GetProperty().SetSpecular(0.8)
actor.GetProperty().SetSpecularPower(120.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.GetActiveCamera().SetPosition(0.0, -1.0, 0.0)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, -1.0)
renderer.GetActiveCamera().Azimuth(-90.0)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 512)
render_window.SetWindowName("ReadSLC")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
