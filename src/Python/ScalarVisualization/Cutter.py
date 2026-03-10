#!/usr/bin/env python

# Cut a cube with a plane using vtkCutter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
yellow = (1.000, 1.000, 0.000)
aquamarine = (0.498, 1.000, 0.831)
silver = (0.753, 0.753, 0.753)

# Source: generate a cube
cube = vtkCubeSource()
cube.SetXLength(40)
cube.SetYLength(30)
cube.SetZLength(20)

# Mapper: map the cube to graphics primitives
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

# Implicit function: cutting plane in the XZ direction
plane = vtkPlane()
plane.SetOrigin(10, 0, 0)
plane.SetNormal(1, 0, 0)

# Filter: cut the cube with the plane
cutter = vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputConnection(cube.GetOutputPort())
cutter.Update()

# Mapper: map the cut line to graphics primitives
cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

# Actor: display the cut line
plane_actor = vtkActor()
plane_actor.SetMapper(cutter_mapper)
plane_actor.GetProperty().SetColor(yellow)
plane_actor.GetProperty().SetLineWidth(2)
plane_actor.GetProperty().SetAmbient(1.0)
plane_actor.GetProperty().SetDiffuse(0.0)

# Actor: display the semi-transparent cube
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(aquamarine)
cube_actor.GetProperty().SetOpacity(0.5)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(cube_actor)
renderer.SetBackground(silver)

camera = renderer.GetActiveCamera()
camera.SetPosition(-37.2611, -86.2155, 44.841)
camera.SetFocalPoint(0.569422, -1.65124, -2.49482)
camera.SetViewUp(0.160129, 0.42663, 0.890138)
camera.SetDistance(104.033)
camera.SetClippingRange(55.2019, 165.753)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Cutter")
render_window.SetSize(600, 600)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
