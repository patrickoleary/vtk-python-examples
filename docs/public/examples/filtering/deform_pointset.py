#!/usr/bin/env python

# Deform a sphere using a control mesh (octahedron) via vtkDeformPointSet,
# with elevation-based scalar coloring.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkDeformPointSet
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere to warp
sphere = vtkSphereSource()
sphere.SetThetaResolution(51)
sphere.SetPhiResolution(17)

# Generate elevation scalars
ele = vtkElevationFilter()
ele.SetInputConnection(sphere.GetOutputPort())
ele.SetLowPoint(0, 0, -0.5)
ele.SetHighPoint(0, 0, 0.5)

# Create control mesh (octahedron)
pts = vtkPoints()
pts.SetNumberOfPoints(6)
pts.SetPoint(0, -1, 0, 0)
pts.SetPoint(1, 1, 0, 0)
pts.SetPoint(2, 0, -1, 0)
pts.SetPoint(3, 0, 1, 0)
pts.SetPoint(4, 0, 0, -1)
pts.SetPoint(5, 0, 0, 1)

tris = vtkCellArray()
tris.InsertNextCell(3)
tris.InsertCellPoint(2)
tris.InsertCellPoint(0)
tris.InsertCellPoint(4)
tris.InsertNextCell(3)
tris.InsertCellPoint(1)
tris.InsertCellPoint(2)
tris.InsertCellPoint(4)
tris.InsertNextCell(3)
tris.InsertCellPoint(3)
tris.InsertCellPoint(1)
tris.InsertCellPoint(4)
tris.InsertNextCell(3)
tris.InsertCellPoint(0)
tris.InsertCellPoint(3)
tris.InsertCellPoint(4)
tris.InsertNextCell(3)
tris.InsertCellPoint(0)
tris.InsertCellPoint(2)
tris.InsertCellPoint(5)
tris.InsertNextCell(3)
tris.InsertCellPoint(2)
tris.InsertCellPoint(1)
tris.InsertCellPoint(5)
tris.InsertNextCell(3)
tris.InsertCellPoint(1)
tris.InsertCellPoint(3)
tris.InsertCellPoint(5)
tris.InsertNextCell(3)
tris.InsertCellPoint(3)
tris.InsertCellPoint(0)
tris.InsertCellPoint(5)

pd = vtkPolyData()
pd.SetPoints(pts)
pd.SetPolys(tris)

# Display the control mesh
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputData(pd)

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetRepresentationToWireframe()
mesh_actor.GetProperty().SetColor(0, 0, 0)

# Compute initial weights then deform
deform = vtkDeformPointSet()
deform.SetInputConnection(ele.GetOutputPort())
deform.SetControlMeshData(pd)
deform.Update()

# Move one control point to deform the sphere
pts.SetPoint(5, 0, 0, 3)
pts.Modified()
deform.Update()

# Display the warped sphere
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(deform.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(mesh_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("deform pointset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(1, 1, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
