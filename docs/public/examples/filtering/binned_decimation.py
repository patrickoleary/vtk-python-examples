#!/usr/bin/env python

# Compare four binned decimation point generation modes on a sphere:
# input points, bin points, bin centers, and bin averages.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import (
    vtkBinnedDecimation,
    vtkPointDataToCellData,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 400
divisions = 40

colors = vtkNamedColors()
tomato = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato)

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(resolution)
sphere.SetPhiResolution(int(resolution / 2))
sphere.GenerateNormalsOff()

# Add elevation scalars
elevation = vtkSimpleElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())

# Convert point data to cell data
point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(elevation.GetOutputPort())
point_to_cell.PassPointDataOn()
point_to_cell.Update()

# --- Top-left viewport: use input points ---

mesh_0 = vtkBinnedDecimation()
mesh_0.SetInputConnection(point_to_cell.GetOutputPort())
mesh_0.SetPointGenerationModeToUseInputPoints()
mesh_0.AutoAdjustNumberOfDivisionsOn()
mesh_0.SetNumberOfXDivisions(divisions)
mesh_0.SetNumberOfYDivisions(divisions)
mesh_0.SetNumberOfZDivisions(divisions)
mesh_0.ProducePointDataOn()
mesh_0.ProduceCellDataOn()
mesh_0.Update()

print("1) Use Input Points:")
print(f"\tNumber output triangles: {mesh_0.GetOutput().GetNumberOfCells()}")

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(mesh_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(tomato)
actor_0.GetProperty().SetDiffuse(0.8)
actor_0.GetProperty().SetSpecular(0.4)
actor_0.GetProperty().SetSpecularPower(30)

# --- Top-right viewport: bin points ---

mesh_1 = vtkBinnedDecimation()
mesh_1.SetInputConnection(point_to_cell.GetOutputPort())
mesh_1.SetPointGenerationModeToBinPoints()
mesh_1.AutoAdjustNumberOfDivisionsOff()
mesh_1.SetDivisionOrigin(mesh_0.GetDivisionOrigin())
mesh_1.SetDivisionSpacing(mesh_0.GetDivisionSpacing())
mesh_1.SetNumberOfXDivisions(divisions)
mesh_1.SetNumberOfYDivisions(divisions)
mesh_1.SetNumberOfZDivisions(divisions)
mesh_1.ProducePointDataOn()
mesh_1.ProduceCellDataOn()
mesh_1.Update()

print("2) Bin Points:")
print(f"\tNumber output triangles: {mesh_1.GetOutput().GetNumberOfCells()}")

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(mesh_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(tomato)
actor_1.GetProperty().SetDiffuse(0.8)
actor_1.GetProperty().SetSpecular(0.4)
actor_1.GetProperty().SetSpecularPower(30)

# --- Bottom-left viewport: bin centers ---

mesh_2 = vtkBinnedDecimation()
mesh_2.SetInputConnection(point_to_cell.GetOutputPort())
mesh_2.SetPointGenerationModeToBinCenters()
mesh_2.AutoAdjustNumberOfDivisionsOn()
mesh_2.SetNumberOfXDivisions(divisions)
mesh_2.SetNumberOfYDivisions(divisions)
mesh_2.SetNumberOfZDivisions(divisions)
mesh_2.ProducePointDataOn()
mesh_2.ProduceCellDataOn()
mesh_2.Update()

print("3) Bin Centers:")
print(f"\tNumber output triangles: {mesh_2.GetOutput().GetNumberOfCells()}")

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(mesh_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetDiffuseColor(tomato)
actor_2.GetProperty().SetDiffuse(0.8)
actor_2.GetProperty().SetSpecular(0.4)
actor_2.GetProperty().SetSpecularPower(30)

# --- Bottom-right viewport: bin averages ---

mesh_3 = vtkBinnedDecimation()
mesh_3.SetInputConnection(point_to_cell.GetOutputPort())
mesh_3.SetPointGenerationModeToBinAverages()
mesh_3.AutoAdjustNumberOfDivisionsOn()
mesh_3.SetNumberOfXDivisions(divisions)
mesh_3.SetNumberOfYDivisions(divisions)
mesh_3.SetNumberOfZDivisions(divisions)
mesh_3.AutoAdjustNumberOfDivisionsOff()
mesh_3.ProducePointDataOn()
mesh_3.ProduceCellDataOn()
mesh_3.Update()

print("4) Bin Averages:")
print(f"\tNumber output triangles: {mesh_3.GetOutput().GetNumberOfCells()}")

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(mesh_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetDiffuseColor(tomato)
actor_3.GetProperty().SetDiffuse(0.8)
actor_3.GetProperty().SetSpecular(0.4)
actor_3.GetProperty().SetSpecularPower(30)

# Four viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 0.5)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(1, 1, 1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1.0)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(1, 1, 1)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddActor(actor_3)
renderer_3.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(400, 400)
render_window.SetWindowName("binned decimation")

# Scene
renderer_1.ResetCamera()
renderer_0.SetActiveCamera(renderer_1.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_1.GetActiveCamera())
renderer_3.SetActiveCamera(renderer_1.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
