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
sphere = vtkSphere()
sphere.SetRadius(3)
sphere.SetCenter(5, 5, 5)

# AMR: two-level overlapping adaptive mesh refinement
# Level 0: one coarse block, dims 11x11x11, spacing 1.0
# Level 1: two refined blocks, dims 11x11x11, spacing 0.5 (refinement ratio 2)
amr = vtkOverlappingAMR()
amr.Initialize([1, 2])

dims = [11, 11, 11]

# Level 0, Block 0: coarse grid at origin
ug1 = vtkUniformGrid()
ug1.SetOrigin(0.0, 0.0, 0.0)
ug1.SetSpacing(1.0, 1.0, 1.0)
ug1.SetDimensions(dims)
scalars1 = vtkFloatArray()
scalars1.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            x = 0.0 + 1.0 * i
            y = 0.0 + 1.0 * j
            z = 0.0 + 1.0 * k
            scalars1.SetValue(k * dims[0] * dims[1] + j * dims[0] + i,
                              sphere.EvaluateFunction(x, y, z))
ug1.GetPointData().SetScalars(scalars1)
box1 = vtkAMRBox()
amr.SetAMRBox(0, 0, box1)
amr.SetDataSet(0, 0, ug1)

# Level 1, Block 0: refined grid at origin
ug2 = vtkUniformGrid()
ug2.SetOrigin(0.0, 0.0, 0.0)
ug2.SetSpacing(0.5, 0.5, 0.5)
ug2.SetDimensions(dims)
scalars2 = vtkFloatArray()
scalars2.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            x = 0.0 + 0.5 * i
            y = 0.0 + 0.5 * j
            z = 0.0 + 0.5 * k
            scalars2.SetValue(k * dims[0] * dims[1] + j * dims[0] + i,
                              sphere.EvaluateFunction(x, y, z))
ug2.GetPointData().SetScalars(scalars2)
box2 = vtkAMRBox()
amr.SetAMRBox(1, 0, box2)
amr.SetDataSet(1, 0, ug2)

# Level 1, Block 1: refined grid at (5, 5, 5)
ug3 = vtkUniformGrid()
ug3.SetOrigin(5.0, 5.0, 5.0)
ug3.SetSpacing(0.5, 0.5, 0.5)
ug3.SetDimensions(dims)
scalars3 = vtkFloatArray()
scalars3.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            x = 5.0 + 0.5 * i
            y = 5.0 + 0.5 * j
            z = 5.0 + 0.5 * k
            scalars3.SetValue(k * dims[0] * dims[1] + j * dims[0] + i,
                              sphere.EvaluateFunction(x, y, z))
ug3.GetPointData().SetScalars(scalars3)
box3 = vtkAMRBox()
amr.SetAMRBox(1, 1, box3)
amr.SetDataSet(1, 1, ug3)
amr.SetRefinementRatio(0, 2)

# Outline filter: show block bounding boxes
outline = vtkOutlineFilter()
outline.SetInputData(amr)

# Mapper: map outline polydata to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: assign the outline wireframe
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(gold_rgb)

# Contour: extract an iso-surface at value 10.0
contour = vtkContourFilter()
contour.SetInputData(amr)
contour.SetNumberOfContours(1)
contour.SetValue(0, 10.0)

# Filter: aggregate composite contour output into one polydata
contour_geometry = vtkCompositeDataGeometryFilter()
contour_geometry.SetInputConnection(contour.GetOutputPort())

# Mapper: map the iso-surface to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_geometry.GetOutputPort())

# Actor: assign the iso-surface geometry
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("OverlappingAMR")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
