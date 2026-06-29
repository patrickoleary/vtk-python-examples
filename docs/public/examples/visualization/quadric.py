#!/usr/bin/env python

# Visualize a quadric function using isosurfaces, color-mapped planes, and contour lines.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import (
    vtkAppendFilter,
    vtkContourFilter,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)

# Source: sample a quadric implicit function on a regular grid
quadric = vtkQuadric()
quadric.SetCoefficients(1, 2, 3, 0, 1, 0, 0, 0, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(25, 25, 25)
sample.SetImplicitFunction(quadric)

# --- Isosurface visualization ---

# Filter: generate isosurfaces from the sampled quadric
iso_contour = vtkContourFilter()
iso_contour.SetInputConnection(sample.GetOutputPort())
iso_contour.GenerateValues(5, 1.0, 6.0)

# Mapper: map isosurfaces to graphics primitives
iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso_contour.GetOutputPort())
iso_mapper.SetScalarRange(0, 7)

# Actor: display the isosurfaces
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)

# Filter/Mapper/Actor: outline for isosurface view
iso_outline = vtkOutlineFilter()
iso_outline.SetInputConnection(sample.GetOutputPort())
iso_outline_mapper = vtkPolyDataMapper()
iso_outline_mapper.SetInputConnection(iso_outline.GetOutputPort())
iso_outline_actor = vtkActor()
iso_outline_actor.SetMapper(iso_outline_mapper)

# --- Color-mapped planes visualization ---

number_of_planes = 3
dims = sample.GetSampleDimensions()
slice_incr = (dims[2] - 1) // (number_of_planes + 1)

# Filter: extract slices and append them
slice_k_0 = -4 + slice_incr
slice_k_1 = slice_k_0 + slice_incr
slice_k_2 = slice_k_1 + slice_incr

planes_extract_0 = vtkExtractVOI()
planes_extract_0.SetInputConnection(sample.GetOutputPort())
planes_extract_0.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_0, slice_k_0)

planes_extract_1 = vtkExtractVOI()
planes_extract_1.SetInputConnection(sample.GetOutputPort())
planes_extract_1.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_1, slice_k_1)

planes_extract_2 = vtkExtractVOI()
planes_extract_2.SetInputConnection(sample.GetOutputPort())
planes_extract_2.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_2, slice_k_2)

planes_append = vtkAppendFilter()
planes_append.AddInputConnection(planes_extract_0.GetOutputPort())
planes_append.AddInputConnection(planes_extract_1.GetOutputPort())
planes_append.AddInputConnection(planes_extract_2.GetOutputPort())
planes_append.Update()

# Mapper: map extracted planes to graphics primitives
planes_mapper = vtkDataSetMapper()
planes_mapper.SetInputConnection(planes_append.GetOutputPort())
planes_mapper.SetScalarRange(0, 7)

# Actor: display the color-mapped planes
planes_actor = vtkActor()
planes_actor.SetMapper(planes_mapper)
planes_actor.GetProperty().SetAmbient(1.0)

# Filter/Mapper/Actor: outline for planes view
planes_outline = vtkOutlineFilter()
planes_outline.SetInputConnection(sample.GetOutputPort())
planes_outline_mapper = vtkPolyDataMapper()
planes_outline_mapper.SetInputConnection(planes_outline.GetOutputPort())
planes_outline_actor = vtkActor()
planes_outline_actor.SetMapper(planes_outline_mapper)

planes_actor.AddPosition(iso_actor.GetBounds()[0] * 2.0, 0, 0)
planes_outline_actor.AddPosition(iso_actor.GetBounds()[0] * 2.0, 0, 0)

# --- Contour lines on planes visualization ---

number_of_contours = 15

contour_extract_0 = vtkExtractVOI()
contour_extract_0.SetInputConnection(sample.GetOutputPort())
contour_extract_0.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_0, slice_k_0)

contour_0 = vtkContourFilter()
contour_0.SetInputConnection(contour_extract_0.GetOutputPort())
contour_0.GenerateValues(number_of_contours, 1.0, 6.0)

contour_extract_1 = vtkExtractVOI()
contour_extract_1.SetInputConnection(sample.GetOutputPort())
contour_extract_1.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_1, slice_k_1)

contour_1 = vtkContourFilter()
contour_1.SetInputConnection(contour_extract_1.GetOutputPort())
contour_1.GenerateValues(number_of_contours, 1.0, 6.0)

contour_extract_2 = vtkExtractVOI()
contour_extract_2.SetInputConnection(sample.GetOutputPort())
contour_extract_2.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, slice_k_2, slice_k_2)

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(contour_extract_2.GetOutputPort())
contour_2.GenerateValues(number_of_contours, 1.0, 6.0)

contour_append = vtkAppendFilter()
contour_append.AddInputConnection(contour_0.GetOutputPort())
contour_append.AddInputConnection(contour_1.GetOutputPort())
contour_append.AddInputConnection(contour_2.GetOutputPort())
contour_append.Update()

# Mapper: map contour lines to graphics primitives
contour_mapper = vtkDataSetMapper()
contour_mapper.SetInputConnection(contour_append.GetOutputPort())
contour_mapper.SetScalarRange(0, 7)

# Actor: display the contour lines
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetAmbient(1.0)

# Filter/Mapper/Actor: outline for contour view
contour_outline = vtkOutlineFilter()
contour_outline.SetInputConnection(sample.GetOutputPort())
contour_outline_mapper = vtkPolyDataMapper()
contour_outline_mapper.SetInputConnection(contour_outline.GetOutputPort())
contour_outline_actor = vtkActor()
contour_outline_actor.SetMapper(contour_outline_mapper)

contour_actor.AddPosition(iso_actor.GetBounds()[0] * 4.0, 0, 0)
contour_outline_actor.AddPosition(iso_actor.GetBounds()[0] * 4.0, 0, 0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(planes_actor)
renderer.AddActor(planes_outline_actor)
renderer.AddActor(contour_actor)
renderer.AddActor(contour_outline_actor)
renderer.AddActor(iso_actor)
renderer.AddActor(iso_outline_actor)
renderer.TwoSidedLightingOn()
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: configure the camera
renderer.GetActiveCamera().SetPosition(0, -1, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(10)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
