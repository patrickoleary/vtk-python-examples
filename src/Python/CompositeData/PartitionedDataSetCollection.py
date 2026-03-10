#!/usr/bin/env python

# Demonstrate vtkPartitionedDataSetCollection by grouping multiple
# partitioned datasets into a collection and rendering with per-block coloring.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkPartitionedDataSet,
    vtkPartitionedDataSetCollection,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositeDataDisplayAttributes,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
gold_rgb = (1.0, 0.843, 0.0)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate spheres for the first partitioned dataset
sphere1 = vtkSphereSource()
sphere1.SetCenter(-2.0, 1.0, 0.0)
sphere1.SetRadius(0.8)
sphere1.SetThetaResolution(20)
sphere1.SetPhiResolution(20)
sphere1.Update()

sphere2 = vtkSphereSource()
sphere2.SetCenter(0.0, 1.0, 0.0)
sphere2.SetRadius(0.8)
sphere2.SetThetaResolution(20)
sphere2.SetPhiResolution(20)
sphere2.Update()

# Partitioned dataset 0: two spheres
pds_spheres = vtkPartitionedDataSet()
pds_spheres.SetNumberOfPartitions(2)
pds_spheres.SetPartition(0, sphere1.GetOutput())
pds_spheres.SetPartition(1, sphere2.GetOutput())

# Source: generate cubes for the second partitioned dataset
cube1 = vtkCubeSource()
cube1.SetCenter(-1.0, -1.0, 0.0)
cube1.Update()

cube2 = vtkCubeSource()
cube2.SetCenter(1.0, -1.0, 0.0)
cube2.Update()

# Partitioned dataset 1: two cubes
pds_cubes = vtkPartitionedDataSet()
pds_cubes.SetNumberOfPartitions(2)
pds_cubes.SetPartition(0, cube1.GetOutput())
pds_cubes.SetPartition(1, cube2.GetOutput())

# Source: generate a cone for the third partitioned dataset
cone = vtkConeSource()
cone.SetCenter(2.0, 1.0, 0.0)
cone.SetRadius(0.7)
cone.SetHeight(1.5)
cone.SetResolution(20)
cone.Update()

# Partitioned dataset 2: one cone
pds_cone = vtkPartitionedDataSet()
pds_cone.SetNumberOfPartitions(1)
pds_cone.SetPartition(0, cone.GetOutput())

# Collection: group all partitioned datasets together
pdsc = vtkPartitionedDataSetCollection()
pdsc.SetNumberOfPartitionedDataSets(3)
pdsc.SetPartitionedDataSet(0, pds_spheres)
pdsc.SetPartitionedDataSet(1, pds_cubes)
pdsc.SetPartitionedDataSet(2, pds_cone)

# Mapper: composite-aware mapper with per-block coloring
# Flat indices walk the tree depth-first:
#   0 = collection root
#   1 = pds_spheres, 2 = sphere1, 3 = sphere2
#   4 = pds_cubes, 5 = cube1, 6 = cube2
#   7 = pds_cone, 8 = cone
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(pdsc)
cdsa = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(cdsa)
mapper.SetBlockColor(2, tomato_rgb)
mapper.SetBlockColor(3, tomato_rgb)
mapper.SetBlockColor(5, steel_blue_rgb)
mapper.SetBlockColor(6, steel_blue_rgb)
mapper.SetBlockColor(8, gold_rgb)

# Actor: assign the mapped composite geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PartitionedDataSetCollection")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
