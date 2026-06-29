#!/usr/bin/env python
# Demonstrate vtkSeedWidget with heterogeneous handle representations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkGlyphSource2D, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkOrientedPolygonalHandleRepresentation3D,
    vtkPointHandleRepresentation3D,
    vtkSeedRepresentation,
    vtkSeedWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
sphere_source = vtkSphereSource()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seed widget non uniform representations")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback prints seed count on placement
def place_point_callback(caller, event_string):
    print(f"Point placed, total of: {seed_rep.GetNumberOfSeeds()}")


# Widget
glyphs = vtkGlyphSource2D()

seed_rep = vtkSeedRepresentation()

seed_widget = vtkSeedWidget()
seed_widget.SetInteractor(interactor)
seed_widget.SetRepresentation(seed_rep)
seed_widget.AddObserver("PlacePointEvent", place_point_callback)
seed_widget.EnabledOn()

# Exit interactive placement mode
seed_widget.CompleteInteraction()

# Seed 1: triangle glyph, oriented polygonal handle
handle_rep_1 = vtkOrientedPolygonalHandleRepresentation3D()
glyphs.SetGlyphTypeToTriangle()
glyphs.SetScale(0.1)
glyphs.Update()
handle_rep_1.SetHandle(glyphs.GetOutput())
handle_rep_1.GetProperty().SetColor(1, 0, 0)
handle_rep_1.SetLabelVisibility(1)
handle_rep_1.SetLabelText("Seed-1")
seed_rep.SetHandleRepresentation(handle_rep_1)
handle_widget_1 = seed_widget.CreateNewHandle()
handle_widget_1.SetEnabled(1)
seed_rep.GetHandleRepresentation(0).SetWorldPosition((0.3, 0.3, 0.6))

# Seed 2: 3D point crosshair handle
handle_rep_2 = vtkPointHandleRepresentation3D()
handle_rep_2.GetProperty().SetColor(0, 1, 0)
seed_rep.SetHandleRepresentation(handle_rep_2)
handle_widget_2 = seed_widget.CreateNewHandle()
handle_widget_2.SetEnabled(1)
seed_rep.GetHandleRepresentation(1).SetWorldPosition((0.3, -0.3, 0.6))

# Seed 3: thick cross glyph, oriented polygonal handle
handle_rep_3 = vtkOrientedPolygonalHandleRepresentation3D()
glyphs.SetGlyphTypeToThickCross()
glyphs.Update()
handle_rep_3.SetHandle(glyphs.GetOutput())
handle_rep_3.GetProperty().SetColor(1, 1, 0)
handle_rep_3.SetLabelVisibility(1)
handle_rep_3.SetLabelText("Seed-2")
seed_rep.SetHandleRepresentation(handle_rep_3)
handle_widget_3 = seed_widget.CreateNewHandle()
handle_widget_3.SetEnabled(1)
seed_rep.GetHandleRepresentation(2).SetWorldPosition((-0.3, 0.3, 0.6))

# Seed 4: diamond glyph, passive (does not respond to interaction)
handle_rep_4 = vtkOrientedPolygonalHandleRepresentation3D()
glyphs.SetGlyphTypeToDiamond()
glyphs.Update()
handle_rep_4.SetHandle(glyphs.GetOutput())
handle_rep_4.GetProperty().SetColor(1, 0, 1)
handle_rep_4.SetLabelVisibility(1)
handle_rep_4.SetLabelText("Passive\nSeed")
seed_rep.SetHandleRepresentation(handle_rep_4)
handle_widget_4 = seed_widget.CreateNewHandle()
handle_widget_4.SetEnabled(1)
handle_widget_4.ProcessEventsOff()
seed_rep.GetHandleRepresentation(3).SetWorldPosition((-0.3, -0.3, 0.6))

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
