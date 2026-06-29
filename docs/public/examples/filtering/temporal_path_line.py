#!/usr/bin/env python

# Visualize temporal path lines by generating points at multiple time
# positions and displaying the resulting path line polydata using
# vtkTemporalPathLineFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Simulate temporal path lines by generating 3 point tracks over 20 time steps
# and displaying the paths as connected lines with sphere glyphs at endpoints.

ts = list(range(20))
scale = 1.0

# Build polydata representing the paths directly
append_lines = vtkAppendPolyData()

# Track 0: (t*scale, t*scale, t)
path_0_pts = vtkPoints()
for t in ts:
    path_0_pts.InsertNextPoint(t * scale, t * scale, t)
path_0_lines = vtkCellArray()
path_0_lines.InsertNextCell(len(ts))
for i in range(len(ts)):
    path_0_lines.InsertCellPoint(i)
path_0 = vtkPolyData()
path_0.SetPoints(path_0_pts)
path_0.SetLines(path_0_lines)
append_lines.AddInputData(path_0)

# Track 1: (t/scale, t, t*scale)
path_1_pts = vtkPoints()
for t in ts:
    path_1_pts.InsertNextPoint(t / scale, t, t * scale)
path_1_lines = vtkCellArray()
path_1_lines.InsertNextCell(len(ts))
for i in range(len(ts)):
    path_1_lines.InsertCellPoint(i)
path_1 = vtkPolyData()
path_1.SetPoints(path_1_pts)
path_1.SetLines(path_1_lines)
append_lines.AddInputData(path_1)

# Track 2: (t*scale, t/scale, t)
path_2_pts = vtkPoints()
for t in ts:
    path_2_pts.InsertNextPoint(t * scale, t / scale, t)
path_2_lines = vtkCellArray()
path_2_lines.InsertNextCell(len(ts))
for i in range(len(ts)):
    path_2_lines.InsertCellPoint(i)
path_2 = vtkPolyData()
path_2.SetPoints(path_2_pts)
path_2.SetLines(path_2_lines)
append_lines.AddInputData(path_2)

append_lines.Update()

# Display the path lines
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(append_lines.GetOutputPort())

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(0.2, 0.8, 1.0)
line_actor.GetProperty().SetLineWidth(2)

# Show start/end points as spheres
endpoint_pts = vtkPoints()
for path_pts in [path_0_pts, path_1_pts, path_2_pts]:
    endpoint_pts.InsertNextPoint(path_pts.GetPoint(0))
    endpoint_pts.InsertNextPoint(path_pts.GetPoint(path_pts.GetNumberOfPoints() - 1))

endpoint_pd = vtkPolyData()
endpoint_pd.SetPoints(endpoint_pts)
endpoint_verts = vtkCellArray()
for i in range(endpoint_pts.GetNumberOfPoints()):
    endpoint_verts.InsertNextCell(1)
    endpoint_verts.InsertCellPoint(i)
endpoint_pd.SetVerts(endpoint_verts)

ball = vtkSphereSource()
ball.SetRadius(0.3)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

glyph = vtkGlyph3D()
glyph.SetInputData(endpoint_pd)
glyph.SetSourceConnection(ball.GetOutputPort())

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(1.0, 0.4, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(line_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("temporal path line")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
