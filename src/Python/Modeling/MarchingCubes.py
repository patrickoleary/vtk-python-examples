#!/usr/bin/env python

# Extract an isosurface from a voxelized sphere using vtkFlyingEdges3D
# (or vtkMarchingCubes as a fallback).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkVoxelModeller
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray_background_rgb = (0.184, 0.310, 0.310)
misty_rose_rgb = (1.000, 0.894, 0.882)

# Source: generate a sphere and voxelize it
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(20)
sphere_source.SetThetaResolution(20)
sphere_source.Update()

bounds = list(sphere_source.GetOutput().GetBounds())
for i in range(0, 6, 2):
    dist = bounds[i + 1] - bounds[i]
    bounds[i] = bounds[i] - 0.1 * dist
    bounds[i + 1] = bounds[i + 1] + 0.1 * dist

voxel_modeller = vtkVoxelModeller()
voxel_modeller.SetSampleDimensions(50, 50, 50)
voxel_modeller.SetModelBounds(bounds)
voxel_modeller.SetScalarTypeToFloat()
voxel_modeller.SetMaximumDistance(0.1)
voxel_modeller.SetInputConnection(sphere_source.GetOutputPort())
voxel_modeller.Update()

volume = vtkImageData()
volume.DeepCopy(voxel_modeller.GetOutput())

# Filter: extract isosurface at value 0.5
surface = vtkFlyingEdges3D()
surface.SetInputData(volume)
surface.ComputeNormalsOn()
surface.SetValue(0, 0.5)

# Mapper: map the isosurface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: the isosurface
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_gray_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("MarchingCubes")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
