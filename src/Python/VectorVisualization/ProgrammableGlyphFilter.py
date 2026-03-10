#!/usr/bin/env python

# Place different glyph shapes at each point using vtkProgrammableGlyphFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableGlyphFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold = (1.000, 0.843, 0.000)
slate_gray = (0.439, 0.502, 0.565)

# Source: three input points
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(5, 0, 0)
points.InsertNextPoint(10, 0, 0)

polydata = vtkPolyData()
polydata.SetPoints(points)


# Callback: select glyph shape based on point index
class CalcGlyph:
    def __init__(self, gf):
        self.gf = gf

    def __call__(self):
        pt = self.gf.GetPoint()
        pid = self.gf.GetPointId()
        if pid == 0:
            src = vtkConeSource()
            src.SetCenter(pt)
            self.gf.SetSourceConnection(src.GetOutputPort())
        elif pid == 1:
            src = vtkCubeSource()
            src.SetCenter(pt)
            self.gf.SetSourceConnection(src.GetOutputPort())
        elif pid == 2:
            src = vtkSphereSource()
            src.SetCenter(pt)
            self.gf.SetSourceConnection(src.GetOutputPort())


# Filter: programmable glyph filter with per-point callback
glyph_filter = vtkProgrammableGlyphFilter()
glyph_filter.SetInputData(polydata)
glyph_filter.SetGlyphMethod(CalcGlyph(glyph_filter))
default_source = vtkConeSource()
glyph_filter.SetSourceConnection(default_source.GetOutputPort())

# Mapper: map glyph data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(0.9)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ProgrammableGlyphFilter")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
