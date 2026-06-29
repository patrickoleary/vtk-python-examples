#!/usr/bin/env python

# Visualize the OBB tree spatial decomposition of a transformed cylinder
# using vtkOBBTree and vtkSpatialRepresentationFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersGeneral import (
    vtkOBBTree,
    vtkSpatialRepresentationFilter,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cylinder and transform it
cylinder = vtkCylinderSource()
cylinder.SetHeight(1)
cylinder.SetRadius(4)
cylinder.SetResolution(100)
cylinder.CappingOff()

xform = vtkTransform()
xform.RotateX(20)
xform.RotateY(10)
xform.RotateZ(27)
xform.Scale(1, 0.7, 0.3)

trans_pd = vtkTransformPolyDataFilter()
trans_pd.SetInputConnection(cylinder.GetOutputPort())
trans_pd.SetTransform(xform)

data_mapper = vtkPolyDataMapper()
data_mapper.SetInputConnection(trans_pd.GetOutputPort())

model_actor = vtkActor()
model_actor.SetMapper(data_mapper)
model_actor.GetProperty().SetColor(1, 0, 0)

# Build OBB tree
obb = vtkOBBTree()
obb.SetMaxLevel(10)
obb.SetNumberOfCellsPerNode(5)
obb.AutomaticOff()

boxes = vtkSpatialRepresentationFilter()
boxes.SetInputConnection(trans_pd.GetOutputPort())
boxes.SetSpatialRepresentation(obb)
boxes.SetGenerateLeaves(1)
boxes.Update()

output = boxes.GetOutput().GetBlock(boxes.GetMaximumLevel() + 1)

box_edges = vtkExtractEdges()
box_edges.SetInputData(output)

box_mapper = vtkPolyDataMapper()
box_mapper.SetInputConnection(box_edges.GetOutputPort())
box_mapper.SetResolveCoincidentTopology(1)

box_actor = vtkActor()
box_actor.SetMapper(box_mapper)
box_actor.GetProperty().SetAmbient(1)
box_actor.GetProperty().SetDiffuse(0)
box_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(model_actor)
renderer.AddActor(box_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("obb cylinder")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
