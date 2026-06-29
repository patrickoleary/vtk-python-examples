#!/usr/bin/env python

# Demonstrate vtkMarkBoundaryFilter on 3D dataset types: image data
# and unstructured grid, with boundary face generation enabled,
# thresholding to show only boundary cells.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkImageData,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkMarkBoundaryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test resolution
res = 50

# 3D image data volume
image = vtkImageData()
image.SetDimensions(res, res, res)
image.SetOrigin(-0.5, -0.5, -0.5)
image.SetSpacing(1.0 / float(res - 1), 1.0 / float(res - 1), 1.0 / float(res - 1))

mark_1 = vtkMarkBoundaryFilter()
mark_1.SetInputData(image)
mark_1.GenerateBoundaryFacesOn()

thresh_1 = vtkThreshold()
thresh_1.SetInputConnection(mark_1.GetOutputPort())
thresh_1.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh_1.SetUpperThreshold(1.0)
thresh_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryCells"
)

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(thresh_1.GetOutputPort())
mapper_1.ScalarVisibilityOff()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Unstructured grid from image data
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1000000)

to_ug = vtkExtractGeometry()
to_ug.SetInputData(image)
to_ug.SetImplicitFunction(sphere)

mark_2 = vtkMarkBoundaryFilter()
mark_2.SetInputConnection(to_ug.GetOutputPort())
mark_2.GenerateBoundaryFacesOn()
mark_2.Update()

thresh_2 = vtkThreshold()
thresh_2.SetInputConnection(mark_2.GetOutputPort())
thresh_2.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh_2.SetUpperThreshold(1.0)
thresh_2.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryCells"
)

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(thresh_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(actor_1)
renderer_0.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_0.GetActiveCamera().SetPosition(0.25, 0.5, 1)
renderer_0.ResetCamera()

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(actor_2)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 150)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("mark boundary3d datasets")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
