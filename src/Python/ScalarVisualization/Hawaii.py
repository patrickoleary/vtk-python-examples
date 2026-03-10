#!/usr/bin/env python

# Color-mapped elevation of the Hawaii coastline using a Brewer palette.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bkg_color = (0.102, 0.200, 0.400)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "honolulu.vtk")

# Reader: load the Hawaii elevation data
hawaii = vtkPolyDataReader()
hawaii.SetFileName(file_name)
hawaii.Update()

# Filter: compute elevation scalars
elevation = vtkElevationFilter()
elevation.SetInputConnection(hawaii.GetOutputPort())
elevation.SetLowPoint(0, 0, 0)
elevation.SetHighPoint(0, 0, 1000)
elevation.SetScalarRange(0, 1000)

# Lookup table: Brewer diverging brown-blue-green palette
color_series = vtkColorSeries()
color_series.SetNumberOfColors(8)
color_series.SetColorScheme(color_series.BREWER_DIVERGING_BROWN_BLUE_GREEN_8)
lut = vtkLookupTable()
color_series.BuildLookupTable(lut, color_series.ORDINAL)
lut.SetNanColor(1, 0, 0, 1)

# Mapper: map elevation data to graphics primitives
hawaii_mapper = vtkDataSetMapper()
hawaii_mapper.SetInputConnection(elevation.GetOutputPort())
hawaii_mapper.SetScalarRange(0, 1000)
hawaii_mapper.ScalarVisibilityOn()
hawaii_mapper.SetLookupTable(lut)

# Actor: display the elevation-colored surface
hawaii_actor = vtkActor()
hawaii_actor.SetMapper(hawaii_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(hawaii_actor)
renderer.SetBackground(bkg_color)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)
renderer.GetActiveCamera().Roll(-90)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Hawaii")
render_window.SetSize(500, 500)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
