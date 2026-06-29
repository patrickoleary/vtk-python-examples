#!/usr/bin/env python
# Demonstrate trackball camera interaction style on a spiked sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()

# Sphere source
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
banana_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("banana", banana_rgb)
sphere_actor.GetProperty().SetDiffuseColor(banana_rgb)
sphere_actor.GetProperty().SetSpecular(0.4)
sphere_actor.GetProperty().SetSpecularPower(20)

# Spikes via cone glyphs on sphere normals
cone = vtkConeSource()
cone.SetResolution(20)

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

spike_actor = vtkActor()
spike_actor.SetMapper(spike_mapper)
tomato_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato_rgb)
spike_actor.GetProperty().SetDiffuseColor(tomato_rgb)
spike_actor.GetProperty().SetSpecular(0.4)
spike_actor.GetProperty().SetSpecularPower(20)

# Rendering
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(spike_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("style trackball camera")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetDesiredUpdateRate(0.00001)

renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Zoom(1.4)
camera.Azimuth(30)
camera.Elevation(30)

interactor.Initialize()
interactor.Start()
