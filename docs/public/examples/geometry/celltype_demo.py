#!/usr/bin/env python

# Demonstrate vtkCellTypeSource for all supported cell types: 1D lines,
# 2D triangles and quads, and 3D tetrahedra, hexahedra, wedges, and
# pyramids — both linear and quadratic variants. Each cell is generated,
# perturbed, shrunk, tessellated, and displayed in a labeled 4×4 grid
# of viewports, each with its own renderer.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_CUBIC_LINE,
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_PYRAMID,
    VTK_QUAD,
    VTK_QUADRATIC_EDGE,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_PYRAMID,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TETRA,
    VTK_QUADRATIC_TRIANGLE,
    VTK_QUADRATIC_WEDGE,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_WEDGE,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkShrinkFilter,
    vtkTessellatorFilter,
)
from vtkmodules.vtkFiltersSources import vtkCellTypeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkTextActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# ---------------------------------------------------------------------------
# Viewport grid: 4 columns × 4 rows, 15 cell types fill positions 0–14
#   Row 0 (top):    1D — Line, Quadratic Edge, Cubic Line, (empty)
#   Row 1:          2D — Triangle, Quadratic Triangle, Quad, Quadratic Quad
#   Row 2:          3D — Tetra, Quadratic Tetra, Hexahedron, Quadratic Hexahedron
#   Row 3 (bottom): 3D — Wedge, Quadratic Wedge, Pyramid, Quadratic Pyramid
# ---------------------------------------------------------------------------

# --- Row 0, Col 0: Line — Source, Filter, Mapper, Actor -------------------
line_source = vtkCellTypeSource()
line_source.SetCellType(VTK_LINE)
line_source.Update()

line_original_points = line_source.GetOutput().GetPoints()
line_points = vtkPoints()
line_points.SetNumberOfPoints(line_source.GetOutput().GetNumberOfPoints())
line_rng = vtkMinimalStandardRandomSequence()
line_rng.SetSeed(5070)
for i in range(line_points.GetNumberOfPoints()):
    line_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        line_rng.Next()
        line_perturbation[j] = line_rng.GetRangeValue(-0.1, 0.1)
    line_current = [0.0, 0.0, 0.0]
    line_original_points.GetPoint(i, line_current)
    line_points.SetPoint(i,
                         line_current[0] + line_perturbation[0],
                         line_current[1] + line_perturbation[1],
                         line_current[2] + line_perturbation[2])
line_source.GetOutput().SetPoints(line_points)

line_num_cells = line_source.GetOutput().GetNumberOfCells()
line_id_array = vtkIntArray()
line_id_array.SetNumberOfTuples(line_num_cells)
for i in range(line_num_cells):
    line_id_array.InsertTuple1(i, i + 1)
line_id_array.SetName("Ids")
line_source.GetOutput().GetCellData().AddArray(line_id_array)
line_source.GetOutput().GetCellData().SetActiveScalars("Ids")

line_shrink = vtkShrinkFilter()
line_shrink.SetInputConnection(line_source.GetOutputPort())
line_shrink.SetShrinkFactor(0.8)

line_tessellator = vtkTessellatorFilter()
line_tessellator.SetInputConnection(line_shrink.GetOutputPort())
line_tessellator.SetMaximumNumberOfSubdivisions(3)

line_mapper = vtkDataSetMapper()
line_mapper.SetInputConnection(line_tessellator.GetOutputPort())
line_mapper.SetScalarRange(0, line_num_cells + 1)
line_mapper.SetScalarModeToUseCellData()
line_mapper.SetResolveCoincidentTopologyToPolygonOffset()

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().EdgeVisibilityOn()

line_text_actor = vtkTextActor()
line_text_actor.SetInput("Line")
line_text_actor.GetTextProperty().SetFontSize(16)
line_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
line_text_actor.GetTextProperty().SetJustificationToCentered()
line_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
line_text_actor.SetPosition(0.5, 0.01)

# --- Row 0, Col 1: Quadratic Edge — Source, Filter, Mapper, Actor ---------
quad_edge_source = vtkCellTypeSource()
quad_edge_source.SetCellType(VTK_QUADRATIC_EDGE)
quad_edge_source.Update()

quad_edge_original_points = quad_edge_source.GetOutput().GetPoints()
quad_edge_points = vtkPoints()
quad_edge_points.SetNumberOfPoints(quad_edge_source.GetOutput().GetNumberOfPoints())
quad_edge_rng = vtkMinimalStandardRandomSequence()
quad_edge_rng.SetSeed(5070)
for i in range(quad_edge_points.GetNumberOfPoints()):
    quad_edge_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_edge_rng.Next()
        quad_edge_perturbation[j] = quad_edge_rng.GetRangeValue(-0.1, 0.1)
    quad_edge_current = [0.0, 0.0, 0.0]
    quad_edge_original_points.GetPoint(i, quad_edge_current)
    quad_edge_points.SetPoint(i,
                              quad_edge_current[0] + quad_edge_perturbation[0],
                              quad_edge_current[1] + quad_edge_perturbation[1],
                              quad_edge_current[2] + quad_edge_perturbation[2])
quad_edge_source.GetOutput().SetPoints(quad_edge_points)

quad_edge_num_cells = quad_edge_source.GetOutput().GetNumberOfCells()
quad_edge_id_array = vtkIntArray()
quad_edge_id_array.SetNumberOfTuples(quad_edge_num_cells)
for i in range(quad_edge_num_cells):
    quad_edge_id_array.InsertTuple1(i, i + 1)
quad_edge_id_array.SetName("Ids")
quad_edge_source.GetOutput().GetCellData().AddArray(quad_edge_id_array)
quad_edge_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_edge_shrink = vtkShrinkFilter()
quad_edge_shrink.SetInputConnection(quad_edge_source.GetOutputPort())
quad_edge_shrink.SetShrinkFactor(0.8)

quad_edge_tessellator = vtkTessellatorFilter()
quad_edge_tessellator.SetInputConnection(quad_edge_shrink.GetOutputPort())
quad_edge_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_edge_mapper = vtkDataSetMapper()
quad_edge_mapper.SetInputConnection(quad_edge_tessellator.GetOutputPort())
quad_edge_mapper.SetScalarRange(0, quad_edge_num_cells + 1)
quad_edge_mapper.SetScalarModeToUseCellData()
quad_edge_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_edge_actor = vtkActor()
quad_edge_actor.SetMapper(quad_edge_mapper)
quad_edge_actor.GetProperty().EdgeVisibilityOn()

quad_edge_text_actor = vtkTextActor()
quad_edge_text_actor.SetInput("Quadratic Edge")
quad_edge_text_actor.GetTextProperty().SetFontSize(16)
quad_edge_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_edge_text_actor.GetTextProperty().SetJustificationToCentered()
quad_edge_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_edge_text_actor.SetPosition(0.5, 0.01)

# --- Row 0, Col 2: Cubic Line — Source, Filter, Mapper, Actor -------------
cubic_line_source = vtkCellTypeSource()
cubic_line_source.SetCellType(VTK_CUBIC_LINE)
cubic_line_source.Update()

cubic_line_original_points = cubic_line_source.GetOutput().GetPoints()
cubic_line_points = vtkPoints()
cubic_line_points.SetNumberOfPoints(cubic_line_source.GetOutput().GetNumberOfPoints())
cubic_line_rng = vtkMinimalStandardRandomSequence()
cubic_line_rng.SetSeed(5070)
for i in range(cubic_line_points.GetNumberOfPoints()):
    cubic_line_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        cubic_line_rng.Next()
        cubic_line_perturbation[j] = cubic_line_rng.GetRangeValue(-0.1, 0.1)
    cubic_line_current = [0.0, 0.0, 0.0]
    cubic_line_original_points.GetPoint(i, cubic_line_current)
    cubic_line_points.SetPoint(i,
                               cubic_line_current[0] + cubic_line_perturbation[0],
                               cubic_line_current[1] + cubic_line_perturbation[1],
                               cubic_line_current[2] + cubic_line_perturbation[2])
cubic_line_source.GetOutput().SetPoints(cubic_line_points)

cubic_line_num_cells = cubic_line_source.GetOutput().GetNumberOfCells()
cubic_line_id_array = vtkIntArray()
cubic_line_id_array.SetNumberOfTuples(cubic_line_num_cells)
for i in range(cubic_line_num_cells):
    cubic_line_id_array.InsertTuple1(i, i + 1)
cubic_line_id_array.SetName("Ids")
cubic_line_source.GetOutput().GetCellData().AddArray(cubic_line_id_array)
cubic_line_source.GetOutput().GetCellData().SetActiveScalars("Ids")

cubic_line_shrink = vtkShrinkFilter()
cubic_line_shrink.SetInputConnection(cubic_line_source.GetOutputPort())
cubic_line_shrink.SetShrinkFactor(0.8)

cubic_line_tessellator = vtkTessellatorFilter()
cubic_line_tessellator.SetInputConnection(cubic_line_shrink.GetOutputPort())
cubic_line_tessellator.SetMaximumNumberOfSubdivisions(3)

cubic_line_mapper = vtkDataSetMapper()
cubic_line_mapper.SetInputConnection(cubic_line_tessellator.GetOutputPort())
cubic_line_mapper.SetScalarRange(0, cubic_line_num_cells + 1)
cubic_line_mapper.SetScalarModeToUseCellData()
cubic_line_mapper.SetResolveCoincidentTopologyToPolygonOffset()

cubic_line_actor = vtkActor()
cubic_line_actor.SetMapper(cubic_line_mapper)
cubic_line_actor.GetProperty().EdgeVisibilityOn()

cubic_line_text_actor = vtkTextActor()
cubic_line_text_actor.SetInput("Cubic Line")
cubic_line_text_actor.GetTextProperty().SetFontSize(16)
cubic_line_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
cubic_line_text_actor.GetTextProperty().SetJustificationToCentered()
cubic_line_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cubic_line_text_actor.SetPosition(0.5, 0.01)

# --- Row 1, Col 0: Triangle — Source, Filter, Mapper, Actor ---------------
triangle_source = vtkCellTypeSource()
triangle_source.SetCellType(VTK_TRIANGLE)
triangle_source.Update()

triangle_original_points = triangle_source.GetOutput().GetPoints()
triangle_points = vtkPoints()
triangle_points.SetNumberOfPoints(triangle_source.GetOutput().GetNumberOfPoints())
triangle_rng = vtkMinimalStandardRandomSequence()
triangle_rng.SetSeed(5070)
for i in range(triangle_points.GetNumberOfPoints()):
    triangle_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        triangle_rng.Next()
        triangle_perturbation[j] = triangle_rng.GetRangeValue(-0.1, 0.1)
    triangle_current = [0.0, 0.0, 0.0]
    triangle_original_points.GetPoint(i, triangle_current)
    triangle_points.SetPoint(i,
                             triangle_current[0] + triangle_perturbation[0],
                             triangle_current[1] + triangle_perturbation[1],
                             triangle_current[2] + triangle_perturbation[2])
triangle_source.GetOutput().SetPoints(triangle_points)

triangle_num_cells = triangle_source.GetOutput().GetNumberOfCells()
triangle_id_array = vtkIntArray()
triangle_id_array.SetNumberOfTuples(triangle_num_cells)
for i in range(triangle_num_cells):
    triangle_id_array.InsertTuple1(i, i + 1)
triangle_id_array.SetName("Ids")
triangle_source.GetOutput().GetCellData().AddArray(triangle_id_array)
triangle_source.GetOutput().GetCellData().SetActiveScalars("Ids")

triangle_shrink = vtkShrinkFilter()
triangle_shrink.SetInputConnection(triangle_source.GetOutputPort())
triangle_shrink.SetShrinkFactor(0.8)

triangle_tessellator = vtkTessellatorFilter()
triangle_tessellator.SetInputConnection(triangle_shrink.GetOutputPort())
triangle_tessellator.SetMaximumNumberOfSubdivisions(3)

triangle_mapper = vtkDataSetMapper()
triangle_mapper.SetInputConnection(triangle_tessellator.GetOutputPort())
triangle_mapper.SetScalarRange(0, triangle_num_cells + 1)
triangle_mapper.SetScalarModeToUseCellData()
triangle_mapper.SetResolveCoincidentTopologyToPolygonOffset()

triangle_actor = vtkActor()
triangle_actor.SetMapper(triangle_mapper)
triangle_actor.GetProperty().EdgeVisibilityOn()

triangle_text_actor = vtkTextActor()
triangle_text_actor.SetInput("Triangle")
triangle_text_actor.GetTextProperty().SetFontSize(16)
triangle_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
triangle_text_actor.GetTextProperty().SetJustificationToCentered()
triangle_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
triangle_text_actor.SetPosition(0.5, 0.01)

# --- Row 1, Col 1: Quadratic Triangle — Source, Filter, Mapper, Actor -----
quad_tri_source = vtkCellTypeSource()
quad_tri_source.SetCellType(VTK_QUADRATIC_TRIANGLE)
quad_tri_source.Update()

quad_tri_original_points = quad_tri_source.GetOutput().GetPoints()
quad_tri_points = vtkPoints()
quad_tri_points.SetNumberOfPoints(quad_tri_source.GetOutput().GetNumberOfPoints())
quad_tri_rng = vtkMinimalStandardRandomSequence()
quad_tri_rng.SetSeed(5070)
for i in range(quad_tri_points.GetNumberOfPoints()):
    quad_tri_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_tri_rng.Next()
        quad_tri_perturbation[j] = quad_tri_rng.GetRangeValue(-0.1, 0.1)
    quad_tri_current = [0.0, 0.0, 0.0]
    quad_tri_original_points.GetPoint(i, quad_tri_current)
    quad_tri_points.SetPoint(i,
                             quad_tri_current[0] + quad_tri_perturbation[0],
                             quad_tri_current[1] + quad_tri_perturbation[1],
                             quad_tri_current[2] + quad_tri_perturbation[2])
quad_tri_source.GetOutput().SetPoints(quad_tri_points)

quad_tri_num_cells = quad_tri_source.GetOutput().GetNumberOfCells()
quad_tri_id_array = vtkIntArray()
quad_tri_id_array.SetNumberOfTuples(quad_tri_num_cells)
for i in range(quad_tri_num_cells):
    quad_tri_id_array.InsertTuple1(i, i + 1)
quad_tri_id_array.SetName("Ids")
quad_tri_source.GetOutput().GetCellData().AddArray(quad_tri_id_array)
quad_tri_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_tri_shrink = vtkShrinkFilter()
quad_tri_shrink.SetInputConnection(quad_tri_source.GetOutputPort())
quad_tri_shrink.SetShrinkFactor(0.8)

quad_tri_tessellator = vtkTessellatorFilter()
quad_tri_tessellator.SetInputConnection(quad_tri_shrink.GetOutputPort())
quad_tri_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_tri_mapper = vtkDataSetMapper()
quad_tri_mapper.SetInputConnection(quad_tri_tessellator.GetOutputPort())
quad_tri_mapper.SetScalarRange(0, quad_tri_num_cells + 1)
quad_tri_mapper.SetScalarModeToUseCellData()
quad_tri_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_tri_actor = vtkActor()
quad_tri_actor.SetMapper(quad_tri_mapper)
quad_tri_actor.GetProperty().EdgeVisibilityOn()

quad_tri_text_actor = vtkTextActor()
quad_tri_text_actor.SetInput("Quadratic Triangle")
quad_tri_text_actor.GetTextProperty().SetFontSize(16)
quad_tri_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_tri_text_actor.GetTextProperty().SetJustificationToCentered()
quad_tri_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_tri_text_actor.SetPosition(0.5, 0.01)

# --- Row 1, Col 2: Quad — Source, Filter, Mapper, Actor -------------------
quad_source = vtkCellTypeSource()
quad_source.SetCellType(VTK_QUAD)
quad_source.Update()

quad_original_points = quad_source.GetOutput().GetPoints()
quad_points = vtkPoints()
quad_points.SetNumberOfPoints(quad_source.GetOutput().GetNumberOfPoints())
quad_rng = vtkMinimalStandardRandomSequence()
quad_rng.SetSeed(5070)
for i in range(quad_points.GetNumberOfPoints()):
    quad_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_rng.Next()
        quad_perturbation[j] = quad_rng.GetRangeValue(-0.1, 0.1)
    quad_current = [0.0, 0.0, 0.0]
    quad_original_points.GetPoint(i, quad_current)
    quad_points.SetPoint(i,
                         quad_current[0] + quad_perturbation[0],
                         quad_current[1] + quad_perturbation[1],
                         quad_current[2] + quad_perturbation[2])
quad_source.GetOutput().SetPoints(quad_points)

quad_num_cells = quad_source.GetOutput().GetNumberOfCells()
quad_id_array = vtkIntArray()
quad_id_array.SetNumberOfTuples(quad_num_cells)
for i in range(quad_num_cells):
    quad_id_array.InsertTuple1(i, i + 1)
quad_id_array.SetName("Ids")
quad_source.GetOutput().GetCellData().AddArray(quad_id_array)
quad_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_shrink = vtkShrinkFilter()
quad_shrink.SetInputConnection(quad_source.GetOutputPort())
quad_shrink.SetShrinkFactor(0.8)

quad_tessellator = vtkTessellatorFilter()
quad_tessellator.SetInputConnection(quad_shrink.GetOutputPort())
quad_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_mapper = vtkDataSetMapper()
quad_mapper.SetInputConnection(quad_tessellator.GetOutputPort())
quad_mapper.SetScalarRange(0, quad_num_cells + 1)
quad_mapper.SetScalarModeToUseCellData()
quad_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_actor = vtkActor()
quad_actor.SetMapper(quad_mapper)
quad_actor.GetProperty().EdgeVisibilityOn()

quad_text_actor = vtkTextActor()
quad_text_actor.SetInput("Quad")
quad_text_actor.GetTextProperty().SetFontSize(16)
quad_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_text_actor.GetTextProperty().SetJustificationToCentered()
quad_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_text_actor.SetPosition(0.5, 0.01)

# --- Row 1, Col 3: Quadratic Quad — Source, Filter, Mapper, Actor ---------
quad_quad_source = vtkCellTypeSource()
quad_quad_source.SetCellType(VTK_QUADRATIC_QUAD)
quad_quad_source.Update()

quad_quad_original_points = quad_quad_source.GetOutput().GetPoints()
quad_quad_points = vtkPoints()
quad_quad_points.SetNumberOfPoints(quad_quad_source.GetOutput().GetNumberOfPoints())
quad_quad_rng = vtkMinimalStandardRandomSequence()
quad_quad_rng.SetSeed(5070)
for i in range(quad_quad_points.GetNumberOfPoints()):
    quad_quad_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_quad_rng.Next()
        quad_quad_perturbation[j] = quad_quad_rng.GetRangeValue(-0.1, 0.1)
    quad_quad_current = [0.0, 0.0, 0.0]
    quad_quad_original_points.GetPoint(i, quad_quad_current)
    quad_quad_points.SetPoint(i,
                              quad_quad_current[0] + quad_quad_perturbation[0],
                              quad_quad_current[1] + quad_quad_perturbation[1],
                              quad_quad_current[2] + quad_quad_perturbation[2])
quad_quad_source.GetOutput().SetPoints(quad_quad_points)

quad_quad_num_cells = quad_quad_source.GetOutput().GetNumberOfCells()
quad_quad_id_array = vtkIntArray()
quad_quad_id_array.SetNumberOfTuples(quad_quad_num_cells)
for i in range(quad_quad_num_cells):
    quad_quad_id_array.InsertTuple1(i, i + 1)
quad_quad_id_array.SetName("Ids")
quad_quad_source.GetOutput().GetCellData().AddArray(quad_quad_id_array)
quad_quad_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_quad_shrink = vtkShrinkFilter()
quad_quad_shrink.SetInputConnection(quad_quad_source.GetOutputPort())
quad_quad_shrink.SetShrinkFactor(0.8)

quad_quad_tessellator = vtkTessellatorFilter()
quad_quad_tessellator.SetInputConnection(quad_quad_shrink.GetOutputPort())
quad_quad_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_quad_mapper = vtkDataSetMapper()
quad_quad_mapper.SetInputConnection(quad_quad_tessellator.GetOutputPort())
quad_quad_mapper.SetScalarRange(0, quad_quad_num_cells + 1)
quad_quad_mapper.SetScalarModeToUseCellData()
quad_quad_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_quad_actor = vtkActor()
quad_quad_actor.SetMapper(quad_quad_mapper)
quad_quad_actor.GetProperty().EdgeVisibilityOn()

quad_quad_text_actor = vtkTextActor()
quad_quad_text_actor.SetInput("Quadratic Quad")
quad_quad_text_actor.GetTextProperty().SetFontSize(16)
quad_quad_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_quad_text_actor.GetTextProperty().SetJustificationToCentered()
quad_quad_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_quad_text_actor.SetPosition(0.5, 0.01)

# --- Row 2, Col 0: Tetra — Source, Filter, Mapper, Actor ------------------
tetra_source = vtkCellTypeSource()
tetra_source.SetCellType(VTK_TETRA)
tetra_source.Update()

tetra_original_points = tetra_source.GetOutput().GetPoints()
tetra_points = vtkPoints()
tetra_points.SetNumberOfPoints(tetra_source.GetOutput().GetNumberOfPoints())
tetra_rng = vtkMinimalStandardRandomSequence()
tetra_rng.SetSeed(5070)
for i in range(tetra_points.GetNumberOfPoints()):
    tetra_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        tetra_rng.Next()
        tetra_perturbation[j] = tetra_rng.GetRangeValue(-0.1, 0.1)
    tetra_current = [0.0, 0.0, 0.0]
    tetra_original_points.GetPoint(i, tetra_current)
    tetra_points.SetPoint(i,
                          tetra_current[0] + tetra_perturbation[0],
                          tetra_current[1] + tetra_perturbation[1],
                          tetra_current[2] + tetra_perturbation[2])
tetra_source.GetOutput().SetPoints(tetra_points)

tetra_num_cells = tetra_source.GetOutput().GetNumberOfCells()
tetra_id_array = vtkIntArray()
tetra_id_array.SetNumberOfTuples(tetra_num_cells)
for i in range(tetra_num_cells):
    tetra_id_array.InsertTuple1(i, i + 1)
tetra_id_array.SetName("Ids")
tetra_source.GetOutput().GetCellData().AddArray(tetra_id_array)
tetra_source.GetOutput().GetCellData().SetActiveScalars("Ids")

tetra_shrink = vtkShrinkFilter()
tetra_shrink.SetInputConnection(tetra_source.GetOutputPort())
tetra_shrink.SetShrinkFactor(0.8)

tetra_tessellator = vtkTessellatorFilter()
tetra_tessellator.SetInputConnection(tetra_shrink.GetOutputPort())
tetra_tessellator.SetMaximumNumberOfSubdivisions(3)

tetra_mapper = vtkDataSetMapper()
tetra_mapper.SetInputConnection(tetra_tessellator.GetOutputPort())
tetra_mapper.SetScalarRange(0, tetra_num_cells + 1)
tetra_mapper.SetScalarModeToUseCellData()
tetra_mapper.SetResolveCoincidentTopologyToPolygonOffset()

tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.GetProperty().EdgeVisibilityOn()
tetra_actor.RotateX(20.0)
tetra_actor.RotateY(-20.0)

tetra_text_actor = vtkTextActor()
tetra_text_actor.SetInput("Tetra")
tetra_text_actor.GetTextProperty().SetFontSize(16)
tetra_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
tetra_text_actor.GetTextProperty().SetJustificationToCentered()
tetra_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
tetra_text_actor.SetPosition(0.5, 0.01)

# --- Row 2, Col 1: Quadratic Tetra — Source, Filter, Mapper, Actor --------
quad_tetra_source = vtkCellTypeSource()
quad_tetra_source.SetCellType(VTK_QUADRATIC_TETRA)
quad_tetra_source.Update()

quad_tetra_original_points = quad_tetra_source.GetOutput().GetPoints()
quad_tetra_points = vtkPoints()
quad_tetra_points.SetNumberOfPoints(quad_tetra_source.GetOutput().GetNumberOfPoints())
quad_tetra_rng = vtkMinimalStandardRandomSequence()
quad_tetra_rng.SetSeed(5070)
for i in range(quad_tetra_points.GetNumberOfPoints()):
    quad_tetra_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_tetra_rng.Next()
        quad_tetra_perturbation[j] = quad_tetra_rng.GetRangeValue(-0.1, 0.1)
    quad_tetra_current = [0.0, 0.0, 0.0]
    quad_tetra_original_points.GetPoint(i, quad_tetra_current)
    quad_tetra_points.SetPoint(i,
                               quad_tetra_current[0] + quad_tetra_perturbation[0],
                               quad_tetra_current[1] + quad_tetra_perturbation[1],
                               quad_tetra_current[2] + quad_tetra_perturbation[2])
quad_tetra_source.GetOutput().SetPoints(quad_tetra_points)

quad_tetra_num_cells = quad_tetra_source.GetOutput().GetNumberOfCells()
quad_tetra_id_array = vtkIntArray()
quad_tetra_id_array.SetNumberOfTuples(quad_tetra_num_cells)
for i in range(quad_tetra_num_cells):
    quad_tetra_id_array.InsertTuple1(i, i + 1)
quad_tetra_id_array.SetName("Ids")
quad_tetra_source.GetOutput().GetCellData().AddArray(quad_tetra_id_array)
quad_tetra_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_tetra_shrink = vtkShrinkFilter()
quad_tetra_shrink.SetInputConnection(quad_tetra_source.GetOutputPort())
quad_tetra_shrink.SetShrinkFactor(0.8)

quad_tetra_tessellator = vtkTessellatorFilter()
quad_tetra_tessellator.SetInputConnection(quad_tetra_shrink.GetOutputPort())
quad_tetra_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_tetra_mapper = vtkDataSetMapper()
quad_tetra_mapper.SetInputConnection(quad_tetra_tessellator.GetOutputPort())
quad_tetra_mapper.SetScalarRange(0, quad_tetra_num_cells + 1)
quad_tetra_mapper.SetScalarModeToUseCellData()
quad_tetra_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_tetra_actor = vtkActor()
quad_tetra_actor.SetMapper(quad_tetra_mapper)
quad_tetra_actor.GetProperty().EdgeVisibilityOn()
quad_tetra_actor.RotateX(20.0)
quad_tetra_actor.RotateY(-20.0)

quad_tetra_text_actor = vtkTextActor()
quad_tetra_text_actor.SetInput("Quadratic Tetra")
quad_tetra_text_actor.GetTextProperty().SetFontSize(16)
quad_tetra_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_tetra_text_actor.GetTextProperty().SetJustificationToCentered()
quad_tetra_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_tetra_text_actor.SetPosition(0.5, 0.01)

# --- Row 2, Col 2: Hexahedron — Source, Filter, Mapper, Actor -------------
hex_source = vtkCellTypeSource()
hex_source.SetCellType(VTK_HEXAHEDRON)
hex_source.Update()

hex_original_points = hex_source.GetOutput().GetPoints()
hex_points = vtkPoints()
hex_points.SetNumberOfPoints(hex_source.GetOutput().GetNumberOfPoints())
hex_rng = vtkMinimalStandardRandomSequence()
hex_rng.SetSeed(5070)
for i in range(hex_points.GetNumberOfPoints()):
    hex_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        hex_rng.Next()
        hex_perturbation[j] = hex_rng.GetRangeValue(-0.1, 0.1)
    hex_current = [0.0, 0.0, 0.0]
    hex_original_points.GetPoint(i, hex_current)
    hex_points.SetPoint(i,
                        hex_current[0] + hex_perturbation[0],
                        hex_current[1] + hex_perturbation[1],
                        hex_current[2] + hex_perturbation[2])
hex_source.GetOutput().SetPoints(hex_points)

hex_num_cells = hex_source.GetOutput().GetNumberOfCells()
hex_id_array = vtkIntArray()
hex_id_array.SetNumberOfTuples(hex_num_cells)
for i in range(hex_num_cells):
    hex_id_array.InsertTuple1(i, i + 1)
hex_id_array.SetName("Ids")
hex_source.GetOutput().GetCellData().AddArray(hex_id_array)
hex_source.GetOutput().GetCellData().SetActiveScalars("Ids")

hex_shrink = vtkShrinkFilter()
hex_shrink.SetInputConnection(hex_source.GetOutputPort())
hex_shrink.SetShrinkFactor(0.8)

hex_tessellator = vtkTessellatorFilter()
hex_tessellator.SetInputConnection(hex_shrink.GetOutputPort())
hex_tessellator.SetMaximumNumberOfSubdivisions(3)

hex_mapper = vtkDataSetMapper()
hex_mapper.SetInputConnection(hex_tessellator.GetOutputPort())
hex_mapper.SetScalarRange(0, hex_num_cells + 1)
hex_mapper.SetScalarModeToUseCellData()
hex_mapper.SetResolveCoincidentTopologyToPolygonOffset()

hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)
hex_actor.GetProperty().EdgeVisibilityOn()
hex_actor.RotateX(20.0)
hex_actor.RotateY(-20.0)

hex_text_actor = vtkTextActor()
hex_text_actor.SetInput("Hexahedron")
hex_text_actor.GetTextProperty().SetFontSize(16)
hex_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
hex_text_actor.GetTextProperty().SetJustificationToCentered()
hex_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
hex_text_actor.SetPosition(0.5, 0.01)

# --- Row 2, Col 3: Quadratic Hexahedron — Source, Filter, Mapper, Actor ---
quad_hex_source = vtkCellTypeSource()
quad_hex_source.SetCellType(VTK_QUADRATIC_HEXAHEDRON)
quad_hex_source.Update()

quad_hex_original_points = quad_hex_source.GetOutput().GetPoints()
quad_hex_points = vtkPoints()
quad_hex_points.SetNumberOfPoints(quad_hex_source.GetOutput().GetNumberOfPoints())
quad_hex_rng = vtkMinimalStandardRandomSequence()
quad_hex_rng.SetSeed(5070)
for i in range(quad_hex_points.GetNumberOfPoints()):
    quad_hex_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_hex_rng.Next()
        quad_hex_perturbation[j] = quad_hex_rng.GetRangeValue(-0.1, 0.1)
    quad_hex_current = [0.0, 0.0, 0.0]
    quad_hex_original_points.GetPoint(i, quad_hex_current)
    quad_hex_points.SetPoint(i,
                             quad_hex_current[0] + quad_hex_perturbation[0],
                             quad_hex_current[1] + quad_hex_perturbation[1],
                             quad_hex_current[2] + quad_hex_perturbation[2])
quad_hex_source.GetOutput().SetPoints(quad_hex_points)

quad_hex_num_cells = quad_hex_source.GetOutput().GetNumberOfCells()
quad_hex_id_array = vtkIntArray()
quad_hex_id_array.SetNumberOfTuples(quad_hex_num_cells)
for i in range(quad_hex_num_cells):
    quad_hex_id_array.InsertTuple1(i, i + 1)
quad_hex_id_array.SetName("Ids")
quad_hex_source.GetOutput().GetCellData().AddArray(quad_hex_id_array)
quad_hex_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_hex_shrink = vtkShrinkFilter()
quad_hex_shrink.SetInputConnection(quad_hex_source.GetOutputPort())
quad_hex_shrink.SetShrinkFactor(0.8)

quad_hex_tessellator = vtkTessellatorFilter()
quad_hex_tessellator.SetInputConnection(quad_hex_shrink.GetOutputPort())
quad_hex_tessellator.SetMaximumNumberOfSubdivisions(3)

quad_hex_mapper = vtkDataSetMapper()
quad_hex_mapper.SetInputConnection(quad_hex_tessellator.GetOutputPort())
quad_hex_mapper.SetScalarRange(0, quad_hex_num_cells + 1)
quad_hex_mapper.SetScalarModeToUseCellData()
quad_hex_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_hex_actor = vtkActor()
quad_hex_actor.SetMapper(quad_hex_mapper)
quad_hex_actor.GetProperty().EdgeVisibilityOn()
quad_hex_actor.RotateX(20.0)
quad_hex_actor.RotateY(-20.0)

quad_hex_text_actor = vtkTextActor()
quad_hex_text_actor.SetInput("Quadratic Hexahedron")
quad_hex_text_actor.GetTextProperty().SetFontSize(16)
quad_hex_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_hex_text_actor.GetTextProperty().SetJustificationToCentered()
quad_hex_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_hex_text_actor.SetPosition(0.5, 0.01)

# --- Row 3, Col 0: Wedge — Source, Filter, Mapper, Actor ------------------
wedge_source = vtkCellTypeSource()
wedge_source.SetCellType(VTK_WEDGE)
wedge_source.Update()

wedge_original_points = wedge_source.GetOutput().GetPoints()
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(wedge_source.GetOutput().GetNumberOfPoints())
wedge_rng = vtkMinimalStandardRandomSequence()
wedge_rng.SetSeed(5070)
for i in range(wedge_points.GetNumberOfPoints()):
    wedge_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        wedge_rng.Next()
        wedge_perturbation[j] = wedge_rng.GetRangeValue(-0.1, 0.1)
    wedge_current = [0.0, 0.0, 0.0]
    wedge_original_points.GetPoint(i, wedge_current)
    wedge_points.SetPoint(i,
                          wedge_current[0] + wedge_perturbation[0],
                          wedge_current[1] + wedge_perturbation[1],
                          wedge_current[2] + wedge_perturbation[2])
wedge_source.GetOutput().SetPoints(wedge_points)

wedge_num_cells = wedge_source.GetOutput().GetNumberOfCells()
wedge_id_array = vtkIntArray()
wedge_id_array.SetNumberOfTuples(wedge_num_cells)
for i in range(wedge_num_cells):
    wedge_id_array.InsertTuple1(i, i + 1)
wedge_id_array.SetName("Ids")
wedge_source.GetOutput().GetCellData().AddArray(wedge_id_array)
wedge_source.GetOutput().GetCellData().SetActiveScalars("Ids")

wedge_shrink = vtkShrinkFilter()
wedge_shrink.SetInputConnection(wedge_source.GetOutputPort())
wedge_shrink.SetShrinkFactor(0.8)

wedge_tessellator = vtkTessellatorFilter()
wedge_tessellator.SetInputConnection(wedge_shrink.GetOutputPort())
wedge_tessellator.SetMaximumNumberOfSubdivisions(3)

wedge_mapper = vtkDataSetMapper()
wedge_mapper.SetInputConnection(wedge_tessellator.GetOutputPort())
wedge_mapper.SetScalarRange(0, wedge_num_cells + 1)
wedge_mapper.SetScalarModeToUseCellData()
wedge_mapper.SetResolveCoincidentTopologyToPolygonOffset()

wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)
wedge_actor.GetProperty().EdgeVisibilityOn()
wedge_actor.RotateX(20.0)
wedge_actor.RotateY(-20.0)

wedge_text_actor = vtkTextActor()
wedge_text_actor.SetInput("Wedge")
wedge_text_actor.GetTextProperty().SetFontSize(16)
wedge_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
wedge_text_actor.GetTextProperty().SetJustificationToCentered()
wedge_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
wedge_text_actor.SetPosition(0.5, 0.01)

# --- Row 3, Col 1: Quadratic Wedge — Source, Filter, Mapper, Actor --------
# Note: tessellation disabled for this cell type
quad_wedge_source = vtkCellTypeSource()
quad_wedge_source.SetCellType(VTK_QUADRATIC_WEDGE)
quad_wedge_source.Update()

quad_wedge_original_points = quad_wedge_source.GetOutput().GetPoints()
quad_wedge_points = vtkPoints()
quad_wedge_points.SetNumberOfPoints(quad_wedge_source.GetOutput().GetNumberOfPoints())
quad_wedge_rng = vtkMinimalStandardRandomSequence()
quad_wedge_rng.SetSeed(5070)
for i in range(quad_wedge_points.GetNumberOfPoints()):
    quad_wedge_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_wedge_rng.Next()
        quad_wedge_perturbation[j] = quad_wedge_rng.GetRangeValue(-0.1, 0.1)
    quad_wedge_current = [0.0, 0.0, 0.0]
    quad_wedge_original_points.GetPoint(i, quad_wedge_current)
    quad_wedge_points.SetPoint(i,
                               quad_wedge_current[0] + quad_wedge_perturbation[0],
                               quad_wedge_current[1] + quad_wedge_perturbation[1],
                               quad_wedge_current[2] + quad_wedge_perturbation[2])
quad_wedge_source.GetOutput().SetPoints(quad_wedge_points)

quad_wedge_num_cells = quad_wedge_source.GetOutput().GetNumberOfCells()
quad_wedge_id_array = vtkIntArray()
quad_wedge_id_array.SetNumberOfTuples(quad_wedge_num_cells)
for i in range(quad_wedge_num_cells):
    quad_wedge_id_array.InsertTuple1(i, i + 1)
quad_wedge_id_array.SetName("Ids")
quad_wedge_source.GetOutput().GetCellData().AddArray(quad_wedge_id_array)
quad_wedge_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_wedge_shrink = vtkShrinkFilter()
quad_wedge_shrink.SetInputConnection(quad_wedge_source.GetOutputPort())
quad_wedge_shrink.SetShrinkFactor(0.8)

quad_wedge_mapper = vtkDataSetMapper()
quad_wedge_mapper.SetInputConnection(quad_wedge_shrink.GetOutputPort())
quad_wedge_mapper.SetScalarRange(0, quad_wedge_num_cells + 1)
quad_wedge_mapper.SetScalarModeToUseCellData()
quad_wedge_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_wedge_actor = vtkActor()
quad_wedge_actor.SetMapper(quad_wedge_mapper)
quad_wedge_actor.GetProperty().EdgeVisibilityOn()
quad_wedge_actor.RotateX(20.0)
quad_wedge_actor.RotateY(-20.0)

quad_wedge_text_actor = vtkTextActor()
quad_wedge_text_actor.SetInput("Quadratic Wedge")
quad_wedge_text_actor.GetTextProperty().SetFontSize(16)
quad_wedge_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_wedge_text_actor.GetTextProperty().SetJustificationToCentered()
quad_wedge_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_wedge_text_actor.SetPosition(0.5, 0.01)

# --- Row 3, Col 2: Pyramid — Source, Filter, Mapper, Actor ----------------
pyramid_source = vtkCellTypeSource()
pyramid_source.SetCellType(VTK_PYRAMID)
pyramid_source.Update()

pyramid_original_points = pyramid_source.GetOutput().GetPoints()
pyramid_points = vtkPoints()
pyramid_points.SetNumberOfPoints(pyramid_source.GetOutput().GetNumberOfPoints())
pyramid_rng = vtkMinimalStandardRandomSequence()
pyramid_rng.SetSeed(5070)
for i in range(pyramid_points.GetNumberOfPoints()):
    pyramid_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        pyramid_rng.Next()
        pyramid_perturbation[j] = pyramid_rng.GetRangeValue(-0.1, 0.1)
    pyramid_current = [0.0, 0.0, 0.0]
    pyramid_original_points.GetPoint(i, pyramid_current)
    pyramid_points.SetPoint(i,
                            pyramid_current[0] + pyramid_perturbation[0],
                            pyramid_current[1] + pyramid_perturbation[1],
                            pyramid_current[2] + pyramid_perturbation[2])
pyramid_source.GetOutput().SetPoints(pyramid_points)

pyramid_num_cells = pyramid_source.GetOutput().GetNumberOfCells()
pyramid_id_array = vtkIntArray()
pyramid_id_array.SetNumberOfTuples(pyramid_num_cells)
for i in range(pyramid_num_cells):
    pyramid_id_array.InsertTuple1(i, i + 1)
pyramid_id_array.SetName("Ids")
pyramid_source.GetOutput().GetCellData().AddArray(pyramid_id_array)
pyramid_source.GetOutput().GetCellData().SetActiveScalars("Ids")

pyramid_shrink = vtkShrinkFilter()
pyramid_shrink.SetInputConnection(pyramid_source.GetOutputPort())
pyramid_shrink.SetShrinkFactor(0.8)

pyramid_tessellator = vtkTessellatorFilter()
pyramid_tessellator.SetInputConnection(pyramid_shrink.GetOutputPort())
pyramid_tessellator.SetMaximumNumberOfSubdivisions(3)

pyramid_mapper = vtkDataSetMapper()
pyramid_mapper.SetInputConnection(pyramid_tessellator.GetOutputPort())
pyramid_mapper.SetScalarRange(0, pyramid_num_cells + 1)
pyramid_mapper.SetScalarModeToUseCellData()
pyramid_mapper.SetResolveCoincidentTopologyToPolygonOffset()

pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)
pyramid_actor.GetProperty().EdgeVisibilityOn()
pyramid_actor.RotateX(20.0)
pyramid_actor.RotateY(-20.0)

pyramid_text_actor = vtkTextActor()
pyramid_text_actor.SetInput("Pyramid")
pyramid_text_actor.GetTextProperty().SetFontSize(16)
pyramid_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
pyramid_text_actor.GetTextProperty().SetJustificationToCentered()
pyramid_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pyramid_text_actor.SetPosition(0.5, 0.01)

# --- Row 3, Col 3: Quadratic Pyramid — Source, Filter, Mapper, Actor ------
# Note: tessellation disabled for this cell type
quad_pyramid_source = vtkCellTypeSource()
quad_pyramid_source.SetCellType(VTK_QUADRATIC_PYRAMID)
quad_pyramid_source.Update()

quad_pyramid_original_points = quad_pyramid_source.GetOutput().GetPoints()
quad_pyramid_points = vtkPoints()
quad_pyramid_points.SetNumberOfPoints(quad_pyramid_source.GetOutput().GetNumberOfPoints())
quad_pyramid_rng = vtkMinimalStandardRandomSequence()
quad_pyramid_rng.SetSeed(5070)
for i in range(quad_pyramid_points.GetNumberOfPoints()):
    quad_pyramid_perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        quad_pyramid_rng.Next()
        quad_pyramid_perturbation[j] = quad_pyramid_rng.GetRangeValue(-0.1, 0.1)
    quad_pyramid_current = [0.0, 0.0, 0.0]
    quad_pyramid_original_points.GetPoint(i, quad_pyramid_current)
    quad_pyramid_points.SetPoint(i,
                                 quad_pyramid_current[0] + quad_pyramid_perturbation[0],
                                 quad_pyramid_current[1] + quad_pyramid_perturbation[1],
                                 quad_pyramid_current[2] + quad_pyramid_perturbation[2])
quad_pyramid_source.GetOutput().SetPoints(quad_pyramid_points)

quad_pyramid_num_cells = quad_pyramid_source.GetOutput().GetNumberOfCells()
quad_pyramid_id_array = vtkIntArray()
quad_pyramid_id_array.SetNumberOfTuples(quad_pyramid_num_cells)
for i in range(quad_pyramid_num_cells):
    quad_pyramid_id_array.InsertTuple1(i, i + 1)
quad_pyramid_id_array.SetName("Ids")
quad_pyramid_source.GetOutput().GetCellData().AddArray(quad_pyramid_id_array)
quad_pyramid_source.GetOutput().GetCellData().SetActiveScalars("Ids")

quad_pyramid_shrink = vtkShrinkFilter()
quad_pyramid_shrink.SetInputConnection(quad_pyramid_source.GetOutputPort())
quad_pyramid_shrink.SetShrinkFactor(0.8)

quad_pyramid_mapper = vtkDataSetMapper()
quad_pyramid_mapper.SetInputConnection(quad_pyramid_shrink.GetOutputPort())
quad_pyramid_mapper.SetScalarRange(0, quad_pyramid_num_cells + 1)
quad_pyramid_mapper.SetScalarModeToUseCellData()
quad_pyramid_mapper.SetResolveCoincidentTopologyToPolygonOffset()

quad_pyramid_actor = vtkActor()
quad_pyramid_actor.SetMapper(quad_pyramid_mapper)
quad_pyramid_actor.GetProperty().EdgeVisibilityOn()
quad_pyramid_actor.RotateX(20.0)
quad_pyramid_actor.RotateY(-20.0)

quad_pyramid_text_actor = vtkTextActor()
quad_pyramid_text_actor.SetInput("Quadratic Pyramid")
quad_pyramid_text_actor.GetTextProperty().SetFontSize(16)
quad_pyramid_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
quad_pyramid_text_actor.GetTextProperty().SetJustificationToCentered()
quad_pyramid_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_pyramid_text_actor.SetPosition(0.5, 0.01)

# --- Renderers: one per viewport ------------------------------------------
line_renderer = vtkRenderer()
line_renderer.AddActor(line_actor)
line_renderer.AddViewProp(line_text_actor)
line_renderer.SetBackground(dark_blue_background_rgb)
line_renderer.SetViewport(0.0, 0.75, 0.25, 1.0)

quad_edge_renderer = vtkRenderer()
quad_edge_renderer.AddActor(quad_edge_actor)
quad_edge_renderer.AddViewProp(quad_edge_text_actor)
quad_edge_renderer.SetBackground(dark_blue_background_rgb)
quad_edge_renderer.SetViewport(0.25, 0.75, 0.5, 1.0)

cubic_line_renderer = vtkRenderer()
cubic_line_renderer.AddActor(cubic_line_actor)
cubic_line_renderer.AddViewProp(cubic_line_text_actor)
cubic_line_renderer.SetBackground(dark_blue_background_rgb)
cubic_line_renderer.SetViewport(0.5, 0.75, 0.75, 1.0)

triangle_renderer = vtkRenderer()
triangle_renderer.AddActor(triangle_actor)
triangle_renderer.AddViewProp(triangle_text_actor)
triangle_renderer.SetBackground(dark_blue_background_rgb)
triangle_renderer.SetViewport(0.0, 0.5, 0.25, 0.75)

quad_tri_renderer = vtkRenderer()
quad_tri_renderer.AddActor(quad_tri_actor)
quad_tri_renderer.AddViewProp(quad_tri_text_actor)
quad_tri_renderer.SetBackground(dark_blue_background_rgb)
quad_tri_renderer.SetViewport(0.25, 0.5, 0.5, 0.75)

quad_renderer = vtkRenderer()
quad_renderer.AddActor(quad_actor)
quad_renderer.AddViewProp(quad_text_actor)
quad_renderer.SetBackground(dark_blue_background_rgb)
quad_renderer.SetViewport(0.5, 0.5, 0.75, 0.75)

quad_quad_renderer = vtkRenderer()
quad_quad_renderer.AddActor(quad_quad_actor)
quad_quad_renderer.AddViewProp(quad_quad_text_actor)
quad_quad_renderer.SetBackground(dark_blue_background_rgb)
quad_quad_renderer.SetViewport(0.75, 0.5, 1.0, 0.75)

tetra_renderer = vtkRenderer()
tetra_renderer.AddActor(tetra_actor)
tetra_renderer.AddViewProp(tetra_text_actor)
tetra_renderer.SetBackground(dark_blue_background_rgb)
tetra_renderer.SetViewport(0.0, 0.25, 0.25, 0.5)

quad_tetra_renderer = vtkRenderer()
quad_tetra_renderer.AddActor(quad_tetra_actor)
quad_tetra_renderer.AddViewProp(quad_tetra_text_actor)
quad_tetra_renderer.SetBackground(dark_blue_background_rgb)
quad_tetra_renderer.SetViewport(0.25, 0.25, 0.5, 0.5)

hex_renderer = vtkRenderer()
hex_renderer.AddActor(hex_actor)
hex_renderer.AddViewProp(hex_text_actor)
hex_renderer.SetBackground(dark_blue_background_rgb)
hex_renderer.SetViewport(0.5, 0.25, 0.75, 0.5)

quad_hex_renderer = vtkRenderer()
quad_hex_renderer.AddActor(quad_hex_actor)
quad_hex_renderer.AddViewProp(quad_hex_text_actor)
quad_hex_renderer.SetBackground(dark_blue_background_rgb)
quad_hex_renderer.SetViewport(0.75, 0.25, 1.0, 0.5)

wedge_renderer = vtkRenderer()
wedge_renderer.AddActor(wedge_actor)
wedge_renderer.AddViewProp(wedge_text_actor)
wedge_renderer.SetBackground(dark_blue_background_rgb)
wedge_renderer.SetViewport(0.0, 0.0, 0.25, 0.25)

quad_wedge_renderer = vtkRenderer()
quad_wedge_renderer.AddActor(quad_wedge_actor)
quad_wedge_renderer.AddViewProp(quad_wedge_text_actor)
quad_wedge_renderer.SetBackground(dark_blue_background_rgb)
quad_wedge_renderer.SetViewport(0.25, 0.0, 0.5, 0.25)

pyramid_renderer = vtkRenderer()
pyramid_renderer.AddActor(pyramid_actor)
pyramid_renderer.AddViewProp(pyramid_text_actor)
pyramid_renderer.SetBackground(dark_blue_background_rgb)
pyramid_renderer.SetViewport(0.5, 0.0, 0.75, 0.25)

quad_pyramid_renderer = vtkRenderer()
quad_pyramid_renderer.AddActor(quad_pyramid_actor)
quad_pyramid_renderer.AddViewProp(quad_pyramid_text_actor)
quad_pyramid_renderer.SetBackground(dark_blue_background_rgb)
quad_pyramid_renderer.SetViewport(0.75, 0.0, 1.0, 0.25)

empty_renderer = vtkRenderer()
empty_renderer.SetBackground(dark_blue_background_rgb)
empty_renderer.SetViewport(0.75, 0.75, 1.0, 1.0)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(line_renderer)
render_window.AddRenderer(quad_edge_renderer)
render_window.AddRenderer(cubic_line_renderer)
render_window.AddRenderer(triangle_renderer)
render_window.AddRenderer(quad_tri_renderer)
render_window.AddRenderer(quad_renderer)
render_window.AddRenderer(quad_quad_renderer)
render_window.AddRenderer(tetra_renderer)
render_window.AddRenderer(quad_tetra_renderer)
render_window.AddRenderer(hex_renderer)
render_window.AddRenderer(quad_hex_renderer)
render_window.AddRenderer(wedge_renderer)
render_window.AddRenderer(quad_wedge_renderer)
render_window.AddRenderer(pyramid_renderer)
render_window.AddRenderer(quad_pyramid_renderer)
render_window.AddRenderer(empty_renderer)
render_window.SetWindowName("celltype demo")
render_window.SetMultiSamples(0)
render_window.SetSize(1200, 900)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure cameras for each viewport
line_renderer.ResetCamera()
line_renderer.GetActiveCamera().Zoom(1.3)
quad_edge_renderer.ResetCamera()
quad_edge_renderer.GetActiveCamera().Zoom(1.3)
cubic_line_renderer.ResetCamera()
cubic_line_renderer.GetActiveCamera().Zoom(1.3)
triangle_renderer.ResetCamera()
triangle_renderer.GetActiveCamera().Zoom(1.3)
quad_tri_renderer.ResetCamera()
quad_tri_renderer.GetActiveCamera().Zoom(1.3)
quad_renderer.ResetCamera()
quad_renderer.GetActiveCamera().Zoom(1.3)
quad_quad_renderer.ResetCamera()
quad_quad_renderer.GetActiveCamera().Zoom(1.3)
tetra_renderer.ResetCamera()
tetra_renderer.GetActiveCamera().Zoom(1.3)
quad_tetra_renderer.ResetCamera()
quad_tetra_renderer.GetActiveCamera().Zoom(1.3)
hex_renderer.ResetCamera()
hex_renderer.GetActiveCamera().Zoom(1.3)
quad_hex_renderer.ResetCamera()
quad_hex_renderer.GetActiveCamera().Zoom(1.3)
wedge_renderer.ResetCamera()
wedge_renderer.GetActiveCamera().Zoom(1.3)
quad_wedge_renderer.ResetCamera()
quad_wedge_renderer.GetActiveCamera().Zoom(1.3)
pyramid_renderer.ResetCamera()
pyramid_renderer.GetActiveCamera().Zoom(1.3)
quad_pyramid_renderer.ResetCamera()
quad_pyramid_renderer.GetActiveCamera().Zoom(1.3)

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
