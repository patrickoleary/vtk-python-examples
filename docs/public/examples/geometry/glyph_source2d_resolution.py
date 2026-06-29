#!/usr/bin/env python

# Demonstrate vtkGlyphSource2D circle resolution parameter by rendering
# five circle glyph variants with different resolutions on random points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMinimalStandardRandomSequence,
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

random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.SetSeed(1)

size = 400
for i in range(100):
    random_sequence.Next()
    x = random_sequence.GetValue() * size
    random_sequence.Next()
    y = random_sequence.GetValue() * size
    point_positions.InsertNextPoint(x, y, 0.0)
    random_sequence.Next()
    scalars.InsertNextValue(5.0 * random_sequence.GetValue())
    random_sequence.Next()
    ihat = random_sequence.GetValue() * 2 - 1
    random_sequence.Next()
    jhat = random_sequence.GetValue() * 2 - 1
    vectors.InsertNextTuple3(ihat, jhat, 0.0)

# Circle glyph (default resolution)
glyph_source = vtkGlyphSource2D()
glyph_source.SetGlyphTypeToCircle()
glyph_source.SetScale(20)
glyph_source.FilledOff()
glyph_source.CrossOn()

# Circle glyph (resolution 24, filled)
glyph_source_1 = vtkGlyphSource2D()
glyph_source_1.SetGlyphTypeToCircle()
glyph_source_1.SetResolution(24)
glyph_source_1.SetScale(30)
glyph_source_1.FilledOn()
glyph_source_1.CrossOff()

# Circle glyph (resolution 6, filled)
glyph_source_2 = vtkGlyphSource2D()
glyph_source_2.SetGlyphTypeToCircle()
glyph_source_2.SetResolution(6)
glyph_source_2.SetScale(20)
glyph_source_2.FilledOn()
glyph_source_2.CrossOff()

# Circle glyph (resolution 5, unfilled with cross)
glyph_source_3 = vtkGlyphSource2D()
glyph_source_3.SetGlyphTypeToCircle()
glyph_source_3.SetResolution(5)
glyph_source_3.SetScale(30)
glyph_source_3.FilledOff()
glyph_source_3.CrossOn()

# Circle glyph (resolution 100, unfilled)
glyph_source_4 = vtkGlyphSource2D()
glyph_source_4.SetGlyphTypeToCircle()
glyph_source_4.SetResolution(100)
glyph_source_4.SetScale(50)
glyph_source_4.FilledOff()
glyph_source_4.CrossOff()

# Glyph filter with multiple sources indexed by scalar
glypher = vtkGlyph2D()
glypher.SetInputData(polydata)
glypher.SetSourceConnection(0, glyph_source.GetOutputPort())
glypher.SetSourceConnection(1, glyph_source_1.GetOutputPort())
glypher.SetSourceConnection(2, glyph_source_2.GetOutputPort())
glypher.SetSourceConnection(3, glyph_source_3.GetOutputPort())
glypher.SetSourceConnection(4, glyph_source_4.GetOutputPort())
glypher.SetIndexModeToScalar()
glypher.SetRange(0, 5)
glypher.SetScaleModeToScaleByVector()

mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(glypher.GetOutputPort())
mapper.SetScalarRange(0, 5)

glyph_actor = vtkActor2D()
glyph_actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(glyph_actor)
renderer.SetBackground(0.3, 0.3, 0.3)

# Window (NPOT size matching original test)
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(size + 1, size - 1)
render_window.SetWindowName("glyph source2d resolution")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
