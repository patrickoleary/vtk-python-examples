#!/usr/bin/env python

# Demonstrate vtkBandedPolyDataContourFilter handling anomalous spikes from
# edges where the difference between end point scalar values is in the order
# of the internal tolerance value. Verifies output bounds do not exceed input.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Scalar values with very small differences near tolerance
values = [-10.0, -5e-6, -1e-6,
          -10.0, -7e-6, -1e-6]

# Generate two quads: 3--4--5 / |  |  | / 0--1--2
points = vtkPoints()
num_x = 3
num_y = int(len(values) / num_x)
for y in range(num_y):
    for x in range(num_x):
        points.InsertNextPoint(x, y, 0)

connectivity = [(0, 1, 4, 3), (1, 2, 5, 4)]
quads = vtkCellArray()
for quad in connectivity:
    quads.InsertNextCell(4, quad)

poly = vtkPolyData()
poly.SetPoints(points)
poly.SetPolys(quads)

array = vtkDoubleArray()
for s in values:
    array.InsertNextValue(s)
poly.GetPointData().SetScalars(array)

inbounds = poly.GetBounds()

# Banded contour filter with adjusted clip tolerance
num_contours = 6
high = max(values)
low = min(values)

banded_contour = vtkBandedPolyDataContourFilter()
banded_contour.GenerateContourEdgesOn()
banded_contour.SetScalarModeToValue()
banded_contour.SetInputData(poly)
banded_contour.GenerateValues(num_contours, low, high)
banded_contour.SetClipTolerance(1e-6)
banded_contour.SetScalarModeToIndex()

# Bands mapper and actor
bands_mapper = vtkPolyDataMapper()
bands_mapper.SetInputConnection(banded_contour.GetOutputPort())
bands_mapper.SetScalarModeToUseCellData()
bands_mapper.SetScalarRange(0, num_contours - 1)

bands_actor = vtkActor()
bands_actor.SetMapper(bands_mapper)

# Contour edges
edges_mapper = vtkPolyDataMapper()
edges_mapper.SetInputConnection(banded_contour.GetOutputPort(1))
edges_mapper.ScalarVisibilityOff()

edges_actor = vtkActor()
edges_actor.GetProperty().SetColor(0.4, 0.4, 0.4)
edges_actor.SetMapper(edges_mapper)

# Input polydata edges for reference
input_edges = vtkExtractEdges()
input_edges.SetInputDataObject(0, poly)

input_edges_mapper = vtkPolyDataMapper()
input_edges_mapper.SetInputConnection(input_edges.GetOutputPort())
input_edges_mapper.ScalarVisibilityOff()

input_edges_actor = vtkActor()
input_edges_actor.GetProperty().SetColor(1, 1, 1)
input_edges_actor.GetProperty().EdgeVisibilityOn()
input_edges_actor.GetProperty().RenderLinesAsTubesOn()
input_edges_actor.SetMapper(input_edges_mapper)

# Verify output bounds don't exceed input bounds
bands_mapper.Update()
outbounds = bands_mapper.GetInputDataObject(0, 0).GetBounds()
if (inbounds[0] > outbounds[0] or inbounds[1] < outbounds[1] or
    inbounds[2] > outbounds[2] or inbounds[3] < outbounds[3] or
    inbounds[4] > outbounds[4] or inbounds[5] < outbounds[5]):
    print("Output bounds exceed input bounds")
    print(f"input bounds={inbounds}")
    print(f"output bounds={outbounds}")

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(bands_actor)
renderer.AddViewProp(edges_actor)
renderer.AddViewProp(input_edges_actor)
renderer.SetBackground(0.6, 0.6, 0.6)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("banded contour edge spikes")

# Scene
renderer.GetActiveCamera().SetFocalPoint(1, 0.5, 0)
renderer.GetActiveCamera().SetPosition(1, 0.5, 5)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
