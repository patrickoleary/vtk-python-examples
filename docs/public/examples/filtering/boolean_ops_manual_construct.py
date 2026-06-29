#!/usr/bin/env python

# Demonstrate boolean operations on polydata using intersection, distance,
# and threshold filters to manually construct union, intersection, and
# difference results from overlapping spheres.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkReverseSense,
    vtkThreshold,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkDistancePolyDataFilter,
    vtkIntersectionPolyDataFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

center_separation = 0.15

# --- Union (left, x_offset=-2.0) ---
union_sphere_1 = vtkSphereSource()
union_sphere_1.SetCenter(-center_separation - 2.0, 0.0, 0.0)

union_sphere_2 = vtkSphereSource()
union_sphere_2.SetCenter(center_separation - 2.0, 0.0, 0.0)

union_intersection = vtkIntersectionPolyDataFilter()
union_intersection.SetInputConnection(0, union_sphere_1.GetOutputPort())
union_intersection.SetInputConnection(1, union_sphere_2.GetOutputPort())

union_distance = vtkDistancePolyDataFilter()
union_distance.SetInputConnection(0, union_intersection.GetOutputPort(1))
union_distance.SetInputConnection(1, union_intersection.GetOutputPort(2))

union_thresh_1 = vtkThreshold()
union_thresh_1.AllScalarsOn()
union_thresh_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
union_thresh_1.SetInputConnection(union_distance.GetOutputPort(0))
union_thresh_1.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
union_thresh_1.SetUpperThreshold(0.0)

union_thresh_2 = vtkThreshold()
union_thresh_2.AllScalarsOn()
union_thresh_2.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
union_thresh_2.SetInputConnection(union_distance.GetOutputPort(1))
union_thresh_2.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
union_thresh_2.SetUpperThreshold(0.0)

union_surface_1 = vtkDataSetSurfaceFilter()
union_surface_1.SetInputConnection(union_thresh_1.GetOutputPort())

union_surface_2 = vtkDataSetSurfaceFilter()
union_surface_2.SetInputConnection(union_thresh_2.GetOutputPort())

union_appender = vtkAppendPolyData()
union_appender.SetInputConnection(union_surface_1.GetOutputPort())
union_appender.AddInputConnection(union_surface_2.GetOutputPort())

union_mapper = vtkPolyDataMapper()
union_mapper.SetInputConnection(union_appender.GetOutputPort())
union_mapper.ScalarVisibilityOff()

union_actor = vtkActor()
union_actor.SetMapper(union_mapper)

# --- Intersection (center, x_offset=0.0) ---
intersect_sphere_1 = vtkSphereSource()
intersect_sphere_1.SetCenter(-center_separation, 0.0, 0.0)

intersect_sphere_2 = vtkSphereSource()
intersect_sphere_2.SetCenter(center_separation, 0.0, 0.0)

intersect_intersection = vtkIntersectionPolyDataFilter()
intersect_intersection.SetInputConnection(0, intersect_sphere_1.GetOutputPort())
intersect_intersection.SetInputConnection(1, intersect_sphere_2.GetOutputPort())

intersect_distance = vtkDistancePolyDataFilter()
intersect_distance.SetInputConnection(0, intersect_intersection.GetOutputPort(1))
intersect_distance.SetInputConnection(1, intersect_intersection.GetOutputPort(2))

intersect_thresh_1 = vtkThreshold()
intersect_thresh_1.AllScalarsOn()
intersect_thresh_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
intersect_thresh_1.SetInputConnection(intersect_distance.GetOutputPort(0))
intersect_thresh_1.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
intersect_thresh_1.SetLowerThreshold(0.0)

intersect_thresh_2 = vtkThreshold()
intersect_thresh_2.AllScalarsOn()
intersect_thresh_2.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
intersect_thresh_2.SetInputConnection(intersect_distance.GetOutputPort(1))
intersect_thresh_2.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
intersect_thresh_2.SetLowerThreshold(0.0)

intersect_surface_1 = vtkDataSetSurfaceFilter()
intersect_surface_1.SetInputConnection(intersect_thresh_1.GetOutputPort())

intersect_surface_2 = vtkDataSetSurfaceFilter()
intersect_surface_2.SetInputConnection(intersect_thresh_2.GetOutputPort())

intersect_appender = vtkAppendPolyData()
intersect_appender.SetInputConnection(intersect_surface_1.GetOutputPort())
intersect_appender.AddInputConnection(intersect_surface_2.GetOutputPort())

intersect_mapper = vtkPolyDataMapper()
intersect_mapper.SetInputConnection(intersect_appender.GetOutputPort())
intersect_mapper.ScalarVisibilityOff()

intersect_actor = vtkActor()
intersect_actor.SetMapper(intersect_mapper)

# --- Difference (right, x_offset=2.0) ---
diff_sphere_1 = vtkSphereSource()
diff_sphere_1.SetCenter(-center_separation + 2.0, 0.0, 0.0)

diff_sphere_2 = vtkSphereSource()
diff_sphere_2.SetCenter(center_separation + 2.0, 0.0, 0.0)

diff_intersection = vtkIntersectionPolyDataFilter()
diff_intersection.SetInputConnection(0, diff_sphere_1.GetOutputPort())
diff_intersection.SetInputConnection(1, diff_sphere_2.GetOutputPort())

diff_distance = vtkDistancePolyDataFilter()
diff_distance.SetInputConnection(0, diff_intersection.GetOutputPort(1))
diff_distance.SetInputConnection(1, diff_intersection.GetOutputPort(2))

diff_thresh_1 = vtkThreshold()
diff_thresh_1.AllScalarsOn()
diff_thresh_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
diff_thresh_1.SetInputConnection(diff_distance.GetOutputPort(0))
diff_thresh_1.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
diff_thresh_1.SetUpperThreshold(0.0)

diff_thresh_2 = vtkThreshold()
diff_thresh_2.AllScalarsOn()
diff_thresh_2.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "Distance"
)
diff_thresh_2.SetInputConnection(diff_distance.GetOutputPort(1))
diff_thresh_2.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
diff_thresh_2.SetLowerThreshold(0.0)

diff_surface_1 = vtkDataSetSurfaceFilter()
diff_surface_1.SetInputConnection(diff_thresh_1.GetOutputPort())

diff_surface_2 = vtkDataSetSurfaceFilter()
diff_surface_2.SetInputConnection(diff_thresh_2.GetOutputPort())

diff_reverse_sense = vtkReverseSense()
diff_reverse_sense.SetInputConnection(diff_surface_2.GetOutputPort())
diff_reverse_sense.ReverseCellsOn()
diff_reverse_sense.ReverseNormalsOn()

diff_appender = vtkAppendPolyData()
diff_appender.SetInputConnection(diff_surface_1.GetOutputPort())
diff_appender.AddInputConnection(diff_reverse_sense.GetOutputPort())

diff_mapper = vtkPolyDataMapper()
diff_mapper.SetInputConnection(diff_appender.GetOutputPort())
diff_mapper.ScalarVisibilityOff()

diff_actor = vtkActor()
diff_actor.SetMapper(diff_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(union_actor)
renderer.AddActor(intersect_actor)
renderer.AddActor(diff_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("boolean ops manual construct")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
