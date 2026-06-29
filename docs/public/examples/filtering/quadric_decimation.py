#!/usr/bin/env python

# Decimate a PLOT3D geometry using quadric decimation, comparing
# results with and without attribute error metrics.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkQuadricDecimation,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load PLOT3D multi-block data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
pl3d_output = plot3d_reader.GetOutput().GetBlock(0)

# Convert to polydata via geometry filter, then triangulate
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputData(pl3d_output)

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(geometry_filter.GetOutputPort())

# Original geometry mapper
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(triangle_filter.GetOutputPort())
geometry_mapper.SetScalarRange(pl3d_output.GetScalarRange())

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)

# Decimation with attribute error metric
decimation_with_attr = vtkQuadricDecimation()
decimation_with_attr.SetInputConnection(triangle_filter.GetOutputPort())
decimation_with_attr.SetTargetReduction(0.90)
decimation_with_attr.SetAttributeErrorMetric(True)

mapper_with_attr = vtkPolyDataMapper()
mapper_with_attr.SetInputConnection(decimation_with_attr.GetOutputPort())

actor_with_attr = vtkActor()
actor_with_attr.SetMapper(mapper_with_attr)

# Decimation without attribute error metric
decimation_no_attr = vtkQuadricDecimation()
decimation_no_attr.SetInputConnection(triangle_filter.GetOutputPort())
decimation_no_attr.SetTargetReduction(0.9)
decimation_no_attr.SetAttributeErrorMetric(False)

mapper_no_attr = vtkPolyDataMapper()
mapper_no_attr.SetInputConnection(decimation_no_attr.GetOutputPort())

actor_no_attr = vtkActor()
actor_no_attr.SetMapper(mapper_no_attr)
actor_no_attr.AddPosition(0, 12, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_with_attr)
renderer.AddActor(actor_no_attr)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("quadric decimation")

# Scene
camera = vtkCamera()
camera.SetPosition(19.34, 6.128, -11.96)
camera.SetFocalPoint(8.25451, 6.0, 29.77)
camera.SetViewUp(0.9664, 0.00605, 0.256883)
camera.SetViewAngle(30)
camera.SetClippingRange(26, 64)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
