#!/usr/bin/env python

# Demonstrate appending data to vtkImplicitModeller to generate an implicit
# model from multiple input primitives (lines and a plane).

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkPlaneSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create line sources along x, y, z axes
line_x = vtkLineSource()
line_x.SetPoint1(-2.0, 0.0, 0.0)
line_x.SetPoint2(2.0, 0.0, 0.0)
line_x.Update()

line_y = vtkLineSource()
line_y.SetPoint1(0.0, -2.0, 0.0)
line_y.SetPoint2(0.0, 2.0, 0.0)
line_y.Update()

line_z = vtkLineSource()
line_z.SetPoint1(0.0, 0.0, -2.0)
line_z.SetPoint2(0.0, 0.0, 2.0)
line_z.Update()

a_plane = vtkPlaneSource()
a_plane.Update()

# Build implicit model by appending each primitive
imp = vtkImplicitModeller()
imp.SetModelBounds(-2.5, 2.5, -2.5, 2.5, -2.5, 2.5)
imp.SetSampleDimensions(60, 60, 60)
imp.SetCapValue(1000)
imp.SetProcessModeToPerVoxel()

imp.StartAppend()
imp.Append(line_x.GetOutput())
imp.Append(line_y.GetOutput())
imp.Append(line_z.GetOutput())
imp.Append(a_plane.GetOutput())
imp.EndAppend()

# Extract isosurface
cf = vtkContourFilter()
cf.SetInputConnection(imp.GetOutputPort())
cf.SetValue(0, 0.1)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cf.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Outline of the implicit model
outline = vtkOutlineFilter()
outline.SetInputConnection(imp.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Slice of the implicit function
plane_filter = vtkImageDataGeometryFilter()
plane_filter.SetInputConnection(imp.GetOutputPort())
plane_filter.SetExtent(0, 60, 0, 60, 30, 30)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_filter.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(plane_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("append implicit model")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
