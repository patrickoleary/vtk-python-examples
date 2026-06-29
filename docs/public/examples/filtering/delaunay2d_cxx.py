#!/usr/bin/env python

# Triangulate a set of precisely placed points using Delaunay 2D and
# verify that all points are connected in the output triangulation.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create specific point coordinates (four concentric squares)
new_pts = vtkPoints()
new_pts.InsertNextPoint(1.5026018771810041, 1.5026019428618222, 0.0)
new_pts.InsertNextPoint(-1.5026020085426373, 1.5026018115001829, 0.0)
new_pts.InsertNextPoint(-1.5026018353814194, -1.5026019846614038, 0.0)
new_pts.InsertNextPoint(1.5026019189805875, -1.5026019010622396, 0.0)
new_pts.InsertNextPoint(5.2149123972752491, 5.2149126252263240, 0.0)
new_pts.InsertNextPoint(-5.2149128531773883, 5.2149121693241645, 0.0)
new_pts.InsertNextPoint(-5.2149122522061022, -5.2149127702954603, 0.0)
new_pts.InsertNextPoint(5.2149125423443916, -5.2149124801571842, 0.0)
new_pts.InsertNextPoint(8.9272229173694946, 8.9272233075908254, 0.0)
new_pts.InsertNextPoint(-8.9272236978121402, 8.9272225271481460, 0.0)
new_pts.InsertNextPoint(-8.9272226690307868, -8.9272235559295172, 0.0)
new_pts.InsertNextPoint(8.9272231657081953, -8.9272230592521282, 0.0)
new_pts.InsertNextPoint(12.639533437463740, 12.639533989955329, 0.0)
new_pts.InsertNextPoint(-12.639534542446890, 12.639532884972127, 0.0)
new_pts.InsertNextPoint(-12.639533085855469, -12.639534341563573, 0.0)
new_pts.InsertNextPoint(12.639533789072001, -12.639533638347073, 0.0)

in_num_pts = new_pts.GetNumberOfPoints()
print(f"input numPts= {in_num_pts}")

point_cloud = vtkPolyData()
point_cloud.SetPoints(new_pts)

# Filter: Delaunay 2D triangulation
delaunay_2d = vtkDelaunay2D()
delaunay_2d.SetInputData(point_cloud)
delaunay_2d.Update()

triangulation = delaunay_2d.GetOutput()
out_num_pts = triangulation.GetNumberOfPoints()
out_num_cells = triangulation.GetNumberOfCells()
out_num_polys = triangulation.GetNumberOfPolys()

print(f"output numPts= {out_num_pts}")
print(f"output numCells= {out_num_cells}")
print(f"output numPolys= {out_num_polys}")

# Verify all points are connected
triangulation.BuildLinks()
num_unconnected = 0
cell_ids = vtkIdList()
for pt_id in range(out_num_pts):
    triangulation.GetPointCells(pt_id, cell_ids)
    if cell_ids.GetNumberOfIds() == 0:
        num_unconnected += 1

print(f"Triangulation has {num_unconnected} unconnected points")

# Filter: shrink triangles for visualization
shrink = vtkShrinkPolyData()
shrink.SetInputConnection(delaunay_2d.GetOutputPort())

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("delaunay2d cxx")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
