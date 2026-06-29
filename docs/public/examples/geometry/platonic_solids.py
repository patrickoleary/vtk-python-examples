#!/usr/bin/env python

# Demonstrate the five Platonic solids from vtkPlatonicSolidSource with
# a color lookup table applied to each face.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkPlatonicSolidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()

# Tetrahedron
tetrahedron = vtkPlatonicSolidSource()
tetrahedron.SetSolidTypeToTetrahedron()
tetrahedron_mapper = vtkPolyDataMapper()
tetrahedron_mapper.SetInputConnection(tetrahedron.GetOutputPort())
tetrahedron_actor = vtkActor()
tetrahedron_actor.SetMapper(tetrahedron_mapper)

# Cube
cube = vtkPlatonicSolidSource()
cube.SetSolidTypeToCube()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.AddPosition(2.0, 0, 0)

# Octahedron
octahedron = vtkPlatonicSolidSource()
octahedron.SetSolidTypeToOctahedron()
octahedron_mapper = vtkPolyDataMapper()
octahedron_mapper.SetInputConnection(octahedron.GetOutputPort())
octahedron_actor = vtkActor()
octahedron_actor.SetMapper(octahedron_mapper)
octahedron_actor.AddPosition(4.0, 0, 0)

# Icosahedron
icosahedron = vtkPlatonicSolidSource()
icosahedron.SetSolidTypeToIcosahedron()
icosahedron_mapper = vtkPolyDataMapper()
icosahedron_mapper.SetInputConnection(icosahedron.GetOutputPort())
icosahedron_actor = vtkActor()
icosahedron_actor.SetMapper(icosahedron_mapper)
icosahedron_actor.AddPosition(6.0, 0, 0)

# Dodecahedron
dodecahedron = vtkPlatonicSolidSource()
dodecahedron.SetSolidTypeToDodecahedron()
dodecahedron_mapper = vtkPolyDataMapper()
dodecahedron_mapper.SetInputConnection(dodecahedron.GetOutputPort())
dodecahedron_actor = vtkActor()
dodecahedron_actor.SetMapper(dodecahedron_mapper)
dodecahedron_actor.AddPosition(8.0, 0, 0)

# Lookup table with named colors for each face
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfColors(20)
lookup_table.Build()

color_names = [
    "red", "lime", "yellow", "blue", "magenta",
    "cyan", "spring_green", "lavender", "mint_cream", "violet",
    "ivory_black", "coral", "pink", "salmon", "sepia",
    "carrot", "gold", "forest_green", "turquoise", "plum",
]
for i, name in enumerate(color_names):
    rgba = [0.0, 0.0, 0.0, 1.0]
    named_colors.GetColor(name, rgba)
    lookup_table.SetTableValue(i, rgba)

lookup_table.SetTableRange(0, 19)

tetrahedron_mapper.SetLookupTable(lookup_table)
tetrahedron_mapper.SetScalarRange(0, 19)
cube_mapper.SetLookupTable(lookup_table)
cube_mapper.SetScalarRange(0, 19)
octahedron_mapper.SetLookupTable(lookup_table)
octahedron_mapper.SetScalarRange(0, 19)
icosahedron_mapper.SetLookupTable(lookup_table)
icosahedron_mapper.SetScalarRange(0, 19)
dodecahedron_mapper.SetLookupTable(lookup_table)
dodecahedron_mapper.SetScalarRange(0, 19)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(tetrahedron_actor)
renderer.AddActor(cube_actor)
renderer.AddActor(octahedron_actor)
renderer.AddActor(icosahedron_actor)
renderer.AddActor(dodecahedron_actor)

rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("black", rgb)
renderer.SetBackground(rgb)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 150)
render_window.SetWindowName("platonic solids")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(3.89696, 7.20771, 1.44123)
camera.SetFocalPoint(3.96132, 0, 0)
camera.SetViewUp(-0.0079335, 0.196002, -0.980571)
camera.SetClippingRange(5.42814, 9.78848)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
