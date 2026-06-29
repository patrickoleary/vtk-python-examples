#!/usr/bin/env python

# Read an Exodus file, crinkle-clip with ExtractGeometry, write to IOSS, read back, and render.

import glob
import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOIOSS import (
    vtkIOSSReader,
    vtkIOSSWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
output_file = os.path.join(temp_dir, "crinkle_clip.ex2")

# Read the source Exodus file
reader_0 = vtkIOSSReader()
reader_0.SetFileName(os.path.join(data_dir, "Exodus", "can.e.4", "can.e.4.0"))
reader_0.SetGroupNumericVectorFieldComponents(True)
reader_0.UpdateInformation()
reader_0.GetElementBlockSelection().EnableAllArrays()
reader_0.GetNodeSetSelection().EnableAllArrays()
reader_0.GetSideSetSelection().EnableAllArrays()

# Crinkle clip with a plane
clip_plane = vtkPlane()
clip_plane.SetNormal(1, 1, 1)

extract_geometry = vtkExtractGeometry()
extract_geometry.SetImplicitFunction(clip_plane)
extract_geometry.SetInputConnection(reader_0.GetOutputPort())

# Write the clipped data
ioss_writer = vtkIOSSWriter()
ioss_writer.SetFileName(output_file)
ioss_writer.SetInputConnection(extract_geometry.GetOutputPort())
ioss_writer.Write()

# Read the written file back
ioss_reader = vtkIOSSReader()
ioss_reader.SetFileName(output_file)
ioss_reader.SetGroupNumericVectorFieldComponents(True)
ioss_reader.GetElementBlockSelection().EnableAllArrays()
ioss_reader.GetNodeSetSelection().EnableAllArrays()
ioss_reader.GetSideSetSelection().EnableAllArrays()
ioss_reader.UpdateInformation()
ioss_reader.UpdateTimeStep(0.00100001)

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputDataObject(ioss_reader.GetOutputDataObject(0))

# Mapper
surface_mapper = vtkCompositePolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(surface_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ioss exodus writer crinkle clip")
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

# Clean up temp files
for f in glob.glob(os.path.join(temp_dir, "*")):
    os.remove(f)
os.rmdir(temp_dir)
