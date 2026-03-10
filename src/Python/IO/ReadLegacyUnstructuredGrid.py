#!/usr/bin/env python

# Read a legacy VTK unstructured grid file containing eleven linear cell
# types, visualize the cells with shrunk geometry, tubed edges, sphere
# glyphs at vertices, point labels, and a category legend.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkCategoryLegend
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkVariantArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellTypeUtilities,
    vtkGenericCell,
)
from vtkmodules.vtkFiltersCore import vtkExtractEdges, vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingContext2D import vtkContextTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkCamera,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper
from vtkmodules.vtkViewsContext2D import vtkContextView

# Colors (normalized RGB)
banana_rgb = (0.890, 0.812, 0.341)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load legacy VTK unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(str(data_dir / "VTKCellTypes.vtk"))
reader.Update()

# Build a legend array from the cell types in the file
legend_values = vtkVariantArray()
it = reader.GetOutput().NewCellIterator()
it.InitTraversal()
while not it.IsDoneWithTraversal():
    cell = vtkGenericCell()
    it.GetCell(cell)
    cell_name = vtkCellTypeUtilities.GetClassNameFromTypeId(cell.GetCellType())
    legend_values.InsertNextValue(cell_name)
    it.GoToNextCell()

# Edge extraction: extract edges and tube them for visibility
extract_edges = vtkExtractEdges()
extract_edges.SetInputConnection(reader.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(extract_edges.GetOutputPort())
tubes.SetRadius(0.05)
tubes.SetNumberOfSides(21)

edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tubes.GetOutputPort())
edge_mapper.SetScalarRange(0, 26)

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetSpecular(0.6)
edge_actor.GetProperty().SetSpecularPower(30)

# Point glyphs: place small spheres at each vertex
sphere = vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)
sphere.SetRadius(0.08)

point_mapper = vtkGlyph3DMapper()
point_mapper.SetInputConnection(reader.GetOutputPort())
point_mapper.SetSourceConnection(sphere.GetOutputPort())
point_mapper.ScalingOff()
point_mapper.ScalarVisibilityOff()

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetDiffuseColor(banana_rgb)
point_actor.GetProperty().SetSpecular(0.6)
point_actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
point_actor.GetProperty().SetSpecularPower(100)

# Point labels: numeric IDs at each vertex
label_mapper = vtkLabeledDataMapper()
label_mapper.SetInputConnection(reader.GetOutputPort())
label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Shrunk geometry: shrink cells to reveal structure
geometry_shrink = vtkShrinkFilter()
geometry_shrink.SetInputConnection(reader.GetOutputPort())
geometry_shrink.SetShrinkFactor(0.8)

# Copy the original lookup table for categorical legend use
categorical_lut = vtkLookupTable()
original_lut = reader.GetOutput().GetCellData().GetScalars().GetLookupTable()
categorical_lut.DeepCopy(original_lut)
categorical_lut.IndexedLookupOn()

geometry_mapper = vtkDataSetMapper()
geometry_mapper.SetInputConnection(geometry_shrink.GetOutputPort())
geometry_mapper.SetScalarModeToUseCellData()
geometry_mapper.SetScalarRange(0, 11)

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)
geometry_actor.GetProperty().SetLineWidth(3)
geometry_actor.GetProperty().EdgeVisibilityOn()
geometry_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Category legend: annotate cell types in the corner
for v in range(legend_values.GetNumberOfTuples()):
    categorical_lut.SetAnnotation(
        legend_values.GetValue(v), legend_values.GetValue(v).ToString()
    )
legend = vtkCategoryLegend()
legend.SetScalarsToColors(categorical_lut)
legend.SetValues(legend_values)
legend.SetTitle("Cell Type")
legend.GetBrush().SetColor(192, 192, 192, 255)

place_legend = vtkContextTransform()
place_legend.AddItem(legend)
place_legend.Translate(640 - 20, 480 - 12 * 16)

# Context view: hosts the 2D legend overlay alongside the 3D scene
context_view = vtkContextView()
context_view.GetScene().AddItem(place_legend)

renderer = context_view.GetRenderer()
render_window = context_view.GetRenderWindow()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddActor(geometry_actor)
renderer.AddActor(label_actor)
renderer.AddActor(edge_actor)
renderer.AddActor(point_actor)
renderer.SetBackground(background_rgb)

camera = vtkCamera()
camera.Azimuth(-40.0)
camera.Elevation(50.0)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

# Window: display the rendered scene
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadLegacyUnstructuredGrid")

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
