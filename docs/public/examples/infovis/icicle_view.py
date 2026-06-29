#!/usr/bin/env python
# Demonstrate icicle (slice-and-dice) tree layout with area coloring and labels.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInfovisCore import vtkStringToNumeric
from vtkmodules.vtkInfovisLayout import vtkAreaLayout, vtkSliceAndDiceLayoutStrategy, vtkTreeMapToPolyData
from vtkmodules.vtkIOInfovis import vtkXMLTreeReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read tree from XML.
reader = vtkXMLTreeReader()
reader.SetFileName(os.path.join(data_dir, "smalltest.xml"))

string_to_numeric = vtkStringToNumeric()
string_to_numeric.SetInputConnection(reader.GetOutputPort())

# Area layout with slice-and-dice strategy (icicle layout).
area_layout = vtkAreaLayout()
area_layout.SetInputConnection(string_to_numeric.GetOutputPort())
slice_and_dice_strategy = vtkSliceAndDiceLayoutStrategy()
area_layout.SetLayoutStrategy(slice_and_dice_strategy)
area_layout.SetSizeArrayName("size")
area_layout.Update()

# Convert tree areas to polydata.
tree_map_to_polydata = vtkTreeMapToPolyData()
tree_map_to_polydata.SetInputConnection(area_layout.GetOutputPort())
tree_map_to_polydata.Update()

# Area mapper and actor (colored by "size").
area_mapper = vtkPolyDataMapper()
area_mapper.SetInputConnection(tree_map_to_polydata.GetOutputPort())
area_mapper.SetScalarModeToUseCellFieldData()
area_mapper.SelectColorArray("size")
area_mapper.SetScalarVisibility(True)
area_actor = vtkActor()
area_actor.SetMapper(area_mapper)

# Area labels.
area_label_mapper = vtkLabeledDataMapper()
area_label_mapper.SetInputConnection(tree_map_to_polydata.GetOutputPort())
area_label_mapper.SetLabelModeToLabelFieldData()
area_label_mapper.SetFieldDataName("label")
area_label_mapper.GetLabelTextProperty().SetColor(0.0, 0.0, 0.0)
area_label_mapper.GetLabelTextProperty().SetFontSize(12)
area_label_mapper.GetLabelTextProperty().ShadowOn()
area_label_actor = vtkActor2D()
area_label_actor.SetMapper(area_label_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(area_actor)
renderer.AddActor(area_label_actor)
renderer.SetBackground(0.2, 0.2, 0.3)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("icicle view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
