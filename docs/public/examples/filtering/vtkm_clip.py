#!/usr/bin/env python
# Demonstrate vtkmClip on polydata, unstructured grid, and image data inputs.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmClip
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkImagingHybrid import vtkImageToPoints
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Clip 1: Polydata (sphere) ---
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(50)
sphere_source.SetPhiResolution(50)
sphere_source.Update()
sphere = sphere_source.GetOutput()

# Add x+y scalar field.
sphere_scalars = vtkDoubleArray()
sphere_scalars.SetName("x+y")
sphere_scalars.SetNumberOfComponents(1)
sphere_scalars.SetNumberOfTuples(sphere.GetNumberOfPoints())
for i in range(sphere.GetNumberOfPoints()):
    pt = sphere.GetPoint(i)
    sphere_scalars.SetComponent(i, 0, pt[0] + pt[1])
sphere.GetPointData().SetScalars(sphere_scalars)

sphere_clipper = vtkmClip()
sphere_clipper.SetInputData(sphere)
sphere_clipper.SetComputeScalars(True)
sphere_clipper.SetValue(0.0)

sphere_surface = vtkDataSetSurfaceFilter()
sphere_surface.SetInputConnection(sphere_clipper.GetOutputPort())

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_surface.GetOutputPort())
sphere_mapper.SetScalarVisibility(1)
sphere_mapper.SetScalarModeToUsePointFieldData()
sphere_mapper.SelectColorArray("x+y")
sphere_mapper.SetScalarRange(0, 1)

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetPosition(0.5, 0.5, 0.0)
sphere_actor.RotateWXYZ(90.0, 0.0, 0.0, 1.0)

# --- Clip 2: Unstructured grid (tetrahedralized wavelet) ---
image_source = vtkRTAnalyticSource()
image_source.SetWholeExtent(-5, 5, -5, 5, -5, 5)

image_to_points = vtkImageToPoints()
image_to_points.SetInputConnection(image_source.GetOutputPort())

tetrahedralizer = vtkDelaunay3D()
tetrahedralizer.SetInputConnection(image_to_points.GetOutputPort())
tetrahedralizer.Update()
tets = tetrahedralizer.GetOutput()

# Add negated x+y scalar field.
tet_scalars = vtkDoubleArray()
tet_scalars.SetName("x+y")
tet_scalars.SetNumberOfComponents(1)
tet_scalars.SetNumberOfTuples(tets.GetNumberOfPoints())
for i in range(tets.GetNumberOfPoints()):
    pt = tets.GetPoint(i)
    tet_scalars.SetComponent(i, 0, -pt[0] - pt[1])
tets.GetPointData().SetScalars(tet_scalars)

tet_clipper = vtkmClip()
tet_clipper.SetInputData(tets)
tet_clipper.SetComputeScalars(True)
tet_clipper.SetValue(0.0)

tet_surface = vtkDataSetSurfaceFilter()
tet_surface.SetInputConnection(tet_clipper.GetOutputPort())

tet_mapper = vtkPolyDataMapper()
tet_mapper.SetInputConnection(tet_surface.GetOutputPort())
tet_mapper.SetScalarVisibility(1)
tet_mapper.SetScalarModeToUsePointFieldData()
tet_mapper.SelectColorArray("x+y")
tet_mapper.SetScalarRange(0, 10)

tet_actor = vtkActor()
tet_actor.SetMapper(tet_mapper)
tet_actor.SetScale(1.0 / 5.0)

# --- Clip 3: Image data ---
image = image_source.GetOutput()

# Add x+y scalar field.
image_scalars = vtkDoubleArray()
image_scalars.SetName("x+y")
image_scalars.SetNumberOfComponents(1)
image_scalars.SetNumberOfTuples(image.GetNumberOfPoints())
for i in range(image.GetNumberOfPoints()):
    pt = image.GetPoint(i)
    image_scalars.SetComponent(i, 0, pt[0] + pt[1])
image.GetPointData().SetScalars(image_scalars)

image_clipper = vtkmClip()
image_clipper.SetInputData(image)
image_clipper.SetComputeScalars(True)
image_clipper.SetValue(0.0)

image_surface = vtkDataSetSurfaceFilter()
image_surface.SetInputConnection(image_clipper.GetOutputPort())

image_mapper = vtkPolyDataMapper()
image_mapper.SetInputConnection(image_surface.GetOutputPort())
image_mapper.SetScalarVisibility(1)
image_mapper.SetScalarModeToUsePointFieldData()
image_mapper.SelectColorArray("x+y")
image_mapper.SetScalarRange(0, 10)

image_actor = vtkActor()
image_actor.SetMapper(image_mapper)
image_actor.SetScale(1.0 / 5.0)
image_actor.SetPosition(1.0, 1.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(tet_actor)
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm clip")

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
