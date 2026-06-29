#!/usr/bin/env python

# Read partitioned Exodus file, clip it, write with vtkIOSSWriter, read back, and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOIOSS import vtkIOSSReader, vtkIOSSWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read partitioned Exodus file
reader_0 = vtkIOSSReader()
reader_0.SetFileName(os.path.join(data_dir, "Exodus", "can.e.4", "can.e.4.0"))
reader_0.UpdateInformation()
reader_0.GetElementBlockSelection().EnableAllArrays()
reader_0.GetNodeSetSelection().EnableAllArrays()
reader_0.GetSideSetSelection().EnableAllArrays()

# Clip
clip_plane = vtkPlane()
clip_plane.SetNormal(1, 0, 0)
clip_plane.SetOrigin(0.21706008911132812, 4, -5.110947132110596)

clip_filter = vtkTableBasedClipDataSet()
clip_filter.SetClipFunction(clip_plane)
clip_filter.SetInputConnection(reader_0.GetOutputPort())

# Write clipped result
temp_dir = tempfile.mkdtemp()
ofname = os.path.join(temp_dir, "test_ioss_exodus_parallel_writer.ex2")

ioss_writer = vtkIOSSWriter()
ioss_writer.SetFileName(ofname)
ioss_writer.SetInputConnection(clip_filter.GetOutputPort())
ioss_writer.PreserveOriginalIdsOn()
ioss_writer.Write()

# Read back
ioss_reader = vtkIOSSReader()
ioss_reader.ReadAllFilesToDetermineStructureOn()
ioss_reader.SetFileName(ofname)
ioss_reader.UpdateInformation()
ioss_reader.GetElementBlockSelection().EnableAllArrays()
ioss_reader.GetNodeSetSelection().EnableAllArrays()
ioss_reader.GetSideSetSelection().EnableAllArrays()

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(ioss_reader.GetOutputPort())

# Mapper
surface_mapper = vtkCompositePolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(surface_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ioss exodus parallel writer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(10.0, 10.0, 5.0)
camera.SetViewUp(0.0, 0.4, 1.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
