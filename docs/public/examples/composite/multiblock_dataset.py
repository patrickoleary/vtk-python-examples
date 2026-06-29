#!/usr/bin/env python

# Build a nested vtkMultiBlockDataSet tree, extract edges from all
# blocks, and render the wireframe using a composite geometry filter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate three spheres at different positions and sizes
sphere_source_0 = vtkSphereSource()
sphere_source_0.SetCenter(0, 0, 0)
sphere_source_0.Update()

sphere_source_1 = vtkSphereSource()
sphere_source_1.SetCenter(1.75, 2.5, 0)
sphere_source_1.SetRadius(1.5)
sphere_source_1.Update()

sphere_source_2 = vtkSphereSource()
sphere_source_2.SetCenter(4, 0, 0)
sphere_source_2.SetRadius(2)
sphere_source_2.Update()

# Multi-block: build a nested tree — branch holds two leaves, root holds
# the branch and a third leaf
branch = vtkMultiBlockDataSet()
branch.SetBlock(0, sphere_source_0.GetOutput())
branch.SetBlock(1, sphere_source_1.GetOutput())

root = vtkMultiBlockDataSet()
root.SetBlock(0, branch)
root.SetBlock(1, sphere_source_2.GetOutput())

# Filter: extract edges from all blocks (non-composite-aware, iterates)
extract_edges = vtkExtractEdges()
extract_edges.SetInputData(root)

# Filter: aggregate all composite blocks into one polydata for rendering
composite_geometry = vtkCompositeDataGeometryFilter()
composite_geometry.SetInputConnection(extract_edges.GetOutputPort())

# Mapper: map the aggregated edge polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(composite_geometry.GetOutputPort())

# Actor: assign the wireframe geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)
actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("multiblock dataset")
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
