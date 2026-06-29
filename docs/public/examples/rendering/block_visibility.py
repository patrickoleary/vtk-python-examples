#!/usr/bin/env python

# Demonstrate vtkCompositePolyDataMapper with per-block visibility control.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPolyData
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositeDataDisplayAttributes,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create multiblock dataset with 18 blocks (spheres & cubes in a 3x3 grid)
multiblock = vtkMultiBlockDataSet()
multiblock.SetNumberOfBlocks(18)

# i=0,j=0: sphere at (0,0), cube around (0,0)
sphere_src_0_0 = vtkSphereSource()
sphere_src_0_0.SetRadius(0.4)
sphere_src_0_0.SetCenter(0, 0, 0.0)
sphere_src_0_0.Update()
sphere_0_0 = vtkPolyData()
sphere_0_0.DeepCopy(sphere_src_0_0.GetOutputDataObject(0))
multiblock.SetBlock(0, sphere_0_0)

cube_src_0_0 = vtkCubeSource()
cube_src_0_0.SetBounds(-0.4, 0.4, -0.4, 0.4, 0.6, 1.4)
cube_src_0_0.Update()
cube_0_0 = vtkPolyData()
cube_0_0.DeepCopy(cube_src_0_0.GetOutputDataObject(0))
multiblock.SetBlock(1, cube_0_0)

# i=0,j=1: sphere at (0,1), cube around (0,1)
sphere_src_0_1 = vtkSphereSource()
sphere_src_0_1.SetRadius(0.4)
sphere_src_0_1.SetCenter(0, 1, 0.0)
sphere_src_0_1.Update()
sphere_0_1 = vtkPolyData()
sphere_0_1.DeepCopy(sphere_src_0_1.GetOutputDataObject(0))
multiblock.SetBlock(2, sphere_0_1)

cube_src_0_1 = vtkCubeSource()
cube_src_0_1.SetBounds(-0.4, 0.4, 0.6, 1.4, 0.6, 1.4)
cube_src_0_1.Update()
cube_0_1 = vtkPolyData()
cube_0_1.DeepCopy(cube_src_0_1.GetOutputDataObject(0))
multiblock.SetBlock(3, cube_0_1)

# i=0,j=2: sphere at (0,2), cube around (0,2)
sphere_src_0_2 = vtkSphereSource()
sphere_src_0_2.SetRadius(0.4)
sphere_src_0_2.SetCenter(0, 2, 0.0)
sphere_src_0_2.Update()
sphere_0_2 = vtkPolyData()
sphere_0_2.DeepCopy(sphere_src_0_2.GetOutputDataObject(0))
multiblock.SetBlock(4, sphere_0_2)

cube_src_0_2 = vtkCubeSource()
cube_src_0_2.SetBounds(-0.4, 0.4, 1.6, 2.4, 0.6, 1.4)
cube_src_0_2.Update()
cube_0_2 = vtkPolyData()
cube_0_2.DeepCopy(cube_src_0_2.GetOutputDataObject(0))
multiblock.SetBlock(5, cube_0_2)

# i=1,j=0: sphere at (1,0), cube around (1,0)
sphere_src_1_0 = vtkSphereSource()
sphere_src_1_0.SetRadius(0.4)
sphere_src_1_0.SetCenter(1, 0, 0.0)
sphere_src_1_0.Update()
sphere_1_0 = vtkPolyData()
sphere_1_0.DeepCopy(sphere_src_1_0.GetOutputDataObject(0))
multiblock.SetBlock(6, sphere_1_0)

cube_src_1_0 = vtkCubeSource()
cube_src_1_0.SetBounds(0.6, 1.4, -0.4, 0.4, 0.6, 1.4)
cube_src_1_0.Update()
cube_1_0 = vtkPolyData()
cube_1_0.DeepCopy(cube_src_1_0.GetOutputDataObject(0))
multiblock.SetBlock(7, cube_1_0)

# i=1,j=1: sphere at (1,1), cube around (1,1)
sphere_src_1_1 = vtkSphereSource()
sphere_src_1_1.SetRadius(0.4)
sphere_src_1_1.SetCenter(1, 1, 0.0)
sphere_src_1_1.Update()
sphere_1_1 = vtkPolyData()
sphere_1_1.DeepCopy(sphere_src_1_1.GetOutputDataObject(0))
multiblock.SetBlock(8, sphere_1_1)

cube_src_1_1 = vtkCubeSource()
cube_src_1_1.SetBounds(0.6, 1.4, 0.6, 1.4, 0.6, 1.4)
cube_src_1_1.Update()
cube_1_1 = vtkPolyData()
cube_1_1.DeepCopy(cube_src_1_1.GetOutputDataObject(0))
multiblock.SetBlock(9, cube_1_1)

# i=1,j=2: sphere at (1,2), cube around (1,2)
sphere_src_1_2 = vtkSphereSource()
sphere_src_1_2.SetRadius(0.4)
sphere_src_1_2.SetCenter(1, 2, 0.0)
sphere_src_1_2.Update()
sphere_1_2 = vtkPolyData()
sphere_1_2.DeepCopy(sphere_src_1_2.GetOutputDataObject(0))
multiblock.SetBlock(10, sphere_1_2)

cube_src_1_2 = vtkCubeSource()
cube_src_1_2.SetBounds(0.6, 1.4, 1.6, 2.4, 0.6, 1.4)
cube_src_1_2.Update()
cube_1_2 = vtkPolyData()
cube_1_2.DeepCopy(cube_src_1_2.GetOutputDataObject(0))
multiblock.SetBlock(11, cube_1_2)

# i=2,j=0: sphere at (2,0), cube around (2,0)
sphere_src_2_0 = vtkSphereSource()
sphere_src_2_0.SetRadius(0.4)
sphere_src_2_0.SetCenter(2, 0, 0.0)
sphere_src_2_0.Update()
sphere_2_0 = vtkPolyData()
sphere_2_0.DeepCopy(sphere_src_2_0.GetOutputDataObject(0))
multiblock.SetBlock(12, sphere_2_0)

cube_src_2_0 = vtkCubeSource()
cube_src_2_0.SetBounds(1.6, 2.4, -0.4, 0.4, 0.6, 1.4)
cube_src_2_0.Update()
cube_2_0 = vtkPolyData()
cube_2_0.DeepCopy(cube_src_2_0.GetOutputDataObject(0))
multiblock.SetBlock(13, cube_2_0)

# i=2,j=1: sphere at (2,1), cube around (2,1)
sphere_src_2_1 = vtkSphereSource()
sphere_src_2_1.SetRadius(0.4)
sphere_src_2_1.SetCenter(2, 1, 0.0)
sphere_src_2_1.Update()
sphere_2_1 = vtkPolyData()
sphere_2_1.DeepCopy(sphere_src_2_1.GetOutputDataObject(0))
multiblock.SetBlock(14, sphere_2_1)

cube_src_2_1 = vtkCubeSource()
cube_src_2_1.SetBounds(1.6, 2.4, 0.6, 1.4, 0.6, 1.4)
cube_src_2_1.Update()
cube_2_1 = vtkPolyData()
cube_2_1.DeepCopy(cube_src_2_1.GetOutputDataObject(0))
multiblock.SetBlock(15, cube_2_1)

# i=2,j=2: sphere at (2,2), cube around (2,2)
sphere_src_2_2 = vtkSphereSource()
sphere_src_2_2.SetRadius(0.4)
sphere_src_2_2.SetCenter(2, 2, 0.0)
sphere_src_2_2.Update()
sphere_2_2 = vtkPolyData()
sphere_2_2.DeepCopy(sphere_src_2_2.GetOutputDataObject(0))
multiblock.SetBlock(16, sphere_2_2)

cube_src_2_2 = vtkCubeSource()
cube_src_2_2.SetBounds(1.6, 2.4, 1.6, 2.4, 0.6, 1.4)
cube_src_2_2.Update()
cube_2_2 = vtkPolyData()
cube_2_2.DeepCopy(cube_src_2_2.GetOutputDataObject(0))
multiblock.SetBlock(17, cube_2_2)

# Mapper with per-block visibility
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputDataObject(multiblock)
composite_mapper.ScalarVisibilityOff()

attrs = vtkCompositeDataDisplayAttributes()
composite_mapper.SetCompositeDataDisplayAttributes(attrs)

# Set checkerboard visibility pattern (blocks 0,3,4,7,8,11,13,14,17 visible)
attrs.SetBlockVisibility(multiblock.GetBlock(0), True)
attrs.SetBlockVisibility(multiblock.GetBlock(1), False)
attrs.SetBlockVisibility(multiblock.GetBlock(2), False)
attrs.SetBlockVisibility(multiblock.GetBlock(3), True)
attrs.SetBlockVisibility(multiblock.GetBlock(4), True)
attrs.SetBlockVisibility(multiblock.GetBlock(5), False)
attrs.SetBlockVisibility(multiblock.GetBlock(6), False)
attrs.SetBlockVisibility(multiblock.GetBlock(7), True)
attrs.SetBlockVisibility(multiblock.GetBlock(8), True)
attrs.SetBlockVisibility(multiblock.GetBlock(9), False)
attrs.SetBlockVisibility(multiblock.GetBlock(10), False)
attrs.SetBlockVisibility(multiblock.GetBlock(11), True)
attrs.SetBlockVisibility(multiblock.GetBlock(12), False)
attrs.SetBlockVisibility(multiblock.GetBlock(13), True)
attrs.SetBlockVisibility(multiblock.GetBlock(14), True)
attrs.SetBlockVisibility(multiblock.GetBlock(15), False)
attrs.SetBlockVisibility(multiblock.GetBlock(16), False)
attrs.SetBlockVisibility(multiblock.GetBlock(17), True)

composite_actor = vtkActor()
composite_actor.SetMapper(composite_mapper)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(composite_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("block visibility")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
