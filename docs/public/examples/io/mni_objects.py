#!/usr/bin/env python

# Read, write, and re-read MNI object files, display polygon and line mesh in three viewports.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkExtractEdges,
    vtkStripper,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkClipClosedSurface,
    vtkCurvatures,
)
from vtkmodules.vtkIOMINC import (
    vtkMNIObjectReader,
    vtkMNIObjectWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Read the ascii MNI surface mesh
ascii_reader = vtkMNIObjectReader()
ascii_reader.SetFileName(os.path.join(data_dir, "mni-surface-mesh.obj"))

surface_property = vtkProperty()
surface_property.SetDiffuseColor(0.95, 0.90, 0.70)

property_1 = ascii_reader.GetProperty()

# Remove normals to force the writer to regenerate them
clip_surface = vtkClipClosedSurface()
clip_surface.SetInputConnection(ascii_reader.GetOutputPort())

# Make triangle strips to force the writer to decompose them
stripper = vtkStripper()
stripper.SetInputConnection(clip_surface.GetOutputPort())

# Write binary and read back
binary_file = os.path.join(temp_dir, "mni-surface-mesh-binary.obj")
binary_writer = vtkMNIObjectWriter()
binary_writer.SetInputConnection(stripper.GetOutputPort())
binary_writer.SetFileName(binary_file)
binary_writer.SetProperty(surface_property)
binary_writer.SetFileTypeToBinary()
binary_writer.Write()

binary_reader = vtkMNIObjectReader()
binary_reader.SetFileName(binary_file)
property_2 = binary_reader.GetProperty()

# Make a polyline object with curvature scalars
curvatures_filter = vtkCurvatures()
curvatures_filter.SetInputConnection(ascii_reader.GetOutputPort())

curvature_lut = vtkLookupTable()
curvature_lut.SetRange(-14.5104, 29.0208)
curvature_lut.SetAlphaRange(1.0, 1.0)
curvature_lut.SetSaturationRange(1.0, 1.0)
curvature_lut.SetValueRange(1.0, 1.0)
curvature_lut.SetHueRange(0.0, 1.0)
curvature_lut.Build()

curvature_mapper = vtkDataSetMapper()
curvature_mapper.SetLookupTable(curvature_lut)
curvature_mapper.UseLookupTableScalarRangeOn()

edge_filter = vtkExtractEdges()
edge_filter.SetInputConnection(curvatures_filter.GetOutputPort())

# Write ascii lines and read back
line_file = os.path.join(temp_dir, "mni-wire-mesh-ascii.obj")
line_writer = vtkMNIObjectWriter()
line_writer.SetMapper(curvature_mapper)
line_writer.SetInputConnection(edge_filter.GetOutputPort())
line_writer.SetFileName(line_file)
line_writer.Write()

line_reader = vtkMNIObjectReader()
line_reader.SetFileName(line_file)

# Mappers
mapper_0 = vtkDataSetMapper()
mapper_0.SetInputConnection(ascii_reader.GetOutputPort())

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(binary_reader.GetOutputPort())

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(line_reader.GetOutputPort())

# Actors
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.SetProperty(property_1)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetProperty(property_2)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.67, 1)
renderer_1.AddActor(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.67, 0, 1, 1)
renderer_2.AddActor(actor_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("mni objects")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Dolly(1.2)
renderer_0.ResetCameraClippingRange()

renderer_1.ResetCamera()
renderer_1.GetActiveCamera().Dolly(1.2)
renderer_1.ResetCameraClippingRange()

renderer_2.ResetCamera()
renderer_2.GetActiveCamera().Dolly(1.2)
renderer_2.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()

# Clean up temp files
for f in [binary_file, line_file]:
    if os.path.exists(f):
        os.remove(f)
os.rmdir(temp_dir)
