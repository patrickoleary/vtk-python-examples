#!/usr/bin/env python

# Generate a surface from voxel contours using
# vtkVoxelContoursToSurfaceFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkVoxelContoursToSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build contour data procedurally
points = vtkPoints()
polys = vtkCellArray()

i = 0
z = -5
while z < 30:
    xtra_x = 0
    while xtra_x < 90:
        xtra_y = 0
        while xtra_y < 90:
            x = -10 + xtra_x
            y = -10 + xtra_y

            if z % 12 == 0:
                x += 1
            if z % 12 == 1:
                x += 2
            if z % 12 == 2:
                x += 3
            if z % 12 == 3:
                x += 3
                y += 1
            if z % 12 == 4:
                x += 3
                y += 2
            if z % 12 == 5:
                x += 3
                y += 3
            if z % 12 == 6:
                x += 2
                y += 3
            if z % 12 == 7:
                x += 1
                y += 3
            if z % 12 == 8:
                y += 3
            if z % 12 == 9:
                y += 2
            if z % 12 == 10:
                y += 1

            if (xtra_x != 30 and xtra_y != 30) or (xtra_x == xtra_y):
                polys.InsertNextCell(4)
                points.InsertPoint(i, x + 0, y + 0, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 20, y + 0, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 20, y + 20, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 0, y + 20, z)
                polys.InsertCellPoint(i)
                i += 1

                polys.InsertNextCell(4)
                points.InsertPoint(i, x + 4, y + 4, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 16, y + 4, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 16, y + 16, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 4, y + 16, z)
                polys.InsertCellPoint(i)
                i += 1

            if xtra_x != 30 or xtra_y != 30:
                polys.InsertNextCell(4)
                points.InsertPoint(i, x + 8, y + 8, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 12, y + 8, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 12, y + 12, z)
                polys.InsertCellPoint(i)
                i += 1
                points.InsertPoint(i, x + 8, y + 12, z)
                polys.InsertCellPoint(i)
                i += 1

            xtra_y += 30
        xtra_x += 30
    z += 1

# Contour poly data
contours = vtkPolyData()
contours.SetPoints(points)
contours.SetPolys(polys)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputData(contours)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1, 0, 0)
contour_actor.GetProperty().SetAmbient(1)
contour_actor.GetProperty().SetDiffuse(0)
contour_actor.GetProperty().SetRepresentationToWireframe()
contour_actor.VisibilityOff()

# Convert contours to surface
surface_filter = vtkVoxelContoursToSurfaceFilter()
surface_filter.SetInputData(contours)
surface_filter.SetMemoryLimitInBytes(100000)

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())
surface_mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(contour_actor)
renderer.AddViewProp(surface_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contours to surface")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(10)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
