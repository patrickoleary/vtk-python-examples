#!/usr/bin/env python

# Test vtkImageRectilinearWipe with various wipe modes on two canvas images.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingHybrid import vtkImageRectilinearWipe
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Two colored canvas images
image1 = vtkImageCanvasSource2D()
image1.SetNumberOfScalarComponents(3)
image1.SetScalarTypeToUnsignedChar()
image1.SetExtent(0, 79, 0, 79, 0, 0)
image1.SetDrawColor(255, 255, 0)
image1.FillBox(0, 79, 0, 79)
image1.Update()

image2 = vtkImageCanvasSource2D()
image2.SetNumberOfScalarComponents(3)
image2.SetScalarTypeToUnsignedChar()
image2.SetExtent(0, 79, 0, 79, 0, 0)
image2.SetDrawColor(0, 255, 255)
image2.FillBox(0, 79, 0, 79)
image2.Update()

# --- Pipeline 0: Quad wipe ---
wipe_0 = vtkImageRectilinearWipe()
wipe_0.SetInput1Data(image1.GetOutput())
wipe_0.SetInput2Data(image2.GetOutput())
wipe_0.SetPosition(20, 20)
wipe_0.SetWipeToQuad()

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(wipe_0.GetOutputPort())
mapper_0.SetColorWindow(255)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

# --- Pipeline 1: Horizontal wipe ---
wipe_1 = vtkImageRectilinearWipe()
wipe_1.SetInput1Data(image1.GetOutput())
wipe_1.SetInput2Data(image2.GetOutput())
wipe_1.SetPosition(20, 20)
wipe_1.SetWipeToHorizontal()

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(wipe_1.GetOutputPort())
mapper_1.SetColorWindow(255)
mapper_1.SetColorLevel(127.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

# --- Pipeline 2: Vertical wipe ---
wipe_2 = vtkImageRectilinearWipe()
wipe_2.SetInput1Data(image1.GetOutput())
wipe_2.SetInput2Data(image2.GetOutput())
wipe_2.SetPosition(20, 20)
wipe_2.SetWipeToVertical()

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(wipe_2.GetOutputPort())
mapper_2.SetColorWindow(255)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

# --- Pipeline 3: LowerLeft wipe ---
wipe_3 = vtkImageRectilinearWipe()
wipe_3.SetInput1Data(image1.GetOutput())
wipe_3.SetInput2Data(image2.GetOutput())
wipe_3.SetPosition(20, 20)
wipe_3.SetWipeToLowerLeft()

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(wipe_3.GetOutputPort())
mapper_3.SetColorWindow(255)
mapper_3.SetColorLevel(127.5)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

# --- Pipeline 4: LowerRight wipe ---
wipe_4 = vtkImageRectilinearWipe()
wipe_4.SetInput1Data(image1.GetOutput())
wipe_4.SetInput2Data(image2.GetOutput())
wipe_4.SetPosition(20, 20)
wipe_4.SetWipeToLowerRight()

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(wipe_4.GetOutputPort())
mapper_4.SetColorWindow(255)
mapper_4.SetColorLevel(127.5)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

# --- Pipeline 5: UpperLeft wipe ---
wipe_5 = vtkImageRectilinearWipe()
wipe_5.SetInput1Data(image1.GetOutput())
wipe_5.SetInput2Data(image2.GetOutput())
wipe_5.SetPosition(20, 20)
wipe_5.SetWipeToUpperLeft()

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(wipe_5.GetOutputPort())
mapper_5.SetColorWindow(255)
mapper_5.SetColorLevel(127.5)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

# --- Pipeline 6: UpperRight wipe ---
wipe_6 = vtkImageRectilinearWipe()
wipe_6.SetInput1Data(image1.GetOutput())
wipe_6.SetInput2Data(image2.GetOutput())
wipe_6.SetPosition(20, 20)
wipe_6.SetWipeToUpperRight()

mapper_6 = vtkImageMapper()
mapper_6.SetInputConnection(wipe_6.GetOutputPort())
mapper_6.SetColorWindow(255)
mapper_6.SetColorLevel(127.5)

actor_6 = vtkActor2D()
actor_6.SetMapper(mapper_6)

# --- Pipeline 7: Reference (no wipe) ---
mapper_7 = vtkImageMapper()
mapper_7.SetInputConnection(image1.GetOutputPort())
mapper_7.SetColorWindow(255)
mapper_7.SetColorLevel(127.5)

actor_7 = vtkActor2D()
actor_7.SetMapper(mapper_7)

# Renderers (4x2 grid)
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0, .5, .25, 1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(.25, .5, .5, 1)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(.5, .5, .75, 1)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(.75, .5, 1, 1)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(0, 0, .25, .5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(.25, 0, .5, .5)

renderer_6 = vtkRenderer()
renderer_6.AddViewProp(actor_6)
renderer_6.SetViewport(.5, 0, .75, .5)

renderer_7 = vtkRenderer()
renderer_7.AddViewProp(actor_7)
renderer_7.SetViewport(.75, 0, 1, .5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetSize(400, 200)
render_window.SetWindowName("wipe")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
