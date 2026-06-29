#!/usr/bin/env python

# Demonstrate vtkProgrammableGlyphFilter by placing different glyph types
# (cone, cube, sphere) at different points, testing SetSourceConnection
# and SetSourceData switching per point.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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

# Create four points
point_positions = vtkPoints()
point_positions.InsertNextPoint(0, 0, 0)
point_positions.InsertNextPoint(5, 0, 0)
point_positions.InsertNextPoint(10, 0, 0)
point_positions.InsertNextPoint(15, 0, 0)

polydata = vtkPolyData()
polydata.SetPoints(point_positions)

# Default glyph source (cone)
cone_source = vtkConeSource()
cone_source.Update()

# Programmable glyph filter.
# The def is required by vtkProgrammableGlyphFilter.SetGlyphMethod().
glyph_filter = vtkProgrammableGlyphFilter()
glyph_filter.SetInputData(polydata)
glyph_filter.SetSourceData(cone_source.GetOutput())


def calc_glyph():
    point_coords = [0.0, 0.0, 0.0]
    glyph_filter.GetPoint(point_coords)
    point_id = glyph_filter.GetPointId()
    print("Calling calc_glyph for point {}".format(point_id))
    print("Point coords are: {} {} {}".format(point_coords[0], point_coords[1], point_coords[2]))

    if point_id == 0:
        # Cone at first point
        src = vtkConeSource()
        src.SetCenter(point_coords)
        glyph_filter.SetSourceConnection(src.GetOutputPort())
    elif point_id == 1:
        # Cube at second point via SetSourceData
        src = vtkCubeSource()
        src.SetCenter(point_coords)
        src.Update()
        glyph_filter.SetSourceConnection(None)
        glyph_filter.SetSourceData(src.GetOutput())
    elif point_id == 2:
        # Sphere at third point
        src = vtkSphereSource()
        src.SetCenter(point_coords)
        glyph_filter.SetSourceConnection(src.GetOutputPort())
    else:
        # Nothing at fourth point
        glyph_filter.SetSourceConnection(None)
        glyph_filter.SetSourceData(None)


glyph_filter.SetGlyphMethod(calc_glyph)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("programmable glyph")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
