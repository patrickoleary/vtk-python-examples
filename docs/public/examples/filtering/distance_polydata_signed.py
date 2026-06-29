#!/usr/bin/env python

# Demonstrate vtkDistancePolyDataFilter with signed distance, negated
# distance, and direction computation on two half-spheres, rendering
# displacement arrows via vtkGlyph3DMapper.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDistancePolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create two half-spheres
sphere_0 = vtkSphereSource()
sphere_0.SetRadius(20.0)
sphere_0.SetStartTheta(180.0)
sphere_0.SetPhiResolution(11)
sphere_0.SetThetaResolution(11)
sphere_0.SetCenter(0.0, 0.0, 0.0)
sphere_0.Update()

sphere_1 = vtkSphereSource()
sphere_1.SetRadius(20.0)
sphere_1.SetStartTheta(180.0)
sphere_1.SetPhiResolution(11)
sphere_1.SetThetaResolution(11)
sphere_1.SetCenter(6.0, 1.0, 2.0)
sphere_1.Update()

# Compute displacement with signed distance and direction
displacement_filter = vtkDistancePolyDataFilter()
displacement_filter.SetInputConnection(0, sphere_0.GetOutputPort())
displacement_filter.SetInputConnection(1, sphere_1.GetOutputPort())
displacement_filter.SignedDistanceOn()
displacement_filter.NegateDistanceOn()
displacement_filter.ComputeDirectionOn()
displacement_filter.Update()

# Get scalar range for symmetric coloring
scalar_range = displacement_filter.GetOutput().GetPointData().GetScalars().GetRange()
lim = max(abs(scalar_range[0]), abs(scalar_range[1]))

# Sphere 0 (transparent)
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sphere_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetOpacity(0.2)

# Sphere 1 (wireframe)
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(sphere_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(0.0, 0.5, 0.0)
actor_1.GetProperty().SetRepresentationToWireframe()

# Arrow glyphs showing displacement
arrow_source = vtkArrowSource()

glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputConnection(displacement_filter.GetOutputPort())
glyph_mapper.SetSourceConnection(arrow_source.GetOutputPort())
glyph_mapper.SetScaleArray("Distance")
glyph_mapper.SetScalarRange(-lim, lim)
glyph_mapper.ScalingOn()
glyph_mapper.SetScaleMode(vtkGlyph3DMapper.SCALE_BY_MAGNITUDE)
glyph_mapper.SetColorModeToMapScalars()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Scalar bar
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(glyph_mapper.GetLookupTable())
scalar_bar.SetTitle("Distance")
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetTextPad(4)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.75, 0.75, 0.75)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(glyph_actor)
renderer.AddViewProp(scalar_bar)

# Window
render_window = vtkRenderWindow()
render_window.SetWindowName("distance polydata signed")
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
