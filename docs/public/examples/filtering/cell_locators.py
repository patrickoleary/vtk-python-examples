#!/usr/bin/env python

# Visualize the clipped Mandelbrot dataset used for cell locator benchmarking,
# showing the unstructured grid that results from clipping with a plane.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 25

# Create Mandelbrot image data
mandel = vtkImageMandelbrotSource()
mandel.SetWholeExtent(-resolution, resolution, -resolution, resolution, -resolution, resolution)
mandel.Update()

# Clip with a diagonal plane to produce unstructured grid
plane = vtkPlane()
plane.SetOrigin(resolution + 1, resolution + 1, resolution + 1)
plane.SetNormal(-1, -1, -1)

clipper = vtkClipDataSet()
clipper.SetInputConnection(mandel.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.Update()

mapper = vtkDataSetMapper()
mapper.SetInputConnection(clipper.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("cell locators")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
