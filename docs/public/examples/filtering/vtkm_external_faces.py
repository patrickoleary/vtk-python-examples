#!/usr/bin/env python
# Demonstrate vtkmExternalFaces on a clipped wavelet with compact points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmExternalFaces
from vtkmodules.vtkCommonDataModel import vtkCylinder, vtkPolyData, vtkSphere
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import (
    vtkRandomAttributeGenerator,
    vtkTableBasedClipDataSet,
    vtkTransformFilter,
)
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source.
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-16, 16, -16, 16, -16, 16)
wavelet.SetCenter(0, 0, 0)

# Clip with cylinder.
cylinder = vtkCylinder()
cylinder.SetCenter(0, 0, 0)
cylinder.SetRadius(15)
cylinder.SetAxis(0, 1, 0)

clip_cyl = vtkTableBasedClipDataSet()
clip_cyl.SetInputConnection(wavelet.GetOutputPort())
clip_cyl.SetClipFunction(cylinder)
clip_cyl.InsideOutOn()

# Clip with sphere.
sphere = vtkSphere()
sphere.SetCenter(0, 0, 4)
sphere.SetRadius(12)

clip_sphr = vtkTableBasedClipDataSet()
clip_sphr.SetInputConnection(clip_cyl.GetOutputPort())
clip_sphr.SetClipFunction(sphere)

# Rotate 45 degrees around Z.
transform = vtkTransform()
transform.RotateZ(45)

trans_filter = vtkTransformFilter()
trans_filter.SetInputConnection(clip_sphr.GetOutputPort())
trans_filter.SetTransform(transform)

# Add random cell data.
cell_data_adder = vtkRandomAttributeGenerator()
cell_data_adder.SetInputConnection(trans_filter.GetOutputPort())
cell_data_adder.SetDataTypeToFloat()
cell_data_adder.GenerateCellVectorsOn()

# External faces via VTK-m with compact points.
external_faces = vtkmExternalFaces()
external_faces.SetInputConnection(cell_data_adder.GetOutputPort())
external_faces.CompactPointsOn()
external_faces.Update()

result = external_faces.GetOutput()

# Convert unstructured grid to polydata for rendering.
# The result contains only 2D cells (triangles/quads).
polydata = vtkPolyData()
polydata.SetPoints(result.GetPoints())
polydata.Allocate(result.GetNumberOfCells())
for i in range(result.GetNumberOfCells()):
    cell = result.GetCell(i)
    polydata.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
polydata.GetPointData().PassData(result.GetPointData())

# Mapper and actor.
scalar_range = polydata.GetPointData().GetArray("RTData").GetRange()

mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)
mapper.SetScalarRange(scalar_range)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm external faces")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
