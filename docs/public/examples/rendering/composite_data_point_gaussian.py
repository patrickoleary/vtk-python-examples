#!/usr/bin/env python

# Demonstrate vtkPointGaussianMapper with hierarchical multiblock composite data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPolyData
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Point gaussian mapper
point_gaussian_mapper = vtkPointGaussianMapper()
point_gaussian_mapper.SetScaleFactor(0.01)

# Cylinder source
resolution = 18
cyl = vtkCylinderSource()
cyl.CappingOn()
cyl.SetRadius(0.2)
cyl.SetResolution(resolution)

# Build hierarchical multiblock dataset
data = vtkMultiBlockDataSet()
blocks_per_level = [1, 32, 64]
blocks = [data]
level_start = 0
level_end = 1
num_levels = len(blocks_per_level)

point_gaussian_mapper.SetInputDataObject(data)

for level in range(1, num_levels):
    nblocks = blocks_per_level[level]
    for parent in range(level_start, level_end):
        blocks[parent].SetNumberOfBlocks(nblocks)
        for block in range(nblocks):
            if level == num_levels - 1:
                # Leaf level: alternating cylinders and None
                if block % 2 == 0:
                    child = vtkPolyData()
                    cyl.SetCenter(block * 0.25, 0.0, parent * 0.5)
                    cyl.Update()
                    child.DeepCopy(cyl.GetOutput(0))
                    blocks[parent].SetBlock(block, child)
                else:
                    blocks[parent].SetBlock(block, None)
            else:
                child = vtkMultiBlockDataSet()
                blocks[parent].SetBlock(block, child)
                blocks.append(child)
    level_start = level_end
    level_end = len(blocks)

point_gaussian_actor = vtkActor()
point_gaussian_actor.SetMapper(point_gaussian_mapper)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(point_gaussian_actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("composite data point gaussian")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

# Camera animation (2 steps)
renderer.GetActiveCamera().Elevation(20.0)
renderer.GetActiveCamera().Zoom(1.414)
renderer.GetActiveCamera().Roll(10.0)

renderer.GetActiveCamera().Elevation(20.0)
renderer.GetActiveCamera().Zoom(1.414)
renderer.GetActiveCamera().Roll(10.0)

interactor.Initialize()
interactor.Start()
