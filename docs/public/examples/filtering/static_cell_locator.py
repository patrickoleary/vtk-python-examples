#!/usr/bin/env python

# Visualize a vtkStaticCellLocator built on a sphere-clipped Mandelbrot set,
# showing the locator bin representation, an outline, and a ray intersection.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkSphere,
    vtkStaticCellLocator,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 15

# Create Mandelbrot image data
mandel = vtkImageMandelbrotSource()
mandel.SetWholeExtent(-res, res, -res, res, -res, res)
mandel.Update()

# Clip with a sphere to produce unstructured grid
sphere = vtkSphere()
sphere.SetCenter(mandel.GetOutput().GetCenter())
sphere.SetRadius(mandel.GetOutput().GetLength() / 4)

clipper = vtkClipDataSet()
clipper.SetInputConnection(mandel.GetOutputPort())
clipper.SetClipFunction(sphere)
clipper.InsideOutOn()
clipper.Update()

output = clipper.GetOutput()

# Build the static cell locator
locator = vtkStaticCellLocator()
locator.SetDataSet(output)
locator.AutomaticOn()
locator.SetNumberOfCellsPerNode(20)
locator.CacheCellBoundsOn()
locator.BuildLocator()

# Generate locator bin representation
locator_pd = vtkPolyData()
locator.GenerateRepresentation(0, locator_pd)

locator_mapper = vtkPolyDataMapper()
locator_mapper.SetInputData(locator_pd)

locator_actor = vtkActor()
locator_actor.SetMapper(locator_mapper)

# Outline around the entire dataset
outline = vtkOutlineFilter()
outline.SetInputConnection(mandel.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Ray for intersection test
ray = vtkPolyData()
ray_pts = vtkPoints()
ray_pts.InsertPoint(0, -7.5, -5, -5)
ray_pts.InsertPoint(1, 2.5, 2, 2.5)
ray_line = vtkCellArray()
ray_line.InsertNextCell(2)
ray_line.InsertCellPoint(0)
ray_line.InsertCellPoint(1)
ray.SetPoints(ray_pts)
ray.SetLines(ray_line)

ray_mapper = vtkPolyDataMapper()
ray_mapper.SetInputData(ray)

ray_actor = vtkActor()
ray_actor.SetMapper(ray_mapper)
ray_actor.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(locator_actor)
renderer.AddActor(ray_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("static cell locator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
