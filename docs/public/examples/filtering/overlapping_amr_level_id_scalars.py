#!/usr/bin/env python

# Demonstrate vtkOverlappingAMRLevelIdScalars by creating a 2-level
# overlapping AMR dataset, applying the level-id filter, and rendering
# the blocks colored by their AMR level.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkAMRBox,
    vtkOverlappingAMR,
    vtkUniformGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkOverlappingAMRLevelIdScalars
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create overlapping AMR with 2 levels
amr = vtkOverlappingAMR()
amr.Initialize([2, 1])

origin = [0.0, 0.0, 0.0]
spacing_0 = [1.0, 1.0, 1.0]
amr.SetOrigin(origin)

# Level 0 block 0
amr.SetSpacing(0, spacing_0)
root_0 = vtkUniformGrid()
root_0.SetDimensions(6, 6, 6)
root_0.SetSpacing(spacing_0)
root_0.SetOrigin(origin)
amr.SetDataSet(0, 0, root_0)
box_0 = vtkAMRBox(origin, root_0.GetDimensions(), spacing_0, origin, amr.GetGridDescription())
amr.SetAMRBox(0, 0, box_0)

# Level 0 block 1
origin_1 = [5.0, 0.0, 0.0]
root_1 = vtkUniformGrid()
root_1.SetDimensions(6, 6, 6)
root_1.SetSpacing(spacing_0)
root_1.SetOrigin(origin_1)
amr.SetDataSet(0, 1, root_1)
box_1 = vtkAMRBox(origin_1, root_1.GetDimensions(), spacing_0, origin, amr.GetGridDescription())
amr.SetAMRBox(0, 1, box_1)

# Level 1 block 0 (refined, overlaps corner of block 0)
spacing_1 = [0.5, 0.5, 0.5]
amr.SetSpacing(1, spacing_1)
block_1 = vtkUniformGrid()
block_1.SetDimensions(6, 6, 6)
block_1.SetOrigin([2.0, 2.0, 2.0])
block_1.SetSpacing(spacing_1)
amr.SetDataSet(1, 0, block_1)
box_2 = vtkAMRBox([2.0, 2.0, 2.0], block_1.GetDimensions(), spacing_1, origin, amr.GetGridDescription())
amr.SetAMRBox(1, 0, box_2)

# Apply level id filter
level_id = vtkOverlappingAMRLevelIdScalars()
level_id.SetInputData(amr)
level_id.Update()

# Extract geometry for rendering
geometry = vtkCompositeDataGeometryFilter()
geometry.SetInputConnection(level_id.GetOutputPort())

# Render with composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0, 0, 0)
actor.GetProperty().SetOpacity(0.7)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("overlapping amr level id scalars")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Azimuth(45)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
