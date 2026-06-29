#!/usr/bin/env python
# Demonstrate vtkmLevelOfDetail at four subdivision levels on a cow mesh.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmLevelOfDetail
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read cow mesh and triangulate.
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

clean = vtkTriangleFilter()
clean.SetInputConnection(reader.GetOutputPort())
clean.Update()

# LOD at 16 divisions.
lod_0 = vtkmLevelOfDetail()
lod_0.SetInputConnection(clean.GetOutputPort())
lod_0.SetNumberOfXDivisions(16)
lod_0.SetNumberOfYDivisions(16)
lod_0.SetNumberOfZDivisions(16)

surface_0 = vtkDataSetSurfaceFilter()
surface_0.SetInputConnection(lod_0.GetOutputPort())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(surface_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetPosition(0, 0, 0)

# LOD at 32 divisions.
lod_1 = vtkmLevelOfDetail()
lod_1.SetInputConnection(clean.GetOutputPort())
lod_1.SetNumberOfXDivisions(32)
lod_1.SetNumberOfYDivisions(32)
lod_1.SetNumberOfZDivisions(32)

surface_1 = vtkDataSetSurfaceFilter()
surface_1.SetInputConnection(lod_1.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(surface_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetPosition(10, 0, 0)

# LOD at 48 divisions.
lod_2 = vtkmLevelOfDetail()
lod_2.SetInputConnection(clean.GetOutputPort())
lod_2.SetNumberOfXDivisions(48)
lod_2.SetNumberOfYDivisions(48)
lod_2.SetNumberOfZDivisions(48)

surface_2 = vtkDataSetSurfaceFilter()
surface_2.SetInputConnection(lod_2.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(surface_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(0, -10, 0)

# LOD at 64 divisions.
lod_3 = vtkmLevelOfDetail()
lod_3.SetInputConnection(clean.GetOutputPort())
lod_3.SetNumberOfXDivisions(64)
lod_3.SetNumberOfYDivisions(64)
lod_3.SetNumberOfZDivisions(64)

surface_3 = vtkDataSetSurfaceFilter()
surface_3.SetInputConnection(lod_3.GetOutputPort())

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(surface_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.SetPosition(10, -10, 0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm level of detail")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
