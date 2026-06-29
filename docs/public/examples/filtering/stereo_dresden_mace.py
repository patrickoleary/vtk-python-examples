#!/usr/bin/env python

# Test stereo rendering with Dresden mode on a spiked sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Sphere with spike glyphs
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkLODActor()
sphere_actor.SetMapper(sphere_mapper)

cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

spike_actor = vtkLODActor()
spike_actor.SetMapper(spike_mapper)

# Set user matrix on spike actor
matrix = vtkMatrix4x4()
spike_actor.SetUserMatrix(matrix)

# Renderer with stereo
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(spike_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("stereo dresden mace")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.StereoCapableWindowOn()
render_window.SetStereoTypeToDresden()
render_window.StereoRenderOn()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

interactor.Initialize()
interactor.Start()
