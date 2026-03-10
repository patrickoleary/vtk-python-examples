#!/usr/bin/env python

# Pseudo volume rendering using translucent cut planes composited back-to-front.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkPolyDataNormals,
    vtkStripper,
    vtkStructuredGridOutlineFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
white_rgb = (1.0, 1.0, 1.0)
banana_rgb = (0.890, 0.812, 0.341)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data: locate the PLOT3D combustor dataset
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
xyz_file = str(data_dir / "combxyz.bin")
q_file = str(data_dir / "combq.bin")

# Source: read PLOT3D structured grid data
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(xyz_file)
pl3d.SetQFileName(q_file)
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

pl3d_output = pl3d.GetOutput().GetBlock(0)

# ExtractGrid: limit data for experimentation
extract = vtkExtractGrid()
extract.SetVOI(1, 55, -1000, 1000, -1000, 1000)
extract.SetInputData(pl3d_output)

# Plane: the implicit plane used for cutting
plane = vtkPlane()
plane.SetOrigin(0, 4, 2)
plane.SetNormal(0, 1, 0)

# Cutter: process each contour value over all cells (sorted by cell for
# ordered output, key to compositing)
cutter = vtkCutter()
cutter.SetInputConnection(extract.GetOutputPort())
cutter.SetCutFunction(plane)
cutter.GenerateCutScalarsOff()
cutter.SetSortByToSortByCell()

# LookupTable: color map for the cut planes
clut = vtkLookupTable()
clut.SetHueRange(0, 0.67)
clut.Build()

# Mapper: map cutter output to graphics primitives
cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())
cutter_mapper.SetScalarRange(0.18, 0.7)
cutter_mapper.SetLookupTable(clut)

# Actor: cut planes
cut_actor = vtkActor()
cut_actor.SetMapper(cutter_mapper)

# ContourFilter: add an isosurface for context
iso = vtkContourFilter()
iso.SetInputData(pl3d_output)
iso.SetValue(0, 0.22)

normals = vtkPolyDataNormals()
normals.SetInputConnection(iso.GetOutputPort())
normals.SetFeatureAngle(60)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetDiffuseColor(tomato_rgb)
iso_actor.GetProperty().SetSpecularColor(white_rgb)
iso_actor.GetProperty().SetDiffuse(0.8)
iso_actor.GetProperty().SetSpecular(0.5)
iso_actor.GetProperty().SetSpecularPower(30)

# Outline: structured grid bounding box rendered as tubes
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(pl3d_output)

outline_strip = vtkStripper()
outline_strip.SetInputConnection(outline.GetOutputPort())

outline_tubes = vtkTubeFilter()
outline_tubes.SetInputConnection(outline_strip.GetOutputPort())
outline_tubes.SetRadius(0.1)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_tubes.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(banana_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(slate_gray_rgb)

# Camera: set a specific viewpoint
renderer.GetActiveCamera().SetClippingRange(3.95297, 50)
renderer.GetActiveCamera().SetFocalPoint(9.71821, 0.458166, 29.3999)
renderer.GetActiveCamera().SetPosition(2.7439, -37.3196, 38.7167)
renderer.GetActiveCamera().ComputeViewPlaneNormal()
renderer.GetActiveCamera().SetViewUp(-0.16123, 0.264271, 0.950876)

# Cut planes: generate n translucent cut planes normal to the camera view
n = 20
opacity = 1.0 / float(n) * 5.0
plane.SetNormal(renderer.GetActiveCamera().GetViewPlaneNormal())
plane.SetOrigin(renderer.GetActiveCamera().GetFocalPoint())
cutter.GenerateValues(n, -5, 5)
clut.SetAlphaRange(opacity, opacity)
cut_actor.GetProperty().SetOpacity(1)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PseudoVolumeRendering")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
