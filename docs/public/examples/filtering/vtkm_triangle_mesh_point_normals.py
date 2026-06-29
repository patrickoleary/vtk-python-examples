#!/usr/bin/env python
# Demonstrate vtkmTriangleMeshPointNormals with arrow glyphs on a cow mesh.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmTriangleMeshPointNormals
from vtkmodules.vtkFiltersCore import vtkCleanPolyData, vtkGlyph3D, vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read cow mesh.
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

# Triangulate and clean.
tri_filter = vtkTriangleFilter()
tri_filter.SetInputConnection(reader.GetOutputPort())

clean_filter = vtkCleanPolyData()
clean_filter.SetInputConnection(tri_filter.GetOutputPort())

# Compute normals via VTK-m.
norm_filter = vtkmTriangleMeshPointNormals()
norm_filter.SetInputConnection(clean_filter.GetOutputPort())

# Cow actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(norm_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Arrow glyphs for normals.
glyph_source = vtkArrowSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(norm_filter.GetOutputPort())
glyph.SetSourceConnection(glyph_source.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetColorModeToColorByVector()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.5)

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetWindowName("vtkm triangle mesh point normals")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
