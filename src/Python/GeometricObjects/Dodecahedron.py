#!/usr/bin/env python

# Construct and render a dodecahedron as a vtkPolyhedron.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyhedron,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
papaya_whip_rgb = (1.0, 0.937, 0.835)
cadet_blue_background_rgb = (0.373, 0.620, 0.627)

# Data: build a dodecahedron as a polyhedron cell with 20 vertices and 12
# pentagonal faces.
dodecahedron = vtkPolyhedron()

# Point IDs: 0 through 19
dodecahedron.GetPointIds().InsertNextId(0)
dodecahedron.GetPointIds().InsertNextId(1)
dodecahedron.GetPointIds().InsertNextId(2)
dodecahedron.GetPointIds().InsertNextId(3)
dodecahedron.GetPointIds().InsertNextId(4)
dodecahedron.GetPointIds().InsertNextId(5)
dodecahedron.GetPointIds().InsertNextId(6)
dodecahedron.GetPointIds().InsertNextId(7)
dodecahedron.GetPointIds().InsertNextId(8)
dodecahedron.GetPointIds().InsertNextId(9)
dodecahedron.GetPointIds().InsertNextId(10)
dodecahedron.GetPointIds().InsertNextId(11)
dodecahedron.GetPointIds().InsertNextId(12)
dodecahedron.GetPointIds().InsertNextId(13)
dodecahedron.GetPointIds().InsertNextId(14)
dodecahedron.GetPointIds().InsertNextId(15)
dodecahedron.GetPointIds().InsertNextId(16)
dodecahedron.GetPointIds().InsertNextId(17)
dodecahedron.GetPointIds().InsertNextId(18)
dodecahedron.GetPointIds().InsertNextId(19)

# Vertex coordinates
dodecahedron.GetPoints().InsertNextPoint(1.21412, 0, 1.58931)
dodecahedron.GetPoints().InsertNextPoint(0.375185, 1.1547, 1.58931)
dodecahedron.GetPoints().InsertNextPoint(-0.982247, 0.713644, 1.58931)
dodecahedron.GetPoints().InsertNextPoint(-0.982247, -0.713644, 1.58931)
dodecahedron.GetPoints().InsertNextPoint(0.375185, -1.1547, 1.58931)
dodecahedron.GetPoints().InsertNextPoint(1.96449, 0, 0.375185)
dodecahedron.GetPoints().InsertNextPoint(0.607062, 1.86835, 0.375185)
dodecahedron.GetPoints().InsertNextPoint(-1.58931, 1.1547, 0.375185)
dodecahedron.GetPoints().InsertNextPoint(-1.58931, -1.1547, 0.375185)
dodecahedron.GetPoints().InsertNextPoint(0.607062, -1.86835, 0.375185)
dodecahedron.GetPoints().InsertNextPoint(1.58931, 1.1547, -0.375185)
dodecahedron.GetPoints().InsertNextPoint(-0.607062, 1.86835, -0.375185)
dodecahedron.GetPoints().InsertNextPoint(-1.96449, 0, -0.375185)
dodecahedron.GetPoints().InsertNextPoint(-0.607062, -1.86835, -0.375185)
dodecahedron.GetPoints().InsertNextPoint(1.58931, -1.1547, -0.375185)
dodecahedron.GetPoints().InsertNextPoint(0.982247, 0.713644, -1.58931)
dodecahedron.GetPoints().InsertNextPoint(-0.375185, 1.1547, -1.58931)
dodecahedron.GetPoints().InsertNextPoint(-1.21412, 0, -1.58931)
dodecahedron.GetPoints().InsertNextPoint(-0.375185, -1.1547, -1.58931)
dodecahedron.GetPoints().InsertNextPoint(0.982247, -0.713644, -1.58931)

# Faces: 12 pentagonal faces stored in a vtkCellArray
face_array = vtkCellArray()
face_array.InsertNextCell(5, [0, 1, 2, 3, 4])
face_array.InsertNextCell(5, [0, 5, 10, 6, 1])
face_array.InsertNextCell(5, [1, 6, 11, 7, 2])
face_array.InsertNextCell(5, [2, 7, 12, 8, 3])
face_array.InsertNextCell(5, [3, 8, 13, 9, 4])
face_array.InsertNextCell(5, [4, 9, 14, 5, 0])
face_array.InsertNextCell(5, [15, 10, 5, 14, 19])
face_array.InsertNextCell(5, [16, 11, 6, 10, 15])
face_array.InsertNextCell(5, [17, 12, 7, 11, 16])
face_array.InsertNextCell(5, [18, 13, 8, 12, 17])
face_array.InsertNextCell(5, [19, 14, 9, 13, 18])
face_array.InsertNextCell(5, [19, 18, 17, 16, 15])

dodecahedron.SetCellFaces(face_array)
dodecahedron.Initialize()

# Mapper: map the polyhedron polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(dodecahedron.GetPolyData())

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(papaya_whip_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(cadet_blue_background_rgb)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Dodecahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
