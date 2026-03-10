#!/usr/bin/env python

# Render an unstructured grid containing both a VTK_POLYHEDRON cell and a
# VTK_HEXAHEDRON cell side-by-side using SetPolyhedralCells().

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_POLYHEDRON,
    vtkCellArray,
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

# ---- Shared point list for both cells ----
points = vtkPoints()

# Points 0-7: polyhedron cube (arbitrary order, z from -10 to 10)
points.InsertNextPoint(-5.0, -5.0, -10.0)  # 0
points.InsertNextPoint(-5.0, -5.0, 10.0)   # 1
points.InsertNextPoint(-5.0, 5.0, -10.0)   # 2
points.InsertNextPoint(-5.0, 5.0, 10.0)    # 3
points.InsertNextPoint(5.0, -5.0, -10.0)   # 4
points.InsertNextPoint(5.0, -5.0, 10.0)    # 5
points.InsertNextPoint(5.0, 5.0, -10.0)    # 6
points.InsertNextPoint(5.0, 5.0, 10.0)     # 7

# Points 8-15: hexahedron (standard order, z from 15 to 35)
points.InsertNextPoint(-5.0, -5.0, 15.0)   # 8
points.InsertNextPoint(5.0, -5.0, 15.0)    # 9
points.InsertNextPoint(5.0, 5.0, 15.0)     # 10
points.InsertNextPoint(-5.0, 5.0, 15.0)    # 11
points.InsertNextPoint(-5.0, -5.0, 35.0)   # 12
points.InsertNextPoint(5.0, -5.0, 35.0)    # 13
points.InsertNextPoint(5.0, 5.0, 35.0)     # 14
points.InsertNextPoint(-5.0, 5.0, 35.0)    # 15

# ---- Cell 0: VTK_POLYHEDRON (faces defined explicitly) ----
polyhedron_point_ids = [0, 1, 2, 3, 4, 5, 6, 7]

face_array = vtkCellArray()
face_array.InsertNextCell(4, [0, 2, 6, 4])  # face 0: back   (−z)
face_array.InsertNextCell(4, [1, 3, 7, 5])  # face 1: front  (+z)
face_array.InsertNextCell(4, [0, 1, 3, 2])  # face 2: left   (−x)
face_array.InsertNextCell(4, [4, 5, 7, 6])  # face 3: right  (+x)
face_array.InsertNextCell(4, [0, 1, 5, 4])  # face 4: bottom (−y)
face_array.InsertNextCell(4, [2, 3, 7, 6])  # face 5: top    (+y)

face_locations = vtkCellArray()
face_locations.InsertNextCell(6, [0, 1, 2, 3, 4, 5])  # polyhedron uses all 6 faces

cells = vtkCellArray()
cells.InsertNextCell(8, polyhedron_point_ids)

cell_types = vtkUnsignedCharArray()
cell_types.InsertNextValue(VTK_POLYHEDRON)

# ---- Cell 1: VTK_HEXAHEDRON (no explicit faces needed) ----
hexahedron_point_ids = [8, 9, 10, 11, 12, 13, 14, 15]

face_locations.InsertNextCell(0)  # empty — hexahedron faces are implicit
cells.InsertNextCell(8, hexahedron_point_ids)
cell_types.InsertNextValue(VTK_HEXAHEDRON)

# Data: assemble the unstructured grid with polyhedral cells
ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.SetPolyhedralCells(cell_types, cells, face_locations, face_array)

# Mapper: map the unstructured grid to graphics primitives
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
render_window.SetWindowName("PolyhedronAndHexahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
