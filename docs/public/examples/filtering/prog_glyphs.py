#!/usr/bin/env python

# Demonstrate vtkProgrammableGlyphFilter by placing superquadric glyphs
# on a plane, varying roundness parameters based on point position.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableGlyphFilter
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkSuperquadricSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 6

# Plane with elevation coloring
plane = vtkPlaneSource()
plane.SetResolution(res, res)

colors = vtkElevationFilter()
colors.SetInputConnection(plane.GetOutputPort())
colors.SetLowPoint(-0.25, -0.25, -0.25)
colors.SetHighPoint(0.25, 0.25, 0.25)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(colors.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetRepresentationToWireframe()

# Superquadric glyph source
superquadric_source = vtkSuperquadricSource()
superquadric_source.Update()

# Programmable glyph filter.
# The def is required by vtkProgrammableGlyphFilter.SetGlyphMethod().
glypher = vtkProgrammableGlyphFilter()
glypher.SetInputConnection(colors.GetOutputPort())
glypher.SetSourceData(superquadric_source.GetOutput())


def glyph():
    x, y, z = glypher.GetPoint()
    length = glypher.GetInput(0).GetLength()
    scale = length / (2.0 * res)
    superquadric_source.SetScale(scale, scale, scale)
    superquadric_source.SetCenter(x, y, z)
    superquadric_source.SetPhiRoundness(abs(x) * 5.0)
    superquadric_source.SetThetaRoundness(abs(y) * 5.0)
    superquadric_source.Update()


glypher.SetGlyphMethod(glyph)

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glypher.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("prog glyphs")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
