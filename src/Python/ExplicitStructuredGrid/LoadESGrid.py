#!/usr/bin/env python

# Load the UNISIM-II-D reservoir model as an unstructured grid, convert
# it to an explicit structured grid, and color by connectivity flags.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkUnstructuredGridToExplicitStructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dim_gray_rgb = (0.412, 0.412, 0.412)

# Data: locate the UNISIM-II-D.vtu file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the unstructured grid from a VTU file
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(str(data_dir / "UNISIM-II-D.vtu"))
reader.Update()

# Convert: unstructured grid → explicit structured grid
converter = vtkUnstructuredGridToExplicitStructuredGrid()
converter.GlobalWarningDisplayOff()
converter.SetInputConnection(reader.GetOutputPort())
converter.SetInputArrayToProcess(0, 0, 0, 1, "BLOCK_I")
converter.SetInputArrayToProcess(1, 0, 0, 1, "BLOCK_J")
converter.SetInputArrayToProcess(2, 0, 0, 1, "BLOCK_K")
converter.Update()

# Connectivity: compute face connectivity flags and set as active scalars
grid = converter.GetOutput()
grid.ComputeFacesConnectivityFlagsArray()
grid.GetCellData().SetActiveScalars("ConnectivityFlags")
scalars = grid.GetCellData().GetArray("ConnectivityFlags")

# Mapper: map the grid to graphics primitives colored by connectivity flags
mapper = vtkDataSetMapper()
mapper.SetInputData(grid)
mapper.SetColorModeToMapScalars()
mapper.SetScalarRange(scalars.GetRange())

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dim_gray_rgb)
camera = renderer.GetActiveCamera()
camera.SetPosition(312452.407650, 7474760.406373, 3507.364723)
camera.SetFocalPoint(314388.388434, 7481520.509575, -2287.477388)
camera.SetViewUp(0.089920, 0.633216, 0.768734)
camera.SetDistance(9111.926908)
camera.SetClippingRange(595.217338, 19595.429475)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("LoadESGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
