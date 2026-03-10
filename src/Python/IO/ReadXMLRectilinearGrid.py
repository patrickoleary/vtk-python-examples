#!/usr/bin/env python

# Read a VTK XML rectilinear grid (.vtr) file using
# vtkXMLRectilinearGridReader and display it with scalar coloring.  A small
# rectilinear grid is generated and written to disk if the file does not
# already exist.

import math
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkIOXML import (
    vtkXMLRectilinearGridReader,
    vtkXMLRectilinearGridWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
vtr_path = data_dir / "rectilinear_grid.vtr"

# Generate a small rectilinear grid if the file does not exist
if not vtr_path.exists():
    nx, ny, nz = 20, 20, 2

    x_coords = vtkFloatArray()
    for i in range(nx):
        x_coords.InsertNextValue(i * 0.5)

    y_coords = vtkFloatArray()
    for j in range(ny):
        y_coords.InsertNextValue(j * 0.5)

    z_coords = vtkFloatArray()
    for k in range(nz):
        z_coords.InsertNextValue(k * 0.5)

    grid = vtkRectilinearGrid()
    grid.SetDimensions(nx, ny, nz)
    grid.SetXCoordinates(x_coords)
    grid.SetYCoordinates(y_coords)
    grid.SetZCoordinates(z_coords)

    scalars = vtkFloatArray()
    scalars.SetName("Distance")
    cx, cy = (nx - 1) * 0.25, (ny - 1) * 0.25
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                x = i * 0.5
                y = j * 0.5
                scalars.InsertNextValue(math.sqrt((x - cx) ** 2 + (y - cy) ** 2))
    grid.GetPointData().SetScalars(scalars)

    writer = vtkXMLRectilinearGridWriter()
    writer.SetFileName(str(vtr_path))
    writer.SetInputData(grid)
    writer.Write()

# Reader: load the rectilinear grid
reader = vtkXMLRectilinearGridReader()
reader.SetFileName(str(vtr_path))
reader.Update()

# Filter: extract surface geometry from the rectilinear grid
geometry = vtkRectilinearGridGeometryFilter()
geometry.SetInputConnection(reader.GetOutputPort())

# Mapper: map polygon data to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetScalarRange(reader.GetOutput().GetScalarRange())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadXMLRectilinearGrid")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
