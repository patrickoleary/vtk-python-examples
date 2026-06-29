#!/usr/bin/env python

# Demonstrate vtkBandedPolyDataContourFilter with cells whose scalar values
# do not monotonously climb from minimum to maximum. Shows contour bands,
# cell edges, contour edges, and scalar labels on a 4x4 grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Build a 4x4 grid of points
points = vtkPoints()
scalars = vtkDoubleArray()
for y in [0, 1, 2, 3]:
    for x in [0, 1, 2, 3]:
        points.InsertNextPoint([x, y, 0])

# Non-monotonic scalar values
for v in [9, 0, 0, 9,
          3, 4, 5, 3,
          9, 5, 0, 9,
          0, 9, 9, 0]:
    scalars.InsertNextValue(v)

# Quad cells
polys = vtkCellArray()
for cell in [[0, 1, 5, 4], [2, 3, 7, 6], [8, 9, 13, 12], [10, 11, 15, 14]]:
    polys.InsertNextCell(4)
    for p in cell:
        polys.InsertCellPoint(p)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.GetPointData().SetScalars(scalars)
poly_data.SetPolys(polys)

producer = vtkTrivialProducer()
producer.SetOutput(poly_data)

# Generate contour bands
bands = vtkBandedPolyDataContourFilter()
bands.SetScalarModeToIndex()
bands.GenerateContourEdgesOn()
bands.ClippingOff()
bands.SetInputConnection(producer.GetOutputPort())

# Set contour values
clip_values = [0, 2, 4, 6, 8, 10]
for v in clip_values:
    bands.SetValue(clip_values.index(v), v)
bands.Update()

# Map indices to clip values
out_indices = bands.GetOutput().GetCellData().GetArray("Scalars")
out_scalars = vtkDoubleArray()
out_scalars.SetName("values")
out_scalars.SetNumberOfTuples(out_indices.GetNumberOfTuples())
for i in range(out_indices.GetNumberOfTuples()):
    index = int(out_indices.GetValue(i))
    out_scalars.SetComponent(i, 0, bands.GetValue(index))

# Output data with mapped values
poly = vtkPolyData()
poly.ShallowCopy(bands.GetOutput())
poly.GetCellData().SetScalars(out_scalars)

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetRange(clip_values[0], clip_values[-1])
lookup_table.SetRampToLinear()
lookup_table.SetHueRange(1, 1)
lookup_table.SetSaturationRange(0, 1)
lookup_table.SetValueRange(0, 1)
lookup_table.SetNumberOfColors(len(clip_values) - 1)

# Contour bands mapper and actor
bands_mapper = vtkPolyDataMapper()
bands_mapper.SetInputDataObject(poly)
bands_mapper.ScalarVisibilityOn()
bands_mapper.SetScalarModeToUseCellData()
bands_mapper.SetScalarRange(out_scalars.GetRange())
bands_mapper.SetLookupTable(lookup_table)
bands_mapper.UseLookupTableScalarRangeOn()

bands_actor = vtkActor()
bands_actor.SetMapper(bands_mapper)

# Cell edges
band_cell_edges = vtkExtractEdges()
band_cell_edges.SetInputDataObject(poly)

band_cell_edges_mapper = vtkPolyDataMapper()
band_cell_edges_mapper.ScalarVisibilityOff()
band_cell_edges_mapper.SetInputConnection(band_cell_edges.GetOutputPort())

band_cell_edges_actor = vtkActor()
band_cell_edges_actor.SetMapper(band_cell_edges_mapper)
band_cell_edges_actor.GetProperty().SetColor(0.4, 0.4, 0.4)

# Contour edges from BPDCF
band_edges_mapper = vtkPolyDataMapper()
band_edges_mapper.SetInputConnection(bands.GetOutputPort(1))

band_edges_actor = vtkActor()
band_edges_actor.SetMapper(band_edges_mapper)
band_edges_actor.GetProperty().SetColor(1, 1, 1)
band_edges_actor.GetProperty().SetLineWidth(1.3)

# Scalar labels
scalar_value_mapper = vtkLabeledDataMapper()
scalar_value_mapper.SetInputConnection(producer.GetOutputPort())
scalar_value_mapper.SetLabelModeToLabelScalars()
scalar_value_mapper.SetLabelFormat("{:1.3f}")

scalar_value_actor = vtkActor2D()
scalar_value_actor.SetMapper(scalar_value_mapper)

# Renderer and camera
renderer = vtkRenderer()
renderer.AddViewProp(bands_actor)
renderer.AddViewProp(band_cell_edges_actor)
renderer.AddViewProp(band_edges_actor)
renderer.AddViewProp(scalar_value_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(450, 450)
render_window.AddRenderer(renderer)
render_window.SetWindowName("banded contour non monotonous")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1.5, 1.5, 1)
camera.SetFocalPoint(1.5, 1.5, 0)
camera.SetViewUp(0, 1, 0)
camera.SetViewAngle(125)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
