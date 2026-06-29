#!/usr/bin/env python

# Demonstrate direct selection rendering with index-based and value-based cell selection.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes, vtkSelection, vtkSelectionNode
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere data
sphere = vtkSphereSource()
sphere.Update()
pd = sphere.GetOutput()
nb_polys = pd.GetNumberOfPolys()

# Add a cell data array with values 0..3
id_array = vtkIdTypeArray()
id_array.SetNumberOfTuples(nb_polys)
id_array.SetName("Odd")
for i in range(nb_polys):
    id_array.SetComponent(i, 0, i % 4)
pd.GetCellData().AddArray(id_array)

# Selection by index: select cells 0 and 3
mapper_idx = vtkPolyDataMapper()
mapper_idx.SetInputData(pd)

selection = vtkSelection()
selection_node = vtkSelectionNode()
selection.AddNode(selection_node)

selection_array = vtkIdTypeArray()
selection_array.SetNumberOfTuples(2)
selection_array.SetComponent(0, 0, 0)
selection_array.SetComponent(1, 0, 3)

selection_attr = vtkDataSetAttributes()
selection_attr.AddArray(selection_array)

selection_node.SetSelectionData(selection_attr)
selection_node.SetFieldType(vtkSelectionNode.CELL)
selection_node.SetContentType(vtkSelectionNode.INDICES)

mapper_idx.SetSelection(selection)

actor_idx = vtkActor()
actor_idx.GetProperty().SetSelectionColor(0.0, 0.0, 1.0, 1.0)
actor_idx.GetProperty().SetSelectionLineWidth(3.0)
actor_idx.SetMapper(mapper_idx)

# Selection by value: select cells where "Odd" == 0
mapper_val = vtkPolyDataMapper()
mapper_val.SetInputData(pd)

selection_val = vtkSelection()
selection_node_val = vtkSelectionNode()
selection_val.AddNode(selection_node_val)

selection_array_val = vtkIdTypeArray()
selection_array_val.SetNumberOfTuples(1)
selection_array_val.SetComponent(0, 0, 0)
selection_array_val.SetName("Odd")

selection_attr_val = vtkDataSetAttributes()
selection_attr_val.AddArray(selection_array_val)

selection_node_val.SetSelectionData(selection_attr_val)
selection_node_val.SetFieldType(vtkSelectionNode.CELL)
selection_node_val.SetContentType(vtkSelectionNode.VALUES)

mapper_val.SetSelection(selection_val)

actor_val = vtkActor()
actor_val.SetPosition(1, 0, 0)
actor_val.GetProperty().SetSelectionColor(0.0, 0.0, 0.0, 0.2)
actor_val.GetProperty().SetSelectionLineWidth(1.0)
actor_val.SetMapper(mapper_val)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(actor_idx)
renderer.AddActor(actor_val)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("direct selection")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
