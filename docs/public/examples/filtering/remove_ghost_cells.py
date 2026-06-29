#!/usr/bin/env python

# Visualize the effect of RemoveGhostCells on a triangulated CT head
# subregion processed with ghost cells, showing before and after.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageClip
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CT head data
reader = vtkImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 64)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)
reader.SetDataSpacing(1.6, 1.6, 1.5)

# Clip a small subregion
clipper = vtkImageClip()
clipper.SetInputConnection(reader.GetOutputPort())
clipper.SetOutputWholeExtent(30, 36, 30, 36, 30, 36)

# Triangulate with ghost cells (piece 0 of 8)
tris = vtkDataSetTriangleFilter()
tris.SetInputConnection(clipper.GetOutputPort())
tris.UpdatePiece(0, 8, 1)

# Before: unstructured grid with ghost cells
before_mapper = vtkDataSetMapper()
before_mapper.SetInputData(tris.GetOutput())
before_mapper.ScalarVisibilityOn()
before_mapper.SetScalarRange(0, 1200)

before_actor = vtkActor()
before_actor.SetMapper(before_mapper)

# After: remove ghost cells from a copy
ug_copy = vtkUnstructuredGrid()
ug_copy.DeepCopy(tris.GetOutput())
ug_copy.RemoveGhostCells()

after_ug_mapper = vtkDataSetMapper()
after_ug_mapper.SetInputData(ug_copy)
after_ug_mapper.ScalarVisibilityOn()
after_ug_mapper.SetScalarRange(0, 1200)

after_ug_actor = vtkActor()
after_ug_actor.SetMapper(after_ug_mapper)

# Also show polydata path: geometry filter then remove ghosts
geom = vtkGeometryFilter()
geom.SetInputConnection(tris.GetOutputPort())
geom.UpdatePiece(0, 8, 1)

pd_copy = vtkPolyData()
pd_copy.DeepCopy(geom.GetOutput())
pd_copy.RemoveGhostCells()

after_pd_mapper = vtkPolyDataMapper()
after_pd_mapper.SetInputData(pd_copy)
after_pd_mapper.ScalarVisibilityOn()
after_pd_mapper.SetScalarRange(0, 1200)

after_pd_actor = vtkActor()
after_pd_actor.SetMapper(after_pd_mapper)

# Renderer 0: before (with ghost cells)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 1)
renderer_0.AddActor(before_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

# Renderer 1: after removing ghosts from unstructured grid
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.666, 1)
renderer_1.AddActor(after_ug_actor)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 2: after removing ghosts from polydata
renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.666, 0, 1, 1)
renderer_2.AddActor(after_pd_actor)
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("remove ghost cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
