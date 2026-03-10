#!/usr/bin/env python

# Demonstrate per-block coloring of a vtkMultiBlockDataSet using
# vtkCompositePolyDataMapper with per-block display attributes.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersSources import vtkSphereSource
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
peach_puff_rgb = (1.0, 0.855, 0.725)
steel_blue_rgb = (0.275, 0.510, 0.706)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate two spheres at different positions and sizes
sphere1 = vtkSphereSource()
sphere1.SetRadius(3)
sphere1.SetCenter(0, 0, 0)
sphere1.SetThetaResolution(30)
sphere1.SetPhiResolution(30)
sphere1.Update()

sphere2 = vtkSphereSource()
sphere2.SetRadius(2)
sphere2.SetCenter(2, 0, 0)
sphere2.SetThetaResolution(30)
sphere2.SetPhiResolution(30)
sphere2.Update()

# Multi-block: assemble spheres into a composite dataset with a NULL block
mbds = vtkMultiBlockDataSet()
mbds.SetNumberOfBlocks(3)
mbds.SetBlock(0, sphere1.GetOutput())
# Block 1 is intentionally left NULL — NULL blocks are valid and must be
# handled by algorithms, especially in parallel where remote blocks are NULL.
mbds.SetBlock(2, sphere2.GetOutput())

# Mapper: composite-aware mapper with per-block display attributes
# Flat indices: 0 = multiblock root, 1 = block 0, 2 = block 1 (NULL), 3 = block 2
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(mbds)
cdsa = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(cdsa)
mapper.SetBlockColor(1, peach_puff_rgb)
mapper.SetBlockColor(3, tomato_rgb)

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
render_window.SetWindowName("CompositePolyDataMapper")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
