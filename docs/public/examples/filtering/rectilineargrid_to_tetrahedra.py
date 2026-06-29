#!/usr/bin/env python

# Convert a rectilinear grid to tetrahedra using vtkRectilinearGridToTetrahedra
# with four different conversion modes (5, 6, 12, and mixed 5/12 per cell),
# displayed side by side as tube-rendered edges.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkExtractEdges,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkRectilinearGridToTetrahedra
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()
peacock_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock_rgb)

# Set up the pipeline
form_mesh = vtkRectilinearGridToTetrahedra()
form_mesh.SetInput(4, 2, 2, 1, 1, 1, 0.001)
form_mesh.RememberVoxelIdOn()

tetra_edges = vtkExtractEdges()
tetra_edges.SetInputConnection(form_mesh.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(tetra_edges.GetOutputPort())
tubes.SetRadius(0.05)
tubes.SetNumberOfSides(6)

# Run with 5 tets per cell
form_mesh.SetTetraPerCellTo5()
tubes.Update()
tubes_1 = vtkPolyData()
tubes_1.DeepCopy(tubes.GetOutput())

# Run with 6 tets per cell
form_mesh.SetTetraPerCellTo6()
tubes.Update()
tubes_2 = vtkPolyData()
tubes_2.DeepCopy(tubes.GetOutput())

# Run with 12 tets per cell
form_mesh.SetTetraPerCellTo12()
tubes.Update()
tubes_3 = vtkPolyData()
tubes_3.DeepCopy(tubes.GetOutput())

# Run with mixed 5 and 12 tets per cell
div_types = vtkIntArray()
num_cell = form_mesh.GetInput().GetNumberOfCells()
div_types.SetNumberOfValues(num_cell)
for i in range(num_cell):
    div_types.SetValue(i, 5 + (7 * (i % 4)))

form_mesh.SetTetraPerCellTo5And12()
form_mesh.GetInput().GetCellData().SetScalars(div_types)
tubes.Update()
tubes_4 = vtkPolyData()
tubes_4.DeepCopy(tubes.GetOutput())

# --- Renderer 1: 5 tets per cell ---
map_edges_1 = vtkPolyDataMapper()
map_edges_1.SetInputData(tubes_1)

edge_actor_1 = vtkActor()
edge_actor_1.SetMapper(map_edges_1)
edge_actor_1.GetProperty().SetColor(peacock_rgb)
edge_actor_1.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor_1.GetProperty().SetSpecular(0.3)
edge_actor_1.GetProperty().SetSpecularPower(20)
edge_actor_1.GetProperty().SetAmbient(0.2)
edge_actor_1.GetProperty().SetDiffuse(0.8)

renderer_0 = vtkRenderer()
renderer_0.AddActor(edge_actor_1)
renderer_0.SetBackground(0, 0, 0)

# --- Renderer 2: 6 tets per cell ---
map_edges_2 = vtkPolyDataMapper()
map_edges_2.SetInputData(tubes_2)

edge_actor_2 = vtkActor()
edge_actor_2.SetMapper(map_edges_2)
edge_actor_2.GetProperty().SetColor(peacock_rgb)
edge_actor_2.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor_2.GetProperty().SetSpecular(0.3)
edge_actor_2.GetProperty().SetSpecularPower(20)
edge_actor_2.GetProperty().SetAmbient(0.2)
edge_actor_2.GetProperty().SetDiffuse(0.8)

renderer_1 = vtkRenderer()
renderer_1.AddActor(edge_actor_2)
renderer_1.SetBackground(0, 0, 0)

# --- Renderer 3: 12 tets per cell ---
map_edges_3 = vtkPolyDataMapper()
map_edges_3.SetInputData(tubes_3)

edge_actor_3 = vtkActor()
edge_actor_3.SetMapper(map_edges_3)
edge_actor_3.GetProperty().SetColor(peacock_rgb)
edge_actor_3.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor_3.GetProperty().SetSpecular(0.3)
edge_actor_3.GetProperty().SetSpecularPower(20)
edge_actor_3.GetProperty().SetAmbient(0.2)
edge_actor_3.GetProperty().SetDiffuse(0.8)

renderer_2 = vtkRenderer()
renderer_2.AddActor(edge_actor_3)
renderer_2.SetBackground(0, 0, 0)

# --- Renderer 4: mixed 5/12 tets per cell ---
map_edges_4 = vtkPolyDataMapper()
map_edges_4.SetInputData(tubes_4)

edge_actor_4 = vtkActor()
edge_actor_4.SetMapper(map_edges_4)
edge_actor_4.GetProperty().SetColor(peacock_rgb)
edge_actor_4.GetProperty().SetSpecularColor(1, 1, 1)
edge_actor_4.GetProperty().SetSpecular(0.3)
edge_actor_4.GetProperty().SetSpecularPower(20)
edge_actor_4.GetProperty().SetAmbient(0.2)
edge_actor_4.GetProperty().SetDiffuse(0.8)

renderer_3 = vtkRenderer()
renderer_3.AddActor(edge_actor_4)
renderer_3.SetBackground(0, 0, 0)

# Window with four viewports
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(600, 300)
render_window.SetWindowName("rectilineargrid to tetrahedra")

renderer_0.SetViewport(0.75, 0, 1, 1)
renderer_1.SetViewport(0.50, 0, 0.75, 1)
renderer_2.SetViewport(0.25, 0, 0.50, 1)
renderer_3.SetViewport(0, 0, 0.25, 1)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetPosition(1.73906, 12.7987, -0.257808)
renderer_0.GetActiveCamera().SetViewUp(0.992444, 0.00890284, -0.122379)
renderer_0.GetActiveCamera().SetClippingRange(9.36398, 15.0496)

renderer_1.ResetCamera()
renderer_1.GetActiveCamera().SetPosition(1.73906, 12.7987, -0.257808)
renderer_1.GetActiveCamera().SetViewUp(0.992444, 0.00890284, -0.122379)
renderer_1.GetActiveCamera().SetClippingRange(9.36398, 15.0496)

renderer_2.ResetCamera()
renderer_2.GetActiveCamera().SetPosition(1.73906, 12.7987, -0.257808)
renderer_2.GetActiveCamera().SetViewUp(0.992444, 0.00890284, -0.122379)
renderer_2.GetActiveCamera().SetClippingRange(9.36398, 15.0496)

renderer_3.ResetCamera()
renderer_3.GetActiveCamera().SetPosition(1.73906, 12.7987, -0.257808)
renderer_3.GetActiveCamera().SetViewUp(0.992444, 0.00890284, -0.122379)
renderer_3.GetActiveCamera().SetClippingRange(9.36398, 15.0496)

interactor.Initialize()
interactor.Start()
