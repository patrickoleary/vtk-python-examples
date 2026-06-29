#!/usr/bin/env python

# Triangulate contour loops using vtkContourTriangulator, including a
# polygon with an internal hole and a separate disjoint polygon.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Manually create contour loops
pts = vtkPoints()
pts.SetNumberOfPoints(12)
pts.SetPoint(0, 0, 0, 0)
pts.SetPoint(1, 10, 0, 0)
pts.SetPoint(2, 10, 10, 0)
pts.SetPoint(3, 0, 10, 0)
pts.SetPoint(4, 2, 2, 0)
pts.SetPoint(5, 8, 2, 0)
pts.SetPoint(6, 8, 8, 0)
pts.SetPoint(7, 2, 8, 0)
pts.SetPoint(8, 12, 0, 0)
pts.SetPoint(9, 22, 0, 0)
pts.SetPoint(10, 22, 10, 0)
pts.SetPoint(11, 12, 10, 0)

# Outer loop
loops = vtkCellArray()
loops.InsertNextCell(2, [0, 1])
loops.InsertNextCell(2, [1, 2])
loops.InsertNextCell(2, [2, 3])
loops.InsertNextCell(2, [3, 0])

# Inner loop - reverse ordering (flipped normal = hole)
loops.InsertNextCell(2, [5, 4])
loops.InsertNextCell(2, [6, 5])
loops.InsertNextCell(2, [7, 6])
loops.InsertNextCell(2, [4, 7])

# Disjoint second polygon
loops.InsertNextCell(2, [8, 9])
loops.InsertNextCell(2, [9, 10])
loops.InsertNextCell(2, [10, 11])
loops.InsertNextCell(2, [11, 8])

pd = vtkPolyData()
pd.SetPoints(pts)
pd.SetLines(loops)

# Triangulate the contours
normal = [0, 0, 1]
output_ca = vtkCellArray()
ct = vtkContourTriangulator()
ct.TriangulateContours(pd, 0, 12, output_ca, normal)

out_pd = vtkPolyData()
out_pd.SetPoints(pts)
out_pd.SetPolys(output_ca)

mapper = vtkPolyDataMapper()
mapper.SetInputData(out_pd)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("triangulate contours")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
