#!/usr/bin/env python

# Demonstrate vtkClipDataSet on polyhedron cells by clipping a grid of
# polyhedra with a plane and rendering the clipped result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    VTK_POLYHEDRON,
    vtkPlane,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkCellTypeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create polyhedron cell source
cell_source = vtkCellTypeSource()
cell_source.SetCellOrder(1)
cell_source.SetCellType(VTK_POLYHEDRON)
cell_source.SetBlocksDimensions(5, 5, 5)

# Define clip plane
plane = vtkPlane()
plane.SetOrigin(8, 2, 4)
plane.SetNormal(0.5, 0.5, 0.5)

# Clip
clip = vtkClipDataSet()
clip.SetInputConnection(cell_source.GetOutputPort())
clip.SetClipFunction(plane)
clip.GenerateClippedOutputOn()

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(clip.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0, 0, 0)
actor.GetProperty().SetColor(0.8, 0.4, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("clip dataset polyhedrons")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
