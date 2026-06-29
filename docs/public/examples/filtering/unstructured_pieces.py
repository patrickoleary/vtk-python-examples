#!/usr/bin/env python
# Demonstrate parallel unstructured grid extraction with contour and piece scalars.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersParallel import (
    vtkExtractUnstructuredGridPiece,
    vtkPieceScalars,
)
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

math_obj = vtkMath()
math_obj.RandomSeed(22)

plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.Update()

plot3d_output = plot3d_reader.GetOutput().GetBlock(0)

# Filter
triangle_filter = vtkDataSetTriangleFilter()
triangle_filter.SetInputData(plot3d_output)

extract_piece = vtkExtractUnstructuredGridPiece()
extract_piece.SetInputConnection(triangle_filter.GetOutputPort())

contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(extract_piece.GetOutputPort())
contour_filter.SetValue(0, 0.24)

normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(contour_filter.GetOutputPort())

piece_scalars = vtkPieceScalars()
piece_scalars.SetInputConnection(normals_filter.GetOutputPort())

# Mapper
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(piece_scalars.GetOutputPort())
contour_mapper.SetNumberOfPieces(3)

# Actor
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(contour_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("unstructured pieces")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
