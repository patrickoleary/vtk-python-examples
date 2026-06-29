#!/usr/bin/env python

# Compute tangents on a cow mesh and display them as arrow glyphs
# alongside the textured surface.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkPolyDataTangents,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToCylinder
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))

# Add random cell scalars
random_attr = vtkRandomAttributeGenerator()
random_attr.SetInputConnection(reader.GetOutputPort())
random_attr.GenerateAllDataOff()
random_attr.GenerateCellScalarsOn()

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(random_attr.GetOutputPort())
normals.SplittingOff()

# Triangulate
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(normals.GetOutputPort())

# Map texture coordinates
texture_map = vtkTextureMapToCylinder()
texture_map.SetInputConnection(triangle_filter.GetOutputPort())

# Compute tangents
tangents = vtkPolyDataTangents()
tangents.SetInputConnection(texture_map.GetOutputPort())

# Arrow source for tangent glyphs
arrow = vtkArrowSource()
arrow.SetTipResolution(20)
arrow.SetShaftResolution(20)

# Surface mapper
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(tangents.GetOutputPort())

# Tangent glyph mapper
tangent_mapper = vtkGlyph3DMapper()
tangent_mapper.SetInputConnection(tangents.GetOutputPort())
tangent_mapper.SetOrientationArray("TCoords")
tangent_mapper.SetSourceConnection(arrow.GetOutputPort())
tangent_mapper.SetScaleFactor(0.5)

# Texture
image_reader = vtkJPEGReader()
image_reader.SetFileName(os.path.join(data_dir, "tex_debug.jpg"))

texture = vtkTexture()
texture.SetInputConnection(image_reader.GetOutputPort())

# Surface actor
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.SetTexture(texture)

# Tangent glyph actor
tangent_actor = vtkActor()
tangent_actor.SetMapper(tangent_mapper)
tangent_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(tangent_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("polydata tangents")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(3.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
