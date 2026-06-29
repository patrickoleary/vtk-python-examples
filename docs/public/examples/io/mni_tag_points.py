#!/usr/bin/env python

# Write and read MNI tag points with labels, display with glyphs and label placement.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkStringArray,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import (
    vtkPointSource,
    vtkSphereSource,
)
from vtkmodules.vtkIOMINC import (
    vtkMNITagPointReader,
    vtkMNITagPointWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLabel import (
    vtkLabelPlacementMapper,
    vtkPointSetToLabelHierarchy,
)

# Temp file for tag points
temp_dir = tempfile.mkdtemp()
tag_file = os.path.join(temp_dir, "mni-tagtest.tag")

# Create random points in a sphere
sphere_source = vtkPointSource()
sphere_source.SetNumberOfPoints(13)

xform = vtkTransform()
xform.RotateWXYZ(20, 1, 0, 0)

xform_filter = vtkTransformFilter()
xform_filter.SetTransform(xform)
xform_filter.SetInputConnection(sphere_source.GetOutputPort())

# Labels
labels = vtkStringArray()
for lbl in ["0", "1", "2", "3", "Halifax", "Toronto", "Vancouver",
            "Larry", "Bob", "Jackie", "10", "11", "12"]:
    labels.InsertNextValue(lbl)

# Weights
weights = vtkDoubleArray()
for w in [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 0.9, 0.8, 0.7]:
    weights.InsertNextValue(w)

# Write tag points
tag_writer = vtkMNITagPointWriter()
tag_writer.SetFileName(tag_file)
tag_writer.SetInputConnection(sphere_source.GetOutputPort())
tag_writer.SetInputConnection(1, xform_filter.GetOutputPort())
tag_writer.SetLabelText(labels)
tag_writer.SetWeights(weights)
tag_writer.SetComments("Volume 1: sphere points\nVolume 2: transformed points")
tag_writer.Write()

# Read tag points back
tag_reader = vtkMNITagPointReader()
tag_reader.SetFileName(tag_file)

# Label hierarchy
label_text_property = vtkTextProperty()
label_text_property.SetFontSize(12)
label_text_property.SetColor(1.0, 1.0, 0.5)

label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputConnection(tag_reader.GetOutputPort())
label_hierarchy.SetTextProperty(label_text_property)
label_hierarchy.SetLabelArrayName("LabelText")
label_hierarchy.SetMaximumDepth(15)
label_hierarchy.SetTargetLabelCount(12)

label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())
label_mapper.UseDepthBufferOff()
label_mapper.SetShapeToRect()
label_mapper.SetStyleToOutline()

label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Glyph the points as spheres
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.05)

glyph_filter = vtkGlyph3D()
glyph_filter.SetSourceConnection(glyph_source.GetOutputPort())
glyph_filter.SetInputConnection(tag_reader.GetOutputPort())

glyph_mapper = vtkDataSetMapper()
glyph_mapper.SetInputConnection(glyph_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(glyph_mapper)
actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(actor)
renderer.AddViewProp(label_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mni tag points")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()

# Clean up
os.remove(tag_file)
os.rmdir(temp_dir)
