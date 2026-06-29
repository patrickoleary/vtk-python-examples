#!/usr/bin/env python
# Demonstrate vtkParallelopipedWidget with an affine-transformed mace geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkMatrixToLinearTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkCubeSource, vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkParallelopipedRepresentation,
    vtkParallelopipedWidget,
)
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sources
cone = vtkConeSource()
cone.SetResolution(6)

sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)

cube = vtkCubeSource()
cube.SetBounds(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

# Filters
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

append_filter = vtkAppendPolyData()
append_filter.AddInputConnection(glyph.GetOutputPort())
append_filter.AddInputConnection(sphere.GetOutputPort())
append_filter.Update()

# Apply an affine shear transform
affine_matrix = vtkMatrix4x4()
matrix_values = [1.0, 0.1, 0.2, 0.0,
                 0.1, 1.0, 0.1, 0.0,
                 0.2, 0.1, 1.0, 0.0,
                 0.0, 0.0, 0.0, 1.0]
affine_matrix.DeepCopy(matrix_values)

transform = vtkMatrixToLinearTransform()
transform.SetInput(affine_matrix)
transform.Update()

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(cube.GetOutputPort())
transform_filter.Update()

# Extract parallelopiped points from the transformed cube
parallelopiped_points = transform_filter.GetOutput().GetPoints()

# Transform the mace geometry
transform_filter.SetInputConnection(append_filter.GetOutputPort())
transform_filter.Update()

# Mapper + Actor
mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(transform_filter.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)

# Cube axes
axes = vtkCubeAxesActor2D()
axes.SetInputConnection(transform_filter.GetOutputPort())
axes.SetLabelFormat("{:6.1f}")
axes.SetFlyModeToOuterEdges()
axes.SetFontFactor(0.8)

# Reorder cube points for parallelopiped convention
corner_points = [[0.0] * 3 for _ in range(8)]
parallelopiped_points.GetPoint(0, corner_points[0])
parallelopiped_points.GetPoint(1, corner_points[1])
parallelopiped_points.GetPoint(2, corner_points[3])
parallelopiped_points.GetPoint(3, corner_points[2])
parallelopiped_points.GetPoint(4, corner_points[4])
parallelopiped_points.GetPoint(5, corner_points[5])
parallelopiped_points.GetPoint(6, corner_points[7])
parallelopiped_points.GetPoint(7, corner_points[6])

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.AddViewProp(axes)
renderer.SetBackground(0.8, 0.8, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("parallelopiped widget")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Set camera on axes (needs renderer's camera)
axes.SetCamera(renderer.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
parallelopiped_rep = vtkParallelopipedRepresentation()
parallelopiped_rep.SetPlaceFactor(0.5)
parallelopiped_rep.PlaceWidget(corner_points)

parallelopiped_widget = vtkParallelopipedWidget()
parallelopiped_widget.SetRepresentation(parallelopiped_rep)
parallelopiped_widget.SetInteractor(interactor)
parallelopiped_widget.EnabledOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
