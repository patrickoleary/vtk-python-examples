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
sphere = vtkSphereSource()
sphere.SetCenter(-3.0, 0.0, 0.0)
sphere.SetRadius(1.0)
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.Update()

cube = vtkCubeSource()
cube.SetCenter(-1.0, 0.0, 0.0)
cube.Update()

cylinder = vtkCylinderSource()
cylinder.SetCenter(1.0, 0.0, 0.0)
cylinder.SetRadius(0.5)
cylinder.SetHeight(1.5)
cylinder.SetResolution(20)
cylinder.Update()

cone = vtkConeSource()
cone.SetCenter(3.0, 0.0, 0.0)
cone.SetRadius(0.7)
cone.SetHeight(1.5)
cone.SetResolution(20)
cone.Update()

# Partitioned dataset: group the four objects as partitions
pds = vtkPartitionedDataSet()
pds.SetNumberOfPartitions(4)
pds.SetPartition(0, sphere.GetOutput())
pds.SetPartition(1, cube.GetOutput())
pds.SetPartition(2, cylinder.GetOutput())
pds.SetPartition(3, cone.GetOutput())

# Mapper: composite-aware mapper with per-partition coloring
# Flat indices: 0 = partitioned dataset root, 1-4 = partitions
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(pds)
cdsa = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(cdsa)
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
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PartitionedDataSet")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
