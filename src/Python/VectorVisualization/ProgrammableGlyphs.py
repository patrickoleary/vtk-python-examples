#!/usr/bin/env python

# Generate superquadric glyphs whose roundness varies with position.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
silver = (0.753, 0.753, 0.753)

# Parameters
res = 6

# Source: plane grid colored by elevation
plane = vtkPlaneSource()
plane.SetResolution(res, res)

elev = vtkElevationFilter()
elev.SetInputConnection(plane.GetOutputPort())
elev.SetLowPoint(-0.25, -0.25, -0.25)
elev.SetHighPoint(0.25, 0.25, 0.25)

# Mapper/Actor: wireframe plane
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputData(elev.GetPolyDataOutput())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetRepresentationToWireframe()

# Source: superquadric glyph whose shape is modified per point
squad = vtkSuperquadricSource()

# Filter: programmable glyph filter with per-point callback
glypher = vtkProgrammableGlyphFilter()
glypher.SetInputConnection(elev.GetOutputPort())
glypher.SetSourceConnection(squad.GetOutputPort())


def calc_glyph():
    xyz = glypher.GetPoint()
    length = glypher.GetInput(0).GetLength()
    scale = length / (2.0 * res)
    squad.SetScale(scale, scale, scale)
    squad.SetCenter(xyz)
    squad.SetPhiRoundness(abs(xyz[0]) * 5.0)
    squad.SetThetaRoundness(abs(xyz[1]) * 5.0)


glypher.SetGlyphMethod(calc_glyph)

# Mapper/Actor: superquadric glyphs
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glypher.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(silver)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("ProgrammableGlyphs")
render_window.SetSize(450, 450)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
