#!/usr/bin/env python

# Demonstrate vtkHull with various plane configurations on a teapot model,
# displayed in a 3x3 grid layout.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkHull
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read teapot geometry
byu_reader = vtkBYUReader()
byu_reader.SetGeometryFileName(os.path.join(data_dir, "teapot.g"))

byu_mapper = vtkPolyDataMapper()
byu_mapper.SetInputConnection(byu_reader.GetOutputPort())

byu_reader.Update()

# Teapot actor 0: cube face planes
byu_actor_0 = vtkActor()
byu_actor_0.SetMapper(byu_mapper)

hull_0 = vtkHull()
hull_0.SetInputConnection(byu_reader.GetOutputPort())
hull_0.AddCubeFacePlanes()

hull_mapper_0 = vtkPolyDataMapper()
hull_mapper_0.SetInputConnection(hull_0.GetOutputPort())

hull_actor_0 = vtkActor()
hull_actor_0.SetMapper(hull_mapper_0)
hull_actor_0.GetProperty().SetColor(1, 0, 0)
hull_actor_0.GetProperty().SetAmbient(0.2)
hull_actor_0.GetProperty().SetDiffuse(0.8)
hull_actor_0.GetProperty().SetRepresentationToWireframe()

# Teapot actor 1: cube edge planes
byu_actor_1 = vtkActor()
byu_actor_1.SetMapper(byu_mapper)

hull_1 = vtkHull()
hull_1.SetInputConnection(byu_reader.GetOutputPort())
hull_1.AddCubeEdgePlanes()

hull_mapper_1 = vtkPolyDataMapper()
hull_mapper_1.SetInputConnection(hull_1.GetOutputPort())

hull_actor_1 = vtkActor()
hull_actor_1.SetMapper(hull_mapper_1)
hull_actor_1.GetProperty().SetColor(1, 0, 0)
hull_actor_1.GetProperty().SetAmbient(0.2)
hull_actor_1.GetProperty().SetDiffuse(0.8)
hull_actor_1.GetProperty().SetRepresentationToWireframe()

# Teapot actor 2: cube vertex planes
byu_actor_2 = vtkActor()
byu_actor_2.SetMapper(byu_mapper)

hull_2 = vtkHull()
hull_2.SetInputConnection(byu_reader.GetOutputPort())
hull_2.AddCubeVertexPlanes()

hull_mapper_2 = vtkPolyDataMapper()
hull_mapper_2.SetInputConnection(hull_2.GetOutputPort())

hull_actor_2 = vtkActor()
hull_actor_2.SetMapper(hull_mapper_2)
hull_actor_2.GetProperty().SetColor(1, 0, 0)
hull_actor_2.GetProperty().SetAmbient(0.2)
hull_actor_2.GetProperty().SetDiffuse(0.8)
hull_actor_2.GetProperty().SetRepresentationToWireframe()

# Teapot actor 3: all cube planes
byu_actor_3 = vtkActor()
byu_actor_3.SetMapper(byu_mapper)

hull_3 = vtkHull()
hull_3.SetInputConnection(byu_reader.GetOutputPort())
hull_3.AddCubeFacePlanes()
hull_3.AddCubeEdgePlanes()
hull_3.AddCubeVertexPlanes()

hull_mapper_3 = vtkPolyDataMapper()
hull_mapper_3.SetInputConnection(hull_3.GetOutputPort())

hull_actor_3 = vtkActor()
hull_actor_3.SetMapper(hull_mapper_3)
hull_actor_3.GetProperty().SetColor(1, 0, 0)
hull_actor_3.GetProperty().SetAmbient(0.2)
hull_actor_3.GetProperty().SetDiffuse(0.8)
hull_actor_3.GetProperty().SetRepresentationToWireframe()

# Teapot actor 4: recursive sphere planes level 0
byu_actor_4 = vtkActor()
byu_actor_4.SetMapper(byu_mapper)

hull_4 = vtkHull()
hull_4.SetInputConnection(byu_reader.GetOutputPort())
hull_4.AddRecursiveSpherePlanes(0)

hull_mapper_4 = vtkPolyDataMapper()
hull_mapper_4.SetInputConnection(hull_4.GetOutputPort())

hull_actor_4 = vtkActor()
hull_actor_4.SetMapper(hull_mapper_4)
hull_actor_4.GetProperty().SetColor(1, 0, 0)
hull_actor_4.GetProperty().SetAmbient(0.2)
hull_actor_4.GetProperty().SetDiffuse(0.8)
hull_actor_4.GetProperty().SetRepresentationToWireframe()

# Teapot actor 5: recursive sphere planes level 1
byu_actor_5 = vtkActor()
byu_actor_5.SetMapper(byu_mapper)

hull_5 = vtkHull()
hull_5.SetInputConnection(byu_reader.GetOutputPort())
hull_5.AddRecursiveSpherePlanes(1)

hull_mapper_5 = vtkPolyDataMapper()
hull_mapper_5.SetInputConnection(hull_5.GetOutputPort())

hull_actor_5 = vtkActor()
hull_actor_5.SetMapper(hull_mapper_5)
hull_actor_5.GetProperty().SetColor(1, 0, 0)
hull_actor_5.GetProperty().SetAmbient(0.2)
hull_actor_5.GetProperty().SetDiffuse(0.8)
hull_actor_5.GetProperty().SetRepresentationToWireframe()

# Teapot actor 6: recursive sphere planes level 2
byu_actor_6 = vtkActor()
byu_actor_6.SetMapper(byu_mapper)

hull_6 = vtkHull()
hull_6.SetInputConnection(byu_reader.GetOutputPort())
hull_6.AddRecursiveSpherePlanes(2)

hull_mapper_6 = vtkPolyDataMapper()
hull_mapper_6.SetInputConnection(hull_6.GetOutputPort())

hull_actor_6 = vtkActor()
hull_actor_6.SetMapper(hull_mapper_6)
hull_actor_6.GetProperty().SetColor(1, 0, 0)
hull_actor_6.GetProperty().SetAmbient(0.2)
hull_actor_6.GetProperty().SetDiffuse(0.8)
hull_actor_6.GetProperty().SetRepresentationToWireframe()

# Teapot actor 7: recursive sphere planes level 3
byu_actor_7 = vtkActor()
byu_actor_7.SetMapper(byu_mapper)

hull_7 = vtkHull()
hull_7.SetInputConnection(byu_reader.GetOutputPort())
hull_7.AddRecursiveSpherePlanes(3)

hull_mapper_7 = vtkPolyDataMapper()
hull_mapper_7.SetInputConnection(hull_7.GetOutputPort())

hull_actor_7 = vtkActor()
hull_actor_7.SetMapper(hull_mapper_7)
hull_actor_7.GetProperty().SetColor(1, 0, 0)
hull_actor_7.GetProperty().SetAmbient(0.2)
hull_actor_7.GetProperty().SetDiffuse(0.8)
hull_actor_7.GetProperty().SetRepresentationToWireframe()

# Teapot actor 8: recursive sphere planes level 4
byu_actor_8 = vtkActor()
byu_actor_8.SetMapper(byu_mapper)

hull_8 = vtkHull()
hull_8.SetInputConnection(byu_reader.GetOutputPort())
hull_8.AddRecursiveSpherePlanes(4)

hull_mapper_8 = vtkPolyDataMapper()
hull_mapper_8.SetInputConnection(hull_8.GetOutputPort())

hull_actor_8 = vtkActor()
hull_actor_8.SetMapper(hull_mapper_8)
hull_actor_8.GetProperty().SetColor(1, 0, 0)
hull_actor_8.GetProperty().SetAmbient(0.2)
hull_actor_8.GetProperty().SetDiffuse(0.8)
hull_actor_8.GetProperty().SetRepresentationToWireframe()

# Position actors in a 3x3 grid
diagonal = byu_actor_0.GetLength()

byu_actor_0.AddPosition(-1 * diagonal, -1 * diagonal, 0)
hull_actor_0.AddPosition(-1 * diagonal, -1 * diagonal, 0)

byu_actor_1.AddPosition(0 * diagonal, -1 * diagonal, 0)
hull_actor_1.AddPosition(0 * diagonal, -1 * diagonal, 0)

byu_actor_2.AddPosition(1 * diagonal, -1 * diagonal, 0)
hull_actor_2.AddPosition(1 * diagonal, -1 * diagonal, 0)

byu_actor_3.AddPosition(-1 * diagonal, 0 * diagonal, 0)
hull_actor_3.AddPosition(-1 * diagonal, 0 * diagonal, 0)

byu_actor_4.AddPosition(0 * diagonal, 0 * diagonal, 0)
hull_actor_4.AddPosition(0 * diagonal, 0 * diagonal, 0)

byu_actor_5.AddPosition(1 * diagonal, 0 * diagonal, 0)
hull_actor_5.AddPosition(1 * diagonal, 0 * diagonal, 0)

byu_actor_6.AddPosition(-1 * diagonal, 1 * diagonal, 0)
hull_actor_6.AddPosition(-1 * diagonal, 1 * diagonal, 0)

byu_actor_7.AddPosition(0 * diagonal, 1 * diagonal, 0)
hull_actor_7.AddPosition(0 * diagonal, 1 * diagonal, 0)

byu_actor_8.AddPosition(1 * diagonal, 1 * diagonal, 0)
hull_actor_8.AddPosition(1 * diagonal, 1 * diagonal, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(byu_actor_0)
renderer.AddActor(hull_actor_0)
renderer.AddActor(byu_actor_1)
renderer.AddActor(hull_actor_1)
renderer.AddActor(byu_actor_2)
renderer.AddActor(hull_actor_2)
renderer.AddActor(byu_actor_3)
renderer.AddActor(hull_actor_3)
renderer.AddActor(byu_actor_4)
renderer.AddActor(hull_actor_4)
renderer.AddActor(byu_actor_5)
renderer.AddActor(hull_actor_5)
renderer.AddActor(byu_actor_6)
renderer.AddActor(hull_actor_6)
renderer.AddActor(byu_actor_7)
renderer.AddActor(hull_actor_7)
renderer.AddActor(byu_actor_8)
renderer.AddActor(hull_actor_8)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)
render_window.SetWindowName("teapot hulls")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
