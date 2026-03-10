#!/usr/bin/env python

# Render a polyhedron (dodecahedron) — a generic polyhedral cell defined by
# its vertices and face connectivity, with 20 points and 12 pentagonal faces.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_POLYHEDRON,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# Points: 20 vertices of a regular dodecahedron, scaled to fit ~[-0.7,0.7]³
scale = 0.35
points = vtkPoints()
raw_coords = [
    (1.21412, 0, 1.58931), (0.375185, 1.1547, 1.58931),
    (-0.982247, 0.713644, 1.58931), (-0.982247, -0.713644, 1.58931),
    (0.375185, -1.1547, 1.58931), (1.96449, 0, 0.375185),
    (0.607062, 1.86835, 0.375185), (-1.58931, 1.1547, 0.375185),
    (-1.58931, -1.1547, 0.375185), (0.607062, -1.86835, 0.375185),
    (1.58931, 1.1547, -0.375185), (-0.607062, 1.86835, -0.375185),
    (-1.96449, 0, -0.375185), (-0.607062, -1.86835, -0.375185),
    (1.58931, -1.1547, -0.375185), (0.982247, 0.713644, -1.58931),
    (-0.375185, 1.1547, -1.58931), (-1.21412, 0, -1.58931),
    (-0.375185, -1.1547, -1.58931), (0.982247, -0.713644, -1.58931),
]
for x, y, z in raw_coords:
    points.InsertNextPoint(x * scale, y * scale, z * scale)

# Faces: 12 pentagonal faces defining the dodecahedron connectivity
faces = [
    [0, 1, 2, 3, 4], [0, 5, 10, 6, 1], [1, 6, 11, 7, 2],
    [2, 7, 12, 8, 3], [3, 8, 13, 9, 4], [4, 9, 14, 5, 0],
    [15, 10, 5, 14, 19], [16, 11, 6, 10, 15], [17, 12, 7, 11, 16],
    [18, 13, 8, 12, 17], [19, 14, 9, 13, 18], [19, 18, 17, 16, 15],
]

# Build the face ID list for InsertNextCell(VTK_POLYHEDRON, ...)
faces_id_list = vtkIdList()
faces_id_list.InsertNextId(len(faces))
for face in faces:
    faces_id_list.InsertNextId(len(face))
    for point_id in face:
        faces_id_list.InsertNextId(point_id)

# Unstructured grid: holds the single polyhedron cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(VTK_POLYHEDRON, faces_id_list)

# Mapper: map the grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(grid)

# Actor: position, orient, and color the cell
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.RotateX(20.0)
actor.RotateY(-20.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_blue_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Cell3DPolyhedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
