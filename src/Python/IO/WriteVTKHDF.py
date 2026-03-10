#!/usr/bin/env python

# Write a VTK dataset to the VTKHDF file format using vtkHDFWriter,
# then read it back with vtkHDFReader and render the result.  This
# round-trip demonstrates the modern HDF5-based VTK file format.

import tempfile
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOHDF import vtkHDFReader, vtkHDFWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Output path: write to a temporary directory
output_path = str(Path(tempfile.mkdtemp()) / "sphere.vtkhdf")

# Source: generate a sphere with elevation scalars
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(32)
sphere_source.SetPhiResolution(32)

elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere_source.GetOutputPort())
elevation.SetLowPoint(0.0, -0.5, 0.0)
elevation.SetHighPoint(0.0, 0.5, 0.0)
elevation.Update()

# Write: save the polydata to a VTKHDF file
writer = vtkHDFWriter()
writer.SetInputData(elevation.GetOutput())
writer.SetFileName(output_path)
writer.SetOverwrite(True)
writer.Write()
print(f"Wrote {output_path}")

# Read: load the VTKHDF file back
reader = vtkHDFReader()
reader.SetFileName(output_path)
reader.Update()

# Mapper: map the round-tripped polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Elevation")
mapper.SetScalarRange(0.0, 1.0)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WriteVTKHDF")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
