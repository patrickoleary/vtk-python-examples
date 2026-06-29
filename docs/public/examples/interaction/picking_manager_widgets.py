#!/usr/bin/env python
# Demonstrate vtkPickingManager with balloon, box, and implicit plane widgets.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkClipPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkCylinderSource, vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkBalloonRepresentation,
    vtkBalloonWidget,
    vtkBoxWidget,
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- BALLOON SOURCES ---
sphere_source = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

cylinder_source = vtkCylinderSource()
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.AddPosition(5, 0, 0)

cone_source = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.AddPosition(0, 5, 0)

# --- BOX WIDGET SOURCES ---
cone_box = vtkConeSource()
cone_box.SetResolution(6)

sphere_box = vtkSphereSource()
sphere_box.SetThetaResolution(8)
sphere_box.SetPhiResolution(8)
sphere_box.SetCenter(5, 5, 0)

glyph_box = vtkGlyph3D()
glyph_box.SetInputConnection(sphere_box.GetOutputPort())
glyph_box.SetSourceData(cone_box.GetOutput())
glyph_box.SetVectorModeToUseNormal()
glyph_box.SetScaleModeToScaleByVector()
glyph_box.SetScaleFactor(0.25)

append_box = vtkAppendPolyData()
append_box.AddInputData(glyph_box.GetOutput())
append_box.AddInputData(sphere_box.GetOutput())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(append_box.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)

# --- IMPLICIT PLANE SOURCES ---
sphere_imp = vtkSphereSource()
cone_imp = vtkConeSource()

glyph_imp = vtkGlyph3D()
glyph_imp.SetInputConnection(sphere_imp.GetOutputPort())
glyph_imp.SetSourceConnection(cone_imp.GetOutputPort())
glyph_imp.SetVectorModeToUseNormal()
glyph_imp.SetScaleModeToScaleByVector()
glyph_imp.SetScaleFactor(0.25)
glyph_imp.Update()

append_imp = vtkAppendPolyData()
append_imp.AddInputData(glyph_imp.GetOutput())
append_imp.AddInputData(sphere_imp.GetOutput())

mace_mapper_imp = vtkPolyDataMapper()
mace_mapper_imp.SetInputConnection(append_imp.GetOutputPort())

mace_actor_imp = vtkActor()
mace_actor_imp.SetMapper(mace_mapper_imp)
mace_actor_imp.AddPosition(0, 0, 0)
mace_actor_imp.VisibilityOn()

# Clip the mace with a plane
plane = vtkPlane()

clipper = vtkClipPolyData()
clipper.SetInputConnection(append_imp.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(clipper.GetOutputPort())

select_actor = vtkActor()
select_actor.SetMapper(select_mapper)
select_actor.GetProperty().SetColor(0, 1, 0)
select_actor.VisibilityOff()
select_actor.AddPosition(0, 0, 0)
select_actor.SetScale(1.01, 1.01, 1.01)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cylinder_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(mace_actor_imp)
renderer.AddActor(select_actor)
renderer.AddActor(mace_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("picking manager widgets")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor_style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(interactor_style)


# Callback to toggle picking manager with Ctrl, optimization with 'o'
def enable_manager_callback(caller, event_string):
    key_sym = caller.GetKeySym()
    if key_sym in ("Control_L", "Control_R") and caller.GetPickingManager():
        pm = caller.GetPickingManager()
        if not pm.GetEnabled():
            print("PickingManager ON !")
            pm.EnabledOn()
        else:
            print("PickingManager OFF !")
            pm.EnabledOff()
    elif key_sym == "o" and caller.GetPickingManager():
        pm = caller.GetPickingManager()
        if not pm.GetOptimizeOnInteractorEvents():
            print("Optimization on Interactor events ON !")
            pm.SetOptimizeOnInteractorEvents(True)
        else:
            print("Optimization on Interactor events OFF !")
            pm.SetOptimizeOnInteractorEvents(False)


interactor.AddObserver("KeyPressEvent", enable_manager_callback)


# Callback for implicit plane interaction
def imp_plane_callback(caller, event_string):
    plane_rep = caller.GetRepresentation()
    plane_rep.GetPlane(plane)
    select_actor.VisibilityOn()


# Prop picker callback for balloon
def balloon_pick_callback(caller, event_string):
    prop = caller.GetViewProp()
    if prop is not None:
        balloon_widget.UpdateBalloonString(prop, "Picked")


# Widget: balloon
balloon_rep = vtkBalloonRepresentation()
balloon_rep.SetBalloonLayoutToImageRight()

balloon_widget = vtkBalloonWidget()
balloon_widget.SetInteractor(interactor)
balloon_widget.SetRepresentation(balloon_rep)
balloon_widget.AddBalloon(sphere_actor, "This is a sphere")
balloon_widget.AddBalloon(cylinder_actor, "This is a\ncylinder")
balloon_widget.AddBalloon(cone_actor, "This is a\ncone,\na really big.")
balloon_widget.On()

picker = vtkPropPicker()
picker.AddObserver("PickEvent", balloon_pick_callback)
interactor.SetPicker(picker)

# Widget: box
box_widget = vtkBoxWidget()
box_widget.SetInteractor(interactor)
box_widget.SetPlaceFactor(1.25)
box_widget.SetProp3D(mace_actor)
box_widget.PlaceWidget()
box_widget.On()

# Widget: first implicit plane (green edge)
imp_plane_rep = vtkImplicitPlaneRepresentation()
imp_plane_rep.SetPlaceFactor(1.0)
imp_plane_rep.SetOutlineTranslation(False)
imp_plane_rep.SetScaleEnabled(0)
imp_plane_rep.PlaceWidget(glyph_imp.GetOutput().GetBounds())
imp_plane_rep.SetEdgeColor(0.0, 1.0, 0.0)
imp_plane_rep.SetNormal(1, 0, 1)

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(imp_plane_rep)
plane_widget.AddObserver("InteractionEvent", imp_plane_callback)
plane_widget.AddObserver("UpdateEvent", imp_plane_callback)
plane_widget.On()

# Widget: second implicit plane (red edge)
imp_plane_rep_2 = vtkImplicitPlaneRepresentation()
imp_plane_rep_2.SetOutlineTranslation(False)
imp_plane_rep_2.SetScaleEnabled(0)
imp_plane_rep_2.SetPlaceFactor(1.0)
imp_plane_rep_2.PlaceWidget(glyph_imp.GetOutput().GetBounds())
imp_plane_rep_2.SetEdgeColor(1.0, 0.0, 0.0)

plane_widget_2 = vtkImplicitPlaneWidget2()
plane_widget_2.SetInteractor(interactor)
plane_widget_2.SetRepresentation(imp_plane_rep_2)
plane_widget_2.On()

# Scene
renderer.ResetCamera((-2, 7, -2, 7, -1, 1))

interactor.Initialize()
interactor.Start()
