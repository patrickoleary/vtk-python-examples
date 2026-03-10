#!/usr/bin/env python

# Read a VTK XML structured grid (.vts) file using vtkXMLStructuredGridReader
# and display it as a wireframe with scalar coloring.  A small structured grid
# is generated and written to disk if the file does not already exist.

import math
import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader, vtkXMLStructuredGridWriter
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
vts_path = data_dir / "structured_grid.vts"

# Generate a small structured grid if the file does not exist
if not vts_path.exists():
    nx, ny, nz = 20, 20, 1
    grid = vtkStructuredGrid()
    grid.SetDimensions(nx, ny, nz)

    points = vtkPoints()
    scalars = vtkFloatArray()
    scalars.SetName("Height")

    for j in range(ny):
        for i in range(nx):
            x = i / (nx - 1.0) * 4.0 - 2.0
            y = j / (ny - 1.0) * 4.0 - 2.0
            z = math.sin(math.sqrt(x * x + y * y))
            points.InsertNextPoint(x, y, z)
            scalars.InsertNextValue(z)

    grid.SetPoints(points)
    grid.GetPointData().SetScalars(scalars)

    writer = vtkXMLStructuredGridWriter()
    writer.SetFileName(str(vts_path))
    writer.SetInputData(grid)
    writer.Write()

# Reader: load the structured grid
reader = vtkXMLStructuredGridReader()
reader.SetFileName(str(vts_path))
reader.Update()

# Filter: extract surface geometry from the structured grid
geometry = vtkStructuredGridGeometryFilter()
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
render_window.SetWindowName("ReadXMLStructuredGrid")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
