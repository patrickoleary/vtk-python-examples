#!/usr/bin/env python
# Demonstrate vtkCirclePackLayout with front chain strategy on a flat tree.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkInfovisCore import vtkTreeFieldAggregator
from vtkmodules.vtkInfovisLayout import (
    vtkCirclePackFrontChainLayoutStrategy,
    vtkCirclePackLayout,
    vtkCirclePackToPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Size values for leaf nodes.
values = [
    1, 100, 1, 400, 500, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 400, 1, 100, 1, 400, 500, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 1, 400, 500, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 400, 1, 100, 1, 400, 500, 1, 1, 1, 1, 77, 1, 1, 1, 1, 1,
    1, 100, 1, 400, 500, 1, 1, 1, 1, 1, 15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 400, 1, 100, 1,
    400, 500, 1, 1, 1, 1, 99, 1, 1, 1, 1, 1, 1, 100, 1, 400, 500, 1, 1, 1, 1, 1, 1, 107, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 432, 1, 100, 1, 400, 500, 1, 1, 259, 1, 1, 1, 1, 1, 1, 242, 1, 100, 306,
    400, 500, 1, 1, 1, 1, 1, 1, 91, 1, 1, 46, 1, 1, 1, 1, 1, 1, 1, 1, 1, 400, 1, 100, 1, 400, 500, 1,
    1, 1, 1, 1, 47, 1, 1, 1, 1, 1, 100, 1, 400, 500, 1, 1, 1, 150, 1, 90, 1, 1, 1, 1, 10, 1, 1, 456,
    1, 1, 1, 1, 1, 40, 1, 100, 1, 400, 500, 1, 1, 1, 1, 1, 1, 1, 98, 1, 1, 1, 100, 1, 400, 500, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 105, 1, 1, 1, 15, 1, 1, 1, 410, 1, 320, 1, 410, 450, 1, 1, 136, 1, 1,
    1, 1, 458, 1, 1,
]

# Build flat tree: root with all leaf children.
builder = vtkMutableDirectedGraph()
size_arr = vtkIntArray()
size_arr.SetName("size")
builder.GetVertexData().AddArray(size_arr)
builder.AddVertex()
size_arr.InsertNextValue(0)
for val in values:
    builder.AddChild(0)
    size_arr.InsertNextValue(val)

tree = vtkTree()
tree.CheckedShallowCopy(builder)

# Aggregate field.
aggregator = vtkTreeFieldAggregator()
aggregator.SetInputData(tree)
aggregator.SetField("size")
aggregator.SetLeafVertexUnitSize(False)

# Front chain layout.
front_chain = vtkCirclePackFrontChainLayoutStrategy()

layout = vtkCirclePackLayout()
layout.SetLayoutStrategy(front_chain)
layout.SetInputConnection(aggregator.GetOutputPort())

# Convert to polydata.
circle_pack_to_poly = vtkCirclePackToPolyData()
circle_pack_to_poly.SetInputConnection(layout.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(circle_pack_to_poly.GetOutputPort())
mapper.SetScalarRange(0, 600)
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("size")

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("circle pack layout strategy")

# Scene
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
