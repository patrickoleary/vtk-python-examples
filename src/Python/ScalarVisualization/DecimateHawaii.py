#!/usr/bin/env python

# Decimate the Hawaii elevation dataset and compare with the original.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkPolyDataNormals,
)
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
sienna = (0.627, 0.322, 0.176)
wheat = (0.961, 0.871, 0.702)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "honolulu.vtk")

# Reader: load the Hawaii elevation data
hawaii = vtkPolyDataReader()
hawaii.SetFileName(file_name)
hawaii.Update()

# Filter: decimate the mesh by 90 percent
deci = vtkDecimatePro()
deci.SetInputConnection(hawaii.GetOutputPort())
deci.SetTargetReduction(0.9)
deci.PreserveTopologyOn()

# Filter: compute normals for the decimated mesh
decimated_normals = vtkPolyDataNormals()
decimated_normals.SetInputConnection(deci.GetOutputPort())
decimated_normals.FlipNormalsOn()
decimated_normals.SetFeatureAngle(60)

# Mapper: map decimated mesh to graphics primitives
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimated_normals.GetOutputPort())
decimated_mapper.SetScalarRange(0, 2000)

# Actor: display the decimated mesh
decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)

# Filter: compute normals for the original mesh
original_normals = vtkPolyDataNormals()
original_normals.SetInputConnection(hawaii.GetOutputPort())
original_normals.FlipNormalsOn()
original_normals.SetFeatureAngle(60)

# Mapper: map original mesh to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(original_normals.GetOutputPort())
original_mapper.SetScalarRange(0, 2000)

# Actor: display the original mesh
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)

# Renderer: left viewport shows decimated mesh
renderer1 = vtkRenderer()
renderer1.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer1.AddActor(decimated_actor)
renderer1.SetBackground(sienna)
renderer1.GetActiveCamera().SetPosition(0, -1, 0)
renderer1.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer1.GetActiveCamera().SetViewUp(0, 0, 1)
renderer1.ResetCamera()
renderer1.GetActiveCamera().Dolly(1.5)
renderer1.ResetCameraClippingRange()

# Renderer: right viewport shows original mesh
renderer2 = vtkRenderer()
renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer2.AddActor(original_actor)
renderer2.SetBackground(wheat)
renderer2.SetActiveCamera(renderer1.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer1)
render_window.AddRenderer(renderer2)
render_window.SetWindowName("DecimateHawaii")
render_window.SetSize(800, 400)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
