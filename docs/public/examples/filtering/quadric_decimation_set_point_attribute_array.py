#!/usr/bin/env python

# Decimate a triangulated plane using vtkQuadricDecimation with
# attribute error metrics, scalar weighting, and point data mapping.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersCore import (
    vtkQuadricDecimation,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: high-resolution plane
plane_source = vtkPlaneSource()
plane_source.SetXResolution(100)
plane_source.SetYResolution(100)
plane_source.Update()

plane = plane_source.GetOutput()
points = plane.GetPoints()
num_points = points.GetNumberOfPoints()

# Create analytical scalar data based on point positions
scalars = vtkDoubleArray()
scalars.SetName("Analytical")
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(num_points)

for i in range(num_points):
    pt = points.GetPoint(i)
    scalars.SetTuple1(i, 2.5 - 2.5 * math.cos(20 * pt[0] + 8 * pt[1]))

plane.GetPointData().SetScalars(scalars)

# Triangulate
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputData(plane)
triangle_filter.Update()
triangle_filter.GetOutput().GetPointData().SetActiveScalars("Analytical")

# Filter: quadric decimation with attribute error metrics
decimator = vtkQuadricDecimation()
decimator.SetInputConnection(triangle_filter.GetOutputPort())
decimator.SetRegularize(False)
decimator.SetTargetReduction(0.95)
decimator.AttributeErrorMetricOn()
decimator.ScalarsAttributeOn()
decimator.SetScalarsWeight(1.0)
decimator.VectorsAttributeOff()
decimator.NormalsAttributeOff()
decimator.VolumePreservationOn()
decimator.WeighBoundaryConstraintsByLengthOn()
decimator.SetMapPointData(True)
decimator.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(decimator.GetOutputPort())
mapper.SetScalarRange(decimator.GetOutput().GetPointData().GetScalars().GetRange())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetEdgeVisibility(True)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric decimation set point attribute array")

# Scene
camera = renderer.GetActiveCamera()
camera.SetParallelProjection(True)
camera.SetParallelScale(0.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
