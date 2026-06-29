#!/usr/bin/env python
# Demonstrate vtkPointCloudWidget with software picking on a point cloud.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkInteractionWidgets import (
    vtkPointCloudRepresentation,
    vtkPointCloudWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
num_points = 10000

point_source = vtkPointSource()
point_source.SetNumberOfPoints(num_points)
point_source.SetCenter(5, 10, 20)
point_source.SetRadius(7.5)
point_source.Update()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pointcloud widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callbacks for point selection
def select_point(widget, event_string):
    print("Point Id {0}: ".format(point_cloud_rep.GetPointId()))


def report_coords(widget, event_string):
    p_id = point_cloud_rep.GetPointId()
    print("Selected Point Id {0}: ".format(point_cloud_rep.GetPointId()))
    print("Point Coordinates {0}: ".format(point_source.GetOutput().GetPoints().GetPoint(p_id)))


# Widget
point_cloud_rep = vtkPointCloudRepresentation()
point_cloud_rep.SetPlaceFactor(1.0)
point_cloud_rep.PlacePointCloud(point_source.GetOutput())
point_cloud_rep.SetPickingModeToSoftware()

point_cloud_widget = vtkPointCloudWidget()
point_cloud_widget.SetInteractor(interactor)
point_cloud_widget.SetRepresentation(point_cloud_rep)
point_cloud_widget.AddObserver("PickEvent", select_point)
point_cloud_widget.AddObserver("WidgetActivateEvent", report_coords)
point_cloud_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
