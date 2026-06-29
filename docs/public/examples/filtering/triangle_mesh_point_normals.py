#!/usr/bin/env python

# Compute point normals on a triangulated cow mesh using
# vtkTriangleMeshPointNormals and display them as arrow glyphs.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkCleanPolyData,
    vtkGlyph3D,
    vtkTriangleFilter,
    vtkTriangleMeshPointNormals,
)
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

# Triangulate
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(reader.GetOutputPort())

# Clean to merge duplicate points
clean_filter = vtkCleanPolyData()
clean_filter.SetInputConnection(triangle_filter.GetOutputPort())

# Compute point normals for triangle mesh
normals_filter = vtkTriangleMeshPointNormals()
normals_filter.SetInputConnection(clean_filter.GetOutputPort())

# Surface mapper and actor
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(normals_filter.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Arrow glyphs to show normals
glyph_source = vtkArrowSource()

glyph = vtkGlyph3D()
glyph.SetInputConnection(normals_filter.GetOutputPort())
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
renderer.AddActor(surface_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetWindowName("triangle mesh point normals")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
