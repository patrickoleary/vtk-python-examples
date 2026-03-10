#!/usr/bin/env python

# Clip geometry using boolean textures and two implicit quadric functions.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkImplicitTextureCoords
from vtkmodules.vtkImagingHybrid import vtkBooleanTexture
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)
misty_rose_rgb = (1.0, 0.894, 0.882)

# Boolean texture region definitions
SOLID = [255, 255]
CLEAR = [255, 0]
EDGE = [0, 255]

# Grid positions for the 16 boolean texture cases (4x4 layout)
POSITIONS = [
    [-4, 4, 0], [-2, 4, 0], [0, 4, 0], [2, 4, 0],
    [-4, 2, 0], [-2, 2, 0], [0, 2, 0], [2, 2, 0],
    [-4, 0, 0], [-2, 0, 0], [0, 0, 0], [2, 0, 0],
    [-4, -2, 0], [-2, -2, 0], [0, -2, 0], [2, -2, 0],
]

# Boolean texture case definitions: each row is
# [InIn, OutIn, InOut, OutOut, OnOn, OnIn, OnOut, InOn, OutOn]
CASES = [
    [SOLID, SOLID, SOLID, SOLID, SOLID, SOLID, SOLID, SOLID, SOLID],
    [CLEAR, SOLID, SOLID, SOLID, EDGE, EDGE, SOLID, EDGE, SOLID],
    [SOLID, CLEAR, SOLID, SOLID, EDGE, EDGE, SOLID, SOLID, EDGE],
    [CLEAR, CLEAR, SOLID, SOLID, EDGE, CLEAR, SOLID, EDGE, EDGE],
    [SOLID, SOLID, CLEAR, SOLID, EDGE, SOLID, EDGE, EDGE, SOLID],
    [CLEAR, SOLID, CLEAR, SOLID, EDGE, EDGE, EDGE, CLEAR, SOLID],
    [SOLID, CLEAR, CLEAR, SOLID, EDGE, EDGE, EDGE, EDGE, EDGE],
    [CLEAR, CLEAR, CLEAR, SOLID, EDGE, CLEAR, EDGE, CLEAR, EDGE],
    [SOLID, SOLID, SOLID, CLEAR, EDGE, SOLID, EDGE, SOLID, EDGE],
    [CLEAR, SOLID, SOLID, CLEAR, EDGE, EDGE, EDGE, EDGE, EDGE],
    [SOLID, CLEAR, SOLID, CLEAR, EDGE, EDGE, EDGE, SOLID, CLEAR],
    [CLEAR, CLEAR, SOLID, CLEAR, EDGE, CLEAR, EDGE, EDGE, CLEAR],
    [SOLID, SOLID, CLEAR, CLEAR, EDGE, SOLID, CLEAR, EDGE, EDGE],
    [CLEAR, SOLID, CLEAR, CLEAR, EDGE, EDGE, CLEAR, CLEAR, EDGE],
    [SOLID, CLEAR, CLEAR, CLEAR, EDGE, EDGE, CLEAR, EDGE, CLEAR],
    [CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR],
]

# Quadrics: define two elliptical cylinders as the R and S implicit functions
quadric1 = vtkQuadric()
quadric1.SetCoefficients(1, 2, 0, 0, 0, 0, 0, 0, 0, -0.07)

quadric2 = vtkQuadric()
quadric2.SetCoefficients(2, 1, 0, 0, 0, 0, 0, 0, 0, -0.07)

# Source: a single sphere shared by all 16 actors
sphere = vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)

# ImplicitTextureCoords: generate 2D texture coordinates from the two quadrics
tcoords = vtkImplicitTextureCoords()
tcoords.SetInputConnection(sphere.GetOutputPort())
tcoords.SetRFunction(quadric1)
tcoords.SetSFunction(quadric2)

# Mapper: shared by all 16 actors
mapper = vtkDataSetMapper()
mapper.SetInputConnection(tcoords.GetOutputPort())

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray_rgb)

# Create 16 actors, one for each boolean texture case
for i in range(16):
    case = CASES[i]
    boolean_texture = vtkBooleanTexture()
    boolean_texture.SetXSize(64)
    boolean_texture.SetYSize(64)
    boolean_texture.SetThickness(0)
    boolean_texture.SetInIn(case[0])
    boolean_texture.SetOutIn(case[1])
    boolean_texture.SetInOut(case[2])
    boolean_texture.SetOutOut(case[3])
    boolean_texture.SetOnOn(case[4])
    boolean_texture.SetOnIn(case[5])
    boolean_texture.SetOnOut(case[6])
    boolean_texture.SetInOn(case[7])
    boolean_texture.SetOutOn(case[8])

    texture = vtkTexture()
    texture.SetInputConnection(boolean_texture.GetOutputPort())
    texture.InterpolateOff()
    texture.RepeatOff()

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
    actor.SetPosition(POSITIONS[i])
    actor.SetScale(2.0, 2.0, 2.0)
    actor.GetProperty().SetColor(misty_rose_rgb)
    renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextureCutQuadric")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
