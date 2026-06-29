#!/usr/bin/env python
# Demonstrate vtkContourWidget with Dijkstra image geodesic path on a medical image.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersModeling import vtkDijkstraImageGeodesicPath
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageAnisotropicDiffusion2D, vtkImageGradientMagnitude
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import (
    vtkContourWidget,
    vtkDijkstraImageContourLineInterpolator,
    vtkImageActorPointPlacer,
    vtkOrientedGlyphContourRepresentation,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
image_reader = vtkPNGReader()
image_reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Filters: smooth → gradient magnitude → invert
diffusion = vtkImageAnisotropicDiffusion2D()
diffusion.SetInputConnection(image_reader.GetOutputPort())
diffusion.SetDiffusionFactor(1.0)
diffusion.SetDiffusionThreshold(200.0)
diffusion.SetNumberOfIterations(5)

gradient_mag = vtkImageGradientMagnitude()
gradient_mag.SetDimensionality(2)
gradient_mag.HandleBoundariesOn()
gradient_mag.SetInputConnection(diffusion.GetOutputPort())
gradient_mag.Update()

scalar_range = gradient_mag.GetOutput().GetScalarRange()

grad_invert = vtkImageShiftScale()
grad_invert.SetShift(-1.0 * scalar_range[1])
grad_invert.SetScale(1.0 / (scalar_range[0] - scalar_range[1]))
grad_invert.SetOutputScalarTypeToFloat()
grad_invert.SetInputConnection(gradient_mag.GetOutputPort())
grad_invert.Update()

# Filter: map inverted gradient to displayable colors
color_map = vtkImageMapToWindowLevelColors()
color_map.SetInputConnection(grad_invert.GetOutputPort())
color_map.SetWindow(1.0)
color_map.SetLevel(0.5)

# Actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
image_actor.SetDisplayExtent(0, 255, 0, 255, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.2, 0.2, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dijkstra image geodesic path")
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

# Widget
contour_rep = vtkOrientedGlyphContourRepresentation()
contour_rep.GetLinesProperty().SetColor(1, 0.2, 0)
contour_rep.GetProperty().SetColor(0, 0.2, 1)
contour_rep.GetLinesProperty().SetLineWidth(3)

placer = vtkImageActorPointPlacer()
placer.SetImageActor(image_actor)
contour_rep.SetPointPlacer(placer)

interpolator = vtkDijkstraImageContourLineInterpolator()
interpolator.SetCostImage(grad_invert.GetOutput())

geodesic_path = vtkDijkstraImageGeodesicPath.SafeDownCast(interpolator.GetDijkstraImageGeodesicPath())
geodesic_path.StopWhenEndReachedOn()
geodesic_path.RepelPathFromVerticesOn()
geodesic_path.SetCurvatureWeight(0.15)
geodesic_path.SetEdgeLengthWeight(0.8)
geodesic_path.SetImageWeight(1.0)

contour_rep.SetLineInterpolator(interpolator)

contour_widget = vtkContourWidget()
contour_widget.SetInteractor(interactor)
contour_widget.SetRepresentation(contour_rep)
contour_widget.EnabledOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
