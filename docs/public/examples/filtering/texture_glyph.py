#!/usr/bin/env python

# Demonstrate textured glyphs using vtkGlyph3D with cube glyphs oriented
# by vectors and textured with a bitmap image.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Cube glyph source
cube = vtkCubeSource()
cube.SetXLength(2.0)
cube.SetYLength(1.0)
cube.SetZLength(0.5)

# Create input point data with three points
points = vtkPoints()
points.InsertPoint(0, (1, 1, 1))
points.InsertPoint(1, (0, 0, 0))
points.InsertPoint(2, (-1, -1, -1))

polys = vtkCellArray()
polys.InsertNextCell(1)
polys.InsertCellPoint(0)
polys.InsertNextCell(1)
polys.InsertCellPoint(1)
polys.InsertNextCell(1)
polys.InsertCellPoint(2)

glyph_input = vtkPolyData()
glyph_input.SetPoints(points)
glyph_input.SetPolys(polys)

# Orientation vectors
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.InsertTuple3(0, 1, 0, 0)
vectors.InsertTuple3(1, 0, 1, 0)
vectors.InsertTuple3(2, 0, 0, 1)
glyph_input.GetPointData().SetVectors(vectors)

# Glyph filter
glyph = vtkGlyph3D()
glyph.SetScaleModeToDataScalingOff()
glyph.SetVectorModeToUseVector()
glyph.SetInputData(glyph_input)
glyph.SetSourceConnection(cube.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Texture from BMP image
img_reader = vtkBMPReader()
img_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

texture = vtkTexture()
texture.SetInputConnection(img_reader.GetOutputPort())
texture.InterpolateOn()
actor.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("texture glyph")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(-90)
camera.Zoom(1.4)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
