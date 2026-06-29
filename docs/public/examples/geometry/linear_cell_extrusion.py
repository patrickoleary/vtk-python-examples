#!/usr/bin/env python

# Demonstrate vtkLinearCellExtrusionFilter by creating a polydata with
# a pentagon, quad, and triangle, extruding cells by a scalar array
# using both normal and user-defined vector modes, and rendering both
# results side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkDataObject, vtkPolyData
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersModeling import vtkLinearCellExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build polydata with three polygonal cells
points = vtkPoints()
points.InsertNextPoint(0.1, 0.0, 0.0)
points.InsertNextPoint(0.5, 0.0, 0.0)
points.InsertNextPoint(0.6, 0.0, 0.2)
points.InsertNextPoint(0.3, 0.0, 0.5)
points.InsertNextPoint(0.1, 0.0, 0.2)
points.InsertNextPoint(0.7, 0.0, 0.5)
points.InsertNextPoint(0.6, 0.0, 0.7)
points.InsertNextPoint(0.8, 0.0, 0.8)

polys = vtkCellArray()
polys.InsertNextCell(5, [0, 1, 2, 3, 4])  # pentagon
polys.InsertNextCell(4, [3, 2, 5, 6])      # quad
polys.InsertNextCell(3, [5, 6, 7])          # triangle

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(polys)

# Cell scalar array for extrusion magnitude
values = vtkDoubleArray()
values.SetNumberOfTuples(3)
values.SetName("Values")
values.SetValue(0, 0.1)
values.SetValue(1, -0.2)
values.SetValue(2, 0.3)
poly_data.GetCellData().SetScalars(values)

# Normal-based extrusion
extrusion = vtkLinearCellExtrusionFilter()
extrusion.SetInputData(poly_data)
extrusion.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Values")
extrusion.SetScaleFactor(1.0)

# User-vector extrusion
extrusion_user = vtkLinearCellExtrusionFilter()
extrusion_user.SetInputData(poly_data)
extrusion_user.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Values")
extrusion_user.SetScaleFactor(0.8)
extrusion_user.UseUserVectorOn()
extrusion_user.SetUserVector(0.707107, 0.707107, 0.0)

# Extract surfaces
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(extrusion.GetOutputPort())

surface_user = vtkDataSetSurfaceFilter()
surface_user.SetInputConnection(extrusion_user.GetOutputPort())

# Mapper and actor for normal extrusion
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SelectColorArray("Values")
mapper.SetScalarRange(0.0, 1.0)
mapper.SetColorModeToMapScalars()

actor = vtkActor()
actor.SetMapper(mapper)

# Mapper and actor for user-vector extrusion
mapper_user = vtkPolyDataMapper()
mapper_user.SetInputConnection(surface_user.GetOutputPort())
mapper_user.SelectColorArray("Values")
mapper_user.SetScalarRange(0.0, 1.0)
mapper_user.SetColorModeToMapScalars()

actor_user = vtkActor()
actor_user.SetPosition(0.0, 0.5, 0.0)
actor_user.SetMapper(mapper_user)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(actor_user)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetWindowName("linear cell extrusion")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
