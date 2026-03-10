#!/usr/bin/env python

# Deform a sphere using vtkDeformPointSet with a control mesh. One
# control point is displaced upward, stretching the sphere into a
# teardrop shape colored by elevation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
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

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(51)
sphere.SetPhiResolution(17)
sphere.Update()
bounds = sphere.GetOutput().GetBounds()

# Elevation: color the sphere by height (z)
elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())
elevation.SetLowPoint(
    (bounds[1] + bounds[0]) / 2.0,
    (bounds[3] + bounds[2]) / 2.0,
    -bounds[5],
)
elevation.SetHighPoint(
    (bounds[1] + bounds[0]) / 2.0,
    (bounds[3] + bounds[2]) / 2.0,
    bounds[5],
)
elevation.Update()

# Control mesh: an octahedron surrounding the sphere
pts = vtkPoints()
pts.SetNumberOfPoints(6)
pts.SetPoint(0, bounds[0] - 0.1 * (bounds[1] - bounds[0]),
             (bounds[3] + bounds[2]) / 2.0,
             (bounds[5] + bounds[4]) / 2.0)
pts.SetPoint(1, bounds[1] + 0.1 * (bounds[1] - bounds[0]),
             (bounds[3] + bounds[2]) / 2.0,
             (bounds[5] + bounds[4]) / 2.0)
pts.SetPoint(2, (bounds[1] + bounds[0]) / 2.0,
             bounds[2] - 0.1 * (bounds[3] - bounds[2]),
             (bounds[5] + bounds[4]) / 2.0)
pts.SetPoint(3, (bounds[1] + bounds[0]) / 2.0,
             bounds[3] + 0.1 * (bounds[3] - bounds[2]),
             (bounds[5] + bounds[4]) / 2.0)
pts.SetPoint(4, (bounds[1] + bounds[0]) / 2.0,
             (bounds[3] + bounds[2]) / 2.0,
             bounds[4] - 0.1 * (bounds[5] - bounds[4]))
pts.SetPoint(5, (bounds[1] + bounds[0]) / 2.0,
             (bounds[3] + bounds[2]) / 2.0,
             bounds[5] + 0.1 * (bounds[5] - bounds[4]))

tris = vtkCellArray()
cells = [[2, 0, 4], [1, 2, 4], [3, 1, 4], [0, 3, 4],
         [0, 2, 5], [2, 1, 5], [1, 3, 5], [3, 0, 5]]
for cell in cells:
    tris.InsertNextCell(3)
    for c in cell:
        tris.InsertCellPoint(c)

control_mesh = vtkPolyData()
control_mesh.SetPoints(pts)
control_mesh.SetPolys(tris)

# Mapper: control mesh wireframe
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputData(control_mesh)

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetRepresentationToWireframe()
mesh_actor.GetProperty().SetColor(0.0, 0.0, 0.0)

# DeformPointSet: deform the sphere using the control mesh
deform = vtkDeformPointSet()
deform.SetInputData(elevation.GetOutput())
deform.SetControlMeshData(control_mesh)
deform.Update()

# Displace the top control point upward to stretch the sphere
control_point = pts.GetPoint(5)
pts.SetPoint(5, control_point[0], control_point[1],
             bounds[5] + 0.8 * (bounds[5] - bounds[4]))
pts.Modified()

# Mapper: map the deformed surface to graphics primitives
deformed_mapper = vtkPolyDataMapper()
deformed_mapper.SetInputConnection(deform.GetOutputPort())

# Actor: assign the deformed geometry
deformed_actor = vtkActor()
deformed_actor.SetMapper(deformed_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(deformed_actor)
renderer.AddActor(mesh_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.GetActiveCamera().SetPosition(1, 1, 1)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("DeformPointSet")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
