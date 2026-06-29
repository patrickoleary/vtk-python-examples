#!/usr/bin/env python

# Generate multiple isosurfaces from PLOT3D combustor data by reusing
# a single vtkContourFilter and copying output at each contour value.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

scalar_range = output.GetPointData().GetScalars().GetRange()
min_val = scalar_range[0]
max_val = scalar_range[1]

# Single contour filter, reused for each value
contour_filter = vtkContourFilter()
contour_filter.SetInputData(output)
contour_filter.SetValue(0, (min_val + max_val) / 2.0)
contour_filter.UseScalarTreeOn()

# Generate 5 contour surfaces, each offset vertically
number_of_contours = 5
epsilon = float(max_val - min_val) / float(number_of_contours * 10)
min_val = min_val + epsilon
max_val = max_val - epsilon

# Renderer
renderer = vtkRenderer()

# Contour 1 (i=1, val = min_val).
contour_filter.SetValue(0, min_val)
contour_filter.Update()
pd_1 = vtkPolyData()
pd_1.CopyStructure(contour_filter.GetOutput())
pd_1.GetPointData().DeepCopy(contour_filter.GetOutput().GetPointData())
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(pd_1)
mapper_1.SetScalarRange(output.GetPointData().GetScalars().GetRange())
actor_1 = vtkActor()
actor_1.AddPosition(0, 1 * 12, 0)
actor_1.SetMapper(mapper_1)
renderer.AddActor(actor_1)

# Contour 2 (i=2, val = min_val + 0.25 * range).
contour_filter.SetValue(0, min_val + 0.25 * (max_val - min_val))
contour_filter.Update()
pd_2 = vtkPolyData()
pd_2.CopyStructure(contour_filter.GetOutput())
pd_2.GetPointData().DeepCopy(contour_filter.GetOutput().GetPointData())
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputData(pd_2)
mapper_2.SetScalarRange(output.GetPointData().GetScalars().GetRange())
actor_2 = vtkActor()
actor_2.AddPosition(0, 2 * 12, 0)
actor_2.SetMapper(mapper_2)
renderer.AddActor(actor_2)

# Contour 3 (i=3, val = min_val + 0.5 * range).
contour_filter.SetValue(0, min_val + 0.5 * (max_val - min_val))
contour_filter.Update()
pd_3 = vtkPolyData()
pd_3.CopyStructure(contour_filter.GetOutput())
pd_3.GetPointData().DeepCopy(contour_filter.GetOutput().GetPointData())
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputData(pd_3)
mapper_3.SetScalarRange(output.GetPointData().GetScalars().GetRange())
actor_3 = vtkActor()
actor_3.AddPosition(0, 3 * 12, 0)
actor_3.SetMapper(mapper_3)
renderer.AddActor(actor_3)

# Contour 4 (i=4, val = min_val + 0.75 * range).
contour_filter.SetValue(0, min_val + 0.75 * (max_val - min_val))
contour_filter.Update()
pd_4 = vtkPolyData()
pd_4.CopyStructure(contour_filter.GetOutput())
pd_4.GetPointData().DeepCopy(contour_filter.GetOutput().GetPointData())
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputData(pd_4)
mapper_4.SetScalarRange(output.GetPointData().GetScalars().GetRange())
actor_4 = vtkActor()
actor_4.AddPosition(0, 4 * 12, 0)
actor_4.SetMapper(mapper_4)
renderer.AddActor(actor_4)

# Contour 5 (i=5, val = max_val).
contour_filter.SetValue(0, max_val)
contour_filter.Update()
pd_5 = vtkPolyData()
pd_5.CopyStructure(contour_filter.GetOutput())
pd_5.GetPointData().DeepCopy(contour_filter.GetOutput().GetPointData())
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputData(pd_5)
mapper_5.SetScalarRange(output.GetPointData().GetScalars().GetRange())
actor_5 = vtkActor()
actor_5.AddPosition(0, 5 * 12, 0)
actor_5.SetMapper(mapper_5)
renderer.AddActor(actor_5)

renderer.SetBackground(0.3, 0.3, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(450, 150)
render_window.SetWindowName("multiple iso")

# Scene
renderer.GetActiveCamera().SetPosition(-36.3762, 32.3855, 51.3652)
renderer.GetActiveCamera().SetFocalPoint(8.255, 33.3861, 29.7687)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
