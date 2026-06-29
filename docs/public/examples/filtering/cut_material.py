#!/usr/bin/env python

# Demonstrate vtkCutMaterial by creating synthetic image data with a
# Gaussian scalar field and an ellipsoid material mask, then cutting
# through the material to show the scalar distribution.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersParallel import vtkCutMaterial
from vtkmodules.vtkImagingSources import (
    vtkImageEllipsoidSource,
    vtkImageGaussianSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create synthetic image data
data = vtkImageData()
data.SetExtent(0, 31, 0, 31, 0, 31)
data.SetScalarType(10, data.GetInformation())

# Gaussian scalar field
gauss = vtkImageGaussianSource()
gauss.SetWholeExtent(0, 30, 0, 30, 0, 30)
gauss.SetCenter(18, 12, 20)
gauss.SetMaximum(1.0)
gauss.SetStandardDeviation(10.0)
gauss.Update()
gauss_scalars = gauss.GetOutput().GetPointData().GetScalars()
gauss_scalars.SetName("Gauss")
data.GetCellData().SetScalars(gauss_scalars)

# Ellipsoid material mask
ellipse = vtkImageEllipsoidSource()
ellipse.SetWholeExtent(0, 30, 0, 30, 0, 30)
ellipse.SetCenter(11, 12, 13)
ellipse.SetRadius(5, 9, 13)
ellipse.SetInValue(1)
ellipse.SetOutValue(0)
ellipse.SetOutputScalarTypeToInt()
ellipse.Update()
material_scalars = ellipse.GetOutput().GetPointData().GetScalars()
material_scalars.SetName("Material")
data.GetCellData().AddArray(material_scalars)

# Cut through material
cut = vtkCutMaterial()
cut.SetInputData(data)
cut.SetMaterialArrayName("Material")
cut.SetMaterial(1)
cut.SetArrayName("Gauss")
cut.SetUpVector(1, 0, 0)
cut.Update()

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cut.GetOutputPort())
mapper.SetScalarRange(0, 1)
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetPosition(1.5, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("cut material")

# Scene
center_point = cut.GetCenterPoint()
normal = cut.GetNormal()
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(center_point)
camera.SetViewUp(cut.GetUpVector())
camera.SetPosition(normal[0] + center_point[0], normal[1] + center_point[1], normal[2] + center_point[2])
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
