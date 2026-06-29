#!/usr/bin/env python
# Demonstrate vtkMagnifierWidget and vtkMagnifierRepresentation on a mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkFeatureEdges,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkMagnifierRepresentation,
    vtkMagnifierWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sources
resolution = 32

sphere = vtkSphereSource()
sphere.SetThetaResolution(resolution)
sphere.SetPhiResolution(int(resolution / 2))

cone = vtkConeSource()
cone.SetResolution(int(resolution / 4))

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleFactor(0.1)

edges = vtkFeatureEdges()
edges.SetInputConnection(sphere.GetOutputPort())
edges.ExtractAllEdgeTypesOff()
edges.ManifoldEdgesOn()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

spike_actor = vtkActor()
spike_actor.SetMapper(spike_mapper)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(edges.GetOutputPort())
edge_mapper.ScalarVisibilityOff()

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(1, 0, 0)

# Renderer (two viewports)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.AddActor(sphere_actor)
renderer_0.AddActor(spike_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.AddActor(sphere_actor)
renderer_1.AddActor(spike_actor)
renderer_1.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("magnifier widget")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback to adjust magnification factor with +/- keys
def change_mag(widget, event_string):
    if interactor.GetKeyCode() == "+":
        magnification_factor = mag_rep.GetMagnificationFactor() + 1
    else:
        magnification_factor = mag_rep.GetMagnificationFactor() - 1
    mag_rep.SetMagnificationFactor(magnification_factor)


# Widget
mag_rep = vtkMagnifierRepresentation()
mag_rep.SetRenderer(renderer_0)
mag_rep.GetMagnificationRenderer().SetBackground(0.8, 0.8, 0.8)
mag_rep.BorderOn()
mag_rep.GetBorderProperty().SetColor(0, 1, 0)
mag_rep.AddViewProp(sphere_actor)
mag_rep.AddViewProp(edge_actor)

mag_widget = vtkMagnifierWidget()
mag_widget.SetInteractor(interactor)
mag_widget.SetRepresentation(mag_rep)
mag_widget.AddObserver("WidgetValueChangedEvent", change_mag)
mag_widget.On()

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
