#!/usr/bin/env python

# Demonstrate 3D image warping using vtkThinPlateSplineTransform,
# vtkTransformToGrid, and vtkGridTransform on medical head data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkFiltersHybrid import (
    vtkGridTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkImageSlice, vtkImageSliceMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read volume data
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataOrigin(-100.8, -100.8, -69)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)
reader.Update()

# Source and target landmark points
p1 = vtkPoints()
p2 = vtkPoints()
p1.InsertNextPoint(0, 0, 0)
p2.InsertNextPoint(-60, 10, 20)
p1.InsertNextPoint(-100, -100, -50)
p2.InsertNextPoint(-100, -100, -50)
p1.InsertNextPoint(-100, -100, 50)
p2.InsertNextPoint(-100, -100, 50)
p1.InsertNextPoint(-100, 100, -50)
p2.InsertNextPoint(-100, 100, -50)
p1.InsertNextPoint(-100, 100, 50)
p2.InsertNextPoint(-100, 100, 50)
p1.InsertNextPoint(100, -100, -50)
p2.InsertNextPoint(100, -100, -50)
p1.InsertNextPoint(100, -100, 50)
p2.InsertNextPoint(100, -100, 50)
p1.InsertNextPoint(100, 100, -50)
p2.InsertNextPoint(100, 100, -50)
p1.InsertNextPoint(100, 100, 50)
p2.InsertNextPoint(100, 100, 50)

# Thin plate spline transform
transform = vtkThinPlateSplineTransform()
transform.SetSourceLandmarks(p1)
transform.SetTargetLandmarks(p2)
transform.SetBasisToR()

# Convert to grid transform
grid_thin_plate = vtkTransformToGrid()
grid_thin_plate.SetInput(transform)
grid_thin_plate.SetGridExtent(0, 64, 0, 64, 0, 50)
grid_thin_plate.SetGridSpacing(3.2, 3.2, 3.0)
grid_thin_plate.SetGridOrigin(-102.4, -102.4, -75)
grid_thin_plate.SetGridScalarTypeToUnsignedChar()
grid_thin_plate.Update()

grid_transform = vtkGridTransform()
grid_transform.SetDisplacementGridData(grid_thin_plate.GetOutput())
grid_transform.SetDisplacementShift(grid_thin_plate.GetDisplacementShift())
grid_transform.SetDisplacementScale(grid_thin_plate.GetDisplacementScale())

# Reslice the image using the grid transform
reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetResliceTransform(grid_transform)
reslice.SetInterpolationModeToLinear()
reslice.SetOutputSpacing(1, 1, 1)

# Display a slice using vtkImageSliceMapper + vtkImageSlice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(reslice.GetOutputPort())
image_mapper.SetSliceNumber(70)

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)
image_slice.GetProperty().SetColorWindow(2000)
image_slice.GetProperty().SetColorLevel(1000)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("grid warp3d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
