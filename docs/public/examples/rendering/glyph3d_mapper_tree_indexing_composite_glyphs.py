#!/usr/bin/env python

# Demonstrate vtkGlyph3DMapper with tree-indexed composite glyph sources.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Input points with glyph index and color arrays
input_data = vtkPolyData()
points = vtkPoints()
index_array = vtkIntArray()
index_array.SetName("GlyphIndex")
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName("Colors")

# row=0, col=0: x=(2-0)*5=10, r=128, g=85, b=64
points.InsertNextPoint(10, 0, 0.0)
index_array.InsertNextValue(0)
colors.InsertNextTuple3(128, 85, 64)

# row=0, col=1: x=(2-1)*5=5, r=128, g=170, b=128
points.InsertNextPoint(5, 0, 0.0)
index_array.InsertNextValue(1)
colors.InsertNextTuple3(128, 170, 128)

# row=0, col=2: x=(2-2)*5=0, r=128, g=255, b=191
points.InsertNextPoint(0, 0, 0.0)
index_array.InsertNextValue(2)
colors.InsertNextTuple3(128, 255, 191)

# row=1, col=0: x=0*5=0, r=255, g=85, b=128
points.InsertNextPoint(0, 5, 0.0)
index_array.InsertNextValue(0)
colors.InsertNextTuple3(255, 85, 128)

# row=1, col=1: x=1*5=5, r=255, g=170, b=191
points.InsertNextPoint(5, 5, 0.0)
index_array.InsertNextValue(1)
colors.InsertNextTuple3(255, 170, 191)

# row=1, col=2: x=2*5=10, r=255, g=255, b=255
points.InsertNextPoint(10, 5, 0.0)
index_array.InsertNextValue(2)
colors.InsertNextTuple3(255, 255, 255)

input_data.SetPoints(points)
input_data.GetPointData().AddArray(index_array)
input_data.GetPointData().AddArray(colors)

# Transform for alternate glyph versions
transform = vtkTransform()
transform.Identity()
transform.RotateZ(45.0)
transform.Scale(0.5, 2, 1.0)
transform.Translate(0.5, 0.5, 0.5)

# Glyph source 0: arrow + transformed arrow
s0a = vtkArrowSource()
s0b = vtkTransformFilter()
s0b.SetInputConnection(s0a.GetOutputPort())
s0b.SetTransform(transform)
s0a.Update()
s0b.Update()

# Glyph source 1: cube + transformed cube
s1a = vtkCubeSource()
s1b = vtkTransformFilter()
s1b.SetInputConnection(s1a.GetOutputPort())
s1b.SetTransform(transform)
s1a.Update()
s1b.Update()

# Glyph source 2: sphere + transformed sphere
s2a = vtkSphereSource()
s2b = vtkTransformFilter()
s2b.SetInputConnection(s2a.GetOutputPort())
s2b.SetTransform(transform)
s2a.Update()
s2b.Update()

# Build multiblock glyph tree
s0 = vtkMultiBlockDataSet()
s0.SetNumberOfBlocks(2)
s0.SetBlock(0, s0a.GetOutputDataObject(0))
s0.SetBlock(1, s0b.GetOutputDataObject(0))

s1 = vtkMultiBlockDataSet()
s1.SetNumberOfBlocks(2)
s1.SetBlock(0, s1a.GetOutputDataObject(0))
s1.SetBlock(1, s1b.GetOutputDataObject(0))

s2 = vtkMultiBlockDataSet()
s2.SetNumberOfBlocks(2)
s2.SetBlock(0, s2a.GetOutputDataObject(0))
s2.SetBlock(1, s2b.GetOutputDataObject(0))

glyph_tree = vtkMultiBlockDataSet()
glyph_tree.SetNumberOfBlocks(3)
glyph_tree.SetBlock(0, s0)
glyph_tree.SetBlock(1, s1)
glyph_tree.SetBlock(2, s2)

# Glyph mapper with tree indexing
mapper = vtkGlyph3DMapper()
mapper.SetInputData(input_data)
mapper.SetSourceTableTree(glyph_tree)
mapper.SetRange(0, 2)
mapper.SetUseSourceTableTree(True)
mapper.SetSourceIndexing(True)
mapper.SetSourceIndexArray("GlyphIndex")
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Colors")

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper tree indexing composite glyphs")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
