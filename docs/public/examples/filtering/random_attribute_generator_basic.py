#!/usr/bin/env python

# Generate random attributes on a plane using vtkRandomAttributeGenerator
# and visualize with tensor glyphs (spheres scaled by random tensors).

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkTensorGlyph,
)
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Force a starting random value
ra_math = vtkMath()
ra_math.RandomSeed(6)

# Generate random attributes on a plane
ps = vtkPlaneSource()
ps.SetXResolution(10)
ps.SetYResolution(10)

ag = vtkRandomAttributeGenerator()
ag.SetInputConnection(ps.GetOutputPort())
ag.GenerateAllDataOn()

# Sphere source for tensor glyphs
ss = vtkSphereSource()
ss.SetPhiResolution(16)
ss.SetThetaResolution(32)

# Tensor glyph
tg = vtkTensorGlyph()
tg.SetInputConnection(ag.GetOutputPort())
tg.SetSourceConnection(ss.GetOutputPort())
tg.SetInputArrayToProcess(1, 0, 0, 0, "RandomPointArray")
tg.SetScaleFactor(0.1)
tg.SetMaxScaleFactor(10)
tg.ClampScalingOn()

# Compute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(tg.GetOutputPort())

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(normals.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Show the base plane
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(ps.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.AddActor(plane_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("random attribute generator basic")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
