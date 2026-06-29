#!/usr/bin/env python

# Extract 2D label boundaries using vtkSurfaceNets2D on a label map of
# overlapping circles, with smoothing and boundary label thresholding
# displayed in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkImageData,
)
from vtkmodules.vtkFiltersCore import (
    vtkSurfaceNets2D,
    vtkThreshold,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

VTK_SHORT = 4
resolution = 500

# Create a labeled image
image = vtkImageData()
image.SetDimensions(resolution, resolution, 1)
image.AllocateScalars(VTK_SHORT, 1)

scalars = image.GetPointData().GetScalars()
scalars.Fill(0)

# Generate circles of labels
circles = [
    ([resolution / 2.5, resolution / 1.75], resolution / 9, 5),
    ([resolution / 2, resolution / 3], resolution / 4, 1),
    ([resolution / 2, resolution / 2], resolution / 6, 2),
    ([resolution / 2, resolution / 1.5], resolution / 9, 3),
    ([resolution / 2, resolution / 1.25], resolution / 12, 4),
    ([resolution / 1.5, resolution / 1.75], resolution / 9, 5),
]

for center, radius, label in circles:
    radius2 = radius * radius
    for y in range(resolution):
        for x in range(resolution):
            r2 = (x - center[0]) ** 2 + (y - center[1]) ** 2
            if r2 <= radius2:
                scalars.SetTuple1(x + y * resolution, label)

# Extract boundaries of labels 1-5 with smoothing
surface_nets = vtkSurfaceNets2D()
surface_nets.SetInputData(image)
surface_nets.SetValue(0, 1)
surface_nets.SetValue(1, 2)
surface_nets.SetValue(2, 3)
surface_nets.SetValue(3, 4)
surface_nets.SetValue(4, 5)
surface_nets.SmoothingOn()
surface_nets.GetSmoother().SetNumberOfIterations(100)
surface_nets.GetSmoother().SetRelaxationFactor(0.2)
surface_nets.GetSmoother().SetConstraintDistance(0.75)
surface_nets.ComputeScalarsOn()
surface_nets.SetBackgroundLabel(-1)
surface_nets.Update()

# All boundaries
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface_nets.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)

# Threshold: boundary edges (borders background)
thresh_lower = vtkThreshold()
thresh_lower.SetInputConnection(surface_nets.GetOutputPort())
thresh_lower.SetLowerThreshold(0)
thresh_lower.SetUpperThreshold(5)
thresh_lower.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryLabels")
thresh_lower.SetComponentModeToUseAny()
thresh_lower.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)

thresh_lower_mapper = vtkDataSetMapper()
thresh_lower_mapper.SetInputConnection(thresh_lower.GetOutputPort())
thresh_lower_mapper.ScalarVisibilityOff()

thresh_lower_actor = vtkActor()
thresh_lower_actor.SetMapper(thresh_lower_mapper)

# Threshold: interior edges (between two segmented objects)
thresh_upper = vtkThreshold()
thresh_upper.SetInputConnection(surface_nets.GetOutputPort())
thresh_upper.SetLowerThreshold(0)
thresh_upper.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "BoundaryLabels")
thresh_upper.SetComponentModeToUseSelected()
thresh_upper.SetSelectedComponent(1)
thresh_upper.InvertOn()
thresh_upper.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)

thresh_upper_mapper = vtkDataSetMapper()
thresh_upper_mapper.SetInputConnection(thresh_upper.GetOutputPort())
thresh_upper_mapper.ScalarVisibilityOff()

thresh_upper_actor = vtkActor()
thresh_upper_actor.SetMapper(thresh_upper_mapper)

# Three viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0, 0, 0)
renderer_0.SetViewport(0, 0, 0.333, 1)
renderer_0.AddActor(actor)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0, 0, 0)
renderer_1.SetViewport(0.333, 0, 0.667, 1)
renderer_1.AddActor(thresh_lower_actor)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0, 0, 0)
renderer_2.SetViewport(0.667, 0, 1, 1)
renderer_2.AddActor(thresh_upper_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 200)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("surface nets2d smoothing")

# Scene
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
