#!/usr/bin/env python

# Demonstrate vtkCellValidator by building an unstructured grid containing
# valid and invalid cells, running the validator, and rendering cells
# colored by their validity state.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_PYRAMID,
    VTK_TETRA,
    VTK_WEDGE,
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkCellValidator
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build an unstructured grid with valid cells
pts = vtkPoints()

# Hexahedron (cell 0)
pts.InsertNextPoint(0, 0, 0)   # 0
pts.InsertNextPoint(1, 0, 0)   # 1
pts.InsertNextPoint(1, 1, 0)   # 2
pts.InsertNextPoint(0, 1, 0)   # 3
pts.InsertNextPoint(0, 0, 1)   # 4
pts.InsertNextPoint(1, 0, 1)   # 5
pts.InsertNextPoint(1, 1, 1)   # 6
pts.InsertNextPoint(0, 1, 1)   # 7

# Tetrahedron (cell 1)
pts.InsertNextPoint(2, 0, 0)   # 8
pts.InsertNextPoint(3, 0, 0)   # 9
pts.InsertNextPoint(2.5, 1, 0) # 10
pts.InsertNextPoint(2.5, 0.5, 1)  # 11

# Pyramid (cell 2)
pts.InsertNextPoint(4, 0, 0)   # 12
pts.InsertNextPoint(5, 0, 0)   # 13
pts.InsertNextPoint(5, 1, 0)   # 14
pts.InsertNextPoint(4, 1, 0)   # 15
pts.InsertNextPoint(4.5, 0.5, 1)  # 16

# Wedge (cell 3)
pts.InsertNextPoint(6, 1, 0)   # 17
pts.InsertNextPoint(6, 0, 0)   # 18
pts.InsertNextPoint(6, 0.5, 0.5)  # 19
pts.InsertNextPoint(7, 1, 0)   # 20
pts.InsertNextPoint(7, 0, 0)   # 21
pts.InsertNextPoint(7, 0.5, 0.5)  # 22

# Broken hexahedron — swapped points (cell 4)
pts.InsertNextPoint(0, 2, 0)   # 23
pts.InsertNextPoint(1, 2, 0)   # 24
pts.InsertNextPoint(1, 3, 0)   # 25
pts.InsertNextPoint(0, 3, 0)   # 26
pts.InsertNextPoint(0, 2, 1)   # 27
pts.InsertNextPoint(1, 2, 1)   # 28
pts.InsertNextPoint(1, 3, 1)   # 29
pts.InsertNextPoint(0, 3, 1)   # 30

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(pts)

# Insert cells
ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, [0, 1, 2, 3, 4, 5, 6, 7])
ugrid.InsertNextCell(VTK_TETRA, 4, [8, 9, 10, 11])
ugrid.InsertNextCell(VTK_PYRAMID, 5, [12, 13, 14, 15, 16])
ugrid.InsertNextCell(VTK_WEDGE, 6, [17, 18, 19, 20, 21, 22])
# Broken hex: swap point 0 and 1
ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, [24, 23, 25, 26, 27, 28, 29, 30])

# Run validator
validator = vtkCellValidator()
validator.SetInputData(ugrid)
validator.Update()

# Render cells colored by validity state
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(validator.GetOutputPort())

mapper = vtkDataSetMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("ValidityState")
mapper.SetScalarRange(0, 4)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("cell validator basic")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
