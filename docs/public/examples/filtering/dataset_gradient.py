#!/usr/bin/env python

# Demonstrate vtkDataSetGradient by computing cell gradients of scalar
# data on an unstructured grid and visualizing them as arrow glyphs.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    reference,
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkGenericCell,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersGeneral import vtkDataSetGradient
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the data
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "hexa.vtk"))

# Compute gradient for each cell
gradient = vtkDataSetGradient()
gradient.SetInputConnection(reader.GetOutputPort())
gradient.SetInputArrayToProcess(0, 0, 0, 0, "scalars")
gradient.Update()

# Build polydata with points at parametric center of each cell
gradient_at_centers = gradient.GetOutput().GetCellData().GetArray("gradient")

poly_data = vtkPolyData()
center_points = vtkPoints()
center_points.SetNumberOfPoints(gradient.GetOutput().GetNumberOfCells())

a_cell = vtkGenericCell()
for cell_id in range(gradient.GetOutput().GetNumberOfCells()):
    reader.GetOutput().GetCell(cell_id, a_cell)
    pcenter = [0.0, 0.0, 0.0]
    a_cell.GetParametricCenter(pcenter)
    weights = [0.0] * a_cell.GetNumberOfPoints()
    center = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    a_cell.EvaluateLocation(sub_id, pcenter, center, weights)
    center_points.SetPoint(cell_id, center)

poly_data.SetPoints(center_points)
poly_data.GetPointData().SetVectors(gradient_at_centers)

# Select a subset of gradients
num_points = reader.GetOutput().GetNumberOfPoints()
on_ratio = max(1, int(num_points / (num_points * 0.1)))

mask_points = vtkMaskPoints()
mask_points.SetInputData(poly_data)
mask_points.RandomModeOff()
mask_points.SetOnRatio(on_ratio)

# Create arrow glyphs for the gradient
arrow_source = vtkArrowSource()

scale_factor = 0.005
vector_glyph = vtkGlyph3D()
vector_glyph.SetSourceConnection(arrow_source.GetOutputPort())
vector_glyph.SetInputConnection(mask_points.GetOutputPort())
vector_glyph.SetScaleModeToScaleByVector()
vector_glyph.SetVectorModeToUseVector()
vector_glyph.SetScaleFactor(scale_factor)

vector_mapper = vtkPolyDataMapper()
vector_mapper.SetInputConnection(vector_glyph.GetOutputPort())
vector_mapper.ScalarVisibilityOff()

vector_actor = vtkActor()
vector_actor.SetMapper(vector_mapper)
vector_actor.GetProperty().SetColor(1.0, 0.3882, 0.2784)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(vector_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("dataset gradient")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(120)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
