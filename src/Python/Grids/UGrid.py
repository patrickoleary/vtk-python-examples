#!/usr/bin/env python

# Create an unstructured grid with various cell types.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_POLYGON,
    VTK_QUAD,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_TRIANGLE_STRIP,
    VTK_VERTEX,
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
peacock_rgb = (0.200, 0.631, 0.788)
beige_rgb = (0.961, 0.961, 0.863)

# Source: define 27 points and 12 cells of various types
x = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0],
     [0, 0, 1], [1, 0, 1], [2, 0, 1], [0, 1, 1], [1, 1, 1], [2, 1, 1],
     [0, 1, 2], [1, 1, 2], [2, 1, 2], [0, 1, 3], [1, 1, 3], [2, 1, 3],
     [0, 1, 4], [1, 1, 4], [2, 1, 4], [0, 1, 5], [1, 1, 5], [2, 1, 5],
     [0, 1, 6], [1, 1, 6], [2, 1, 6]]

pts = [[0, 1, 4, 3, 6, 7, 10, 9], [1, 2, 5, 4, 7, 8, 11, 10],
       [6, 10, 9, 12], [8, 11, 10, 14],
       [16, 17, 14, 13, 12, 15], [18, 15, 19, 16, 20, 17],
       [22, 23, 20, 19], [21, 22, 18], [22, 19, 18],
       [23, 26], [21, 24], [25]]

points = vtkPoints()
for i in range(len(x)):
    points.InsertPoint(i, x[i])

ugrid = vtkUnstructuredGrid()
ugrid.Allocate(100)
ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, pts[0])
ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, pts[1])
ugrid.InsertNextCell(VTK_TETRA, 4, pts[2])
ugrid.InsertNextCell(VTK_TETRA, 4, pts[3])
ugrid.InsertNextCell(VTK_POLYGON, 6, pts[4])
ugrid.InsertNextCell(VTK_TRIANGLE_STRIP, 6, pts[5])
ugrid.InsertNextCell(VTK_QUAD, 4, pts[6])
ugrid.InsertNextCell(VTK_TRIANGLE, 3, pts[7])
ugrid.InsertNextCell(VTK_TRIANGLE, 3, pts[8])
ugrid.InsertNextCell(VTK_LINE, 2, pts[9])
ugrid.InsertNextCell(VTK_LINE, 2, pts[10])
ugrid.InsertNextCell(VTK_VERTEX, 1, pts[11])
ugrid.SetPoints(points)

# Mapper: map the unstructured grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(ugrid)

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peacock_rgb)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(beige_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("UGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
