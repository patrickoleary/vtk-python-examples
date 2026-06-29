#!/usr/bin/env python

# Build a two-level overlapping AMR dataset with scalar values from an
# implicit sphere, then render the block outlines and an iso-surface.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkAMRBox,
    vtkOverlappingAMR,
    vtkSphere,
    vtkUniformGrid,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.200, 0.302, 0.400)

# Implicit function: sphere centered at (5, 5, 5) with radius 3
implicit_sphere = vtkSphere()
implicit_sphere.SetRadius(3)
implicit_sphere.SetCenter(5, 5, 5)

# AMR: two-level overlapping adaptive mesh refinement
# Level 0: one coarse block, dims 11x11x11, spacing 1.0
# Level 1: two refined blocks, dims 11x11x11, spacing 0.5 (refinement ratio 2)
overlapping_amr = vtkOverlappingAMR()
overlapping_amr.Initialize([1, 2])

grid_dimensions = [11, 11, 11]

# Level 0, Block 0: coarse grid at origin
coarse_grid = vtkUniformGrid()
coarse_grid.SetOrigin(0.0, 0.0, 0.0)
coarse_grid.SetSpacing(1.0, 1.0, 1.0)
coarse_grid.SetDimensions(grid_dimensions)
coarse_scalars = vtkFloatArray()
coarse_scalars.SetNumberOfTuples(grid_dimensions[0] * grid_dimensions[1] * grid_dimensions[2])
for k in range(grid_dimensions[2]):
    for j in range(grid_dimensions[1]):
        for i in range(grid_dimensions[0]):
            x = 0.0 + 1.0 * i
            y = 0.0 + 1.0 * j
            z = 0.0 + 1.0 * k
            coarse_scalars.SetValue(k * grid_dimensions[0] * grid_dimensions[1] + j * grid_dimensions[0] + i,
                                    implicit_sphere.EvaluateFunction(x, y, z))
coarse_grid.GetPointData().SetScalars(coarse_scalars)
coarse_box = vtkAMRBox()
overlapping_amr.SetAMRBox(0, 0, coarse_box)
overlapping_amr.SetDataSet(0, 0, coarse_grid)

# Level 1, Block 0: refined grid at origin
refined_grid_0 = vtkUniformGrid()
refined_grid_0.SetOrigin(0.0, 0.0, 0.0)
refined_grid_0.SetSpacing(0.5, 0.5, 0.5)
refined_grid_0.SetDimensions(grid_dimensions)
refined_scalars_0 = vtkFloatArray()
refined_scalars_0.SetNumberOfTuples(grid_dimensions[0] * grid_dimensions[1] * grid_dimensions[2])
for k in range(grid_dimensions[2]):
    for j in range(grid_dimensions[1]):
        for i in range(grid_dimensions[0]):
            x = 0.0 + 0.5 * i
            y = 0.0 + 0.5 * j
            z = 0.0 + 0.5 * k
            refined_scalars_0.SetValue(k * grid_dimensions[0] * grid_dimensions[1] + j * grid_dimensions[0] + i,
                                       implicit_sphere.EvaluateFunction(x, y, z))
refined_grid_0.GetPointData().SetScalars(refined_scalars_0)
refined_box_0 = vtkAMRBox()
overlapping_amr.SetAMRBox(1, 0, refined_box_0)
overlapping_amr.SetDataSet(1, 0, refined_grid_0)

# Level 1, Block 1: refined grid at (5, 5, 5)
refined_grid_1 = vtkUniformGrid()
refined_grid_1.SetOrigin(5.0, 5.0, 5.0)
refined_grid_1.SetSpacing(0.5, 0.5, 0.5)
refined_grid_1.SetDimensions(grid_dimensions)
refined_scalars_1 = vtkFloatArray()
refined_scalars_1.SetNumberOfTuples(grid_dimensions[0] * grid_dimensions[1] * grid_dimensions[2])
for k in range(grid_dimensions[2]):
    for j in range(grid_dimensions[1]):
        for i in range(grid_dimensions[0]):
            x = 5.0 + 0.5 * i
            y = 5.0 + 0.5 * j
            z = 5.0 + 0.5 * k
            refined_scalars_1.SetValue(k * grid_dimensions[0] * grid_dimensions[1] + j * grid_dimensions[0] + i,
                                       implicit_sphere.EvaluateFunction(x, y, z))
refined_grid_1.GetPointData().SetScalars(refined_scalars_1)
refined_box_1 = vtkAMRBox()
overlapping_amr.SetAMRBox(1, 1, refined_box_1)
overlapping_amr.SetDataSet(1, 1, refined_grid_1)
overlapping_amr.SetRefinementRatio(0, 2)

# Outline filter: show block bounding boxes
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(overlapping_amr)

# Mapper: map outline polydata to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

# Actor: assign the outline wireframe
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(gold_rgb)

# Contour: extract an iso-surface at value 10.0
contour_filter = vtkContourFilter()
contour_filter.SetInputData(overlapping_amr)
contour_filter.SetNumberOfContours(1)
contour_filter.SetValue(0, 10.0)

# Filter: aggregate composite contour output into one polydata
contour_composite_geometry = vtkCompositeDataGeometryFilter()
contour_composite_geometry.SetInputConnection(contour_filter.GetOutputPort())

# Mapper: map the iso-surface to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_composite_geometry.GetOutputPort())

# Actor: assign the iso-surface geometry
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("overlapping amr")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
