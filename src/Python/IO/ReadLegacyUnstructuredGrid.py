#!/usr/bin/env python

# Read a legacy VTK unstructured grid file containing eleven linear cell
# types, visualize the cells with shrunk geometry, tubed edges, sphere
# glyphs at vertices, point labels, and a legend box.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkCellTypeUtilities,
    vtkGenericCell,
)
from vtkmodules.vtkFiltersCore import vtkExtractEdges, vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkLegendBoxActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkCamera,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Colors (normalized RGB)
banana_rgb = (0.890, 0.812, 0.341)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load legacy VTK unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(str(data_dir / "VTKCellTypes.vtk"))
reader.Update()

# Collect cell type names and their scalar values for the legend
cell_type_names = []
it = reader.GetOutput().NewCellIterator()
it.InitTraversal()
while not it.IsDoneWithTraversal():
    cell = vtkGenericCell()
    it.GetCell(cell)
    cell_name = vtkCellTypeUtilities.GetClassNameFromTypeId(cell.GetCellType())
    cell_type_names.append(cell_name)
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
label_mapper.SetLabelModeToLabelIds()
label_mapper.SetLabelFormat("%d")
label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Shrunk geometry: shrink cells to reveal structure
geometry_shrink = vtkShrinkFilter()
geometry_shrink.SetInputConnection(reader.GetOutputPort())
geometry_shrink.SetShrinkFactor(0.8)

# Lookup table: copy the original for legend color retrieval
original_lut = reader.GetOutput().GetCellData().GetScalars().GetLookupTable()
legend_lut = vtkLookupTable()
legend_lut.DeepCopy(original_lut)

geometry_mapper = vtkDataSetMapper()
geometry_mapper.SetInputConnection(geometry_shrink.GetOutputPort())
geometry_mapper.SetScalarModeToUseCellData()
geometry_mapper.SetScalarRange(0, 11)

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)
geometry_actor.GetProperty().SetLineWidth(3)
geometry_actor.GetProperty().EdgeVisibilityOn()
geometry_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Legend box: annotate cell types in the corner
legend_symbol = vtkSphereSource()
legend_symbol.SetRadius(0.5)
legend_symbol.SetPhiResolution(12)
legend_symbol.SetThetaResolution(12)
legend_symbol.Update()

num_cells = len(cell_type_names)
legend_box = vtkLegendBoxActor()
legend_box.SetNumberOfEntries(num_cells)
for i in range(num_cells):
    rgba = legend_lut.GetTableValue(i)
    legend_box.SetEntry(
        i, legend_symbol.GetOutput(), cell_type_names[i],
        (rgba[0], rgba[1], rgba[2]),
    )
legend_box.UseBackgroundOn()
legend_box.SetBackgroundColor(0.75, 0.75, 0.75)
legend_box.SetBackgroundOpacity(0.8)
legend_box.GetEntryTextProperty().SetFontSize(10)
legend_box.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
legend_box.GetPositionCoordinate().SetValue(0.025, 0.025)
legend_box.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
legend_box.GetPosition2Coordinate().SetValue(0.35, 0.95)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(geometry_actor)
renderer.AddActor(label_actor)
renderer.AddActor(edge_actor)
renderer.AddActor(point_actor)
renderer.AddActor(legend_box)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)

camera = vtkCamera()
camera.Azimuth(-40.0)
camera.Elevation(50.0)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

render_window.SetSize(640, 480)
render_window.SetWindowName("ReadLegacyUnstructuredGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
