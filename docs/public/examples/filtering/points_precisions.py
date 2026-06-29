#!/usr/bin/env python

# Verify that clipping filters preserve double-precision points by
# visualizing clipped unstructured grid, structured grid, and polydata
# side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
    vtkStructuredGrid,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.util.vtkConstants import VTK_HEXAHEDRON, VTK_QUAD

# Clipping plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 0, 0)

# --- Unstructured grid (hexahedron) ---
ug_pts = vtkPoints()
ug_pts.SetDataTypeToDouble()
ug_pts.InsertNextPoint(-1.0, -1.0, -1.0)
ug_pts.InsertNextPoint(1.0, -1.0, -1.0)
ug_pts.InsertNextPoint(1.0, 1.0, -1.0)
ug_pts.InsertNextPoint(-1.0, 1.0, -1.0)
ug_pts.InsertNextPoint(-1.0, -1.0, 1.0)
ug_pts.InsertNextPoint(1.0, -1.0, 1.0)
ug_pts.InsertNextPoint(1.0, 1.0, 1.0)
ug_pts.InsertNextPoint(-1.0, 1.0, 1.0)

ug = vtkUnstructuredGrid()
ug.SetPoints(ug_pts)
ug.Allocate(1, 1)
ug_ids = vtkIdList()
for i in range(8):
    ug_ids.InsertId(i, i)
ug.InsertNextCell(VTK_HEXAHEDRON, ug_ids)

ug_scalar = vtkDoubleArray()
ug_scalar.SetName("scalar")
ug_scalar.SetNumberOfTuples(8)
for i in range(4):
    ug_scalar.SetValue(i, 0.0)
for i in range(4, 8):
    ug_scalar.SetValue(i, 1.0)
ug.GetPointData().SetScalars(ug_scalar)

ug_clip = vtkClipDataSet()
ug_clip.SetInputData(ug)
ug_clip.SetClipFunction(plane)
ug_clip.SetValue(0)

ug_mapper = vtkDataSetMapper()
ug_mapper.SetInputConnection(ug_clip.GetOutputPort())

ug_actor = vtkActor()
ug_actor.SetMapper(ug_mapper)
ug_actor.GetProperty().EdgeVisibilityOn()
ug_actor.GetProperty().SetEdgeColor(0, 0, 0)

# --- Structured grid ---
sg_pts = vtkPoints()
sg_pts.SetDataTypeToDouble()
sg_pts.InsertNextPoint(-1.0, -1.0, -1.0)
sg_pts.InsertNextPoint(1.0, -1.0, -1.0)
sg_pts.InsertNextPoint(1.0, 1.0, -1.0)
sg_pts.InsertNextPoint(-1.0, 1.0, -1.0)
sg_pts.InsertNextPoint(-1.0, -1.0, 1.0)
sg_pts.InsertNextPoint(1.0, -1.0, 1.0)
sg_pts.InsertNextPoint(1.0, 1.0, 1.0)
sg_pts.InsertNextPoint(-1.0, 1.0, 1.0)

sg = vtkStructuredGrid()
sg.SetDimensions(2, 2, 2)
sg.SetPoints(sg_pts)

sg_scalar = vtkDoubleArray()
sg_scalar.SetName("scalar")
sg_scalar.SetNumberOfTuples(8)
for i in range(4):
    sg_scalar.SetValue(i, 0.0)
for i in range(4, 8):
    sg_scalar.SetValue(i, 1.0)
sg.GetPointData().SetScalars(sg_scalar)

sg_clip = vtkClipDataSet()
sg_clip.SetInputData(sg)
sg_clip.SetClipFunction(plane)
sg_clip.SetValue(0)

sg_mapper = vtkDataSetMapper()
sg_mapper.SetInputConnection(sg_clip.GetOutputPort())

sg_actor = vtkActor()
sg_actor.SetMapper(sg_mapper)
sg_actor.AddPosition(3, 0, 0)
sg_actor.GetProperty().EdgeVisibilityOn()
sg_actor.GetProperty().SetEdgeColor(0, 0, 0)

# --- PolyData (quad) ---
pd_pts = vtkPoints()
pd_pts.SetDataTypeToDouble()
pd_pts.InsertNextPoint(-1.0, -1.0, -1.0)
pd_pts.InsertNextPoint(1.0, -1.0, -1.0)
pd_pts.InsertNextPoint(1.0, 1.0, -1.0)
pd_pts.InsertNextPoint(-1.0, 1.0, -1.0)

pd = vtkPolyData()
pd.SetPoints(pd_pts)
pd.Allocate(1, 1)
pd_ids = vtkIdList()
for i in range(4):
    pd_ids.InsertId(i, i)
pd.InsertNextCell(VTK_QUAD, pd_ids)

pd_scalar = vtkDoubleArray()
pd_scalar.SetName("scalar")
pd_scalar.SetNumberOfTuples(4)
pd_scalar.SetValue(0, 0.0)
pd_scalar.SetValue(1, 0.0)
pd_scalar.SetValue(2, 1.0)
pd_scalar.SetValue(3, 1.0)
pd.GetPointData().SetScalars(pd_scalar)

pd_clip = vtkClipDataSet()
pd_clip.SetInputData(pd)
pd_clip.SetClipFunction(plane)
pd_clip.SetValue(0)

pd_mapper = vtkDataSetMapper()
pd_mapper.SetInputConnection(pd_clip.GetOutputPort())

pd_actor = vtkActor()
pd_actor.SetMapper(pd_mapper)
pd_actor.AddPosition(6, 0, 0)
pd_actor.GetProperty().EdgeVisibilityOn()
pd_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ug_actor)
renderer.AddActor(sg_actor)
renderer.AddActor(pd_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 300)
render_window.SetWindowName("points precisions")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
