#!/usr/bin/env python

# Demonstrate cylindrical texture mapping on a Delaunay triangulation
# of random points using vtkTextureMapToCylinder.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkFiltersTexture import (
    vtkTextureMapToCylinder,
    vtkTransformTextureCoords,
)
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Create random points in a sphere
sphere = vtkPointSource()
sphere.SetNumberOfPoints(25)

# Triangulate the points
delaunay = vtkDelaunay3D()
delaunay.SetInputConnection(sphere.GetOutputPort())
delaunay.SetTolerance(0.01)

# Cylindrical texture coordinate mapping
texture_mapper = vtkTextureMapToCylinder()
texture_mapper.SetInputConnection(delaunay.GetOutputPort())
texture_mapper.PreventSeamOn()

# Scale texture coordinates
texture_transform = vtkTransformTextureCoords()
texture_transform.SetInputConnection(texture_mapper.GetOutputPort())
texture_transform.SetScale(4, 4, 1)

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(texture_transform.GetOutputPort())

# Load texture map
bmp_reader = vtkBMPReader()
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

texture = vtkTexture()
texture.SetInputConnection(bmp_reader.GetOutputPort())
texture.InterpolateOn()

# Actor with texture
triangulation = vtkActor()
triangulation.SetMapper(mapper)
triangulation.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(triangulation)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("cyl map")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
