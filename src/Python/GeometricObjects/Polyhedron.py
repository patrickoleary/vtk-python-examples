#!/usr/bin/env python

# Construct a polyhedron (cube) using VTK_POLYHEDRON and render it.

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
silver_rgb = (0.75, 0.75, 0.75)
salmon_background_rgb = (0.980, 0.502, 0.447)

# Data: eight vertices of a cube
points = vtkPoints()
points.InsertNextPoint(-1.0, -1.0, -1.0)
points.InsertNextPoint(1.0, -1.0, -1.0)
points.InsertNextPoint(1.0, 1.0, -1.0)
points.InsertNextPoint(-1.0, 1.0, -1.0)
points.InsertNextPoint(-1.0, -1.0, 1.0)
points.InsertNextPoint(1.0, -1.0, 1.0)
points.InsertNextPoint(1.0, 1.0, 1.0)
points.InsertNextPoint(-1.0, 1.0, 1.0)

# Cell: a polyhedron defined by six quad faces
face_id = vtkIdList()
face_id.InsertNextId(6)  # number of faces

face_id.InsertNextId(4)  # face 0: back   (−z)
face_id.InsertNextId(0)
face_id.InsertNextId(3)
face_id.InsertNextId(2)
face_id.InsertNextId(1)

face_id.InsertNextId(4)  # face 1: left   (−x)
face_id.InsertNextId(0)
face_id.InsertNextId(4)
face_id.InsertNextId(7)
face_id.InsertNextId(3)

face_id.InsertNextId(4)  # face 2: front  (+z)
face_id.InsertNextId(4)
face_id.InsertNextId(5)
face_id.InsertNextId(6)
face_id.InsertNextId(7)

face_id.InsertNextId(4)  # face 3: right  (+x)
face_id.InsertNextId(5)
face_id.InsertNextId(1)
face_id.InsertNextId(2)
face_id.InsertNextId(6)

face_id.InsertNextId(4)  # face 4: bottom (−y)
face_id.InsertNextId(0)
face_id.InsertNextId(1)
face_id.InsertNextId(5)
face_id.InsertNextId(4)

face_id.InsertNextId(4)  # face 5: top    (+y)
face_id.InsertNextId(2)
face_id.InsertNextId(3)
face_id.InsertNextId(7)
face_id.InsertNextId(6)

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.InsertNextCell(VTK_POLYHEDRON, face_id)

# Mapper: map the polyhedron to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(ugrid)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(silver_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(salmon_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Polyhedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
