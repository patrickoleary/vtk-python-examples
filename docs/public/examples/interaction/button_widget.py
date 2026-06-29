#!/usr/bin/env python
# Demonstrate vtkButtonWidget with textured 3D, 2D, and Prop3D button representations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkEllipticalButtonSource,
    vtkPlatonicSolidSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkButtonWidget,
    vtkProp3DButtonRepresentation,
    vtkTexturedButtonRepresentation,
    vtkTexturedButtonRepresentation2D,
)
from vtkmodules.vtkIOImage import (
    vtkPNGReader,
    vtkTIFFReader,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Load images for button textures
image_1 = vtkTIFFReader()
image_1.SetFileName(os.path.join(data_dir, "beach.tif"))
image_1.SetOrientationType(4)
image_1.Update()

image_2 = vtkPNGReader()
image_2.SetFileName(os.path.join(data_dir, "fran_cut.png"))
image_2.Update()

# Create a mace geometry (sphere + cone glyphs)
sphere = vtkSphereSource()

cone = vtkConeSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
glyph.Update()

apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(apd.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("button widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback prints state and adjusts glyph scale
def button_callback(caller, event_string):
    rep = caller.GetRepresentation()
    state = rep.GetState()
    print(f"State: {state}")
    glyph.SetScaleFactor(0.05 * (1 + state))


# Initialize OpenGL context for textured button representations
render_window.Render()

# --- Button 1: 3D textured button (follow camera) ---
button_1 = vtkEllipticalButtonSource()
button_1.TwoSidedOn()
button_1.SetCircumferentialResolution(24)
button_1.SetShoulderResolution(24)
button_1.SetTextureResolution(24)

rep_1 = vtkTexturedButtonRepresentation()
rep_1.SetNumberOfStates(2)
rep_1.SetButtonTexture(0, image_1.GetOutput())
rep_1.SetButtonTexture(1, image_2.GetOutput())
rep_1.SetButtonGeometryConnection(button_1.GetOutputPort())
rep_1.SetPlaceFactor(1)
rep_1.PlaceWidget([0.6, 0.75, 0.6, 0.75, 0.6, 0.75])
rep_1.FollowCameraOn()

button_widget_1 = vtkButtonWidget()
button_widget_1.SetInteractor(interactor)
button_widget_1.SetRepresentation(rep_1)
button_widget_1.AddObserver("StateChangedEvent", button_callback)
button_widget_1.EnabledOn()

# --- Button 2: 3D textured button (no follow camera, alternative placement) ---
button_2 = vtkEllipticalButtonSource()
button_2.TwoSidedOn()
button_2.SetCircumferentialResolution(24)
button_2.SetShoulderResolution(24)
button_2.SetTextureResolution(24)
button_2.SetWidth(0.65)
button_2.SetHeight(0.45)
button_2.SetTextureStyleToFitImage()

rep_2 = vtkTexturedButtonRepresentation()
rep_2.SetNumberOfStates(2)
rep_2.SetButtonTexture(0, image_1.GetOutput())
rep_2.SetButtonTexture(1, image_2.GetOutput())
rep_2.SetButtonGeometryConnection(button_2.GetOutputPort())
rep_2.SetPlaceFactor(1)
rep_2.PlaceWidget(0.5, [0.0, 0.0, -0.65], [0.0, 0.0, 1.0])
rep_2.FollowCameraOff()

button_widget_2 = vtkButtonWidget()
button_widget_2.SetInteractor(interactor)
button_widget_2.SetRepresentation(rep_2)
button_widget_2.AddObserver("StateChangedEvent", button_callback)
button_widget_2.EnabledOn()

# --- Button 3: 2D textured button (display space) ---
rep_3 = vtkTexturedButtonRepresentation2D()
rep_3.SetNumberOfStates(2)
rep_3.SetButtonTexture(0, image_1.GetOutput())
rep_3.SetButtonTexture(1, image_2.GetOutput())
rep_3.SetPlaceFactor(1)
rep_3.PlaceWidget([25, 65, 50, 200, 0, 0])

button_widget_3 = vtkButtonWidget()
button_widget_3.SetInteractor(interactor)
button_widget_3.SetRepresentation(rep_3)
button_widget_3.AddObserver("StateChangedEvent", button_callback)
button_widget_3.EnabledOn()

# --- Button 4: 2D textured button (world space) ---
rep_4 = vtkTexturedButtonRepresentation2D()
rep_4.SetNumberOfStates(2)
rep_4.SetButtonTexture(0, image_1.GetOutput())
rep_4.SetButtonTexture(1, image_2.GetOutput())
rep_4.SetPlaceFactor(1)
rep_4.PlaceWidget([0.75, 0.0, 0.0], [25, 45])

button_widget_4 = vtkButtonWidget()
button_widget_4.SetInteractor(interactor)
button_widget_4.SetRepresentation(rep_4)
button_widget_4.AddObserver("StateChangedEvent", button_callback)
button_widget_4.EnabledOn()

# --- Button 5: Prop3D button with platonic solids ---
lut = vtkLookupTable()
lut.SetNumberOfColors(20)
lut.Build()
lut.SetTableValue(0, 1, 0, 0, 1)
lut.SetTableValue(1, 0, 1, 0, 1)
lut.SetTableValue(2, 1, 1, 0, 1)
lut.SetTableValue(3, 0, 0, 1, 1)
lut.SetTableValue(4, 1, 0, 1, 1)
lut.SetTableValue(5, 0, 1, 1, 1)
lut.SetTableValue(6, 0.0, 1.0, 0.498, 1.0)
lut.SetTableValue(7, 0.902, 0.902, 0.9804, 1.0)
lut.SetTableValue(8, 0.9608, 1.0, 0.9804, 1.0)
lut.SetTableValue(9, 0.56, 0.37, 0.60, 1.0)
lut.SetTableValue(10, 0.16, 0.14, 0.13, 1.0)
lut.SetTableValue(11, 1.0, 0.498, 0.3137, 1.0)
lut.SetTableValue(12, 1.0, 0.7529, 0.7961, 1.0)
lut.SetTableValue(13, 0.9804, 0.502, 0.4471, 1.0)
lut.SetTableValue(14, 0.37, 0.15, 0.07, 1.0)
lut.SetTableValue(15, 0.93, 0.57, 0.13, 1.0)
lut.SetTableValue(16, 1.0, 0.8431, 0.0, 1.0)
lut.SetTableValue(17, 0.1333, 0.5451, 0.1333, 1.0)
lut.SetTableValue(18, 0.251, 0.8784, 0.8157, 1.0)
lut.SetTableValue(19, 0.8667, 0.6275, 0.8667, 1.0)
lut.SetTableRange(0, 19)

tet = vtkPlatonicSolidSource()
tet.SetSolidTypeToTetrahedron()
tet_mapper = vtkPolyDataMapper()
tet_mapper.SetInputConnection(tet.GetOutputPort())
tet_mapper.SetLookupTable(lut)
tet_mapper.SetScalarRange(0, 19)
tet_actor = vtkActor()
tet_actor.SetMapper(tet_mapper)

cube = vtkPlatonicSolidSource()
cube.SetSolidTypeToCube()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_mapper.SetLookupTable(lut)
cube_mapper.SetScalarRange(0, 19)
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

oct_solid = vtkPlatonicSolidSource()
oct_solid.SetSolidTypeToOctahedron()
oct_mapper = vtkPolyDataMapper()
oct_mapper.SetInputConnection(oct_solid.GetOutputPort())
oct_mapper.SetLookupTable(lut)
oct_mapper.SetScalarRange(0, 19)
oct_actor = vtkActor()
oct_actor.SetMapper(oct_mapper)

ico = vtkPlatonicSolidSource()
ico.SetSolidTypeToIcosahedron()
ico_mapper = vtkPolyDataMapper()
ico_mapper.SetInputConnection(ico.GetOutputPort())
ico_mapper.SetLookupTable(lut)
ico_mapper.SetScalarRange(0, 19)
ico_actor = vtkActor()
ico_actor.SetMapper(ico_mapper)

dode = vtkPlatonicSolidSource()
dode.SetSolidTypeToDodecahedron()
dode_mapper = vtkPolyDataMapper()
dode_mapper.SetInputConnection(dode.GetOutputPort())
dode_mapper.SetLookupTable(lut)
dode_mapper.SetScalarRange(0, 19)
dode_actor = vtkActor()
dode_actor.SetMapper(dode_mapper)

rep_5 = vtkProp3DButtonRepresentation()
rep_5.SetNumberOfStates(5)
rep_5.SetButtonProp(0, tet_actor)
rep_5.SetButtonProp(1, cube_actor)
rep_5.SetButtonProp(2, oct_actor)
rep_5.SetButtonProp(3, ico_actor)
rep_5.SetButtonProp(4, dode_actor)
rep_5.SetPlaceFactor(1)
rep_5.PlaceWidget([0.65, 0.75, -0.75, -0.65, 0.65, 0.75])
rep_5.FollowCameraOn()

button_widget_5 = vtkButtonWidget()
button_widget_5.SetInteractor(interactor)
button_widget_5.SetRepresentation(rep_5)
button_widget_5.AddObserver("StateChangedEvent", button_callback)
button_widget_5.EnabledOn()

interactor.Initialize()
interactor.Start()
