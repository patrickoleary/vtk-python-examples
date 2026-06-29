#!/usr/bin/env python

# Demonstrate vtkClipDataSet on higher-order (quadratic) tetrahedra by
# creating three quadratic tetrahedra, clipping them, and rendering
# the clipped output surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_QUADRATIC_TETRA,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Reference quadratic tetra coordinates (10 points)
ref_coords = [
    (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (0.5, 0, 0), (0.5, 0.5, 0), (0, 0.5, 0),
    (0, 0, 0.5), (0.5, 0, 0.5), (0, 0.5, 0.5),
]

# Build 3 quadratic tetrahedra at different x offsets
all_points = vtkDoubleArray()
all_points.SetNumberOfComponents(3)
all_points.SetNumberOfTuples(30)

for ip in range(10):
    x, y, z = ref_coords[ip]
    all_points.SetTuple3(ip, x, y, z)
    all_points.SetTuple3(ip + 10, x - 1, y, z)
    all_points.SetTuple3(ip + 20, x + 1, y, z)

pts = vtkPoints()
pts.SetData(all_points)

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(pts)
ugrid.Allocate(3)
ugrid.InsertNextCell(VTK_QUADRATIC_TETRA, 10, list(range(0, 10)))
ugrid.InsertNextCell(VTK_QUADRATIC_TETRA, 10, list(range(10, 20)))
ugrid.InsertNextCell(VTK_QUADRATIC_TETRA, 10, list(range(20, 30)))

# Scalar field set to x coordinate
scalars = vtkDoubleArray()
scalars.SetName("X")
scalars.SetNumberOfTuples(30)
for ip in range(30):
    scalars.SetValue(ip, ugrid.GetPoints().GetData().GetComponent(ip, 0))

ugrid.GetPointData().AddArray(scalars)
ugrid.GetPointData().SetScalars(scalars)

# Clip at x=0.7 (inside out)
clip = vtkClipDataSet()
clip.SetInputData(ugrid)
clip.SetValue(0.7)
clip.SetInsideOut(True)

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(clip.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

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
render_window.SetWindowName("ho stable clip")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
