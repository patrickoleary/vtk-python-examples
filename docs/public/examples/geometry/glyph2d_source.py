#!/usr/bin/env python

# Demonstrate vtkGlyph2D with multiple 2D glyph types (circle, triangle,
# square, diamond, thick arrow) indexed by scalar value on random points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph2D
from vtkmodules.vtkFiltersSources import vtkGlyphSource2D
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create random points with scalars and vectors
polydata = vtkPolyData()
point_positions = vtkPoints()
scalars = vtkFloatArray()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)

polydata.SetPoints(point_positions)
polydata.GetPointData().SetScalars(scalars)
polydata.GetPointData().SetVectors(vectors)

random_sequence = vtkMath()
size = 500
for i in range(100):
    point_positions.InsertNextPoint(random_sequence.Random(0, size - 1), random_sequence.Random(0, size - 1), 0.0)
    scalars.InsertNextValue(random_sequence.Random(0.0, 5))
    vectors.InsertNextTuple3(random_sequence.Random(-1, 1), random_sequence.Random(-1, 1), 0.0)

# Circle glyph
glyph_source = vtkGlyphSource2D()
glyph_source.SetGlyphTypeToCircle()
glyph_source.SetScale(20)
glyph_source.FilledOff()
glyph_source.CrossOn()
glyph_source.Update()

# Triangle glyph
glyph_source_1 = vtkGlyphSource2D()
glyph_source_1.SetGlyphTypeToTriangle()
glyph_source_1.SetScale(20)
glyph_source_1.FilledOff()
glyph_source_1.CrossOn()
glyph_source_1.Update()

# Square glyph
glyph_source_2 = vtkGlyphSource2D()
glyph_source_2.SetGlyphTypeToSquare()
glyph_source_2.SetScale(20)
glyph_source_2.FilledOff()
glyph_source_2.CrossOn()
glyph_source_2.Update()

# Diamond glyph
glyph_source_3 = vtkGlyphSource2D()
glyph_source_3.SetGlyphTypeToDiamond()
glyph_source_3.SetScale(20)
glyph_source_3.FilledOff()
glyph_source_3.CrossOn()
glyph_source_3.Update()

# Filled diamond with dash
glyph_source_4 = vtkGlyphSource2D()
glyph_source_4.SetGlyphTypeToDiamond()
glyph_source_4.SetScale(20)
glyph_source_4.FilledOn()
glyph_source_4.DashOn()
glyph_source_4.CrossOff()
glyph_source_4.Update()

# Thick arrow glyph
glyph_source_5 = vtkGlyphSource2D()
glyph_source_5.SetGlyphTypeToThickArrow()
glyph_source_5.SetScale(20)
glyph_source_5.FilledOn()
glyph_source_5.CrossOff()
glyph_source_5.Update()

# Table of glyphs indexed by scalar
glypher = vtkGlyph2D()
glypher.SetInputData(polydata)
glypher.SetSourceData(0, glyph_source.GetOutput())
glypher.SetSourceData(1, glyph_source_1.GetOutput())
glypher.SetSourceData(2, glyph_source_2.GetOutput())
glypher.SetSourceData(3, glyph_source_3.GetOutput())
glypher.SetSourceData(4, glyph_source_4.GetOutput())
glypher.SetSourceData(5, glyph_source_5.GetOutput())
glypher.SetIndexModeToScalar()
glypher.SetRange(0, 5)
glypher.SetScaleModeToDataScalingOff()

mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(glypher.GetOutputPort())
mapper.SetScalarRange(0, 5)

glyph_actor = vtkActor2D()
glyph_actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(size, size)
render_window.SetWindowName("glyph2d source")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
