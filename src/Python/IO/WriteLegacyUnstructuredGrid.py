#!/usr/bin/env python

# Create a hexahedron, write it to a legacy VTK unstructured grid
# (.vtk) file using vtkUnstructuredGridWriter, read it back, and
# render the result for verification.

import os
import tempfile

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkHexahedron, vtkUnstructuredGrid
from vtkmodules.vtkIOLegacy import (
    vtkUnstructuredGridReader,
    vtkUnstructuredGridWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# Output path: write to a temporary file
vtk_path = os.path.join(tempfile.gettempdir(), "WriteLegacyUnstructuredGrid.vtk")

# Source: build a hexahedron from its parametric coordinates
cell = vtkHexahedron()
pcoords = cell.GetParametricCoords()
for i in range(cell.GetNumberOfPoints()):
    cell.GetPointIds().SetId(i, i)
    cell.GetPoints().SetPoint(
        i, pcoords[3 * i], pcoords[3 * i + 1], pcoords[3 * i + 2])

ug = vtkUnstructuredGrid()
ug.SetPoints(cell.GetPoints())
ug.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

# Writer: save to legacy VTK unstructured grid file
writer = vtkUnstructuredGridWriter()
writer.SetFileName(vtk_path)
writer.SetInputData(ug)
writer.Write()
print(f"Wrote: {vtk_path}")

# Reader: read back the written file for verification
reader = vtkUnstructuredGridReader()
reader.SetFileName(vtk_path)
reader.Update()

# Mapper: map unstructured grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor: assign the mapped geometry
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetLineWidth(2.0)
actor.SetBackfaceProperty(back_property)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WriteLegacyUnstructuredGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
