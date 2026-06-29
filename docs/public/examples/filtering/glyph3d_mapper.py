#!/usr/bin/env python

# Place cone glyphs at points oriented by 2-component vectors.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create 2-component vectors as orientation data
vectors = vtkDoubleArray()
vectors.SetName("Normals")
vectors.SetNumberOfComponents(2)
vectors.InsertNextTuple2(1, 1)
vectors.InsertNextTuple2(1, 0)
vectors.InsertNextTuple2(0, 1)

# Create three points
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(2, 2, 2)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().AddArray(vectors)

# Glyph source: cone
glyph_source = vtkConeSource()

# Filter: place glyphs at each point
glyph_3d = vtkGlyph3D()
glyph_3d.SetSourceConnection(glyph_source.GetOutputPort())
glyph_3d.SetInputData(polydata)
glyph_3d.SetInputArrayToProcess(1, 0, 0, 0, "Normals")
glyph_3d.SetVectorModeToUseVector()
glyph_3d.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph_3d.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("glyph3d mapper")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
