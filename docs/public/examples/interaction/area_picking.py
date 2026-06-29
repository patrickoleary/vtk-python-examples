#!/usr/bin/env python

# Area picking with rubber-band selection. Press 'r' to enter rubber-band
# mode, then drag a rectangle to select actors. Selected actors are
# highlighted in red; non-selected actors are restored to their original color.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandPick
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAreaPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
steel_blue_rgb = (0.275, 0.510, 0.706)
white_rgb = (1.0, 1.0, 1.0)

def pick_callback(obj, event):
    """Callback invoked when an area pick completes."""
    picker = obj
    props = picker.GetProp3Ds()
    props.InitTraversal()

    # Reset all actors to original color first
    actors = renderer.GetActors()
    actors.InitTraversal()
    for _ in range(actors.GetNumberOfItems()):
        a = actors.GetNextActor()
        a.GetProperty().SetColor(a.GetProperty().GetDiffuseColor())

    # Highlight picked actors in red
    num_picked = props.GetNumberOfItems()
    for _ in range(num_picked):
        prop = props.GetNextProp3D()
        if prop:
            prop.GetProperty().SetColor(red_rgb)

    if num_picked > 0:
        print(f"Picked {num_picked} actor(s)")

    renderer.GetRenderWindow().Render()


# Source: 20 randomly placed spheres
source_0 = vtkSphereSource()
source_0.SetRadius(0.3936)
source_0.SetCenter(0.9463, -4.8686, 3.0200)
source_0.SetPhiResolution(11)
source_0.SetThetaResolution(21)

source_1 = vtkSphereSource()
source_1.SetRadius(0.3399)
source_1.SetCenter(0.9038, 0.7512, -4.7596)
source_1.SetPhiResolution(11)
source_1.SetThetaResolution(21)

source_2 = vtkSphereSource()
source_2.SetRadius(0.4566)
source_2.SetCenter(3.2573, -3.7712, -3.2553)
source_2.SetPhiResolution(11)
source_2.SetThetaResolution(21)

source_3 = vtkSphereSource()
source_3.SetRadius(0.4770)
source_3.SetCenter(-1.2821, 1.9590, 4.0833)
source_3.SetPhiResolution(11)
source_3.SetThetaResolution(21)

source_4 = vtkSphereSource()
source_4.SetRadius(0.5152)
source_4.SetCenter(-4.9000, -3.4790, -1.0889)
source_4.SetPhiResolution(11)
source_4.SetThetaResolution(21)

source_5 = vtkSphereSource()
source_5.SetRadius(0.5569)
source_5.SetCenter(4.6296, -0.6932, -0.9068)
source_5.SetPhiResolution(11)
source_5.SetThetaResolution(21)

source_6 = vtkSphereSource()
source_6.SetRadius(0.7914)
source_6.SetCenter(-4.0024, 2.1089, 3.6577)
source_6.SetPhiResolution(11)
source_6.SetThetaResolution(21)

source_7 = vtkSphereSource()
source_7.SetRadius(0.4710)
source_7.SetCenter(1.7914, -2.0026, 2.6714)
source_7.SetPhiResolution(11)
source_7.SetThetaResolution(21)

source_8 = vtkSphereSource()
source_8.SetRadius(0.6590)
source_8.SetCenter(2.3649, -2.8627, -2.8903)
source_8.SetPhiResolution(11)
source_8.SetThetaResolution(21)

source_9 = vtkSphereSource()
source_9.SetRadius(0.6184)
source_9.SetCenter(4.8909, 1.8100, 0.0388)
source_9.SetPhiResolution(11)
source_9.SetThetaResolution(21)

source_10 = vtkSphereSource()
source_10.SetRadius(0.6126)
source_10.SetCenter(-3.0675, -4.7939, -0.3801)
source_10.SetPhiResolution(11)
source_10.SetThetaResolution(21)

source_11 = vtkSphereSource()
source_11.SetRadius(0.3947)
source_11.SetCenter(3.1209, 2.5694, 4.4646)
source_11.SetPhiResolution(11)
source_11.SetThetaResolution(21)

source_12 = vtkSphereSource()
source_12.SetRadius(0.4874)
source_12.SetCenter(1.4878, -4.3480, 3.5020)
source_12.SetPhiResolution(11)
source_12.SetThetaResolution(21)

source_13 = vtkSphereSource()
source_13.SetRadius(0.6036)
source_13.SetCenter(1.6633, -4.3536, -0.9132)
source_13.SetPhiResolution(11)
source_13.SetThetaResolution(21)

source_14 = vtkSphereSource()
source_14.SetRadius(0.3425)
source_14.SetCenter(4.9689, 1.6280, 1.6473)
source_14.SetPhiResolution(11)
source_14.SetThetaResolution(21)

source_15 = vtkSphereSource()
source_15.SetRadius(0.5720)
source_15.SetCenter(-4.9156, 2.6753, 4.3821)
source_15.SetPhiResolution(11)
source_15.SetThetaResolution(21)

source_16 = vtkSphereSource()
source_16.SetRadius(0.5177)
source_16.SetCenter(-2.2901, 0.4258, -3.0589)
source_16.SetPhiResolution(11)
source_16.SetThetaResolution(21)

source_17 = vtkSphereSource()
source_17.SetRadius(0.4666)
source_17.SetCenter(-2.8213, 2.0836, -1.1401)
source_17.SetPhiResolution(11)
source_17.SetThetaResolution(21)

source_18 = vtkSphereSource()
source_18.SetRadius(0.6067)
source_18.SetCenter(-2.3739, 1.6092, -3.5032)
source_18.SetPhiResolution(11)
source_18.SetThetaResolution(21)

source_19 = vtkSphereSource()
source_19.SetRadius(0.6607)
source_19.SetCenter(4.7403, 0.4194, -0.6865)
source_19.SetPhiResolution(11)
source_19.SetThetaResolution(21)

# Mapper: sphere 0
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(source_0.GetOutputPort())
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(0.880, 0.647, 0.707)
actor_0.GetProperty().SetDiffuse(0.8)
actor_0.GetProperty().SetSpecular(0.5)
actor_0.GetProperty().SetSpecularColor(white_rgb)
actor_0.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 1
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(source_1.GetOutputPort())
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(0.814, 0.754, 0.565)
actor_1.GetProperty().SetDiffuse(0.8)
actor_1.GetProperty().SetSpecular(0.5)
actor_1.GetProperty().SetSpecularColor(white_rgb)
actor_1.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 2
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(source_2.GetOutputPort())
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(0.790, 0.775, 0.562)
actor_2.GetProperty().SetDiffuse(0.8)
actor_2.GetProperty().SetSpecular(0.5)
actor_2.GetProperty().SetSpecularColor(white_rgb)
actor_2.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 3
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(source_3.GetOutputPort())
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetDiffuseColor(0.801, 0.686, 0.730)
actor_3.GetProperty().SetDiffuse(0.8)
actor_3.GetProperty().SetSpecular(0.5)
actor_3.GetProperty().SetSpecularColor(white_rgb)
actor_3.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 4
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(source_4.GetOutputPort())
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetDiffuseColor(0.438, 0.586, 0.831)
actor_4.GetProperty().SetDiffuse(0.8)
actor_4.GetProperty().SetSpecular(0.5)
actor_4.GetProperty().SetSpecularColor(white_rgb)
actor_4.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 5
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(source_5.GetOutputPort())
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetDiffuseColor(0.724, 0.762, 0.512)
actor_5.GetProperty().SetDiffuse(0.8)
actor_5.GetProperty().SetSpecular(0.5)
actor_5.GetProperty().SetSpecularColor(white_rgb)
actor_5.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 6
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(source_6.GetOutputPort())
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetDiffuseColor(0.429, 0.780, 0.598)
actor_6.GetProperty().SetDiffuse(0.8)
actor_6.GetProperty().SetSpecular(0.5)
actor_6.GetProperty().SetSpecularColor(white_rgb)
actor_6.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 7
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(source_7.GetOutputPort())
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetDiffuseColor(0.603, 0.455, 0.850)
actor_7.GetProperty().SetDiffuse(0.8)
actor_7.GetProperty().SetSpecular(0.5)
actor_7.GetProperty().SetSpecularColor(white_rgb)
actor_7.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 8
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(source_8.GetOutputPort())
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetDiffuseColor(0.473, 0.635, 0.759)
actor_8.GetProperty().SetDiffuse(0.8)
actor_8.GetProperty().SetSpecular(0.5)
actor_8.GetProperty().SetSpecularColor(white_rgb)
actor_8.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 9
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(source_9.GetOutputPort())
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetDiffuseColor(0.578, 0.884, 0.543)
actor_9.GetProperty().SetDiffuse(0.8)
actor_9.GetProperty().SetSpecular(0.5)
actor_9.GetProperty().SetSpecularColor(white_rgb)
actor_9.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 10
mapper_10 = vtkPolyDataMapper()
mapper_10.SetInputConnection(source_10.GetOutputPort())
actor_10 = vtkActor()
actor_10.SetMapper(mapper_10)
actor_10.GetProperty().SetDiffuseColor(0.978, 0.678, 0.974)
actor_10.GetProperty().SetDiffuse(0.8)
actor_10.GetProperty().SetSpecular(0.5)
actor_10.GetProperty().SetSpecularColor(white_rgb)
actor_10.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 11
mapper_11 = vtkPolyDataMapper()
mapper_11.SetInputConnection(source_11.GetOutputPort())
actor_11 = vtkActor()
actor_11.SetMapper(mapper_11)
actor_11.GetProperty().SetDiffuseColor(0.676, 0.615, 0.736)
actor_11.GetProperty().SetDiffuse(0.8)
actor_11.GetProperty().SetSpecular(0.5)
actor_11.GetProperty().SetSpecularColor(white_rgb)
actor_11.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 12
mapper_12 = vtkPolyDataMapper()
mapper_12.SetInputConnection(source_12.GetOutputPort())
actor_12 = vtkActor()
actor_12.SetMapper(mapper_12)
actor_12.GetProperty().SetDiffuseColor(0.629, 0.706, 0.624)
actor_12.GetProperty().SetDiffuse(0.8)
actor_12.GetProperty().SetSpecular(0.5)
actor_12.GetProperty().SetSpecularColor(white_rgb)
actor_12.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 13
mapper_13 = vtkPolyDataMapper()
mapper_13.SetInputConnection(source_13.GetOutputPort())
actor_13 = vtkActor()
actor_13.SetMapper(mapper_13)
actor_13.GetProperty().SetDiffuseColor(0.860, 0.950, 0.898)
actor_13.GetProperty().SetDiffuse(0.8)
actor_13.GetProperty().SetSpecular(0.5)
actor_13.GetProperty().SetSpecularColor(white_rgb)
actor_13.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 14
mapper_14 = vtkPolyDataMapper()
mapper_14.SetInputConnection(source_14.GetOutputPort())
actor_14 = vtkActor()
actor_14.SetMapper(mapper_14)
actor_14.GetProperty().SetDiffuseColor(0.736, 0.989, 0.654)
actor_14.GetProperty().SetDiffuse(0.8)
actor_14.GetProperty().SetSpecular(0.5)
actor_14.GetProperty().SetSpecularColor(white_rgb)
actor_14.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 15
mapper_15 = vtkPolyDataMapper()
mapper_15.SetInputConnection(source_15.GetOutputPort())
actor_15 = vtkActor()
actor_15.SetMapper(mapper_15)
actor_15.GetProperty().SetDiffuseColor(0.635, 0.454, 0.850)
actor_15.GetProperty().SetDiffuse(0.8)
actor_15.GetProperty().SetSpecular(0.5)
actor_15.GetProperty().SetSpecularColor(white_rgb)
actor_15.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 16
mapper_16 = vtkPolyDataMapper()
mapper_16.SetInputConnection(source_16.GetOutputPort())
actor_16 = vtkActor()
actor_16.SetMapper(mapper_16)
actor_16.GetProperty().SetDiffuseColor(0.998, 0.612, 0.744)
actor_16.GetProperty().SetDiffuse(0.8)
actor_16.GetProperty().SetSpecular(0.5)
actor_16.GetProperty().SetSpecularColor(white_rgb)
actor_16.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 17
mapper_17 = vtkPolyDataMapper()
mapper_17.SetInputConnection(source_17.GetOutputPort())
actor_17 = vtkActor()
actor_17.SetMapper(mapper_17)
actor_17.GetProperty().SetDiffuseColor(0.769, 0.673, 0.463)
actor_17.GetProperty().SetDiffuse(0.8)
actor_17.GetProperty().SetSpecular(0.5)
actor_17.GetProperty().SetSpecularColor(white_rgb)
actor_17.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 18
mapper_18 = vtkPolyDataMapper()
mapper_18.SetInputConnection(source_18.GetOutputPort())
actor_18 = vtkActor()
actor_18.SetMapper(mapper_18)
actor_18.GetProperty().SetDiffuseColor(0.803, 0.832, 0.419)
actor_18.GetProperty().SetDiffuse(0.8)
actor_18.GetProperty().SetSpecular(0.5)
actor_18.GetProperty().SetSpecularColor(white_rgb)
actor_18.GetProperty().SetSpecularPower(30.0)

# Mapper: sphere 19
mapper_19 = vtkPolyDataMapper()
mapper_19.SetInputConnection(source_19.GetOutputPort())
actor_19 = vtkActor()
actor_19.SetMapper(mapper_19)
actor_19.GetProperty().SetDiffuseColor(0.761, 0.616, 0.598)
actor_19.GetProperty().SetDiffuse(0.8)
actor_19.GetProperty().SetSpecular(0.5)
actor_19.GetProperty().SetSpecularColor(white_rgb)
actor_19.GetProperty().SetSpecularPower(30.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(actor_8)
renderer.AddActor(actor_9)
renderer.AddActor(actor_10)
renderer.AddActor(actor_11)
renderer.AddActor(actor_12)
renderer.AddActor(actor_13)
renderer.AddActor(actor_14)
renderer.AddActor(actor_15)
renderer.AddActor(actor_16)
renderer.AddActor(actor_17)
renderer.AddActor(actor_18)
renderer.AddActor(actor_19)
renderer.SetBackground(steel_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("area picking")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# AreaPicker: select actors within a rectangular region
area_picker = vtkAreaPicker()
area_picker.AddObserver("EndPickEvent", pick_callback)

# Interactor: rubber-band selection style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetPicker(area_picker)

style = vtkInteractorStyleRubberBandPick()
render_window_interactor.SetInteractorStyle(style)

render_window_interactor.Initialize()
render_window_interactor.Start()
