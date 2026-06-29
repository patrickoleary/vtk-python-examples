#!/usr/bin/env python

# Resample an Exodus II dataset onto a regular image grid using
# vtkResampleWithDataSet, contour the valid point mask, and
# color by velocity magnitude.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import (
    vtkArrayCalculator,
    vtkResampleWithDataSet,
    vtkThreshold,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load Exodus II file
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))
reader.UpdateInformation()
reader.SetObjectArrayStatus(reader.NODAL, "VEL", 1)
reader.Update()

# Create a regular image grid based on can.ex2 bounds
origin = [-7.8, -1.0, -15.0]
spacing = [1.0, 0.56, 0.95]
dims = [16, 16, 16]

input_image = vtkImageData()
input_image.SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1)
input_image.SetOrigin(origin)
input_image.SetSpacing(spacing)

# Resample the Exodus data onto the image grid
resample = vtkResampleWithDataSet()
resample.SetInputData(input_image)
resample.SetSourceConnection(reader.GetOutputPort())
resample.UpdateTimeStep(0.00199999)

# Threshold on valid point mask to keep only resampled cells
thresh = vtkThreshold()
thresh.SetInputConnection(resample.GetOutputPort())
thresh.SetInputArrayToProcess(0, 0, 0, 0, "vtkValidPointMask")
thresh.SetUpperThreshold(0.5)
thresh.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh.Update()

# Extract surface for rendering
surf = vtkDataSetSurfaceFilter()
surf.SetInputConnection(thresh.GetOutputPort())

# Compute velocity magnitude
calculator = vtkArrayCalculator()
calculator.SetInputConnection(surf.GetOutputPort())
calculator.AddVectorArrayName("VEL")
calculator.SetFunction("mag(VEL)")
calculator.SetResultArrayName("VEL_MAG")
calculator.Update()

vel_mag = calculator.GetOutput().GetPointData().GetArray("VEL_MAG")
if vel_mag is not None:
    scalar_range = vel_mag.GetRange()
else:
    scalar_range = (0.0, 1.0)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(calculator.GetOutputPort())
mapper.SelectColorArray("VEL_MAG")
mapper.SetScalarModeToUsePointFieldData()
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(scalar_range)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(800, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("resample exodus to image")

# Scene
renderer.GetActiveCamera().SetPosition(0.0, -1.0, 0.0)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
