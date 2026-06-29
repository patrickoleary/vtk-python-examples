#!/usr/bin/env python

# Demonstrate vtkRandomHyperTreeGridSource with four viewports showing
# different numbers of pieces (1, 2, 4, 8), each with colored actors
# and piece count labels.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridGeometry
from vtkmodules.vtkFiltersSources import vtkRandomHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Viewport 0: 1 piece (top-left)
source_0_0 = vtkRandomHyperTreeGridSource()
source_0_0.SetDimensions(5, 5, 2)
source_0_0.SetSeed(371399)
source_0_0.SetSplitFraction(0.5)
source_0_0.SetMaskedFraction(0.5)
source_0_0.Update()

geometry_filter_0_0 = vtkHyperTreeGridGeometry()
geometry_filter_0_0.SetInputConnection(source_0_0.GetOutputPort())

mapper_0_0 = vtkPolyDataMapper()
mapper_0_0.SetInputConnection(geometry_filter_0_0.GetOutputPort())
mapper_0_0.SetPiece(0)
mapper_0_0.SetNumberOfPieces(1)

actor_0_0 = vtkActor()
actor_0_0.SetMapper(mapper_0_0)
actor_0_0.GetProperty().SetRepresentationToSurface()
actor_0_0.GetProperty().EdgeVisibilityOn()
actor_0_0.GetProperty().SetColor(1.0, 1.0, 1.0)

label_0 = vtkTextActor()
label_0.SetInput("NumPieces: 1")
label_0.GetTextProperty().SetVerticalJustificationToBottom()
label_0.GetTextProperty().SetJustificationToCentered()
label_0.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
label_0.GetPositionCoordinate().SetValue(0.5, 0.0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_0.AddActor(actor_0_0)
renderer_0.AddActor(label_0)

# Viewport 1: 2 pieces (top-right)
source_1_0 = vtkRandomHyperTreeGridSource()
source_1_0.SetDimensions(5, 5, 2)
source_1_0.SetSeed(371399)
source_1_0.SetSplitFraction(0.5)
source_1_0.SetMaskedFraction(0.25)
source_1_0.Update()

geometry_filter_1_0 = vtkHyperTreeGridGeometry()
geometry_filter_1_0.SetInputConnection(source_1_0.GetOutputPort())

mapper_1_0 = vtkPolyDataMapper()
mapper_1_0.SetInputConnection(geometry_filter_1_0.GetOutputPort())
mapper_1_0.SetPiece(0)
mapper_1_0.SetNumberOfPieces(2)

actor_1_0 = vtkActor()
actor_1_0.SetMapper(mapper_1_0)
actor_1_0.GetProperty().SetRepresentationToSurface()
actor_1_0.GetProperty().EdgeVisibilityOn()
actor_1_0.GetProperty().SetColor(1.0, 1.0, 1.0)

source_1_1 = vtkRandomHyperTreeGridSource()
source_1_1.SetDimensions(5, 5, 2)
source_1_1.SetSeed(371399)
source_1_1.SetSplitFraction(0.5)
source_1_1.SetMaskedFraction(0.25)
source_1_1.Update()

geometry_filter_1_1 = vtkHyperTreeGridGeometry()
geometry_filter_1_1.SetInputConnection(source_1_1.GetOutputPort())

mapper_1_1 = vtkPolyDataMapper()
mapper_1_1.SetInputConnection(geometry_filter_1_1.GetOutputPort())
mapper_1_1.SetPiece(1)
mapper_1_1.SetNumberOfPieces(2)

actor_1_1 = vtkActor()
actor_1_1.SetMapper(mapper_1_1)
actor_1_1.GetProperty().SetRepresentationToSurface()
actor_1_1.GetProperty().EdgeVisibilityOn()
actor_1_1.GetProperty().SetColor(0.0, 1.0, 1.0)

label_1 = vtkTextActor()
label_1.SetInput("NumPieces: 2")
label_1.GetTextProperty().SetVerticalJustificationToBottom()
label_1.GetTextProperty().SetJustificationToCentered()
label_1.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
label_1.GetPositionCoordinate().SetValue(0.5, 0.0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_1.AddActor(actor_1_0)
renderer_1.AddActor(actor_1_1)
renderer_1.AddActor(label_1)

# Viewport 2: 4 pieces (bottom-left)
source_2_0 = vtkRandomHyperTreeGridSource()
source_2_0.SetDimensions(5, 5, 2)
source_2_0.SetSeed(371399)
source_2_0.SetSplitFraction(0.5)
source_2_0.SetMaskedFraction(0.125)
source_2_0.Update()

geometry_filter_2_0 = vtkHyperTreeGridGeometry()
geometry_filter_2_0.SetInputConnection(source_2_0.GetOutputPort())

mapper_2_0 = vtkPolyDataMapper()
mapper_2_0.SetInputConnection(geometry_filter_2_0.GetOutputPort())
mapper_2_0.SetPiece(0)
mapper_2_0.SetNumberOfPieces(4)

actor_2_0 = vtkActor()
actor_2_0.SetMapper(mapper_2_0)
actor_2_0.GetProperty().SetRepresentationToSurface()
actor_2_0.GetProperty().EdgeVisibilityOn()
actor_2_0.GetProperty().SetColor(1.0, 1.0, 1.0)

source_2_1 = vtkRandomHyperTreeGridSource()
source_2_1.SetDimensions(5, 5, 2)
source_2_1.SetSeed(371399)
source_2_1.SetSplitFraction(0.5)
source_2_1.SetMaskedFraction(0.125)
source_2_1.Update()

geometry_filter_2_1 = vtkHyperTreeGridGeometry()
geometry_filter_2_1.SetInputConnection(source_2_1.GetOutputPort())

mapper_2_1 = vtkPolyDataMapper()
mapper_2_1.SetInputConnection(geometry_filter_2_1.GetOutputPort())
mapper_2_1.SetPiece(1)
mapper_2_1.SetNumberOfPieces(4)

actor_2_1 = vtkActor()
actor_2_1.SetMapper(mapper_2_1)
actor_2_1.GetProperty().SetRepresentationToSurface()
actor_2_1.GetProperty().EdgeVisibilityOn()
actor_2_1.GetProperty().SetColor(0.0, 1.0, 1.0)

source_2_2 = vtkRandomHyperTreeGridSource()
source_2_2.SetDimensions(5, 5, 2)
source_2_2.SetSeed(371399)
source_2_2.SetSplitFraction(0.5)
source_2_2.SetMaskedFraction(0.125)
source_2_2.Update()

geometry_filter_2_2 = vtkHyperTreeGridGeometry()
geometry_filter_2_2.SetInputConnection(source_2_2.GetOutputPort())

mapper_2_2 = vtkPolyDataMapper()
mapper_2_2.SetInputConnection(geometry_filter_2_2.GetOutputPort())
mapper_2_2.SetPiece(2)
mapper_2_2.SetNumberOfPieces(4)

actor_2_2 = vtkActor()
actor_2_2.SetMapper(mapper_2_2)
actor_2_2.GetProperty().SetRepresentationToSurface()
actor_2_2.GetProperty().EdgeVisibilityOn()
actor_2_2.GetProperty().SetColor(1.0, 0.0, 1.0)

source_2_3 = vtkRandomHyperTreeGridSource()
source_2_3.SetDimensions(5, 5, 2)
source_2_3.SetSeed(371399)
source_2_3.SetSplitFraction(0.5)
source_2_3.SetMaskedFraction(0.125)
source_2_3.Update()

geometry_filter_2_3 = vtkHyperTreeGridGeometry()
geometry_filter_2_3.SetInputConnection(source_2_3.GetOutputPort())

mapper_2_3 = vtkPolyDataMapper()
mapper_2_3.SetInputConnection(geometry_filter_2_3.GetOutputPort())
mapper_2_3.SetPiece(3)
mapper_2_3.SetNumberOfPieces(4)

actor_2_3 = vtkActor()
actor_2_3.SetMapper(mapper_2_3)
actor_2_3.GetProperty().SetRepresentationToSurface()
actor_2_3.GetProperty().EdgeVisibilityOn()
actor_2_3.GetProperty().SetColor(1.0, 1.0, 0.0)

label_2 = vtkTextActor()
label_2.SetInput("NumPieces: 4")
label_2.GetTextProperty().SetVerticalJustificationToBottom()
label_2.GetTextProperty().SetJustificationToCentered()
label_2.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
label_2.GetPositionCoordinate().SetValue(0.5, 0.0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_2.AddActor(actor_2_0)
renderer_2.AddActor(actor_2_1)
renderer_2.AddActor(actor_2_2)
renderer_2.AddActor(actor_2_3)
renderer_2.AddActor(label_2)

# Viewport 3: 8 pieces (bottom-right)
source_3_0 = vtkRandomHyperTreeGridSource()
source_3_0.SetDimensions(5, 5, 2)
source_3_0.SetSeed(371399)
source_3_0.SetSplitFraction(0.5)
source_3_0.SetMaskedFraction(0.0625)
source_3_0.Update()

geometry_filter_3_0 = vtkHyperTreeGridGeometry()
geometry_filter_3_0.SetInputConnection(source_3_0.GetOutputPort())

mapper_3_0 = vtkPolyDataMapper()
mapper_3_0.SetInputConnection(geometry_filter_3_0.GetOutputPort())
mapper_3_0.SetPiece(0)
mapper_3_0.SetNumberOfPieces(8)

actor_3_0 = vtkActor()
actor_3_0.SetMapper(mapper_3_0)
actor_3_0.GetProperty().SetRepresentationToSurface()
actor_3_0.GetProperty().EdgeVisibilityOn()
actor_3_0.GetProperty().SetColor(1.0, 1.0, 1.0)

source_3_1 = vtkRandomHyperTreeGridSource()
source_3_1.SetDimensions(5, 5, 2)
source_3_1.SetSeed(371399)
source_3_1.SetSplitFraction(0.5)
source_3_1.SetMaskedFraction(0.0625)
source_3_1.Update()

geometry_filter_3_1 = vtkHyperTreeGridGeometry()
geometry_filter_3_1.SetInputConnection(source_3_1.GetOutputPort())

mapper_3_1 = vtkPolyDataMapper()
mapper_3_1.SetInputConnection(geometry_filter_3_1.GetOutputPort())
mapper_3_1.SetPiece(1)
mapper_3_1.SetNumberOfPieces(8)

actor_3_1 = vtkActor()
actor_3_1.SetMapper(mapper_3_1)
actor_3_1.GetProperty().SetRepresentationToSurface()
actor_3_1.GetProperty().EdgeVisibilityOn()
actor_3_1.GetProperty().SetColor(0.0, 1.0, 1.0)

source_3_2 = vtkRandomHyperTreeGridSource()
source_3_2.SetDimensions(5, 5, 2)
source_3_2.SetSeed(371399)
source_3_2.SetSplitFraction(0.5)
source_3_2.SetMaskedFraction(0.0625)
source_3_2.Update()

geometry_filter_3_2 = vtkHyperTreeGridGeometry()
geometry_filter_3_2.SetInputConnection(source_3_2.GetOutputPort())

mapper_3_2 = vtkPolyDataMapper()
mapper_3_2.SetInputConnection(geometry_filter_3_2.GetOutputPort())
mapper_3_2.SetPiece(2)
mapper_3_2.SetNumberOfPieces(8)

actor_3_2 = vtkActor()
actor_3_2.SetMapper(mapper_3_2)
actor_3_2.GetProperty().SetRepresentationToSurface()
actor_3_2.GetProperty().EdgeVisibilityOn()
actor_3_2.GetProperty().SetColor(1.0, 0.0, 1.0)

source_3_3 = vtkRandomHyperTreeGridSource()
source_3_3.SetDimensions(5, 5, 2)
source_3_3.SetSeed(371399)
source_3_3.SetSplitFraction(0.5)
source_3_3.SetMaskedFraction(0.0625)
source_3_3.Update()

geometry_filter_3_3 = vtkHyperTreeGridGeometry()
geometry_filter_3_3.SetInputConnection(source_3_3.GetOutputPort())

mapper_3_3 = vtkPolyDataMapper()
mapper_3_3.SetInputConnection(geometry_filter_3_3.GetOutputPort())
mapper_3_3.SetPiece(3)
mapper_3_3.SetNumberOfPieces(8)

actor_3_3 = vtkActor()
actor_3_3.SetMapper(mapper_3_3)
actor_3_3.GetProperty().SetRepresentationToSurface()
actor_3_3.GetProperty().EdgeVisibilityOn()
actor_3_3.GetProperty().SetColor(1.0, 1.0, 0.0)

source_3_4 = vtkRandomHyperTreeGridSource()
source_3_4.SetDimensions(5, 5, 2)
source_3_4.SetSeed(371399)
source_3_4.SetSplitFraction(0.5)
source_3_4.SetMaskedFraction(0.0625)
source_3_4.Update()

geometry_filter_3_4 = vtkHyperTreeGridGeometry()
geometry_filter_3_4.SetInputConnection(source_3_4.GetOutputPort())

mapper_3_4 = vtkPolyDataMapper()
mapper_3_4.SetInputConnection(geometry_filter_3_4.GetOutputPort())
mapper_3_4.SetPiece(4)
mapper_3_4.SetNumberOfPieces(8)

actor_3_4 = vtkActor()
actor_3_4.SetMapper(mapper_3_4)
actor_3_4.GetProperty().SetRepresentationToSurface()
actor_3_4.GetProperty().EdgeVisibilityOn()
actor_3_4.GetProperty().SetColor(1.0, 0.0, 0.0)

source_3_5 = vtkRandomHyperTreeGridSource()
source_3_5.SetDimensions(5, 5, 2)
source_3_5.SetSeed(371399)
source_3_5.SetSplitFraction(0.5)
source_3_5.SetMaskedFraction(0.0625)
source_3_5.Update()

geometry_filter_3_5 = vtkHyperTreeGridGeometry()
geometry_filter_3_5.SetInputConnection(source_3_5.GetOutputPort())

mapper_3_5 = vtkPolyDataMapper()
mapper_3_5.SetInputConnection(geometry_filter_3_5.GetOutputPort())
mapper_3_5.SetPiece(5)
mapper_3_5.SetNumberOfPieces(8)

actor_3_5 = vtkActor()
actor_3_5.SetMapper(mapper_3_5)
actor_3_5.GetProperty().SetRepresentationToSurface()
actor_3_5.GetProperty().EdgeVisibilityOn()
actor_3_5.GetProperty().SetColor(0.0, 1.0, 0.0)

source_3_6 = vtkRandomHyperTreeGridSource()
source_3_6.SetDimensions(5, 5, 2)
source_3_6.SetSeed(371399)
source_3_6.SetSplitFraction(0.5)
source_3_6.SetMaskedFraction(0.0625)
source_3_6.Update()

geometry_filter_3_6 = vtkHyperTreeGridGeometry()
geometry_filter_3_6.SetInputConnection(source_3_6.GetOutputPort())

mapper_3_6 = vtkPolyDataMapper()
mapper_3_6.SetInputConnection(geometry_filter_3_6.GetOutputPort())
mapper_3_6.SetPiece(6)
mapper_3_6.SetNumberOfPieces(8)

actor_3_6 = vtkActor()
actor_3_6.SetMapper(mapper_3_6)
actor_3_6.GetProperty().SetRepresentationToSurface()
actor_3_6.GetProperty().EdgeVisibilityOn()
actor_3_6.GetProperty().SetColor(0.0, 0.0, 1.0)

source_3_7 = vtkRandomHyperTreeGridSource()
source_3_7.SetDimensions(5, 5, 2)
source_3_7.SetSeed(371399)
source_3_7.SetSplitFraction(0.5)
source_3_7.SetMaskedFraction(0.0625)
source_3_7.Update()

geometry_filter_3_7 = vtkHyperTreeGridGeometry()
geometry_filter_3_7.SetInputConnection(source_3_7.GetOutputPort())

mapper_3_7 = vtkPolyDataMapper()
mapper_3_7.SetInputConnection(geometry_filter_3_7.GetOutputPort())
mapper_3_7.SetPiece(7)
mapper_3_7.SetNumberOfPieces(8)

actor_3_7 = vtkActor()
actor_3_7.SetMapper(mapper_3_7)
actor_3_7.GetProperty().SetRepresentationToSurface()
actor_3_7.GetProperty().EdgeVisibilityOn()
actor_3_7.GetProperty().SetColor(0.7, 0.3, 0.3)

label_3 = vtkTextActor()
label_3.SetInput("NumPieces: 8")
label_3.GetTextProperty().SetVerticalJustificationToBottom()
label_3.GetTextProperty().SetJustificationToCentered()
label_3.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
label_3.GetPositionCoordinate().SetValue(0.5, 0.0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_3.AddActor(actor_3_0)
renderer_3.AddActor(actor_3_1)
renderer_3.AddActor(actor_3_2)
renderer_3.AddActor(actor_3_3)
renderer_3.AddActor(actor_3_4)
renderer_3.AddActor(actor_3_5)
renderer_3.AddActor(actor_3_6)
renderer_3.AddActor(actor_3_7)
renderer_3.AddActor(label_3)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)
render_window.SetWindowName("random hypertreegrid source")
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
