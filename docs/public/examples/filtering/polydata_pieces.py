#!/usr/bin/env python
# Demonstrate parallel poly data extraction with piece scalars and ghost levels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersParallel import (
    vtkExtractPolyDataPiece,
    vtkPieceScalars,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

math_obj = vtkMath()
math_obj.RandomSeed(22)

# Source / Filter / Mapper / Actor - piece scalars with normals
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(32)
sphere_source.SetThetaResolution(32)

extract_piece = vtkExtractPolyDataPiece()
extract_piece.SetInputConnection(sphere_source.GetOutputPort())

normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(extract_piece.GetOutputPort())

piece_scalars = vtkPieceScalars()
piece_scalars.SetInputConnection(normals_filter.GetOutputPort())

piece_mapper = vtkPolyDataMapper()
piece_mapper.SetInputConnection(piece_scalars.GetOutputPort())
piece_mapper.SetNumberOfPieces(2)

piece_actor = vtkActor()
piece_actor.SetMapper(piece_mapper)

# Source / Filter / Mapper / Actor - ghost level coloring
sphere_source_2 = vtkSphereSource()
sphere_source_2.SetPhiResolution(32)
sphere_source_2.SetThetaResolution(32)

extract_piece_2 = vtkExtractPolyDataPiece()
extract_piece_2.SetInputConnection(sphere_source_2.GetOutputPort())

ghost_mapper = vtkPolyDataMapper()
ghost_mapper.SetInputConnection(extract_piece_2.GetOutputPort())
ghost_mapper.SetNumberOfPieces(2)
ghost_mapper.SetPiece(1)
ghost_mapper.SetScalarRange(0, 4)
ghost_mapper.SetScalarModeToUseCellFieldData()
ghost_mapper.SetColorModeToMapScalars()
ghost_mapper.ColorByArrayComponent(vtkDataSetAttributes.GhostArrayName(), 0)
ghost_mapper.SetGhostLevel(4)

ghost_actor = vtkActor()
ghost_actor.SetMapper(ghost_mapper)
ghost_actor.SetPosition(1.5, 0, 0)

# Source / Filter / Mapper / Actor - sub-pieces
sphere_source_3 = vtkSphereSource()
sphere_source_3.SetPhiResolution(32)
sphere_source_3.SetThetaResolution(32)

extract_piece_3 = vtkExtractPolyDataPiece()
extract_piece_3.SetInputConnection(sphere_source_3.GetOutputPort())

piece_scalars_3 = vtkPieceScalars()
piece_scalars_3.SetInputConnection(extract_piece_3.GetOutputPort())

subpiece_mapper = vtkPolyDataMapper()
subpiece_mapper.SetInputConnection(piece_scalars_3.GetOutputPort())
subpiece_mapper.SetNumberOfSubPieces(8)
subpiece_mapper.SetScalarRange(0, 8)

subpiece_actor = vtkActor()
subpiece_actor.SetMapper(subpiece_mapper)
subpiece_actor.SetPosition(0, -1.5, 0)

# Source / Filter / Mapper / Actor - random mode cell data
sphere_source_4 = vtkSphereSource()
sphere_source_4.SetPhiResolution(32)
sphere_source_4.SetThetaResolution(32)

extract_piece_4 = vtkExtractPolyDataPiece()
extract_piece_4.SetInputConnection(sphere_source_4.GetOutputPort())

piece_scalars_4 = vtkPieceScalars()
piece_scalars_4.RandomModeOn()
piece_scalars_4.SetScalarModeToCellData()
piece_scalars_4.SetInputConnection(extract_piece_4.GetOutputPort())

random_mapper = vtkPolyDataMapper()
random_mapper.SetInputConnection(piece_scalars_4.GetOutputPort())
random_mapper.SetNumberOfSubPieces(8)
random_mapper.SetScalarRange(0, 8)

random_actor = vtkActor()
random_actor.SetMapper(random_mapper)
random_actor.SetPosition(1.5, -1.5, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(piece_actor)
renderer.AddActor(ghost_actor)
renderer.AddActor(subpiece_actor)
renderer.AddActor(random_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polydata pieces")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
