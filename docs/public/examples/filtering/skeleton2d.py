#!/usr/bin/env python

# Skeletonize a 2D canvas image with various drawn shapes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import (
    vtkImageClip,
    vtkImageMagnify,
)
from vtkmodules.vtkImagingMorphological import vtkImageSkeleton2D
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Draw various shapes on canvas
image_canvas = vtkImageCanvasSource2D()
image_canvas.SetScalarTypeToUnsignedChar()
image_canvas.SetExtent(0, 339, 0, 339, 0, 0)
# Background black
image_canvas.SetDrawColor(0)
image_canvas.FillBox(0, 511, 0, 511)
# Thick box
image_canvas.SetDrawColor(255)
image_canvas.FillBox(10, 110, 10, 110)
image_canvas.SetDrawColor(0)
image_canvas.FillBox(30, 90, 30, 90)
# Stop sign shape
image_canvas.SetDrawColor(255)
image_canvas.DrawSegment(52, 80, 68, 80)
image_canvas.DrawSegment(68, 80, 80, 68)
image_canvas.DrawSegment(80, 68, 80, 52)
image_canvas.DrawSegment(80, 52, 68, 40)
image_canvas.DrawSegment(68, 40, 52, 40)
image_canvas.DrawSegment(52, 40, 40, 52)
image_canvas.DrawSegment(40, 52, 40, 68)
image_canvas.DrawSegment(40, 68, 52, 80)
image_canvas.FillPixel(60, 60)
# Diamond
image_canvas.SetDrawColor(255)
image_canvas.FillTube(145, 145, 195, 195, 34)
image_canvas.SetDrawColor(0)
image_canvas.FillTube(165, 165, 175, 175, 7)
# H
image_canvas.SetDrawColor(255)
image_canvas.FillBox(230, 250, 230, 330)
image_canvas.FillBox(310, 330, 230, 330)
image_canvas.FillBox(230, 330, 270, 290)
# Circle
image_canvas.SetDrawColor(255)
image_canvas.DrawCircle(280, 170, 50.0)
image_canvas.DrawPoint(280, 170)
# Lines +
image_canvas.DrawSegment(60, 120, 60, 220)
image_canvas.DrawSegment(10, 170, 110, 170)
# Lines X
image_canvas.DrawSegment(10, 230, 110, 330)
image_canvas.DrawSegment(110, 230, 10, 330)
# Sloped lines
image_canvas.DrawSegment(120, 230, 220, 230)
image_canvas.DrawSegment(120, 230, 220, 250)
image_canvas.DrawSegment(120, 230, 220, 270)
image_canvas.DrawSegment(120, 230, 220, 290)
image_canvas.DrawSegment(120, 230, 220, 310)
image_canvas.DrawSegment(120, 230, 220, 330)
image_canvas.DrawSegment(120, 230, 200, 330)
image_canvas.DrawSegment(120, 230, 180, 330)
image_canvas.DrawSegment(120, 230, 160, 330)
image_canvas.DrawSegment(120, 230, 140, 330)
image_canvas.DrawSegment(120, 230, 120, 330)
# Double thickness lines +
image_canvas.DrawSegment(120, 60, 220, 60)
image_canvas.DrawSegment(120, 61, 220, 61)
image_canvas.DrawSegment(170, 10, 170, 110)
image_canvas.DrawSegment(171, 10, 171, 110)
# Lines X
image_canvas.DrawSegment(230, 10, 330, 110)
image_canvas.DrawSegment(231, 10, 331, 110)
image_canvas.DrawSegment(230, 110, 330, 10)
image_canvas.DrawSegment(231, 110, 331, 10)

# Skeleton
skeleton1 = vtkImageSkeleton2D()
skeleton1.SetInputConnection(image_canvas.GetOutputPort())
skeleton1.SetPrune(0)
skeleton1.SetNumberOfIterations(20)
skeleton1.ReleaseDataFlagOff()
skeleton1.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(skeleton1.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(340, 340)
render_window.SetWindowName("skeleton2d")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
