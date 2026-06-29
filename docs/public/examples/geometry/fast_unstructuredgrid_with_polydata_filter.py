#!/usr/bin/env python

# Demonstrate vtkGeometryFilter on an unstructured grid extracted
# from a sphere source via double selection, with pass-through IDs.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSelectionNode
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersSources import (
    vtkSelectionSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.5)
sphere.SetThetaResolution(16)
sphere.SetPhiResolution(16)

# First selection: pick specific cells from sphere
selection_1 = vtkSelectionSource()
selection_1.SetContentType(vtkSelectionNode.INDICES)
selection_1.SetFieldType(vtkSelectionNode.CELL)
for i in range(16):
    selection_1.AddID(0, i)
for i in [32, 33, 58, 59, 84, 85, 110, 111, 136, 137, 162, 163,
          188, 189, 214, 215, 240, 241, 266, 267, 292, 293, 318, 319,
          344, 345, 370, 371, 396, 397, 422, 423]:
    selection_1.AddID(0, i)

extract_1 = vtkExtractSelection()
extract_1.SetInputConnection(0, sphere.GetOutputPort())
extract_1.SetInputConnection(1, selection_1.GetOutputPort())
extract_1.Update()

# Second selection: pick first 16 cells from previous extraction
selection_2 = vtkSelectionSource()
selection_2.SetContentType(vtkSelectionNode.INDICES)
selection_2.SetFieldType(vtkSelectionNode.CELL)
for i in range(16):
    selection_2.AddID(0, i)

extract_2 = vtkExtractSelection()
extract_2.SetInputConnection(0, extract_1.GetOutputPort())
extract_2.SetInputConnection(1, selection_2.GetOutputPort())

# Geometry filter with pass-through IDs
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(extract_2.GetOutputPort())
geometry_filter.PassThroughPointIdsOn()
geometry_filter.PassThroughCellIdsOn()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("fast unstructuredgrid with polydata filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
