#!/usr/bin/env python

# Manually construct a cube as vtkPolyData with per-vertex scalar coloring.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornsilk_background_rgb = (1.0, 0.969, 0.859)

# Data: 8 vertices of a unit cube
points = vtkPoints()
points.InsertPoint(0, 0.0, 0.0, 0.0)
points.InsertPoint(1, 1.0, 0.0, 0.0)
points.InsertPoint(2, 1.0, 1.0, 0.0)
points.InsertPoint(3, 0.0, 1.0, 0.0)
points.InsertPoint(4, 0.0, 0.0, 1.0)
points.InsertPoint(5, 1.0, 0.0, 1.0)
points.InsertPoint(6, 1.0, 1.0, 1.0)
points.InsertPoint(7, 0.0, 1.0, 1.0)

# Faces: 6 quads defined by vertex indices
polys = vtkCellArray()

face0 = vtkIdList()
face0.InsertNextId(0)
face0.InsertNextId(3)
face0.InsertNextId(2)
face0.InsertNextId(1)
polys.InsertNextCell(face0)

face1 = vtkIdList()
face1.InsertNextId(4)
face1.InsertNextId(5)
face1.InsertNextId(6)
face1.InsertNextId(7)
polys.InsertNextCell(face1)

face2 = vtkIdList()
face2.InsertNextId(0)
face2.InsertNextId(1)
face2.InsertNextId(5)
face2.InsertNextId(4)
polys.InsertNextCell(face2)

face3 = vtkIdList()
face3.InsertNextId(1)
face3.InsertNextId(2)
face3.InsertNextId(6)
face3.InsertNextId(5)
polys.InsertNextCell(face3)

face4 = vtkIdList()
face4.InsertNextId(2)
face4.InsertNextId(3)
face4.InsertNextId(7)
face4.InsertNextId(6)
polys.InsertNextCell(face4)

face5 = vtkIdList()
face5.InsertNextId(3)
face5.InsertNextId(0)
face5.InsertNextId(4)
face5.InsertNextId(7)
polys.InsertNextCell(face5)

# Scalars: one value per vertex for color mapping
scalars = vtkFloatArray()
scalars.InsertTuple1(0, 0)
scalars.InsertTuple1(1, 1)
scalars.InsertTuple1(2, 2)
scalars.InsertTuple1(3, 3)
scalars.InsertTuple1(4, 4)
scalars.InsertTuple1(5, 5)
scalars.InsertTuple1(6, 6)
scalars.InsertTuple1(7, 7)

# Assemble the polydata
cube = vtkPolyData()
cube.SetPoints(points)
cube.SetPolys(polys)
cube.GetPointData().SetScalars(scalars)

# Mapper: map cube polydata to graphics primitives with scalar coloring
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputData(cube)
cube_mapper.SetScalarRange(cube.GetScalarRange())

# Actor: display the cube
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Camera: position for a 3D view
camera = vtkCamera()
camera.SetPosition(1, 1, 1)
camera.SetFocalPoint(0, 0, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cube_actor)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.SetBackground(cornsilk_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("Cube")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
