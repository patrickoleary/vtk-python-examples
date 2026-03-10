#!/usr/bin/env python

# Read a VTK XML multi-block dataset (.vtm) file using
# vtkXMLMultiBlockDataReader and display each block in a different color.
# A small multi-block dataset (sphere + cube) is generated and written to
# disk if the file does not already exist.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkIOXML import vtkXMLMultiBlockDataReader, vtkXMLMultiBlockDataWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
vtm_path = data_dir / "multi_block.vtm"

# Generate a multi-block dataset if the file does not exist
if not vtm_path.exists():
    sphere = vtkSphereSource()
    sphere.SetCenter(-1.5, 0, 0)
    sphere.SetPhiResolution(32)
    sphere.SetThetaResolution(32)
    sphere.Update()

    cube = vtkCubeSource()
    cube.SetCenter(1.5, 0, 0)
    cube.Update()

    mb = vtkMultiBlockDataSet()
    mb.SetNumberOfBlocks(2)
    mb.SetBlock(0, sphere.GetOutput())
    mb.SetBlock(1, cube.GetOutput())

    writer = vtkXMLMultiBlockDataWriter()
    writer.SetFileName(str(vtm_path))
    writer.SetInputData(mb)
    writer.Write()

# Reader: load the multi-block dataset
reader = vtkXMLMultiBlockDataReader()
reader.SetFileName(str(vtm_path))
reader.Update()

# Mapper: composite mapper handles multi-block data directly
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadXMLMultiBlockData")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
