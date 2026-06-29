#!/usr/bin/env python

# Test vtkVoxelModeller by voxelizing a sphere and contouring the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os
import tempfile

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOLegacy import (
    vtkDataSetReader,
    vtkDataSetWriter,
)
from vtkmodules.vtkImagingHybrid import vtkVoxelModeller
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere_model = vtkSphereSource()
sphere_model.SetThetaResolution(10)
sphere_model.SetPhiResolution(10)

# Voxelize the sphere
voxel_model = vtkVoxelModeller()
voxel_model.SetInputConnection(sphere_model.GetOutputPort())
voxel_model.SetSampleDimensions(21, 21, 21)
voxel_model.SetModelBounds(-1.5, 1.5, -1.5, 1.5, -1.5, 1.5)
voxel_model.SetScalarTypeToBit()
voxel_model.SetForegroundValue(1)
voxel_model.SetBackgroundValue(0)

# Write and read back to test the writer/reader round-trip
tmp_file = os.path.join(tempfile.gettempdir(), "voxelModel.vtk")

writer = vtkDataSetWriter()
writer.SetFileName(tmp_file)
writer.SetInputConnection(voxel_model.GetOutputPort())
writer.Update()

reader = vtkDataSetReader()
reader.SetFileName(tmp_file)

# Contour the voxelized data
voxel_surface = vtkContourFilter()
voxel_surface.SetInputConnection(reader.GetOutputPort())
voxel_surface.SetValue(0, .999)

voxel_mapper = vtkPolyDataMapper()
voxel_mapper.SetInputConnection(voxel_surface.GetOutputPort())

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)

# Original sphere for comparison
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_model.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Cleanup temp file
try:
    os.remove(tmp_file)
except OSError:
    pass

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(voxel_actor)
renderer.SetBackground(.1, .2, .4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("voxel model")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetViewUp(0, -1, 0)
renderer.GetActiveCamera().Azimuth(180)
renderer.GetActiveCamera().Dolly(1.75)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
