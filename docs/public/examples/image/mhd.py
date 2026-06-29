#!/usr/bin/env python

# Read image data, write as MetaImage, re-read, contour, and render.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOImage import (
    vtkImageReader,
    vtkMetaImageReader,
    vtkMetaImageWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()
mhd_file = os.path.join(temp_dir, "mhdWriter.mhd")

# Read image data
image_reader = vtkImageReader()
image_reader.SetDataByteOrderToLittleEndian()
image_reader.SetDataExtent(0, 63, 0, 63, 1, 93)
image_reader.SetDataSpacing(3.2, 3.2, 1.5)
image_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
image_reader.SetDataMask(0x7fff)
image_reader.Update()

# Write as MetaImage
meta_writer = vtkMetaImageWriter()
meta_writer.SetFileName(mhd_file)
meta_writer.SetInputData(image_reader.GetOutput())
meta_writer.Write()

# Re-read
meta_reader = vtkMetaImageReader()
meta_reader.SetFileName(mhd_file)
meta_reader.Update()

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(256)
lookup_table.SetHueRange(0.6667, 0)
lookup_table.SetSaturationRange(1, 1)
lookup_table.SetValueRange(1, 1)
lookup_table.SetTableRange(37.3531, 260)
lookup_table.SetVectorComponent(0)
lookup_table.Build()

# Contour
contour = vtkContourFilter()
contour.SetInputData(meta_reader.GetOutput(0))
contour.SetValue(0, 1150)
contour.SetComputeNormals(1)
contour.SetComputeGradients(0)
contour.SetComputeScalars(0)

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(contour.GetOutputPort())
poly_mapper.SetScalarRange(0, 1)
poly_mapper.UseLookupTableScalarRangeOn()
poly_mapper.SetScalarVisibility(1)
poly_mapper.SetScalarModeToUsePointFieldData()
poly_mapper.SelectColorArray("ImageFile")
poly_mapper.SetLookupTable(lookup_table)

# Actor
contour_actor = vtkActor()
contour_actor.SetMapper(poly_mapper)
contour_actor.GetProperty().SetRepresentationToSurface()
contour_actor.GetProperty().SetInterpolationToGouraud()
contour_actor.GetProperty().SetAmbient(0)
contour_actor.GetProperty().SetDiffuse(1)
contour_actor.GetProperty().SetSpecular(0)
contour_actor.GetProperty().SetSpecularPower(1)
contour_actor.GetProperty().SetSpecularColor(1, 1, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(contour_actor)
renderer.SetBackground(0.33, 0.35, 0.43)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mhd")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up temp files
for f in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, f))
os.rmdir(temp_dir)
