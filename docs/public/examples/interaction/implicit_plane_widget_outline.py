#!/usr/bin/env python
# Demonstrate vtkImplicitPlaneWidget2 with programmatic origin and bounds changes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Plane origins to cycle through on timer events
plane_origins = [[0, 10, 0], [10, 0, 0], [0, 0, 0]]
count = [0]

# Sources
sphere = vtkSphereSource()
cone = vtkConeSource()

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
glyph.Update()

append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(glyph.GetOutputPort())
append_filter.AddInputConnection(sphere.GetOutputPort())

plane = vtkPlane()
clipper = vtkClipPolyData()
clipper.SetInputConnection(append_filter.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

# Mapper + Actor: mace
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append_filter.GetOutputPort())

mace_actor = vtkLODActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Mapper + Actor: clipped selection
select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkLODActor()
select_actor.SetMapper(select_mapper)
select_actor.GetProperty().SetColor(0, 1, 0)
select_actor.VisibilityOff()
select_actor.SetScale(1.01, 1.01, 1.01)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.AddActor(select_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit plane widget outline")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
plane_rep = vtkImplicitPlaneRepresentation()
plane_rep.SetPlaceFactor(1.25)
plane_rep.PlaceWidget(glyph.GetOutput().GetBounds())

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(plane_rep)
plane_widget.SetEnabled(1)


# Timer callback to cycle the widget origin and bounds
def timer_callback(caller, event_string):
    count[0] += 1
    origin = plane_origins[count[0] % 3]
    plane_rep.SetOrigin(origin)
    bounds = [0.0] * 6
    for i in range(3):
        bounds[2 * i] = origin[i] - 0.625
        bounds[2 * i + 1] = origin[i] + 0.625
    plane_rep.PlaceWidget(bounds)
    renderer.ResetCamera()
    plane_widget.Render()
    print(f"Origin of the widget = ({origin[0]} {origin[1]} {origin[2]})")
    print(f"Bounds of the widget = ({bounds[0]} {bounds[1]} {bounds[2]} {bounds[3]} {bounds[4]} {bounds[5]})")


interactor.AddObserver("TimerEvent", timer_callback)
timer_id = interactor.CreateRepeatingTimer(2000)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
