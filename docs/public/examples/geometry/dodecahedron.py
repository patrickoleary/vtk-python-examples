#!/usr/bin/env python

# Construct and render a dodecahedron as a vtkPolyhedron.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
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
papaya_whip_rgb = (1.0, 0.937, 0.835)
cadet_blue_background_rgb = (0.373, 0.620, 0.627)

# Data: 20 vertices of a dodecahedron
points = vtkPoints()
points.InsertNextPoint(1.21412, 0, 1.58931)
points.InsertNextPoint(0.375185, 1.1547, 1.58931)
points.InsertNextPoint(-0.982247, 0.713644, 1.58931)
points.InsertNextPoint(-0.982247, -0.713644, 1.58931)
points.InsertNextPoint(0.375185, -1.1547, 1.58931)
points.InsertNextPoint(1.96449, 0, 0.375185)
points.InsertNextPoint(0.607062, 1.86835, 0.375185)
points.InsertNextPoint(-1.58931, 1.1547, 0.375185)
points.InsertNextPoint(-1.58931, -1.1547, 0.375185)
points.InsertNextPoint(0.607062, -1.86835, 0.375185)
points.InsertNextPoint(1.58931, 1.1547, -0.375185)
points.InsertNextPoint(-0.607062, 1.86835, -0.375185)
points.InsertNextPoint(-1.96449, 0, -0.375185)
points.InsertNextPoint(-0.607062, -1.86835, -0.375185)
points.InsertNextPoint(1.58931, -1.1547, -0.375185)
points.InsertNextPoint(0.982247, 0.713644, -1.58931)
points.InsertNextPoint(-0.375185, 1.1547, -1.58931)
points.InsertNextPoint(-1.21412, 0, -1.58931)
points.InsertNextPoint(-0.375185, -1.1547, -1.58931)
points.InsertNextPoint(0.982247, -0.713644, -1.58931)

# Faces: 12 pentagonal faces stored in a vtkIdList
# Format: num_faces, then for each face: num_pts, pt0, pt1, ...
dodecahedron_faces = [
    [0, 1, 2, 3, 4], [0, 5, 10, 6, 1], [1, 6, 11, 7, 2],
    [2, 7, 12, 8, 3], [3, 8, 13, 9, 4], [4, 9, 14, 5, 0],
    [15, 10, 5, 14, 19], [16, 11, 6, 10, 15], [17, 12, 7, 11, 16],
    [18, 13, 8, 12, 17], [19, 14, 9, 13, 18], [19, 18, 17, 16, 15],
]

face_id_list = vtkIdList()
face_id_list.InsertNextId(len(dodecahedron_faces))
for face in dodecahedron_faces:
    face_id_list.InsertNextId(len(face))
    for pid in face:
        face_id_list.InsertNextId(pid)

# Unstructured grid: store the polyhedron cell
ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.InsertNextCell(VTK_POLYHEDRON, face_id_list)

# Mapper: map the polyhedron to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(ugrid)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(papaya_whip_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(cadet_blue_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dodecahedron")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
