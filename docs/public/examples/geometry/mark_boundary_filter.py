#!/usr/bin/env python

# Demonstrate vtkMarkBoundaryFilter on 2D dataset types: polydata,
# unstructured grid, and structured (image) data, thresholding to
# show only boundary cells.

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
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test resolution
res = 50

# Polydata from plane source
plane = vtkPlaneSource()
plane.SetResolution(res, res)

mark_1 = vtkMarkBoundaryFilter()
mark_1.SetInputConnection(plane.GetOutputPort())
mark_1.Update()

thresh_1 = vtkThreshold()
thresh_1.SetInputConnection(mark_1.GetOutputPort())
thresh_1.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh_1.SetUpperThreshold(1.0)
thresh_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryCells"
)
thresh_1.Update()

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(thresh_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Unstructured grid
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1000000)

to_ug = vtkExtractGeometry()
to_ug.SetInputConnection(plane.GetOutputPort())
to_ug.SetImplicitFunction(sphere)

mark_2 = vtkMarkBoundaryFilter()
mark_2.SetInputConnection(to_ug.GetOutputPort())
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

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Structured 2D image data
image = vtkImageData()
image.SetDimensions(res, res, 1)
image.SetOrigin(-0.5, -0.5, 0.0)
image.SetSpacing(1.0 / float(res - 1), 1.0 / float(res - 1), 1.0)

mark_3 = vtkMarkBoundaryFilter()
mark_3.SetInputData(image)

thresh_3 = vtkThreshold()
thresh_3.SetInputConnection(mark_3.GetOutputPort())
thresh_3.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh_3.SetUpperThreshold(1.0)
thresh_3.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryCells"
)

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(thresh_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 1)
renderer_0.SetBackground(0.5, 0.5, 0.5)
renderer_0.AddActor(actor_1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.667, 1)
renderer_1.SetBackground(0.5, 0.5, 0.5)
renderer_1.AddActor(actor_2)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.667, 0, 1, 1)
renderer_2.SetBackground(0.5, 0.5, 0.5)
renderer_2.AddActor(actor_3)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(450, 150)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("mark boundary filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().SetPosition(0, 0, 1)
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
