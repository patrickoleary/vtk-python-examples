#!/usr/bin/env python

# Demonstrate vtkPartitionedDataSet by grouping multiple geometric
# objects as partitions and rendering them with per-block coloring.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPartitionedDataSet
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
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

# Source: generate four geometric objects at different positions
sphere_source = vtkSphereSource()
sphere_source.SetCenter(-3.0, 0.0, 0.0)
sphere_source.SetRadius(1.0)
sphere_source.SetThetaResolution(20)
sphere_source.SetPhiResolution(20)
sphere_source.Update()

cube_source = vtkCubeSource()
cube_source.SetCenter(-1.0, 0.0, 0.0)
cube_source.Update()

cylinder_source = vtkCylinderSource()
cylinder_source.SetCenter(1.0, 0.0, 0.0)
cylinder_source.SetRadius(0.5)
cylinder_source.SetHeight(1.5)
cylinder_source.SetResolution(20)
cylinder_source.Update()

cone_source = vtkConeSource()
cone_source.SetCenter(3.0, 0.0, 0.0)
cone_source.SetRadius(0.7)
cone_source.SetHeight(1.5)
cone_source.SetResolution(20)
cone_source.Update()

# Partitioned dataset: group the four objects as partitions
partitioned_dataset = vtkPartitionedDataSet()
partitioned_dataset.SetNumberOfPartitions(4)
partitioned_dataset.SetPartition(0, sphere_source.GetOutput())
partitioned_dataset.SetPartition(1, cube_source.GetOutput())
partitioned_dataset.SetPartition(2, cylinder_source.GetOutput())
partitioned_dataset.SetPartition(3, cone_source.GetOutput())

# Mapper: composite-aware mapper with per-partition coloring
# Flat indices: 0 = partitioned dataset root, 1-4 = partitions
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(partitioned_dataset)
display_attributes = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(display_attributes)
mapper.SetBlockColor(1, tomato_rgb)
mapper.SetBlockColor(2, steel_blue_rgb)
mapper.SetBlockColor(3, gold_rgb)
mapper.SetBlockColor(4, peach_puff_rgb)

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
render_window.SetWindowName("partitioned dataset")
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
