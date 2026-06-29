#!/usr/bin/env python

# Test vtkCompositePolyDataMapper bounds with empty blocks.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkMultiBlockDataSet,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create points for a quad
points = vtkPoints()
bounds = [2.0, 4.0, -5.0, -3.0, 0.0, 0.0]
for y in [bounds[2], bounds[3]]:
    for x in [bounds[0], bounds[1]]:
        points.InsertNextPoint(x, y, 0)

# One quad cell
polys = vtkCellArray()
polys.InsertNextCell(4)
for pid in [0, 1, 3, 2]:
    polys.InsertCellPoint(pid)

# Polydata with single quad
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(polys)

# Empty polydata
empty = vtkPolyData()

# Composite dataset with empty block following non-empty block
multi_block = vtkMultiBlockDataSet()
multi_block.SetBlock(0, poly_data)
multi_block.SetBlock(1, empty)

# Map the composite dataset
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputDataObject(multi_block)

# Display the composite dataset
actor = vtkActor()
actor.SetMapper(composite_mapper)
actor.GetProperty().SetColor(0.2, 0.6, 0.9)
actor.GetProperty().EdgeVisibilityOn()

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("composite polydata mapper bounds")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
