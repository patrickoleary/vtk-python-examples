#!/usr/bin/env python

# Demonstrate vtkNormalizeMatrixVectors by creating a diagonal matrix
# with off-diagonal entries, normalizing its column vectors, and
# visualizing the before/after matrices as colored heatmaps.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkNormalizeMatrixVectors
from vtkmodules.vtkFiltersSources import (
    vtkDiagonalMatrixSource,
    vtkPlaneSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Create a 3x3 diagonal matrix with sub- and super-diagonals
source = vtkDiagonalMatrixSource()
source.SetExtents(3)
source.SetArrayType(0)  # 0 = DENSE
source.SetDiagonal(1.0)
source.SetSuperDiagonal(0.5)
source.SetSubDiagonal(-0.5)
source.Update()

# Normalize column vectors
normalize = vtkNormalizeMatrixVectors()
normalize.AddInputConnection(source.GetOutputPort())
normalize.SetVectorDimension(1)
normalize.Update()

# Read values from the source and normalized arrays
src_arr = source.GetOutput().GetArray(0)
norm_arr = normalize.GetOutput().GetArray(0)

# Visualize both as 3x3 heatmaps side by side
# Source matrix (diagonal=1.0, super=0.5, sub=-0.5):
#   [1.0,  0.5,  0.0]
#   [-0.5, 1.0,  0.5]
#   [0.0, -0.5,  1.0]
# Color mapping: norm_val = (val + 1.0) / 2.0

# Source matrix (left) — row 0
src_cell_0_0 = vtkPlaneSource()
src_cell_0_0.SetOrigin(0, 2, 0)
src_cell_0_0.SetPoint1(0.9, 2, 0)
src_cell_0_0.SetPoint2(0, 2.9, 0)

src_cell_mapper_0_0 = vtkPolyDataMapper()
src_cell_mapper_0_0.SetInputConnection(src_cell_0_0.GetOutputPort())

src_cell_actor_0_0 = vtkActor()
src_cell_actor_0_0.SetMapper(src_cell_mapper_0_0)
src_cell_actor_0_0.GetProperty().SetColor(1.0, 0.2, 0.0)

src_cell_0_1 = vtkPlaneSource()
src_cell_0_1.SetOrigin(1, 2, 0)
src_cell_0_1.SetPoint1(1.9, 2, 0)
src_cell_0_1.SetPoint2(1, 2.9, 0)

src_cell_mapper_0_1 = vtkPolyDataMapper()
src_cell_mapper_0_1.SetInputConnection(src_cell_0_1.GetOutputPort())

src_cell_actor_0_1 = vtkActor()
src_cell_actor_0_1.SetMapper(src_cell_mapper_0_1)
src_cell_actor_0_1.GetProperty().SetColor(0.75, 0.2, 0.25)

src_cell_0_2 = vtkPlaneSource()
src_cell_0_2.SetOrigin(2, 2, 0)
src_cell_0_2.SetPoint1(2.9, 2, 0)
src_cell_0_2.SetPoint2(2, 2.9, 0)

src_cell_mapper_0_2 = vtkPolyDataMapper()
src_cell_mapper_0_2.SetInputConnection(src_cell_0_2.GetOutputPort())

src_cell_actor_0_2 = vtkActor()
src_cell_actor_0_2.SetMapper(src_cell_mapper_0_2)
src_cell_actor_0_2.GetProperty().SetColor(0.5, 0.2, 0.5)

# Source matrix (left) — row 1
src_cell_1_0 = vtkPlaneSource()
src_cell_1_0.SetOrigin(0, 1, 0)
src_cell_1_0.SetPoint1(0.9, 1, 0)
src_cell_1_0.SetPoint2(0, 1.9, 0)

src_cell_mapper_1_0 = vtkPolyDataMapper()
src_cell_mapper_1_0.SetInputConnection(src_cell_1_0.GetOutputPort())

src_cell_actor_1_0 = vtkActor()
src_cell_actor_1_0.SetMapper(src_cell_mapper_1_0)
src_cell_actor_1_0.GetProperty().SetColor(0.25, 0.2, 0.75)

src_cell_1_1 = vtkPlaneSource()
src_cell_1_1.SetOrigin(1, 1, 0)
src_cell_1_1.SetPoint1(1.9, 1, 0)
src_cell_1_1.SetPoint2(1, 1.9, 0)

src_cell_mapper_1_1 = vtkPolyDataMapper()
src_cell_mapper_1_1.SetInputConnection(src_cell_1_1.GetOutputPort())

src_cell_actor_1_1 = vtkActor()
src_cell_actor_1_1.SetMapper(src_cell_mapper_1_1)
src_cell_actor_1_1.GetProperty().SetColor(1.0, 0.2, 0.0)

src_cell_1_2 = vtkPlaneSource()
src_cell_1_2.SetOrigin(2, 1, 0)
src_cell_1_2.SetPoint1(2.9, 1, 0)
src_cell_1_2.SetPoint2(2, 1.9, 0)

src_cell_mapper_1_2 = vtkPolyDataMapper()
src_cell_mapper_1_2.SetInputConnection(src_cell_1_2.GetOutputPort())

src_cell_actor_1_2 = vtkActor()
src_cell_actor_1_2.SetMapper(src_cell_mapper_1_2)
src_cell_actor_1_2.GetProperty().SetColor(0.75, 0.2, 0.25)

# Source matrix (left) — row 2
src_cell_2_0 = vtkPlaneSource()
src_cell_2_0.SetOrigin(0, 0, 0)
src_cell_2_0.SetPoint1(0.9, 0, 0)
src_cell_2_0.SetPoint2(0, 0.9, 0)

src_cell_mapper_2_0 = vtkPolyDataMapper()
src_cell_mapper_2_0.SetInputConnection(src_cell_2_0.GetOutputPort())

src_cell_actor_2_0 = vtkActor()
src_cell_actor_2_0.SetMapper(src_cell_mapper_2_0)
src_cell_actor_2_0.GetProperty().SetColor(0.5, 0.2, 0.5)

src_cell_2_1 = vtkPlaneSource()
src_cell_2_1.SetOrigin(1, 0, 0)
src_cell_2_1.SetPoint1(1.9, 0, 0)
src_cell_2_1.SetPoint2(1, 0.9, 0)

src_cell_mapper_2_1 = vtkPolyDataMapper()
src_cell_mapper_2_1.SetInputConnection(src_cell_2_1.GetOutputPort())

src_cell_actor_2_1 = vtkActor()
src_cell_actor_2_1.SetMapper(src_cell_mapper_2_1)
src_cell_actor_2_1.GetProperty().SetColor(0.25, 0.2, 0.75)

src_cell_2_2 = vtkPlaneSource()
src_cell_2_2.SetOrigin(2, 0, 0)
src_cell_2_2.SetPoint1(2.9, 0, 0)
src_cell_2_2.SetPoint2(2, 0.9, 0)

src_cell_mapper_2_2 = vtkPolyDataMapper()
src_cell_mapper_2_2.SetInputConnection(src_cell_2_2.GetOutputPort())

src_cell_actor_2_2 = vtkActor()
src_cell_actor_2_2.SetMapper(src_cell_mapper_2_2)
src_cell_actor_2_2.GetProperty().SetColor(1.0, 0.2, 0.0)

# Normalized matrix (right, offset by 4) — use norm_arr runtime values
norm_color_0_0 = (norm_arr.GetValue(0, 0) + 1.0) / 2.0
norm_color_0_1 = (norm_arr.GetValue(0, 1) + 1.0) / 2.0
norm_color_0_2 = (norm_arr.GetValue(0, 2) + 1.0) / 2.0
norm_color_1_0 = (norm_arr.GetValue(1, 0) + 1.0) / 2.0
norm_color_1_1 = (norm_arr.GetValue(1, 1) + 1.0) / 2.0
norm_color_1_2 = (norm_arr.GetValue(1, 2) + 1.0) / 2.0
norm_color_2_0 = (norm_arr.GetValue(2, 0) + 1.0) / 2.0
norm_color_2_1 = (norm_arr.GetValue(2, 1) + 1.0) / 2.0
norm_color_2_2 = (norm_arr.GetValue(2, 2) + 1.0) / 2.0

# Normalized — row 0
norm_cell_0_0 = vtkPlaneSource()
norm_cell_0_0.SetOrigin(4, 2, 0)
norm_cell_0_0.SetPoint1(4.9, 2, 0)
norm_cell_0_0.SetPoint2(4, 2.9, 0)

norm_cell_mapper_0_0 = vtkPolyDataMapper()
norm_cell_mapper_0_0.SetInputConnection(norm_cell_0_0.GetOutputPort())

norm_cell_actor_0_0 = vtkActor()
norm_cell_actor_0_0.SetMapper(norm_cell_mapper_0_0)
norm_cell_actor_0_0.GetProperty().SetColor(norm_color_0_0, 0.2, 1.0 - norm_color_0_0)

norm_cell_0_1 = vtkPlaneSource()
norm_cell_0_1.SetOrigin(5, 2, 0)
norm_cell_0_1.SetPoint1(5.9, 2, 0)
norm_cell_0_1.SetPoint2(5, 2.9, 0)

norm_cell_mapper_0_1 = vtkPolyDataMapper()
norm_cell_mapper_0_1.SetInputConnection(norm_cell_0_1.GetOutputPort())

norm_cell_actor_0_1 = vtkActor()
norm_cell_actor_0_1.SetMapper(norm_cell_mapper_0_1)
norm_cell_actor_0_1.GetProperty().SetColor(norm_color_0_1, 0.2, 1.0 - norm_color_0_1)

norm_cell_0_2 = vtkPlaneSource()
norm_cell_0_2.SetOrigin(6, 2, 0)
norm_cell_0_2.SetPoint1(6.9, 2, 0)
norm_cell_0_2.SetPoint2(6, 2.9, 0)

norm_cell_mapper_0_2 = vtkPolyDataMapper()
norm_cell_mapper_0_2.SetInputConnection(norm_cell_0_2.GetOutputPort())

norm_cell_actor_0_2 = vtkActor()
norm_cell_actor_0_2.SetMapper(norm_cell_mapper_0_2)
norm_cell_actor_0_2.GetProperty().SetColor(norm_color_0_2, 0.2, 1.0 - norm_color_0_2)

# Normalized — row 1
norm_cell_1_0 = vtkPlaneSource()
norm_cell_1_0.SetOrigin(4, 1, 0)
norm_cell_1_0.SetPoint1(4.9, 1, 0)
norm_cell_1_0.SetPoint2(4, 1.9, 0)

norm_cell_mapper_1_0 = vtkPolyDataMapper()
norm_cell_mapper_1_0.SetInputConnection(norm_cell_1_0.GetOutputPort())

norm_cell_actor_1_0 = vtkActor()
norm_cell_actor_1_0.SetMapper(norm_cell_mapper_1_0)
norm_cell_actor_1_0.GetProperty().SetColor(norm_color_1_0, 0.2, 1.0 - norm_color_1_0)

norm_cell_1_1 = vtkPlaneSource()
norm_cell_1_1.SetOrigin(5, 1, 0)
norm_cell_1_1.SetPoint1(5.9, 1, 0)
norm_cell_1_1.SetPoint2(5, 1.9, 0)

norm_cell_mapper_1_1 = vtkPolyDataMapper()
norm_cell_mapper_1_1.SetInputConnection(norm_cell_1_1.GetOutputPort())

norm_cell_actor_1_1 = vtkActor()
norm_cell_actor_1_1.SetMapper(norm_cell_mapper_1_1)
norm_cell_actor_1_1.GetProperty().SetColor(norm_color_1_1, 0.2, 1.0 - norm_color_1_1)

norm_cell_1_2 = vtkPlaneSource()
norm_cell_1_2.SetOrigin(6, 1, 0)
norm_cell_1_2.SetPoint1(6.9, 1, 0)
norm_cell_1_2.SetPoint2(6, 1.9, 0)

norm_cell_mapper_1_2 = vtkPolyDataMapper()
norm_cell_mapper_1_2.SetInputConnection(norm_cell_1_2.GetOutputPort())

norm_cell_actor_1_2 = vtkActor()
norm_cell_actor_1_2.SetMapper(norm_cell_mapper_1_2)
norm_cell_actor_1_2.GetProperty().SetColor(norm_color_1_2, 0.2, 1.0 - norm_color_1_2)

# Normalized — row 2
norm_cell_2_0 = vtkPlaneSource()
norm_cell_2_0.SetOrigin(4, 0, 0)
norm_cell_2_0.SetPoint1(4.9, 0, 0)
norm_cell_2_0.SetPoint2(4, 0.9, 0)

norm_cell_mapper_2_0 = vtkPolyDataMapper()
norm_cell_mapper_2_0.SetInputConnection(norm_cell_2_0.GetOutputPort())

norm_cell_actor_2_0 = vtkActor()
norm_cell_actor_2_0.SetMapper(norm_cell_mapper_2_0)
norm_cell_actor_2_0.GetProperty().SetColor(norm_color_2_0, 0.2, 1.0 - norm_color_2_0)

norm_cell_2_1 = vtkPlaneSource()
norm_cell_2_1.SetOrigin(5, 0, 0)
norm_cell_2_1.SetPoint1(5.9, 0, 0)
norm_cell_2_1.SetPoint2(5, 0.9, 0)

norm_cell_mapper_2_1 = vtkPolyDataMapper()
norm_cell_mapper_2_1.SetInputConnection(norm_cell_2_1.GetOutputPort())

norm_cell_actor_2_1 = vtkActor()
norm_cell_actor_2_1.SetMapper(norm_cell_mapper_2_1)
norm_cell_actor_2_1.GetProperty().SetColor(norm_color_2_1, 0.2, 1.0 - norm_color_2_1)

norm_cell_2_2 = vtkPlaneSource()
norm_cell_2_2.SetOrigin(6, 0, 0)
norm_cell_2_2.SetPoint1(6.9, 0, 0)
norm_cell_2_2.SetPoint2(6, 0.9, 0)

norm_cell_mapper_2_2 = vtkPolyDataMapper()
norm_cell_mapper_2_2.SetInputConnection(norm_cell_2_2.GetOutputPort())

norm_cell_actor_2_2 = vtkActor()
norm_cell_actor_2_2.SetMapper(norm_cell_mapper_2_2)
norm_cell_actor_2_2.GetProperty().SetColor(norm_color_2_2, 0.2, 1.0 - norm_color_2_2)

# Label
label = vtkTextActor()
label.SetInput("NormalizeMatrixVectors: Source (left) / Normalized (right)")
label.GetTextProperty().SetFontSize(14)
label.GetTextProperty().SetColor(1, 1, 1)
label.SetPosition(10, 10)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(src_cell_actor_0_0)
renderer.AddActor(src_cell_actor_0_1)
renderer.AddActor(src_cell_actor_0_2)
renderer.AddActor(src_cell_actor_1_0)
renderer.AddActor(src_cell_actor_1_1)
renderer.AddActor(src_cell_actor_1_2)
renderer.AddActor(src_cell_actor_2_0)
renderer.AddActor(src_cell_actor_2_1)
renderer.AddActor(src_cell_actor_2_2)
renderer.AddActor(norm_cell_actor_0_0)
renderer.AddActor(norm_cell_actor_0_1)
renderer.AddActor(norm_cell_actor_0_2)
renderer.AddActor(norm_cell_actor_1_0)
renderer.AddActor(norm_cell_actor_1_1)
renderer.AddActor(norm_cell_actor_1_2)
renderer.AddActor(norm_cell_actor_2_0)
renderer.AddActor(norm_cell_actor_2_1)
renderer.AddActor(norm_cell_actor_2_2)
renderer.AddViewProp(label)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 300)
render_window.SetWindowName("array normalize matrix vectors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
