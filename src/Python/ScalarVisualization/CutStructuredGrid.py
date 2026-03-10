#!/usr/bin/env python

# Cut through a structured grid with a plane.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
slate_gray = (0.439, 0.502, 0.565)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
xyz_file = str(data_dir / "combxyz.bin")
q_file = str(data_dir / "combq.bin")

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(xyz_file)
pl3d.SetQFileName(q_file)
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)

# Implicit function: cutting plane through the dataset center
plane = vtkPlane()
plane.SetOrigin(sg.GetCenter())
plane.SetNormal(-0.287, 0, 0.9579)

# Filter: cut the structured grid with the plane
plane_cut = vtkCutter()
plane_cut.SetInputData(sg)
plane_cut.SetCutFunction(plane)

# Mapper: map the cut surface with scalar coloring
cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(plane_cut.GetOutputPort())
cut_mapper.SetScalarRange(sg.GetPointData().GetScalars().GetRange())

# Actor: display the cut surface
cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Filter: extract a computational plane at constant k for comparison
comp_plane = vtkStructuredGridGeometryFilter()
comp_plane.SetInputData(sg)
comp_plane.SetExtent(0, 100, 0, 100, 9, 9)

# Mapper: map the computational plane
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(comp_plane.GetOutputPort())
plane_mapper.ScalarVisibilityOff()

# Actor: display the computational plane as wireframe
plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetRepresentationToWireframe()
plane_actor.GetProperty().SetColor(wheat)

# Filter: structured grid outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

# Mapper: map outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(wheat)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(plane_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(slate_gray)

camera = renderer.GetActiveCamera()
camera.SetPosition(5.02611, -23.535, 50.3979)
camera.SetFocalPoint(9.33614, 0.0414149, 30.112)
camera.SetViewUp(-0.0676794, 0.657814, 0.750134)
camera.SetDistance(31.3997)
camera.SetClippingRange(12.1468, 55.8147)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CutStructuredGrid")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
