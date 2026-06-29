#!/usr/bin/env python
# Demonstrate vtkBrokenLineWidget for interactive element selection on an unstructured grid.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPolyData
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSelection import vtkLinearSelector
from vtkmodules.vtkInteractionWidgets import vtkBrokenLineWidget
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "AngularSector.vtk"))
reader.Update()

# Data modification
mesh = reader.GetOutput()
mesh_mb = vtkMultiBlockDataSet()
mesh_mb.SetNumberOfBlocks(1)
mesh_mb.SetBlock(0, mesh)

points = vtkPoints()
points.InsertNextPoint(0.23, 0.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(0.23, 0.04, 0.04)

# Filters
selector = vtkLinearSelector()
selector.SetInputData(mesh_mb)
selector.SetPoints(points)
selector.IncludeVerticesOff()
selector.SetVertexEliminationTolerance(1.0e-12)

extractor = vtkExtractSelection()
extractor.SetInputData(0, mesh_mb)
extractor.SetInputConnection(1, selector.GetOutputPort())
extractor.Update()
out_mb = extractor.GetOutput()
selection = out_mb.GetBlock(0)

# Mapper + Actor: mesh (wireframe)
mesh_mapper = vtkDataSetMapper()
mesh_mapper.SetInputConnection(reader.GetOutputPort())

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(0.23, 0.37, 0.17)
mesh_actor.GetProperty().SetRepresentationToWireframe()

# Mapper + Actor: broken line polydata
line_pd = vtkPolyData()

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(line_pd)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
line_actor.GetProperty().SetLineWidth(2.0)

# Mapper + Actor: selection (wireframe)
sel_mapper = vtkDataSetMapper()
sel_mapper.SetInputData(selection)

sel_actor = vtkActor()
sel_actor.SetMapper(sel_mapper)
sel_actor.GetProperty().SetColor(0.0, 0.0, 0.0)
sel_actor.GetProperty().SetRepresentationToWireframe()

# Text annotation
num_cells = selection.GetNumberOfCells() if selection else 0
txt_actor = vtkTextActor()
txt_actor.SetInput(f"Number of selected elements: {num_cells}")
txt_actor.SetTextScaleModeToViewport()
txt_actor.SetNonLinearFontScale(0.2, 18)
txt_actor.GetTextProperty().SetColor(0.0, 0.0, 1.0)
txt_actor.GetTextProperty().SetFontSize(18)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.4, 0.4, 0.4)
renderer_0.SetBackground2(0.8, 0.8, 0.8)
renderer_0.GradientBackgroundOn()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(mesh_actor)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(1.0, 1.0, 1.0)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddActor(line_actor)
renderer_1.AddActor(sel_actor)
renderer_1.AddActor(txt_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetMultiSamples(0)
render_window.SetWindowName("broken line widget")
render_window.SetSize(600, 300)

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetFocalPoint(0.12, 0.0, 0.0)
camera.SetPosition(0.38, 0.3, 0.15)
camera.SetViewUp(0.0, 0.0, 1.0)
renderer_0.ResetCameraClippingRange()
renderer_1.SetActiveCamera(camera)
renderer_1.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Callback updates selection when the broken line is moved
def broken_line_callback(caller, event_string):
    caller.GetPolyData(line_pd)
    selector.SetPoints(line_pd.GetPoints())
    extractor.Update()
    out = extractor.GetOutput()
    sel = out.GetBlock(0)
    sel_mapper.SetInputData(sel)
    n = sel.GetNumberOfCells() if sel else 0
    txt_actor.SetInput(f"Number of selected elements: {n}")


# Widget
broken_line = vtkBrokenLineWidget()
broken_line.SetInteractor(interactor)
broken_line.SetInputData(mesh)
broken_line.SetPriority(1.0)
broken_line.KeyPressActivationOff()
broken_line.PlaceWidget()
broken_line.ProjectToPlaneOff()
broken_line.SetHandleSizeFactor(1.2)
broken_line.InitializeHandles(points)
broken_line.GetPolyData(line_pd)
broken_line.AddObserver("InteractionEvent", broken_line_callback)
broken_line.On()

interactor.Initialize()
interactor.Start()
