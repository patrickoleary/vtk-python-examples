#!/usr/bin/env python

# Demonstrate vtkExtractBlock to extract a single block from a multi-block
# dataset containing a sphere and a cube, displaying only the sphere.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersExtraction import vtkExtractBlock
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: sphere (block 0)
sphere_source = vtkSphereSource()
sphere_source.SetCenter(-1.5, 0, 0)
sphere_source.SetPhiResolution(32)
sphere_source.SetThetaResolution(32)
sphere_source.Update()

# Source: cube (block 1)
cube_source = vtkCubeSource()
cube_source.SetCenter(1.5, 0, 0)
cube_source.Update()

# Build a multi-block dataset
multi_block = vtkMultiBlockDataSet()
multi_block.SetNumberOfBlocks(2)
multi_block.SetBlock(0, sphere_source.GetOutput())
multi_block.SetBlock(1, cube_source.GetOutput())

# Filter: extract only block 0 (the sphere)
extract_block = vtkExtractBlock()
extract_block.SetInputData(multi_block)
extract_block.AddIndex(1)

# Filter: extract geometry from the composite output
composite_geometry = vtkCompositeDataGeometryFilter()
composite_geometry.SetInputConnection(extract_block.GetOutputPort())

# Mapper: map the extracted geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(composite_geometry.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract block")
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
