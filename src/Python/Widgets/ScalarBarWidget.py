#!/usr/bin/env python

# Display a scalar bar widget showing a color lookup table for an unstructured grid.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Data: read uGridEx.vtk
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "uGridEx.vtk"

# Lookup table: custom color map
lut = vtkLookupTable()
lut.Build()

# Reader: load legacy unstructured grid data
reader = vtkUnstructuredGridReader()
reader.SetFileName(str(file_path))
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetScalarRange()

# Mapper: map unstructured grid data to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(output)
mapper.SetScalarRange(scalar_range)
mapper.SetLookupTable(lut)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("ScalarBarWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# ScalarBarWidget: interactive scalar bar overlay
scalar_bar = vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(lut)

scalar_bar_widget = vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(render_window_interactor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()

# Camera: set a good viewing angle
render_window_interactor.Initialize()
render_window.Render()
renderer.GetActiveCamera().SetPosition(-6.4, 10.3, 1.4)
renderer.GetActiveCamera().SetFocalPoint(1.0, 0.5, 3.0)
renderer.GetActiveCamera().SetViewUp(0.6, 0.4, -0.7)
render_window.Render()

# Launch the interactive visualization
render_window_interactor.Start()
