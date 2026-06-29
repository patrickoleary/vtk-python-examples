#!/usr/bin/env python

# Compare quadric decimation with and without volume preservation
# on a noisy planar surface, shown in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkQuadricDecimation,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkRandomAttributeGenerator,
    vtkWarpScalar,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 100

# Source: high-resolution plane
plane_source = vtkPlaneSource()
plane_source.SetResolution(resolution, resolution)

# Triangulate
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(plane_source.GetOutputPort())

# Add random scalars for jitter
random_attr = vtkRandomAttributeGenerator()
random_attr.SetInputConnection(triangle_filter.GetOutputPort())
random_attr.GeneratePointScalarsOn()
random_attr.SetMinimumComponentValue(-0.05)
random_attr.SetMaximumComponentValue(0.05)

# Warp geometry by the random scalars
warp = vtkWarpScalar()
warp.SetInputConnection(random_attr.GetOutputPort())
warp.SetScaleFactor(0.02)

# Decimation without volume constraint
decimation_no_volume = vtkQuadricDecimation()
decimation_no_volume.SetInputConnection(warp.GetOutputPort())
decimation_no_volume.SetTargetReduction(0.95)
decimation_no_volume.AttributeErrorMetricOn()
decimation_no_volume.VolumePreservationOff()

# Decimation with volume constraint
decimation_with_volume = vtkQuadricDecimation()
decimation_with_volume.SetInputConnection(warp.GetOutputPort())
decimation_with_volume.SetTargetReduction(0.95)
decimation_with_volume.AttributeErrorMetricOn()
decimation_with_volume.VolumePreservationOn()

# Left viewport: original warped surface
mapper0 = vtkPolyDataMapper()
mapper0.SetInputConnection(warp.GetOutputPort())
actor0 = vtkActor()
actor0.SetMapper(mapper0)

# Middle viewport: decimated without volume preservation
mapper1 = vtkPolyDataMapper()
mapper1.SetInputConnection(decimation_no_volume.GetOutputPort())
actor1 = vtkActor()
actor1.SetMapper(mapper1)

# Right viewport: decimated with volume preservation
mapper2 = vtkPolyDataMapper()
mapper2.SetInputConnection(decimation_with_volume.GetOutputPort())
actor2 = vtkActor()
actor2.SetMapper(mapper2)

# Three side-by-side viewports
renderer0 = vtkRenderer()
renderer0.SetViewport(0, 0, 0.33, 1)
renderer0.AddActor(actor0)
renderer0.SetBackground(0, 0, 0)

renderer1 = vtkRenderer()
renderer1.SetViewport(0.33, 0, 0.66, 1)
renderer1.AddActor(actor1)
renderer1.SetBackground(0, 0, 0)

renderer2 = vtkRenderer()
renderer2.SetViewport(0.66, 0, 1, 1)
renderer2.AddActor(actor2)
renderer2.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer0)
render_window.AddRenderer(renderer1)
render_window.AddRenderer(renderer2)
render_window.SetSize(600, 300)
render_window.SetWindowName("quadric decimation volume preserve")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0, 0, 1)
camera.Elevation(45.0)
renderer0.SetActiveCamera(camera)
renderer1.SetActiveCamera(camera)
renderer2.SetActiveCamera(camera)
renderer0.ResetCamera()

# Print bounds for comparison
decimation_no_volume.Update()
decimation_with_volume.Update()
print(f"Bounds (volume preserve off): ({decimation_no_volume.GetOutput().GetPoints().GetBounds()})")
print(f"Bounds (volume preserve on): ({decimation_with_volume.GetOutput().GetPoints().GetBounds()})")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
