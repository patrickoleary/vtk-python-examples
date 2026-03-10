#!/usr/bin/env python

# Perform 2D Delaunay triangulation on random points and display
# the mesh with tube edges and sphere glyphs at the vertices.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkDelaunay2D,
    vtkExtractEdges,
    vtkGlyph3D,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
alice_blue_background_rgb = (0.941, 0.973, 1.000)
midnight_blue_rgb = (0.098, 0.098, 0.439)
peacock_rgb = (0.200, 0.631, 0.788)
hot_pink_rgb = (1.000, 0.412, 0.706)

# Source: generate random 2D points
points = vtkPoints()
random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.SetSeed(1)
for i in range(50):
    p1 = random_sequence.GetValue()
    random_sequence.Next()
    p2 = random_sequence.GetValue()
    random_sequence.Next()
    points.InsertPoint(i, p1, p2, 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Filter: 2D Delaunay triangulation
delaunay = vtkDelaunay2D()
delaunay.SetInputData(profile)
delaunay.SetTolerance(0.001)

# Mapper: triangulated mesh fill
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(delaunay.GetOutputPort())

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(midnight_blue_rgb)

# Filter: extract edges and wrap them in tubes
extract = vtkExtractEdges()
extract.SetInputConnection(delaunay.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(extract.GetOutputPort())
tubes.SetRadius(0.01)
tubes.SetNumberOfSides(6)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(peacock_rgb)
edge_actor.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor.GetProperty().SetSpecular(0.3)
edge_actor.GetProperty().SetSpecularPower(20)
edge_actor.GetProperty().SetAmbient(0.2)
edge_actor.GetProperty().SetDiffuse(0.8)

# Filter: place sphere glyphs at each vertex
ball = vtkSphereSource()
ball.SetRadius(0.025)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

balls = vtkGlyph3D()
balls.SetInputConnection(delaunay.GetOutputPort())
balls.SetSourceConnection(ball.GetOutputPort())

ball_mapper = vtkPolyDataMapper()
ball_mapper.SetInputConnection(balls.GetOutputPort())

ball_actor = vtkActor()
ball_actor.SetMapper(ball_mapper)
ball_actor.GetProperty().SetColor(hot_pink_rgb)
ball_actor.GetProperty().SetSpecularColor(1, 1, 1)
ball_actor.GetProperty().SetSpecular(0.3)
ball_actor.GetProperty().SetSpecularPower(20)
ball_actor.GetProperty().SetAmbient(0.2)
ball_actor.GetProperty().SetDiffuse(0.8)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(ball_actor)
renderer.AddActor(edge_actor)
renderer.SetBackground(alice_blue_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("DelaunayMesh")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
