#!/usr/bin/env python

# Demonstrate vtkPLinearExtrusionFilter with vtkExtractPolyDataPiece by
# extruding a disk source, extracting piece 1 of 2, and rendering with
# a backface property.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkFiltersParallel import (
    vtkExtractPolyDataPiece,
    vtkPLinearExtrusionFilter,
)
from vtkmodules.vtkFiltersSources import vtkDiskSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Disk source
disk = vtkDiskSource()
disk.SetRadialResolution(2)
disk.SetCircumferentialResolution(9)

# Clean duplicate points
clean = vtkCleanPolyData()
clean.SetInputConnection(disk.GetOutputPort())
clean.SetTolerance(0.01)

# Extract piece
piece = vtkExtractPolyDataPiece()
piece.SetInputConnection(clean.GetOutputPort())

# Parallel linear extrusion
extrude = vtkPLinearExtrusionFilter()
extrude.SetInputConnection(piece.GetOutputPort())
extrude.PieceInvariantOn()

# Mapper — render piece 1 of 2
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extrude.GetOutputPort())
mapper.SetNumberOfPieces(2)
mapper.SetPiece(1)
mapper.Update()
mapper.GetInput().RemoveGhostCells()

# Backface property (red)
back_property = vtkProperty()
back_property.SetColor(1, 0, 0)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 1, 0.8)
actor.SetBackfaceProperty(back_property)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extrude piece")

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(20)
camera.Elevation(40)
renderer.ResetCamera()
camera.Zoom(1.2)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
