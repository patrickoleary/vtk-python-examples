#!/usr/bin/env python

# Demonstrate vtkEllipticalButtonSource and vtkRectangularButtonSource
# with texture mapping from a JPEG image, showing four button variants.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import (
    vtkEllipticalButtonSource,
    vtkRectangularButtonSource,
)
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read texture image
reader = vtkJPEGReader()
reader.SetFileName(os.path.join(data_dir, "beach.jpg"))
reader.Update()

texture = vtkTexture()
texture.SetInputConnection(reader.GetOutputPort())

dims = reader.GetOutput().GetDimensions()
d1 = dims[0]
d2 = dims[1]

# First elliptical button
button_source = vtkEllipticalButtonSource()
button_source.SetWidth(2)
button_source.SetHeight(1)
button_source.SetDepth(0.2)
button_source.SetCircumferentialResolution(64)
button_source.SetRadialRatio(1.1)
button_source.SetShoulderResolution(8)
button_source.SetTextureResolution(4)
button_source.TwoSidedOn()

button_mapper = vtkPolyDataMapper()
button_mapper.SetInputConnection(button_source.GetOutputPort())

button_actor = vtkActor()
button_actor.SetMapper(button_mapper)
button_actor.SetTexture(texture)

# Second elliptical button (fit image)
button_source_2 = vtkEllipticalButtonSource()
button_source_2.SetWidth(2)
button_source_2.SetHeight(1)
button_source_2.SetDepth(0.2)
button_source_2.SetCircumferentialResolution(64)
button_source_2.SetRadialRatio(1.1)
button_source_2.SetShoulderResolution(8)
button_source_2.SetTextureResolution(4)
button_source_2.TwoSidedOn()
button_source_2.SetCenter(2, 0, 0)
button_source_2.SetTextureStyleToFitImage()
button_source_2.SetTextureDimensions(d1, d2)

button_mapper_2 = vtkPolyDataMapper()
button_mapper_2.SetInputConnection(button_source_2.GetOutputPort())

button_actor_2 = vtkActor()
button_actor_2.SetMapper(button_mapper_2)
button_actor_2.SetTexture(texture)

# Third rectangular button
button_source_3 = vtkRectangularButtonSource()
button_source_3.SetWidth(1.5)
button_source_3.SetHeight(0.75)
button_source_3.SetDepth(0.2)
button_source_3.TwoSidedOn()
button_source_3.SetCenter(0, 1, 0)
button_source_3.SetTextureDimensions(d1, d2)

button_mapper_3 = vtkPolyDataMapper()
button_mapper_3.SetInputConnection(button_source_3.GetOutputPort())

button_actor_3 = vtkActor()
button_actor_3.SetMapper(button_mapper_3)
button_actor_3.SetTexture(texture)

# Fourth rectangular button (fit image)
button_source_4 = vtkRectangularButtonSource()
button_source_4.SetWidth(1.5)
button_source_4.SetHeight(0.75)
button_source_4.SetDepth(0.2)
button_source_4.TwoSidedOn()
button_source_4.SetCenter(2, 1, 0)
button_source_4.SetTextureStyleToFitImage()
button_source_4.SetTextureDimensions(d1, d2)

button_mapper_4 = vtkPolyDataMapper()
button_mapper_4.SetInputConnection(button_source_4.GetOutputPort())

button_actor_4 = vtkActor()
button_actor_4.SetMapper(button_mapper_4)
button_actor_4.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(button_actor)
renderer.AddActor(button_actor_2)
renderer.AddActor(button_actor_3)
renderer.AddActor(button_actor_4)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 150)
render_window.SetWindowName("button source")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
