#!/usr/bin/env python

# Demonstrate vtkConvertToPointCloud by reading a cow mesh, converting
# it to a point cloud with different cell generation modes, and rendering
# the polyvertex result.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersPoints import vtkConvertToPointCloud
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

# Convert to point cloud
conv_point_cloud = vtkConvertToPointCloud()
conv_point_cloud.SetInputConnection(reader.GetOutputPort())

# Verify NO_CELLS mode
conv_point_cloud.SetCellGenerationMode(vtkConvertToPointCloud.NO_CELLS)
conv_point_cloud.Update()
output = conv_point_cloud.GetOutput()
print("NO_CELLS mode: {} cells".format(output.GetNumberOfCells()))

# Verify VERTEX_CELLS mode
conv_point_cloud.SetCellGenerationMode(vtkConvertToPointCloud.VERTEX_CELLS)
conv_point_cloud.Update()
output = conv_point_cloud.GetOutput()
print("VERTEX_CELLS mode: {} cells".format(output.GetNumberOfCells()))

# Use POLYVERTEX_CELL mode for rendering
conv_point_cloud.SetCellGenerationMode(vtkConvertToPointCloud.POLYVERTEX_CELL)
conv_point_cloud.Update()
output = conv_point_cloud.GetOutput()
print("POLYVERTEX_CELL mode: {} cells".format(output.GetNumberOfCells()))

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(conv_point_cloud.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("convert to pointcloud filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
