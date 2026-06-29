#!/usr/bin/env python

# Test vtkExtractVOI with direction matrix preservation on analytic data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import (
    vtkExtractVOI,
    vtkRTAnalyticSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Origin marker
sphere = vtkSphereSource()
sphere.SetRadius(2.0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Analytic source with direction matrix
analytic_source = vtkRTAnalyticSource()
analytic_source.SetWholeExtent(-40, 60, -25, 75, 0, 0)
analytic_source.Update()
image = analytic_source.GetOutput()
image.SetDirectionMatrix(-1, 0, 0, 0, -1, 0, 0, 0, 1)

# Extract VOI
extract_voi = vtkExtractVOI()
extract_voi.SetInputData(image)
extract_voi.SetVOI(-11, 39, 5, 45, 0, 0)
extract_voi.SetSampleRate(5, 5, 1)

# Verify direction matrix preservation
extract_voi.Update()
direction_matrix = extract_voi.GetOutput().GetDirectionMatrix()
if direction_matrix.GetElement(0, 0) != -1 or direction_matrix.GetElement(1, 1) != -1 or direction_matrix.GetElement(2, 2) != 1:
    print("ERROR: vtkExtractVOI not passing DirectionMatrix unchanged")

# Surface extraction
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(extract_voi.GetOutputPort())

triangles = vtkTriangleFilter()
triangles.SetInputConnection(surface.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(triangles.GetOutputPort())
mapper.SetScalarRange(130, 280)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(sphere_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract voi")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
