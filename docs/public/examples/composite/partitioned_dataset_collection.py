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
sphere_source_0 = vtkSphereSource()
sphere_source_0.SetCenter(-2.0, 1.0, 0.0)
sphere_source_0.SetRadius(0.8)
sphere_source_0.SetThetaResolution(20)
sphere_source_0.SetPhiResolution(20)
sphere_source_0.Update()

sphere_source_1 = vtkSphereSource()
sphere_source_1.SetCenter(0.0, 1.0, 0.0)
sphere_source_1.SetRadius(0.8)
sphere_source_1.SetThetaResolution(20)
sphere_source_1.SetPhiResolution(20)
sphere_source_1.Update()

# Partitioned dataset 0: two spheres
sphere_partitions = vtkPartitionedDataSet()
sphere_partitions.SetNumberOfPartitions(2)
sphere_partitions.SetPartition(0, sphere_source_0.GetOutput())
sphere_partitions.SetPartition(1, sphere_source_1.GetOutput())

# Source: generate cubes for the second partitioned dataset
cube_source_0 = vtkCubeSource()
cube_source_0.SetCenter(-1.0, -1.0, 0.0)
cube_source_0.Update()

cube_source_1 = vtkCubeSource()
cube_source_1.SetCenter(1.0, -1.0, 0.0)
cube_source_1.Update()

# Partitioned dataset 1: two cubes
cube_partitions = vtkPartitionedDataSet()
cube_partitions.SetNumberOfPartitions(2)
cube_partitions.SetPartition(0, cube_source_0.GetOutput())
cube_partitions.SetPartition(1, cube_source_1.GetOutput())

# Source: generate a cone for the third partitioned dataset
cone_source = vtkConeSource()
cone_source.SetCenter(2.0, 1.0, 0.0)
cone_source.SetRadius(0.7)
cone_source.SetHeight(1.5)
cone_source.SetResolution(20)
cone_source.Update()

# Partitioned dataset 2: one cone
cone_partition = vtkPartitionedDataSet()
cone_partition.SetNumberOfPartitions(1)
cone_partition.SetPartition(0, cone_source.GetOutput())

# Collection: group all partitioned datasets together
partition_collection = vtkPartitionedDataSetCollection()
partition_collection.SetNumberOfPartitionedDataSets(3)
partition_collection.SetPartitionedDataSet(0, sphere_partitions)
partition_collection.SetPartitionedDataSet(1, cube_partitions)
partition_collection.SetPartitionedDataSet(2, cone_partition)

# Mapper: composite-aware mapper with per-block coloring
# Flat indices walk the tree depth-first:
#   0 = collection root
#   1 = sphere_partitions, 2 = sphere_source_0, 3 = sphere_source_1
#   4 = cube_partitions, 5 = cube_source_0, 6 = cube_source_1
#   7 = cone_partition, 8 = cone_source
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(partition_collection)
display_attributes = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(display_attributes)
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

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("partitioned dataset collection")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
