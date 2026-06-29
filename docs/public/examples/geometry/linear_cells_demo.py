#!/usr/bin/env python

# Display sixteen linear cell types in a 4 × 4 grid of viewports, each
# with its own renderer.  Each cell shows vertex-ordering labels and gold
# sphere glyphs at the vertices.  Three-dimensional cells are rotated and
# sit on a translucent plinth.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkHexagonalPrism,
    vtkHexahedron,
    vtkLine,
    vtkPentagonalPrism,
    vtkPixel,
    vtkPolyLine,
    vtkPolyVertex,
    vtkPolygon,
    vtkPyramid,
    vtkQuad,
    vtkTetra,
    vtkTriangle,
    vtkTriangleStrip,
    vtkUnstructuredGrid,
    vtkVertex,
    vtkVoxel,
    vtkWedge,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Colors (normalized RGB)
dark_salmon_rgb = (0.914, 0.588, 0.478)
seashell_rgb = (1.0, 0.961, 0.933)
gold_rgb = (1.0, 0.843, 0.0)
yellow_rgb = (1.0, 1.0, 0.0)
steel_blue_rgb = (0.275, 0.510, 0.706)
light_steel_blue_rgb = (0.690, 0.769, 0.871)
deep_pink_rgb = (1.0, 0.078, 0.576)
background_rgb = (0.690, 0.769, 0.871)

# Viewport grid: 4 columns × 4 rows
num_cols = 4
num_rows = 4

# Shared sphere source for vertex glyphs
sphere = vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)
sphere.SetRadius(0.04)

# ---------------------------------------------------------------------------
# Cell 0: Vertex (row 0, col 0) — 2D surface
# ---------------------------------------------------------------------------
vertex_points = vtkPoints()
vertex_points.InsertNextPoint(0, 0, 0)
vertex_cell = vtkVertex()
vertex_cell.GetPointIds().SetId(0, 0)
vertex_grid = vtkUnstructuredGrid()
vertex_grid.SetPoints(vertex_points)
vertex_grid.InsertNextCell(vertex_cell.GetCellType(), vertex_cell.GetPointIds())

# Center
vertex_bounds = vertex_grid.GetBounds()
vertex_pts = vertex_grid.GetPoints()
vertex_new_pts = vtkPoints()
vertex_new_pts.SetNumberOfPoints(vertex_pts.GetNumberOfPoints())
for i in range(vertex_pts.GetNumberOfPoints()):
    px, py, pz = vertex_pts.GetPoint(i)
    vertex_new_pts.SetPoint(i, px - (vertex_bounds[0] + vertex_bounds[1]) / 2.0,
                            py - (vertex_bounds[2] + vertex_bounds[3]) / 2.0,
                            pz - (vertex_bounds[4] + vertex_bounds[5]) / 2.0)
vertex_grid.SetPoints(vertex_new_pts)

vertex_surface_property = vtkProperty()
vertex_surface_property.SetAmbientColor(dark_salmon_rgb)
vertex_surface_property.SetDiffuseColor(seashell_rgb)
vertex_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
vertex_surface_property.SetSpecular(0.5)
vertex_surface_property.SetDiffuse(0.7)
vertex_surface_property.SetAmbient(0.5)
vertex_surface_property.SetSpecularPower(20.0)
vertex_surface_property.SetOpacity(0.9)
vertex_surface_property.EdgeVisibilityOn()
vertex_surface_property.SetLineWidth(3)

vertex_mapper = vtkDataSetMapper()
vertex_mapper.SetInputData(vertex_grid)
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.SetProperty(vertex_surface_property)

vertex_label_text_property = vtkTextProperty()
vertex_label_text_property.BoldOn()
vertex_label_text_property.ShadowOn()
vertex_label_text_property.SetJustificationToCentered()
vertex_label_text_property.SetColor(deep_pink_rgb)
vertex_label_text_property.SetFontSize(14)
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputData(vertex_grid)
vertex_label_mapper.SetLabelTextProperty(vertex_label_text_property)
vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

vertex_glyph_property = vtkProperty()
vertex_glyph_property.SetAmbientColor(gold_rgb)
vertex_glyph_property.SetDiffuseColor(yellow_rgb)
vertex_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
vertex_glyph_property.SetSpecular(0.5)
vertex_glyph_property.SetDiffuse(0.7)
vertex_glyph_property.SetAmbient(0.5)
vertex_glyph_property.SetSpecularPower(20.0)
vertex_glyph_property.SetOpacity(1.0)
vertex_glyph_mapper = vtkGlyph3DMapper()
vertex_glyph_mapper.SetInputData(vertex_grid)
vertex_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
vertex_glyph_mapper.ScalingOn()
vertex_glyph_mapper.ScalarVisibilityOff()
vertex_glyph_actor = vtkActor()
vertex_glyph_actor.SetMapper(vertex_glyph_mapper)
vertex_glyph_actor.SetProperty(vertex_glyph_property)

vertex_text_actor = vtkTextActor()
vertex_text_actor.SetInput("Vertex")
vertex_text_actor.GetTextProperty().SetFontSize(12)
vertex_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
vertex_text_actor.GetTextProperty().SetJustificationToCentered()
vertex_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
vertex_text_actor.SetPosition(0.5, 0.01)

vertex_renderer = vtkRenderer()
vertex_renderer.AddActor(vertex_actor)
vertex_renderer.AddActor(vertex_label_actor)
vertex_renderer.AddActor(vertex_glyph_actor)
vertex_renderer.AddViewProp(vertex_text_actor)
vertex_renderer.SetBackground(background_rgb)
vertex_renderer.SetViewport(0 / num_cols, 3 / num_rows, 1 / num_cols, 4 / num_rows)

# ---------------------------------------------------------------------------
# Cell 1: Poly Vertex (row 0, col 1) — 3D surface
# ---------------------------------------------------------------------------
sf_pv = 1.5
poly_vertex_points = vtkPoints()
poly_vertex_points.InsertNextPoint(0 / sf_pv, 0 / sf_pv, 0 / sf_pv)
poly_vertex_points.InsertNextPoint(1 / sf_pv, 0 / sf_pv, 0 / sf_pv)
poly_vertex_points.InsertNextPoint(0 / sf_pv, 1 / sf_pv, 0 / sf_pv)
poly_vertex_points.InsertNextPoint(0 / sf_pv, 0 / sf_pv, 1 / sf_pv)
poly_vertex_points.InsertNextPoint(1 / sf_pv, 0 / sf_pv, 0.4 / sf_pv)
poly_vertex_points.InsertNextPoint(0 / sf_pv, 1 / sf_pv, 0.6 / sf_pv)
poly_vertex_cell = vtkPolyVertex()
poly_vertex_cell.GetPointIds().SetNumberOfIds(6)
for i in range(6):
    poly_vertex_cell.GetPointIds().SetId(i, i)
poly_vertex_grid = vtkUnstructuredGrid()
poly_vertex_grid.SetPoints(poly_vertex_points)
poly_vertex_grid.InsertNextCell(poly_vertex_cell.GetCellType(), poly_vertex_cell.GetPointIds())

# 3D rotation
poly_vertex_rot = vtkTransform()
poly_vertex_rot.RotateX(-20)
poly_vertex_rot.RotateY(20)
poly_vertex_rtf = vtkTransformFilter()
poly_vertex_rtf.SetTransform(poly_vertex_rot)
poly_vertex_rtf.SetInputData(poly_vertex_grid)
poly_vertex_rtf.Update()
poly_vertex_grid.SetPoints(poly_vertex_rtf.GetOutput().GetPoints())

# Center
poly_vertex_bounds = poly_vertex_grid.GetBounds()
poly_vertex_pts = poly_vertex_grid.GetPoints()
poly_vertex_new_pts = vtkPoints()
poly_vertex_new_pts.SetNumberOfPoints(poly_vertex_pts.GetNumberOfPoints())
for i in range(poly_vertex_pts.GetNumberOfPoints()):
    px, py, pz = poly_vertex_pts.GetPoint(i)
    poly_vertex_new_pts.SetPoint(i, px - (poly_vertex_bounds[0] + poly_vertex_bounds[1]) / 2.0,
                                 py - (poly_vertex_bounds[2] + poly_vertex_bounds[3]) / 2.0,
                                 pz - (poly_vertex_bounds[4] + poly_vertex_bounds[5]) / 2.0)
poly_vertex_grid.SetPoints(poly_vertex_new_pts)

poly_vertex_surface_property = vtkProperty()
poly_vertex_surface_property.SetAmbientColor(dark_salmon_rgb)
poly_vertex_surface_property.SetDiffuseColor(seashell_rgb)
poly_vertex_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
poly_vertex_surface_property.SetSpecular(0.5)
poly_vertex_surface_property.SetDiffuse(0.7)
poly_vertex_surface_property.SetAmbient(0.5)
poly_vertex_surface_property.SetSpecularPower(20.0)
poly_vertex_surface_property.SetOpacity(0.9)
poly_vertex_surface_property.EdgeVisibilityOn()
poly_vertex_surface_property.SetLineWidth(3)

poly_vertex_mapper = vtkDataSetMapper()
poly_vertex_mapper.SetInputData(poly_vertex_grid)
poly_vertex_actor = vtkActor()
poly_vertex_actor.SetMapper(poly_vertex_mapper)
poly_vertex_actor.SetProperty(poly_vertex_surface_property)

poly_vertex_label_text_property = vtkTextProperty()
poly_vertex_label_text_property.BoldOn()
poly_vertex_label_text_property.ShadowOn()
poly_vertex_label_text_property.SetJustificationToCentered()
poly_vertex_label_text_property.SetColor(deep_pink_rgb)
poly_vertex_label_text_property.SetFontSize(14)
poly_vertex_label_mapper = vtkLabeledDataMapper()
poly_vertex_label_mapper.SetInputData(poly_vertex_grid)
poly_vertex_label_mapper.SetLabelTextProperty(poly_vertex_label_text_property)
poly_vertex_label_actor = vtkActor2D()
poly_vertex_label_actor.SetMapper(poly_vertex_label_mapper)

poly_vertex_glyph_property = vtkProperty()
poly_vertex_glyph_property.SetAmbientColor(gold_rgb)
poly_vertex_glyph_property.SetDiffuseColor(yellow_rgb)
poly_vertex_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
poly_vertex_glyph_property.SetSpecular(0.5)
poly_vertex_glyph_property.SetDiffuse(0.7)
poly_vertex_glyph_property.SetAmbient(0.5)
poly_vertex_glyph_property.SetSpecularPower(20.0)
poly_vertex_glyph_property.SetOpacity(1.0)
poly_vertex_glyph_mapper = vtkGlyph3DMapper()
poly_vertex_glyph_mapper.SetInputData(poly_vertex_grid)
poly_vertex_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
poly_vertex_glyph_mapper.ScalingOn()
poly_vertex_glyph_mapper.ScalarVisibilityOff()
poly_vertex_glyph_actor = vtkActor()
poly_vertex_glyph_actor.SetMapper(poly_vertex_glyph_mapper)
poly_vertex_glyph_actor.SetProperty(poly_vertex_glyph_property)

# Plinth for poly vertex (3D cell)
poly_vertex_nb = poly_vertex_grid.GetBounds()
poly_vertex_nd = (poly_vertex_nb[1] - poly_vertex_nb[0], poly_vertex_nb[3] - poly_vertex_nb[2], poly_vertex_nb[5] - poly_vertex_nb[4])
poly_vertex_thick = poly_vertex_nd[2] * 0.01
poly_vertex_plinth_source = vtkCubeSource()
poly_vertex_plinth_source.SetCenter((poly_vertex_nb[1] + poly_vertex_nb[0]) / 2.0,
                                    poly_vertex_nb[2] - poly_vertex_thick / 2.0 - 0.05,
                                    (poly_vertex_nb[5] + poly_vertex_nb[4]) / 2.0)
poly_vertex_plinth_source.SetXLength(poly_vertex_nd[0] + poly_vertex_nd[0] * 0.5)
poly_vertex_plinth_source.SetYLength(poly_vertex_thick)
poly_vertex_plinth_source.SetZLength(poly_vertex_nd[2] + poly_vertex_nd[2] * 0.5)
poly_vertex_plinth_property = vtkProperty()
poly_vertex_plinth_property.SetAmbientColor(steel_blue_rgb)
poly_vertex_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
poly_vertex_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
poly_vertex_plinth_property.SetSpecular(0.5)
poly_vertex_plinth_property.SetDiffuse(0.7)
poly_vertex_plinth_property.SetAmbient(0.5)
poly_vertex_plinth_property.SetSpecularPower(20.0)
poly_vertex_plinth_property.SetOpacity(0.8)
poly_vertex_plinth_property.EdgeVisibilityOn()
poly_vertex_plinth_property.SetLineWidth(1)
poly_vertex_plinth_mapper = vtkPolyDataMapper()
poly_vertex_plinth_mapper.SetInputConnection(poly_vertex_plinth_source.GetOutputPort())
poly_vertex_plinth_actor = vtkActor()
poly_vertex_plinth_actor.SetMapper(poly_vertex_plinth_mapper)
poly_vertex_plinth_actor.SetProperty(poly_vertex_plinth_property)

poly_vertex_text_actor = vtkTextActor()
poly_vertex_text_actor.SetInput("Poly Vertex")
poly_vertex_text_actor.GetTextProperty().SetFontSize(12)
poly_vertex_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
poly_vertex_text_actor.GetTextProperty().SetJustificationToCentered()
poly_vertex_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
poly_vertex_text_actor.SetPosition(0.5, 0.01)

poly_vertex_renderer = vtkRenderer()
poly_vertex_renderer.AddActor(poly_vertex_actor)
poly_vertex_renderer.AddActor(poly_vertex_label_actor)
poly_vertex_renderer.AddActor(poly_vertex_glyph_actor)
poly_vertex_renderer.AddActor(poly_vertex_plinth_actor)
poly_vertex_renderer.AddViewProp(poly_vertex_text_actor)
poly_vertex_renderer.SetBackground(background_rgb)
poly_vertex_renderer.SetViewport(1 / num_cols, 3 / num_rows, 2 / num_cols, 4 / num_rows)

# ---------------------------------------------------------------------------
# Cell 2: Line (row 0, col 2) — 2D wireframe
# ---------------------------------------------------------------------------
line_cell_points = vtkPoints()
line_cell_points.InsertNextPoint(0, 0, 0)
line_cell_points.InsertNextPoint(0.5, 0.5, 0)
line_cell_cell = vtkLine()
line_cell_cell.GetPointIds().SetId(0, 0)
line_cell_cell.GetPointIds().SetId(1, 1)
line_cell_grid = vtkUnstructuredGrid()
line_cell_grid.SetPoints(line_cell_points)
line_cell_grid.InsertNextCell(line_cell_cell.GetCellType(), line_cell_cell.GetPointIds())

# Center
line_cell_bounds = line_cell_grid.GetBounds()
line_cell_pts = line_cell_grid.GetPoints()
line_cell_new_pts = vtkPoints()
line_cell_new_pts.SetNumberOfPoints(line_cell_pts.GetNumberOfPoints())
for i in range(line_cell_pts.GetNumberOfPoints()):
    px, py, pz = line_cell_pts.GetPoint(i)
    line_cell_new_pts.SetPoint(i, px - (line_cell_bounds[0] + line_cell_bounds[1]) / 2.0,
                               py - (line_cell_bounds[2] + line_cell_bounds[3]) / 2.0,
                               pz - (line_cell_bounds[4] + line_cell_bounds[5]) / 2.0)
line_cell_grid.SetPoints(line_cell_new_pts)

line_cell_wireframe_property = vtkProperty()
line_cell_wireframe_property.SetRepresentationToWireframe()
line_cell_wireframe_property.SetLineWidth(2)
line_cell_wireframe_property.SetOpacity(1)
line_cell_wireframe_property.SetColor(0.0, 0.0, 0.0)

line_cell_mapper = vtkDataSetMapper()
line_cell_mapper.SetInputData(line_cell_grid)
line_cell_actor = vtkActor()
line_cell_actor.SetMapper(line_cell_mapper)
line_cell_actor.SetProperty(line_cell_wireframe_property)

line_cell_label_text_property = vtkTextProperty()
line_cell_label_text_property.BoldOn()
line_cell_label_text_property.ShadowOn()
line_cell_label_text_property.SetJustificationToCentered()
line_cell_label_text_property.SetColor(deep_pink_rgb)
line_cell_label_text_property.SetFontSize(14)
line_cell_label_mapper = vtkLabeledDataMapper()
line_cell_label_mapper.SetInputData(line_cell_grid)
line_cell_label_mapper.SetLabelTextProperty(line_cell_label_text_property)
line_cell_label_actor = vtkActor2D()
line_cell_label_actor.SetMapper(line_cell_label_mapper)

line_cell_glyph_property = vtkProperty()
line_cell_glyph_property.SetAmbientColor(gold_rgb)
line_cell_glyph_property.SetDiffuseColor(yellow_rgb)
line_cell_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
line_cell_glyph_property.SetSpecular(0.5)
line_cell_glyph_property.SetDiffuse(0.7)
line_cell_glyph_property.SetAmbient(0.5)
line_cell_glyph_property.SetSpecularPower(20.0)
line_cell_glyph_property.SetOpacity(1.0)
line_cell_glyph_mapper = vtkGlyph3DMapper()
line_cell_glyph_mapper.SetInputData(line_cell_grid)
line_cell_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
line_cell_glyph_mapper.ScalingOn()
line_cell_glyph_mapper.ScalarVisibilityOff()
line_cell_glyph_actor = vtkActor()
line_cell_glyph_actor.SetMapper(line_cell_glyph_mapper)
line_cell_glyph_actor.SetProperty(line_cell_glyph_property)

line_cell_text_actor = vtkTextActor()
line_cell_text_actor.SetInput("Line")
line_cell_text_actor.GetTextProperty().SetFontSize(12)
line_cell_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
line_cell_text_actor.GetTextProperty().SetJustificationToCentered()
line_cell_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
line_cell_text_actor.SetPosition(0.5, 0.01)

line_cell_renderer = vtkRenderer()
line_cell_renderer.AddActor(line_cell_actor)
line_cell_renderer.AddActor(line_cell_label_actor)
line_cell_renderer.AddActor(line_cell_glyph_actor)
line_cell_renderer.AddViewProp(line_cell_text_actor)
line_cell_renderer.SetBackground(background_rgb)
line_cell_renderer.SetViewport(2 / num_cols, 3 / num_rows, 3 / num_cols, 4 / num_rows)

# ---------------------------------------------------------------------------
# Cell 3: Poly Line (row 0, col 3) — 2D wireframe
# ---------------------------------------------------------------------------
sf_pl = 2.0
poly_line_points = vtkPoints()
poly_line_points.InsertNextPoint(0 / sf_pl, 0.5 / sf_pl, 0)
poly_line_points.InsertNextPoint(0.5 / sf_pl, 0 / sf_pl, 0)
poly_line_points.InsertNextPoint(1 / sf_pl, 0.3 / sf_pl, 0)
poly_line_points.InsertNextPoint(1.5 / sf_pl, 0.4 / sf_pl, 0)
poly_line_points.InsertNextPoint(2.0 / sf_pl, 0.4 / sf_pl, 0)
poly_line_cell = vtkPolyLine()
poly_line_cell.GetPointIds().SetNumberOfIds(5)
for i in range(5):
    poly_line_cell.GetPointIds().SetId(i, i)
poly_line_grid = vtkUnstructuredGrid()
poly_line_grid.SetPoints(poly_line_points)
poly_line_grid.InsertNextCell(poly_line_cell.GetCellType(), poly_line_cell.GetPointIds())

# Center
poly_line_bounds = poly_line_grid.GetBounds()
poly_line_pts = poly_line_grid.GetPoints()
poly_line_new_pts = vtkPoints()
poly_line_new_pts.SetNumberOfPoints(poly_line_pts.GetNumberOfPoints())
for i in range(poly_line_pts.GetNumberOfPoints()):
    px, py, pz = poly_line_pts.GetPoint(i)
    poly_line_new_pts.SetPoint(i, px - (poly_line_bounds[0] + poly_line_bounds[1]) / 2.0,
                               py - (poly_line_bounds[2] + poly_line_bounds[3]) / 2.0,
                               pz - (poly_line_bounds[4] + poly_line_bounds[5]) / 2.0)
poly_line_grid.SetPoints(poly_line_new_pts)

poly_line_wireframe_property = vtkProperty()
poly_line_wireframe_property.SetRepresentationToWireframe()
poly_line_wireframe_property.SetLineWidth(2)
poly_line_wireframe_property.SetOpacity(1)
poly_line_wireframe_property.SetColor(0.0, 0.0, 0.0)

poly_line_mapper = vtkDataSetMapper()
poly_line_mapper.SetInputData(poly_line_grid)
poly_line_actor = vtkActor()
poly_line_actor.SetMapper(poly_line_mapper)
poly_line_actor.SetProperty(poly_line_wireframe_property)

poly_line_label_text_property = vtkTextProperty()
poly_line_label_text_property.BoldOn()
poly_line_label_text_property.ShadowOn()
poly_line_label_text_property.SetJustificationToCentered()
poly_line_label_text_property.SetColor(deep_pink_rgb)
poly_line_label_text_property.SetFontSize(14)
poly_line_label_mapper = vtkLabeledDataMapper()
poly_line_label_mapper.SetInputData(poly_line_grid)
poly_line_label_mapper.SetLabelTextProperty(poly_line_label_text_property)
poly_line_label_actor = vtkActor2D()
poly_line_label_actor.SetMapper(poly_line_label_mapper)

poly_line_glyph_property = vtkProperty()
poly_line_glyph_property.SetAmbientColor(gold_rgb)
poly_line_glyph_property.SetDiffuseColor(yellow_rgb)
poly_line_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
poly_line_glyph_property.SetSpecular(0.5)
poly_line_glyph_property.SetDiffuse(0.7)
poly_line_glyph_property.SetAmbient(0.5)
poly_line_glyph_property.SetSpecularPower(20.0)
poly_line_glyph_property.SetOpacity(1.0)
poly_line_glyph_mapper = vtkGlyph3DMapper()
poly_line_glyph_mapper.SetInputData(poly_line_grid)
poly_line_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
poly_line_glyph_mapper.ScalingOn()
poly_line_glyph_mapper.ScalarVisibilityOff()
poly_line_glyph_actor = vtkActor()
poly_line_glyph_actor.SetMapper(poly_line_glyph_mapper)
poly_line_glyph_actor.SetProperty(poly_line_glyph_property)

poly_line_text_actor = vtkTextActor()
poly_line_text_actor.SetInput("Poly Line")
poly_line_text_actor.GetTextProperty().SetFontSize(12)
poly_line_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
poly_line_text_actor.GetTextProperty().SetJustificationToCentered()
poly_line_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
poly_line_text_actor.SetPosition(0.5, 0.01)

poly_line_renderer = vtkRenderer()
poly_line_renderer.AddActor(poly_line_actor)
poly_line_renderer.AddActor(poly_line_label_actor)
poly_line_renderer.AddActor(poly_line_glyph_actor)
poly_line_renderer.AddViewProp(poly_line_text_actor)
poly_line_renderer.SetBackground(background_rgb)
poly_line_renderer.SetViewport(3 / num_cols, 3 / num_rows, 4 / num_cols, 4 / num_rows)

# ---------------------------------------------------------------------------
# Cell 4: Triangle (row 1, col 0) — 2D surface
# ---------------------------------------------------------------------------
triangle_points = vtkPoints()
triangle_points.InsertNextPoint(0, 0, 0)
triangle_points.InsertNextPoint(0.5, 0.5, 0)
triangle_points.InsertNextPoint(0.2, 1, 0)
triangle_cell = vtkTriangle()
for i in range(3):
    triangle_cell.GetPointIds().SetId(i, i)
triangle_grid = vtkUnstructuredGrid()
triangle_grid.SetPoints(triangle_points)
triangle_grid.InsertNextCell(triangle_cell.GetCellType(), triangle_cell.GetPointIds())

# Center
triangle_bounds = triangle_grid.GetBounds()
triangle_pts = triangle_grid.GetPoints()
triangle_new_pts = vtkPoints()
triangle_new_pts.SetNumberOfPoints(triangle_pts.GetNumberOfPoints())
for i in range(triangle_pts.GetNumberOfPoints()):
    px, py, pz = triangle_pts.GetPoint(i)
    triangle_new_pts.SetPoint(i, px - (triangle_bounds[0] + triangle_bounds[1]) / 2.0,
                              py - (triangle_bounds[2] + triangle_bounds[3]) / 2.0,
                              pz - (triangle_bounds[4] + triangle_bounds[5]) / 2.0)
triangle_grid.SetPoints(triangle_new_pts)

triangle_surface_property = vtkProperty()
triangle_surface_property.SetAmbientColor(dark_salmon_rgb)
triangle_surface_property.SetDiffuseColor(seashell_rgb)
triangle_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
triangle_surface_property.SetSpecular(0.5)
triangle_surface_property.SetDiffuse(0.7)
triangle_surface_property.SetAmbient(0.5)
triangle_surface_property.SetSpecularPower(20.0)
triangle_surface_property.SetOpacity(0.9)
triangle_surface_property.EdgeVisibilityOn()
triangle_surface_property.SetLineWidth(3)

triangle_mapper = vtkDataSetMapper()
triangle_mapper.SetInputData(triangle_grid)
triangle_actor = vtkActor()
triangle_actor.SetMapper(triangle_mapper)
triangle_actor.SetProperty(triangle_surface_property)

triangle_label_text_property = vtkTextProperty()
triangle_label_text_property.BoldOn()
triangle_label_text_property.ShadowOn()
triangle_label_text_property.SetJustificationToCentered()
triangle_label_text_property.SetColor(deep_pink_rgb)
triangle_label_text_property.SetFontSize(14)
triangle_label_mapper = vtkLabeledDataMapper()
triangle_label_mapper.SetInputData(triangle_grid)
triangle_label_mapper.SetLabelTextProperty(triangle_label_text_property)
triangle_label_actor = vtkActor2D()
triangle_label_actor.SetMapper(triangle_label_mapper)

triangle_glyph_property = vtkProperty()
triangle_glyph_property.SetAmbientColor(gold_rgb)
triangle_glyph_property.SetDiffuseColor(yellow_rgb)
triangle_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
triangle_glyph_property.SetSpecular(0.5)
triangle_glyph_property.SetDiffuse(0.7)
triangle_glyph_property.SetAmbient(0.5)
triangle_glyph_property.SetSpecularPower(20.0)
triangle_glyph_property.SetOpacity(1.0)
triangle_glyph_mapper = vtkGlyph3DMapper()
triangle_glyph_mapper.SetInputData(triangle_grid)
triangle_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
triangle_glyph_mapper.ScalingOn()
triangle_glyph_mapper.ScalarVisibilityOff()
triangle_glyph_actor = vtkActor()
triangle_glyph_actor.SetMapper(triangle_glyph_mapper)
triangle_glyph_actor.SetProperty(triangle_glyph_property)

triangle_text_actor = vtkTextActor()
triangle_text_actor.SetInput("Triangle")
triangle_text_actor.GetTextProperty().SetFontSize(12)
triangle_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
triangle_text_actor.GetTextProperty().SetJustificationToCentered()
triangle_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
triangle_text_actor.SetPosition(0.5, 0.01)

triangle_renderer = vtkRenderer()
triangle_renderer.AddActor(triangle_actor)
triangle_renderer.AddActor(triangle_label_actor)
triangle_renderer.AddActor(triangle_glyph_actor)
triangle_renderer.AddViewProp(triangle_text_actor)
triangle_renderer.SetBackground(background_rgb)
triangle_renderer.SetViewport(0 / num_cols, 2 / num_rows, 1 / num_cols, 3 / num_rows)

# ---------------------------------------------------------------------------
# Cell 5: Triangle Strip (row 1, col 1) — 2D surface
# ---------------------------------------------------------------------------
sf_ts = 3.0
triangle_strip_points = vtkPoints()
triangle_strip_points.InsertNextPoint(0 / sf_ts, 0 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(1 / sf_ts, -0.1 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(0.5 / sf_ts, 1 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(2.0 / sf_ts, -0.1 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(1.5 / sf_ts, 0.8 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(3.0 / sf_ts, 0 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(2.5 / sf_ts, 0.9 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(4.0 / sf_ts, -0.2 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(3.5 / sf_ts, 0.8 / sf_ts, 0)
triangle_strip_points.InsertNextPoint(4.5 / sf_ts, 1.1 / sf_ts, 0)
triangle_strip_cell = vtkTriangleStrip()
triangle_strip_cell.GetPointIds().SetNumberOfIds(10)
for i in range(10):
    triangle_strip_cell.GetPointIds().SetId(i, i)
triangle_strip_grid = vtkUnstructuredGrid()
triangle_strip_grid.SetPoints(triangle_strip_points)
triangle_strip_grid.InsertNextCell(triangle_strip_cell.GetCellType(), triangle_strip_cell.GetPointIds())

# Center
triangle_strip_bounds = triangle_strip_grid.GetBounds()
triangle_strip_pts = triangle_strip_grid.GetPoints()
triangle_strip_new_pts = vtkPoints()
triangle_strip_new_pts.SetNumberOfPoints(triangle_strip_pts.GetNumberOfPoints())
for i in range(triangle_strip_pts.GetNumberOfPoints()):
    px, py, pz = triangle_strip_pts.GetPoint(i)
    triangle_strip_new_pts.SetPoint(i, px - (triangle_strip_bounds[0] + triangle_strip_bounds[1]) / 2.0,
                                    py - (triangle_strip_bounds[2] + triangle_strip_bounds[3]) / 2.0,
                                    pz - (triangle_strip_bounds[4] + triangle_strip_bounds[5]) / 2.0)
triangle_strip_grid.SetPoints(triangle_strip_new_pts)

triangle_strip_surface_property = vtkProperty()
triangle_strip_surface_property.SetAmbientColor(dark_salmon_rgb)
triangle_strip_surface_property.SetDiffuseColor(seashell_rgb)
triangle_strip_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
triangle_strip_surface_property.SetSpecular(0.5)
triangle_strip_surface_property.SetDiffuse(0.7)
triangle_strip_surface_property.SetAmbient(0.5)
triangle_strip_surface_property.SetSpecularPower(20.0)
triangle_strip_surface_property.SetOpacity(0.9)
triangle_strip_surface_property.EdgeVisibilityOn()
triangle_strip_surface_property.SetLineWidth(3)

triangle_strip_mapper = vtkDataSetMapper()
triangle_strip_mapper.SetInputData(triangle_strip_grid)
triangle_strip_actor = vtkActor()
triangle_strip_actor.SetMapper(triangle_strip_mapper)
triangle_strip_actor.SetProperty(triangle_strip_surface_property)

triangle_strip_label_text_property = vtkTextProperty()
triangle_strip_label_text_property.BoldOn()
triangle_strip_label_text_property.ShadowOn()
triangle_strip_label_text_property.SetJustificationToCentered()
triangle_strip_label_text_property.SetColor(deep_pink_rgb)
triangle_strip_label_text_property.SetFontSize(14)
triangle_strip_label_mapper = vtkLabeledDataMapper()
triangle_strip_label_mapper.SetInputData(triangle_strip_grid)
triangle_strip_label_mapper.SetLabelTextProperty(triangle_strip_label_text_property)
triangle_strip_label_actor = vtkActor2D()
triangle_strip_label_actor.SetMapper(triangle_strip_label_mapper)

triangle_strip_glyph_property = vtkProperty()
triangle_strip_glyph_property.SetAmbientColor(gold_rgb)
triangle_strip_glyph_property.SetDiffuseColor(yellow_rgb)
triangle_strip_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
triangle_strip_glyph_property.SetSpecular(0.5)
triangle_strip_glyph_property.SetDiffuse(0.7)
triangle_strip_glyph_property.SetAmbient(0.5)
triangle_strip_glyph_property.SetSpecularPower(20.0)
triangle_strip_glyph_property.SetOpacity(1.0)
triangle_strip_glyph_mapper = vtkGlyph3DMapper()
triangle_strip_glyph_mapper.SetInputData(triangle_strip_grid)
triangle_strip_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
triangle_strip_glyph_mapper.ScalingOn()
triangle_strip_glyph_mapper.ScalarVisibilityOff()
triangle_strip_glyph_actor = vtkActor()
triangle_strip_glyph_actor.SetMapper(triangle_strip_glyph_mapper)
triangle_strip_glyph_actor.SetProperty(triangle_strip_glyph_property)

triangle_strip_text_actor = vtkTextActor()
triangle_strip_text_actor.SetInput("Triangle Strip")
triangle_strip_text_actor.GetTextProperty().SetFontSize(12)
triangle_strip_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
triangle_strip_text_actor.GetTextProperty().SetJustificationToCentered()
triangle_strip_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
triangle_strip_text_actor.SetPosition(0.5, 0.01)

triangle_strip_renderer = vtkRenderer()
triangle_strip_renderer.AddActor(triangle_strip_actor)
triangle_strip_renderer.AddActor(triangle_strip_label_actor)
triangle_strip_renderer.AddActor(triangle_strip_glyph_actor)
triangle_strip_renderer.AddViewProp(triangle_strip_text_actor)
triangle_strip_renderer.SetBackground(background_rgb)
triangle_strip_renderer.SetViewport(1 / num_cols, 2 / num_rows, 2 / num_cols, 3 / num_rows)

# ---------------------------------------------------------------------------
# Cell 6: Polygon (row 1, col 2) — 2D surface
# ---------------------------------------------------------------------------
polygon_points = vtkPoints()
polygon_points.InsertNextPoint(0, 0, 0)
polygon_points.InsertNextPoint(1, -0.1, 0)
polygon_points.InsertNextPoint(0.8, 0.5, 0)
polygon_points.InsertNextPoint(1, 1, 0)
polygon_points.InsertNextPoint(0.6, 1.2, 0)
polygon_points.InsertNextPoint(0, 0.8, 0)
polygon_cell = vtkPolygon()
polygon_cell.GetPointIds().SetNumberOfIds(6)
for i in range(6):
    polygon_cell.GetPointIds().SetId(i, i)
polygon_grid = vtkUnstructuredGrid()
polygon_grid.SetPoints(polygon_points)
polygon_grid.InsertNextCell(polygon_cell.GetCellType(), polygon_cell.GetPointIds())

# Center
polygon_bounds = polygon_grid.GetBounds()
polygon_pts = polygon_grid.GetPoints()
polygon_new_pts = vtkPoints()
polygon_new_pts.SetNumberOfPoints(polygon_pts.GetNumberOfPoints())
for i in range(polygon_pts.GetNumberOfPoints()):
    px, py, pz = polygon_pts.GetPoint(i)
    polygon_new_pts.SetPoint(i, px - (polygon_bounds[0] + polygon_bounds[1]) / 2.0,
                             py - (polygon_bounds[2] + polygon_bounds[3]) / 2.0,
                             pz - (polygon_bounds[4] + polygon_bounds[5]) / 2.0)
polygon_grid.SetPoints(polygon_new_pts)

polygon_surface_property = vtkProperty()
polygon_surface_property.SetAmbientColor(dark_salmon_rgb)
polygon_surface_property.SetDiffuseColor(seashell_rgb)
polygon_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
polygon_surface_property.SetSpecular(0.5)
polygon_surface_property.SetDiffuse(0.7)
polygon_surface_property.SetAmbient(0.5)
polygon_surface_property.SetSpecularPower(20.0)
polygon_surface_property.SetOpacity(0.9)
polygon_surface_property.EdgeVisibilityOn()
polygon_surface_property.SetLineWidth(3)

polygon_mapper = vtkDataSetMapper()
polygon_mapper.SetInputData(polygon_grid)
polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)
polygon_actor.SetProperty(polygon_surface_property)

polygon_label_text_property = vtkTextProperty()
polygon_label_text_property.BoldOn()
polygon_label_text_property.ShadowOn()
polygon_label_text_property.SetJustificationToCentered()
polygon_label_text_property.SetColor(deep_pink_rgb)
polygon_label_text_property.SetFontSize(14)
polygon_label_mapper = vtkLabeledDataMapper()
polygon_label_mapper.SetInputData(polygon_grid)
polygon_label_mapper.SetLabelTextProperty(polygon_label_text_property)
polygon_label_actor = vtkActor2D()
polygon_label_actor.SetMapper(polygon_label_mapper)

polygon_glyph_property = vtkProperty()
polygon_glyph_property.SetAmbientColor(gold_rgb)
polygon_glyph_property.SetDiffuseColor(yellow_rgb)
polygon_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
polygon_glyph_property.SetSpecular(0.5)
polygon_glyph_property.SetDiffuse(0.7)
polygon_glyph_property.SetAmbient(0.5)
polygon_glyph_property.SetSpecularPower(20.0)
polygon_glyph_property.SetOpacity(1.0)
polygon_glyph_mapper = vtkGlyph3DMapper()
polygon_glyph_mapper.SetInputData(polygon_grid)
polygon_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
polygon_glyph_mapper.ScalingOn()
polygon_glyph_mapper.ScalarVisibilityOff()
polygon_glyph_actor = vtkActor()
polygon_glyph_actor.SetMapper(polygon_glyph_mapper)
polygon_glyph_actor.SetProperty(polygon_glyph_property)

polygon_text_actor = vtkTextActor()
polygon_text_actor.SetInput("Polygon")
polygon_text_actor.GetTextProperty().SetFontSize(12)
polygon_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
polygon_text_actor.GetTextProperty().SetJustificationToCentered()
polygon_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
polygon_text_actor.SetPosition(0.5, 0.01)

polygon_renderer = vtkRenderer()
polygon_renderer.AddActor(polygon_actor)
polygon_renderer.AddActor(polygon_label_actor)
polygon_renderer.AddActor(polygon_glyph_actor)
polygon_renderer.AddViewProp(polygon_text_actor)
polygon_renderer.SetBackground(background_rgb)
polygon_renderer.SetViewport(2 / num_cols, 2 / num_rows, 3 / num_cols, 3 / num_rows)

# ---------------------------------------------------------------------------
# Cell 7: Pixel (row 1, col 3) — 2D surface
# ---------------------------------------------------------------------------
pixel_cell = vtkPixel()
pixel_cell.GetPoints().SetPoint(0, 0, 0, 0)
pixel_cell.GetPoints().SetPoint(1, 1, 0, 0)
pixel_cell.GetPoints().SetPoint(2, 0, 1, 0)
pixel_cell.GetPoints().SetPoint(3, 1, 1, 0)
for i in range(4):
    pixel_cell.GetPointIds().SetId(i, i)
pixel_grid = vtkUnstructuredGrid()
pixel_grid.SetPoints(pixel_cell.GetPoints())
pixel_grid.InsertNextCell(pixel_cell.GetCellType(), pixel_cell.GetPointIds())

# Center
pixel_bounds = pixel_grid.GetBounds()
pixel_pts = pixel_grid.GetPoints()
pixel_new_pts = vtkPoints()
pixel_new_pts.SetNumberOfPoints(pixel_pts.GetNumberOfPoints())
for i in range(pixel_pts.GetNumberOfPoints()):
    px, py, pz = pixel_pts.GetPoint(i)
    pixel_new_pts.SetPoint(i, px - (pixel_bounds[0] + pixel_bounds[1]) / 2.0,
                           py - (pixel_bounds[2] + pixel_bounds[3]) / 2.0,
                           pz - (pixel_bounds[4] + pixel_bounds[5]) / 2.0)
pixel_grid.SetPoints(pixel_new_pts)

pixel_surface_property = vtkProperty()
pixel_surface_property.SetAmbientColor(dark_salmon_rgb)
pixel_surface_property.SetDiffuseColor(seashell_rgb)
pixel_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
pixel_surface_property.SetSpecular(0.5)
pixel_surface_property.SetDiffuse(0.7)
pixel_surface_property.SetAmbient(0.5)
pixel_surface_property.SetSpecularPower(20.0)
pixel_surface_property.SetOpacity(0.9)
pixel_surface_property.EdgeVisibilityOn()
pixel_surface_property.SetLineWidth(3)

pixel_mapper = vtkDataSetMapper()
pixel_mapper.SetInputData(pixel_grid)
pixel_actor = vtkActor()
pixel_actor.SetMapper(pixel_mapper)
pixel_actor.SetProperty(pixel_surface_property)

pixel_label_text_property = vtkTextProperty()
pixel_label_text_property.BoldOn()
pixel_label_text_property.ShadowOn()
pixel_label_text_property.SetJustificationToCentered()
pixel_label_text_property.SetColor(deep_pink_rgb)
pixel_label_text_property.SetFontSize(14)
pixel_label_mapper = vtkLabeledDataMapper()
pixel_label_mapper.SetInputData(pixel_grid)
pixel_label_mapper.SetLabelTextProperty(pixel_label_text_property)
pixel_label_actor = vtkActor2D()
pixel_label_actor.SetMapper(pixel_label_mapper)

pixel_glyph_property = vtkProperty()
pixel_glyph_property.SetAmbientColor(gold_rgb)
pixel_glyph_property.SetDiffuseColor(yellow_rgb)
pixel_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
pixel_glyph_property.SetSpecular(0.5)
pixel_glyph_property.SetDiffuse(0.7)
pixel_glyph_property.SetAmbient(0.5)
pixel_glyph_property.SetSpecularPower(20.0)
pixel_glyph_property.SetOpacity(1.0)
pixel_glyph_mapper = vtkGlyph3DMapper()
pixel_glyph_mapper.SetInputData(pixel_grid)
pixel_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
pixel_glyph_mapper.ScalingOn()
pixel_glyph_mapper.ScalarVisibilityOff()
pixel_glyph_actor = vtkActor()
pixel_glyph_actor.SetMapper(pixel_glyph_mapper)
pixel_glyph_actor.SetProperty(pixel_glyph_property)

pixel_text_actor = vtkTextActor()
pixel_text_actor.SetInput("Pixel")
pixel_text_actor.GetTextProperty().SetFontSize(12)
pixel_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
pixel_text_actor.GetTextProperty().SetJustificationToCentered()
pixel_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pixel_text_actor.SetPosition(0.5, 0.01)

pixel_renderer = vtkRenderer()
pixel_renderer.AddActor(pixel_actor)
pixel_renderer.AddActor(pixel_label_actor)
pixel_renderer.AddActor(pixel_glyph_actor)
pixel_renderer.AddViewProp(pixel_text_actor)
pixel_renderer.SetBackground(background_rgb)
pixel_renderer.SetViewport(3 / num_cols, 2 / num_rows, 4 / num_cols, 3 / num_rows)

# ---------------------------------------------------------------------------
# Cell 8: Quad (row 2, col 0) — 2D surface
# ---------------------------------------------------------------------------
quad_cell = vtkQuad()
quad_cell.GetPoints().SetPoint(0, 0, 0, 0)
quad_cell.GetPoints().SetPoint(1, 1, 0, 0)
quad_cell.GetPoints().SetPoint(2, 1, 1, 0)
quad_cell.GetPoints().SetPoint(3, 0, 1, 0)
for i in range(4):
    quad_cell.GetPointIds().SetId(i, i)
quad_grid = vtkUnstructuredGrid()
quad_grid.SetPoints(quad_cell.GetPoints())
quad_grid.InsertNextCell(quad_cell.GetCellType(), quad_cell.GetPointIds())

# Center
quad_bounds = quad_grid.GetBounds()
quad_pts = quad_grid.GetPoints()
quad_new_pts = vtkPoints()
quad_new_pts.SetNumberOfPoints(quad_pts.GetNumberOfPoints())
for i in range(quad_pts.GetNumberOfPoints()):
    px, py, pz = quad_pts.GetPoint(i)
    quad_new_pts.SetPoint(i, px - (quad_bounds[0] + quad_bounds[1]) / 2.0,
                          py - (quad_bounds[2] + quad_bounds[3]) / 2.0,
                          pz - (quad_bounds[4] + quad_bounds[5]) / 2.0)
quad_grid.SetPoints(quad_new_pts)

quad_surface_property = vtkProperty()
quad_surface_property.SetAmbientColor(dark_salmon_rgb)
quad_surface_property.SetDiffuseColor(seashell_rgb)
quad_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
quad_surface_property.SetSpecular(0.5)
quad_surface_property.SetDiffuse(0.7)
quad_surface_property.SetAmbient(0.5)
quad_surface_property.SetSpecularPower(20.0)
quad_surface_property.SetOpacity(0.9)
quad_surface_property.EdgeVisibilityOn()
quad_surface_property.SetLineWidth(3)

quad_mapper = vtkDataSetMapper()
quad_mapper.SetInputData(quad_grid)
quad_actor = vtkActor()
quad_actor.SetMapper(quad_mapper)
quad_actor.SetProperty(quad_surface_property)

quad_label_text_property = vtkTextProperty()
quad_label_text_property.BoldOn()
quad_label_text_property.ShadowOn()
quad_label_text_property.SetJustificationToCentered()
quad_label_text_property.SetColor(deep_pink_rgb)
quad_label_text_property.SetFontSize(14)
quad_label_mapper = vtkLabeledDataMapper()
quad_label_mapper.SetInputData(quad_grid)
quad_label_mapper.SetLabelTextProperty(quad_label_text_property)
quad_label_actor = vtkActor2D()
quad_label_actor.SetMapper(quad_label_mapper)

quad_glyph_property = vtkProperty()
quad_glyph_property.SetAmbientColor(gold_rgb)
quad_glyph_property.SetDiffuseColor(yellow_rgb)
quad_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
quad_glyph_property.SetSpecular(0.5)
quad_glyph_property.SetDiffuse(0.7)
quad_glyph_property.SetAmbient(0.5)
quad_glyph_property.SetSpecularPower(20.0)
quad_glyph_property.SetOpacity(1.0)
quad_glyph_mapper = vtkGlyph3DMapper()
quad_glyph_mapper.SetInputData(quad_grid)
quad_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
quad_glyph_mapper.ScalingOn()
quad_glyph_mapper.ScalarVisibilityOff()
quad_glyph_actor = vtkActor()
quad_glyph_actor.SetMapper(quad_glyph_mapper)
quad_glyph_actor.SetProperty(quad_glyph_property)

quad_text_actor = vtkTextActor()
quad_text_actor.SetInput("Quad")
quad_text_actor.GetTextProperty().SetFontSize(12)
quad_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
quad_text_actor.GetTextProperty().SetJustificationToCentered()
quad_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
quad_text_actor.SetPosition(0.5, 0.01)

quad_renderer = vtkRenderer()
quad_renderer.AddActor(quad_actor)
quad_renderer.AddActor(quad_label_actor)
quad_renderer.AddActor(quad_glyph_actor)
quad_renderer.AddViewProp(quad_text_actor)
quad_renderer.SetBackground(background_rgb)
quad_renderer.SetViewport(0 / num_cols, 1 / num_rows, 1 / num_cols, 2 / num_rows)

# ---------------------------------------------------------------------------
# Cell 9: Tetra (row 2, col 1) — 3D surface
# ---------------------------------------------------------------------------
tetra_points = vtkPoints()
tetra_points.InsertNextPoint(0, 0, 0)
tetra_points.InsertNextPoint(1, 0, 0)
tetra_points.InsertNextPoint(1, 0, -1)
tetra_points.InsertNextPoint(0, 1, -1)
tetra_cell = vtkTetra()
for i in range(4):
    tetra_cell.GetPointIds().SetId(i, i)
tetra_grid = vtkUnstructuredGrid()
tetra_grid.SetPoints(tetra_points)
tetra_grid.InsertNextCell(tetra_cell.GetCellType(), tetra_cell.GetPointIds())

# 3D rotation
tetra_rot = vtkTransform()
tetra_rot.RotateX(-20)
tetra_rot.RotateY(20)
tetra_rtf = vtkTransformFilter()
tetra_rtf.SetTransform(tetra_rot)
tetra_rtf.SetInputData(tetra_grid)
tetra_rtf.Update()
tetra_grid.SetPoints(tetra_rtf.GetOutput().GetPoints())

# Center
tetra_bounds = tetra_grid.GetBounds()
tetra_pts = tetra_grid.GetPoints()
tetra_new_pts = vtkPoints()
tetra_new_pts.SetNumberOfPoints(tetra_pts.GetNumberOfPoints())
for i in range(tetra_pts.GetNumberOfPoints()):
    px, py, pz = tetra_pts.GetPoint(i)
    tetra_new_pts.SetPoint(i, px - (tetra_bounds[0] + tetra_bounds[1]) / 2.0,
                           py - (tetra_bounds[2] + tetra_bounds[3]) / 2.0,
                           pz - (tetra_bounds[4] + tetra_bounds[5]) / 2.0)
tetra_grid.SetPoints(tetra_new_pts)

tetra_surface_property = vtkProperty()
tetra_surface_property.SetAmbientColor(dark_salmon_rgb)
tetra_surface_property.SetDiffuseColor(seashell_rgb)
tetra_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
tetra_surface_property.SetSpecular(0.5)
tetra_surface_property.SetDiffuse(0.7)
tetra_surface_property.SetAmbient(0.5)
tetra_surface_property.SetSpecularPower(20.0)
tetra_surface_property.SetOpacity(0.9)
tetra_surface_property.EdgeVisibilityOn()
tetra_surface_property.SetLineWidth(3)

tetra_mapper = vtkDataSetMapper()
tetra_mapper.SetInputData(tetra_grid)
tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.SetProperty(tetra_surface_property)

tetra_label_text_property = vtkTextProperty()
tetra_label_text_property.BoldOn()
tetra_label_text_property.ShadowOn()
tetra_label_text_property.SetJustificationToCentered()
tetra_label_text_property.SetColor(deep_pink_rgb)
tetra_label_text_property.SetFontSize(14)
tetra_label_mapper = vtkLabeledDataMapper()
tetra_label_mapper.SetInputData(tetra_grid)
tetra_label_mapper.SetLabelTextProperty(tetra_label_text_property)
tetra_label_actor = vtkActor2D()
tetra_label_actor.SetMapper(tetra_label_mapper)

tetra_glyph_property = vtkProperty()
tetra_glyph_property.SetAmbientColor(gold_rgb)
tetra_glyph_property.SetDiffuseColor(yellow_rgb)
tetra_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
tetra_glyph_property.SetSpecular(0.5)
tetra_glyph_property.SetDiffuse(0.7)
tetra_glyph_property.SetAmbient(0.5)
tetra_glyph_property.SetSpecularPower(20.0)
tetra_glyph_property.SetOpacity(1.0)
tetra_glyph_mapper = vtkGlyph3DMapper()
tetra_glyph_mapper.SetInputData(tetra_grid)
tetra_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
tetra_glyph_mapper.ScalingOn()
tetra_glyph_mapper.ScalarVisibilityOff()
tetra_glyph_actor = vtkActor()
tetra_glyph_actor.SetMapper(tetra_glyph_mapper)
tetra_glyph_actor.SetProperty(tetra_glyph_property)

# Plinth
tetra_nb = tetra_grid.GetBounds()
tetra_nd = (tetra_nb[1] - tetra_nb[0], tetra_nb[3] - tetra_nb[2], tetra_nb[5] - tetra_nb[4])
tetra_thick = tetra_nd[2] * 0.01
tetra_plinth_source = vtkCubeSource()
tetra_plinth_source.SetCenter((tetra_nb[1] + tetra_nb[0]) / 2.0,
                              tetra_nb[2] - tetra_thick / 2.0 - 0.05,
                              (tetra_nb[5] + tetra_nb[4]) / 2.0)
tetra_plinth_source.SetXLength(tetra_nd[0] + tetra_nd[0] * 0.5)
tetra_plinth_source.SetYLength(tetra_thick)
tetra_plinth_source.SetZLength(tetra_nd[2] + tetra_nd[2] * 0.5)
tetra_plinth_property = vtkProperty()
tetra_plinth_property.SetAmbientColor(steel_blue_rgb)
tetra_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
tetra_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
tetra_plinth_property.SetSpecular(0.5)
tetra_plinth_property.SetDiffuse(0.7)
tetra_plinth_property.SetAmbient(0.5)
tetra_plinth_property.SetSpecularPower(20.0)
tetra_plinth_property.SetOpacity(0.8)
tetra_plinth_property.EdgeVisibilityOn()
tetra_plinth_property.SetLineWidth(1)
tetra_plinth_mapper = vtkPolyDataMapper()
tetra_plinth_mapper.SetInputConnection(tetra_plinth_source.GetOutputPort())
tetra_plinth_actor = vtkActor()
tetra_plinth_actor.SetMapper(tetra_plinth_mapper)
tetra_plinth_actor.SetProperty(tetra_plinth_property)

tetra_text_actor = vtkTextActor()
tetra_text_actor.SetInput("Tetra")
tetra_text_actor.GetTextProperty().SetFontSize(12)
tetra_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
tetra_text_actor.GetTextProperty().SetJustificationToCentered()
tetra_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
tetra_text_actor.SetPosition(0.5, 0.01)

tetra_renderer = vtkRenderer()
tetra_renderer.AddActor(tetra_actor)
tetra_renderer.AddActor(tetra_label_actor)
tetra_renderer.AddActor(tetra_glyph_actor)
tetra_renderer.AddActor(tetra_plinth_actor)
tetra_renderer.AddViewProp(tetra_text_actor)
tetra_renderer.SetBackground(background_rgb)
tetra_renderer.SetViewport(1 / num_cols, 1 / num_rows, 2 / num_cols, 2 / num_rows)

# ---------------------------------------------------------------------------
# Cell 10: Voxel (row 2, col 2) — 3D surface
# ---------------------------------------------------------------------------
voxel_points = vtkPoints()
voxel_points.InsertNextPoint(0, 0, 0)
voxel_points.InsertNextPoint(1, 0, 0)
voxel_points.InsertNextPoint(0, 1, 0)
voxel_points.InsertNextPoint(1, 1, 0)
voxel_points.InsertNextPoint(0, 0, 1)
voxel_points.InsertNextPoint(1, 0, 1)
voxel_points.InsertNextPoint(0, 1, 1)
voxel_points.InsertNextPoint(1, 1, 1)
voxel_cell = vtkVoxel()
for i in range(8):
    voxel_cell.GetPointIds().SetId(i, i)
voxel_grid = vtkUnstructuredGrid()
voxel_grid.SetPoints(voxel_points)
voxel_grid.InsertNextCell(voxel_cell.GetCellType(), voxel_cell.GetPointIds())

# 3D rotation
voxel_rot = vtkTransform()
voxel_rot.RotateX(-20)
voxel_rot.RotateY(20)
voxel_rtf = vtkTransformFilter()
voxel_rtf.SetTransform(voxel_rot)
voxel_rtf.SetInputData(voxel_grid)
voxel_rtf.Update()
voxel_grid.SetPoints(voxel_rtf.GetOutput().GetPoints())

# Center
voxel_bounds = voxel_grid.GetBounds()
voxel_pts = voxel_grid.GetPoints()
voxel_new_pts = vtkPoints()
voxel_new_pts.SetNumberOfPoints(voxel_pts.GetNumberOfPoints())
for i in range(voxel_pts.GetNumberOfPoints()):
    px, py, pz = voxel_pts.GetPoint(i)
    voxel_new_pts.SetPoint(i, px - (voxel_bounds[0] + voxel_bounds[1]) / 2.0,
                           py - (voxel_bounds[2] + voxel_bounds[3]) / 2.0,
                           pz - (voxel_bounds[4] + voxel_bounds[5]) / 2.0)
voxel_grid.SetPoints(voxel_new_pts)

voxel_surface_property = vtkProperty()
voxel_surface_property.SetAmbientColor(dark_salmon_rgb)
voxel_surface_property.SetDiffuseColor(seashell_rgb)
voxel_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
voxel_surface_property.SetSpecular(0.5)
voxel_surface_property.SetDiffuse(0.7)
voxel_surface_property.SetAmbient(0.5)
voxel_surface_property.SetSpecularPower(20.0)
voxel_surface_property.SetOpacity(0.9)
voxel_surface_property.EdgeVisibilityOn()
voxel_surface_property.SetLineWidth(3)

voxel_mapper = vtkDataSetMapper()
voxel_mapper.SetInputData(voxel_grid)
voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.SetProperty(voxel_surface_property)

voxel_label_text_property = vtkTextProperty()
voxel_label_text_property.BoldOn()
voxel_label_text_property.ShadowOn()
voxel_label_text_property.SetJustificationToCentered()
voxel_label_text_property.SetColor(deep_pink_rgb)
voxel_label_text_property.SetFontSize(14)
voxel_label_mapper = vtkLabeledDataMapper()
voxel_label_mapper.SetInputData(voxel_grid)
voxel_label_mapper.SetLabelTextProperty(voxel_label_text_property)
voxel_label_actor = vtkActor2D()
voxel_label_actor.SetMapper(voxel_label_mapper)

voxel_glyph_property = vtkProperty()
voxel_glyph_property.SetAmbientColor(gold_rgb)
voxel_glyph_property.SetDiffuseColor(yellow_rgb)
voxel_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
voxel_glyph_property.SetSpecular(0.5)
voxel_glyph_property.SetDiffuse(0.7)
voxel_glyph_property.SetAmbient(0.5)
voxel_glyph_property.SetSpecularPower(20.0)
voxel_glyph_property.SetOpacity(1.0)
voxel_glyph_mapper = vtkGlyph3DMapper()
voxel_glyph_mapper.SetInputData(voxel_grid)
voxel_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
voxel_glyph_mapper.ScalingOn()
voxel_glyph_mapper.ScalarVisibilityOff()
voxel_glyph_actor = vtkActor()
voxel_glyph_actor.SetMapper(voxel_glyph_mapper)
voxel_glyph_actor.SetProperty(voxel_glyph_property)

# Plinth
voxel_nb = voxel_grid.GetBounds()
voxel_nd = (voxel_nb[1] - voxel_nb[0], voxel_nb[3] - voxel_nb[2], voxel_nb[5] - voxel_nb[4])
voxel_thick = voxel_nd[2] * 0.01
voxel_plinth_source = vtkCubeSource()
voxel_plinth_source.SetCenter((voxel_nb[1] + voxel_nb[0]) / 2.0,
                              voxel_nb[2] - voxel_thick / 2.0 - 0.05,
                              (voxel_nb[5] + voxel_nb[4]) / 2.0)
voxel_plinth_source.SetXLength(voxel_nd[0] + voxel_nd[0] * 0.5)
voxel_plinth_source.SetYLength(voxel_thick)
voxel_plinth_source.SetZLength(voxel_nd[2] + voxel_nd[2] * 0.5)
voxel_plinth_property = vtkProperty()
voxel_plinth_property.SetAmbientColor(steel_blue_rgb)
voxel_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
voxel_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
voxel_plinth_property.SetSpecular(0.5)
voxel_plinth_property.SetDiffuse(0.7)
voxel_plinth_property.SetAmbient(0.5)
voxel_plinth_property.SetSpecularPower(20.0)
voxel_plinth_property.SetOpacity(0.8)
voxel_plinth_property.EdgeVisibilityOn()
voxel_plinth_property.SetLineWidth(1)
voxel_plinth_mapper = vtkPolyDataMapper()
voxel_plinth_mapper.SetInputConnection(voxel_plinth_source.GetOutputPort())
voxel_plinth_actor = vtkActor()
voxel_plinth_actor.SetMapper(voxel_plinth_mapper)
voxel_plinth_actor.SetProperty(voxel_plinth_property)

voxel_text_actor = vtkTextActor()
voxel_text_actor.SetInput("Voxel")
voxel_text_actor.GetTextProperty().SetFontSize(12)
voxel_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
voxel_text_actor.GetTextProperty().SetJustificationToCentered()
voxel_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
voxel_text_actor.SetPosition(0.5, 0.01)

voxel_renderer = vtkRenderer()
voxel_renderer.AddActor(voxel_actor)
voxel_renderer.AddActor(voxel_label_actor)
voxel_renderer.AddActor(voxel_glyph_actor)
voxel_renderer.AddActor(voxel_plinth_actor)
voxel_renderer.AddViewProp(voxel_text_actor)
voxel_renderer.SetBackground(background_rgb)
voxel_renderer.SetViewport(2 / num_cols, 1 / num_rows, 3 / num_cols, 2 / num_rows)

# ---------------------------------------------------------------------------
# Cell 11: Hexahedron (row 2, col 3) — 3D surface
# ---------------------------------------------------------------------------
hexahedron_points = vtkPoints()
hexahedron_points.InsertNextPoint(0, 0, 0)
hexahedron_points.InsertNextPoint(1, 0, 0)
hexahedron_points.InsertNextPoint(1, 1, 0)
hexahedron_points.InsertNextPoint(0, 1, 0)
hexahedron_points.InsertNextPoint(0, 0, 1)
hexahedron_points.InsertNextPoint(1, 0, 1)
hexahedron_points.InsertNextPoint(1, 1, 1)
hexahedron_points.InsertNextPoint(0, 1, 1)
hexahedron_cell = vtkHexahedron()
for i in range(8):
    hexahedron_cell.GetPointIds().SetId(i, i)
hexahedron_grid = vtkUnstructuredGrid()
hexahedron_grid.SetPoints(hexahedron_points)
hexahedron_grid.InsertNextCell(hexahedron_cell.GetCellType(), hexahedron_cell.GetPointIds())

# 3D rotation
hexahedron_rot = vtkTransform()
hexahedron_rot.RotateX(-20)
hexahedron_rot.RotateY(20)
hexahedron_rtf = vtkTransformFilter()
hexahedron_rtf.SetTransform(hexahedron_rot)
hexahedron_rtf.SetInputData(hexahedron_grid)
hexahedron_rtf.Update()
hexahedron_grid.SetPoints(hexahedron_rtf.GetOutput().GetPoints())

# Center
hexahedron_bounds = hexahedron_grid.GetBounds()
hexahedron_pts = hexahedron_grid.GetPoints()
hexahedron_new_pts = vtkPoints()
hexahedron_new_pts.SetNumberOfPoints(hexahedron_pts.GetNumberOfPoints())
for i in range(hexahedron_pts.GetNumberOfPoints()):
    px, py, pz = hexahedron_pts.GetPoint(i)
    hexahedron_new_pts.SetPoint(i, px - (hexahedron_bounds[0] + hexahedron_bounds[1]) / 2.0,
                                py - (hexahedron_bounds[2] + hexahedron_bounds[3]) / 2.0,
                                pz - (hexahedron_bounds[4] + hexahedron_bounds[5]) / 2.0)
hexahedron_grid.SetPoints(hexahedron_new_pts)

hexahedron_surface_property = vtkProperty()
hexahedron_surface_property.SetAmbientColor(dark_salmon_rgb)
hexahedron_surface_property.SetDiffuseColor(seashell_rgb)
hexahedron_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
hexahedron_surface_property.SetSpecular(0.5)
hexahedron_surface_property.SetDiffuse(0.7)
hexahedron_surface_property.SetAmbient(0.5)
hexahedron_surface_property.SetSpecularPower(20.0)
hexahedron_surface_property.SetOpacity(0.9)
hexahedron_surface_property.EdgeVisibilityOn()
hexahedron_surface_property.SetLineWidth(3)

hexahedron_mapper = vtkDataSetMapper()
hexahedron_mapper.SetInputData(hexahedron_grid)
hexahedron_actor = vtkActor()
hexahedron_actor.SetMapper(hexahedron_mapper)
hexahedron_actor.SetProperty(hexahedron_surface_property)

hexahedron_label_text_property = vtkTextProperty()
hexahedron_label_text_property.BoldOn()
hexahedron_label_text_property.ShadowOn()
hexahedron_label_text_property.SetJustificationToCentered()
hexahedron_label_text_property.SetColor(deep_pink_rgb)
hexahedron_label_text_property.SetFontSize(14)
hexahedron_label_mapper = vtkLabeledDataMapper()
hexahedron_label_mapper.SetInputData(hexahedron_grid)
hexahedron_label_mapper.SetLabelTextProperty(hexahedron_label_text_property)
hexahedron_label_actor = vtkActor2D()
hexahedron_label_actor.SetMapper(hexahedron_label_mapper)

hexahedron_glyph_property = vtkProperty()
hexahedron_glyph_property.SetAmbientColor(gold_rgb)
hexahedron_glyph_property.SetDiffuseColor(yellow_rgb)
hexahedron_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
hexahedron_glyph_property.SetSpecular(0.5)
hexahedron_glyph_property.SetDiffuse(0.7)
hexahedron_glyph_property.SetAmbient(0.5)
hexahedron_glyph_property.SetSpecularPower(20.0)
hexahedron_glyph_property.SetOpacity(1.0)
hexahedron_glyph_mapper = vtkGlyph3DMapper()
hexahedron_glyph_mapper.SetInputData(hexahedron_grid)
hexahedron_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
hexahedron_glyph_mapper.ScalingOn()
hexahedron_glyph_mapper.ScalarVisibilityOff()
hexahedron_glyph_actor = vtkActor()
hexahedron_glyph_actor.SetMapper(hexahedron_glyph_mapper)
hexahedron_glyph_actor.SetProperty(hexahedron_glyph_property)

# Plinth
hexahedron_nb = hexahedron_grid.GetBounds()
hexahedron_nd = (hexahedron_nb[1] - hexahedron_nb[0], hexahedron_nb[3] - hexahedron_nb[2], hexahedron_nb[5] - hexahedron_nb[4])
hexahedron_thick = hexahedron_nd[2] * 0.01
hexahedron_plinth_source = vtkCubeSource()
hexahedron_plinth_source.SetCenter((hexahedron_nb[1] + hexahedron_nb[0]) / 2.0,
                                   hexahedron_nb[2] - hexahedron_thick / 2.0 - 0.05,
                                   (hexahedron_nb[5] + hexahedron_nb[4]) / 2.0)
hexahedron_plinth_source.SetXLength(hexahedron_nd[0] + hexahedron_nd[0] * 0.5)
hexahedron_plinth_source.SetYLength(hexahedron_thick)
hexahedron_plinth_source.SetZLength(hexahedron_nd[2] + hexahedron_nd[2] * 0.5)
hexahedron_plinth_property = vtkProperty()
hexahedron_plinth_property.SetAmbientColor(steel_blue_rgb)
hexahedron_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
hexahedron_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
hexahedron_plinth_property.SetSpecular(0.5)
hexahedron_plinth_property.SetDiffuse(0.7)
hexahedron_plinth_property.SetAmbient(0.5)
hexahedron_plinth_property.SetSpecularPower(20.0)
hexahedron_plinth_property.SetOpacity(0.8)
hexahedron_plinth_property.EdgeVisibilityOn()
hexahedron_plinth_property.SetLineWidth(1)
hexahedron_plinth_mapper = vtkPolyDataMapper()
hexahedron_plinth_mapper.SetInputConnection(hexahedron_plinth_source.GetOutputPort())
hexahedron_plinth_actor = vtkActor()
hexahedron_plinth_actor.SetMapper(hexahedron_plinth_mapper)
hexahedron_plinth_actor.SetProperty(hexahedron_plinth_property)

hexahedron_text_actor = vtkTextActor()
hexahedron_text_actor.SetInput("Hexahedron")
hexahedron_text_actor.GetTextProperty().SetFontSize(12)
hexahedron_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
hexahedron_text_actor.GetTextProperty().SetJustificationToCentered()
hexahedron_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
hexahedron_text_actor.SetPosition(0.5, 0.01)

hexahedron_renderer = vtkRenderer()
hexahedron_renderer.AddActor(hexahedron_actor)
hexahedron_renderer.AddActor(hexahedron_label_actor)
hexahedron_renderer.AddActor(hexahedron_glyph_actor)
hexahedron_renderer.AddActor(hexahedron_plinth_actor)
hexahedron_renderer.AddViewProp(hexahedron_text_actor)
hexahedron_renderer.SetBackground(background_rgb)
hexahedron_renderer.SetViewport(3 / num_cols, 1 / num_rows, 4 / num_cols, 2 / num_rows)

# ---------------------------------------------------------------------------
# Cell 12: Wedge (row 3, col 0) — 3D surface
# ---------------------------------------------------------------------------
wedge_points = vtkPoints()
wedge_points.InsertNextPoint(0, 0, 0)
wedge_points.InsertNextPoint(0, 0, 1)
wedge_points.InsertNextPoint(0, 0.5, 0.5)
wedge_points.InsertNextPoint(1, 0, 0)
wedge_points.InsertNextPoint(1, 0, 1)
wedge_points.InsertNextPoint(1, 0.5, 0.5)
wedge_cell = vtkWedge()
for i in range(6):
    wedge_cell.GetPointIds().SetId(i, i)
wedge_grid = vtkUnstructuredGrid()
wedge_grid.SetPoints(wedge_points)
wedge_grid.InsertNextCell(wedge_cell.GetCellType(), wedge_cell.GetPointIds())

# 3D rotation
wedge_rot = vtkTransform()
wedge_rot.RotateX(-20)
wedge_rot.RotateY(20)
wedge_rtf = vtkTransformFilter()
wedge_rtf.SetTransform(wedge_rot)
wedge_rtf.SetInputData(wedge_grid)
wedge_rtf.Update()
wedge_grid.SetPoints(wedge_rtf.GetOutput().GetPoints())

# Center
wedge_bounds = wedge_grid.GetBounds()
wedge_pts = wedge_grid.GetPoints()
wedge_new_pts = vtkPoints()
wedge_new_pts.SetNumberOfPoints(wedge_pts.GetNumberOfPoints())
for i in range(wedge_pts.GetNumberOfPoints()):
    px, py, pz = wedge_pts.GetPoint(i)
    wedge_new_pts.SetPoint(i, px - (wedge_bounds[0] + wedge_bounds[1]) / 2.0,
                           py - (wedge_bounds[2] + wedge_bounds[3]) / 2.0,
                           pz - (wedge_bounds[4] + wedge_bounds[5]) / 2.0)
wedge_grid.SetPoints(wedge_new_pts)

wedge_surface_property = vtkProperty()
wedge_surface_property.SetAmbientColor(dark_salmon_rgb)
wedge_surface_property.SetDiffuseColor(seashell_rgb)
wedge_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
wedge_surface_property.SetSpecular(0.5)
wedge_surface_property.SetDiffuse(0.7)
wedge_surface_property.SetAmbient(0.5)
wedge_surface_property.SetSpecularPower(20.0)
wedge_surface_property.SetOpacity(0.9)
wedge_surface_property.EdgeVisibilityOn()
wedge_surface_property.SetLineWidth(3)

wedge_mapper = vtkDataSetMapper()
wedge_mapper.SetInputData(wedge_grid)
wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)
wedge_actor.SetProperty(wedge_surface_property)

wedge_label_text_property = vtkTextProperty()
wedge_label_text_property.BoldOn()
wedge_label_text_property.ShadowOn()
wedge_label_text_property.SetJustificationToCentered()
wedge_label_text_property.SetColor(deep_pink_rgb)
wedge_label_text_property.SetFontSize(14)
wedge_label_mapper = vtkLabeledDataMapper()
wedge_label_mapper.SetInputData(wedge_grid)
wedge_label_mapper.SetLabelTextProperty(wedge_label_text_property)
wedge_label_actor = vtkActor2D()
wedge_label_actor.SetMapper(wedge_label_mapper)

wedge_glyph_property = vtkProperty()
wedge_glyph_property.SetAmbientColor(gold_rgb)
wedge_glyph_property.SetDiffuseColor(yellow_rgb)
wedge_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
wedge_glyph_property.SetSpecular(0.5)
wedge_glyph_property.SetDiffuse(0.7)
wedge_glyph_property.SetAmbient(0.5)
wedge_glyph_property.SetSpecularPower(20.0)
wedge_glyph_property.SetOpacity(1.0)
wedge_glyph_mapper = vtkGlyph3DMapper()
wedge_glyph_mapper.SetInputData(wedge_grid)
wedge_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
wedge_glyph_mapper.ScalingOn()
wedge_glyph_mapper.ScalarVisibilityOff()
wedge_glyph_actor = vtkActor()
wedge_glyph_actor.SetMapper(wedge_glyph_mapper)
wedge_glyph_actor.SetProperty(wedge_glyph_property)

# Plinth
wedge_nb = wedge_grid.GetBounds()
wedge_nd = (wedge_nb[1] - wedge_nb[0], wedge_nb[3] - wedge_nb[2], wedge_nb[5] - wedge_nb[4])
wedge_thick = wedge_nd[2] * 0.01
wedge_plinth_source = vtkCubeSource()
wedge_plinth_source.SetCenter((wedge_nb[1] + wedge_nb[0]) / 2.0,
                              wedge_nb[2] - wedge_thick / 2.0 - 0.05,
                              (wedge_nb[5] + wedge_nb[4]) / 2.0)
wedge_plinth_source.SetXLength(wedge_nd[0] + wedge_nd[0] * 0.5)
wedge_plinth_source.SetYLength(wedge_thick)
wedge_plinth_source.SetZLength(wedge_nd[2] + wedge_nd[2] * 0.5)
wedge_plinth_property = vtkProperty()
wedge_plinth_property.SetAmbientColor(steel_blue_rgb)
wedge_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
wedge_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
wedge_plinth_property.SetSpecular(0.5)
wedge_plinth_property.SetDiffuse(0.7)
wedge_plinth_property.SetAmbient(0.5)
wedge_plinth_property.SetSpecularPower(20.0)
wedge_plinth_property.SetOpacity(0.8)
wedge_plinth_property.EdgeVisibilityOn()
wedge_plinth_property.SetLineWidth(1)
wedge_plinth_mapper = vtkPolyDataMapper()
wedge_plinth_mapper.SetInputConnection(wedge_plinth_source.GetOutputPort())
wedge_plinth_actor = vtkActor()
wedge_plinth_actor.SetMapper(wedge_plinth_mapper)
wedge_plinth_actor.SetProperty(wedge_plinth_property)

wedge_text_actor = vtkTextActor()
wedge_text_actor.SetInput("Wedge")
wedge_text_actor.GetTextProperty().SetFontSize(12)
wedge_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
wedge_text_actor.GetTextProperty().SetJustificationToCentered()
wedge_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
wedge_text_actor.SetPosition(0.5, 0.01)

wedge_renderer = vtkRenderer()
wedge_renderer.AddActor(wedge_actor)
wedge_renderer.AddActor(wedge_label_actor)
wedge_renderer.AddActor(wedge_glyph_actor)
wedge_renderer.AddActor(wedge_plinth_actor)
wedge_renderer.AddViewProp(wedge_text_actor)
wedge_renderer.SetBackground(background_rgb)
wedge_renderer.SetViewport(0 / num_cols, 0 / num_rows, 1 / num_cols, 1 / num_rows)

# ---------------------------------------------------------------------------
# Cell 13: Pyramid (row 3, col 1) — 3D surface
# ---------------------------------------------------------------------------
pyramid_points = vtkPoints()
pyramid_points.InsertNextPoint(0.5, 0, -0.5)
pyramid_points.InsertNextPoint(-0.5, 0, -0.5)
pyramid_points.InsertNextPoint(-0.5, 0, 0.5)
pyramid_points.InsertNextPoint(0.5, 0, 0.5)
pyramid_points.InsertNextPoint(0, 1, 0)
pyramid_cell = vtkPyramid()
for i in range(5):
    pyramid_cell.GetPointIds().SetId(i, i)
pyramid_grid = vtkUnstructuredGrid()
pyramid_grid.SetPoints(pyramid_points)
pyramid_grid.InsertNextCell(pyramid_cell.GetCellType(), pyramid_cell.GetPointIds())

# 3D rotation
pyramid_rot = vtkTransform()
pyramid_rot.RotateX(-20)
pyramid_rot.RotateY(20)
pyramid_rtf = vtkTransformFilter()
pyramid_rtf.SetTransform(pyramid_rot)
pyramid_rtf.SetInputData(pyramid_grid)
pyramid_rtf.Update()
pyramid_grid.SetPoints(pyramid_rtf.GetOutput().GetPoints())

# Center
pyramid_bounds = pyramid_grid.GetBounds()
pyramid_pts = pyramid_grid.GetPoints()
pyramid_new_pts = vtkPoints()
pyramid_new_pts.SetNumberOfPoints(pyramid_pts.GetNumberOfPoints())
for i in range(pyramid_pts.GetNumberOfPoints()):
    px, py, pz = pyramid_pts.GetPoint(i)
    pyramid_new_pts.SetPoint(i, px - (pyramid_bounds[0] + pyramid_bounds[1]) / 2.0,
                             py - (pyramid_bounds[2] + pyramid_bounds[3]) / 2.0,
                             pz - (pyramid_bounds[4] + pyramid_bounds[5]) / 2.0)
pyramid_grid.SetPoints(pyramid_new_pts)

pyramid_surface_property = vtkProperty()
pyramid_surface_property.SetAmbientColor(dark_salmon_rgb)
pyramid_surface_property.SetDiffuseColor(seashell_rgb)
pyramid_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
pyramid_surface_property.SetSpecular(0.5)
pyramid_surface_property.SetDiffuse(0.7)
pyramid_surface_property.SetAmbient(0.5)
pyramid_surface_property.SetSpecularPower(20.0)
pyramid_surface_property.SetOpacity(0.9)
pyramid_surface_property.EdgeVisibilityOn()
pyramid_surface_property.SetLineWidth(3)

pyramid_mapper = vtkDataSetMapper()
pyramid_mapper.SetInputData(pyramid_grid)
pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)
pyramid_actor.SetProperty(pyramid_surface_property)

pyramid_label_text_property = vtkTextProperty()
pyramid_label_text_property.BoldOn()
pyramid_label_text_property.ShadowOn()
pyramid_label_text_property.SetJustificationToCentered()
pyramid_label_text_property.SetColor(deep_pink_rgb)
pyramid_label_text_property.SetFontSize(14)
pyramid_label_mapper = vtkLabeledDataMapper()
pyramid_label_mapper.SetInputData(pyramid_grid)
pyramid_label_mapper.SetLabelTextProperty(pyramid_label_text_property)
pyramid_label_actor = vtkActor2D()
pyramid_label_actor.SetMapper(pyramid_label_mapper)

pyramid_glyph_property = vtkProperty()
pyramid_glyph_property.SetAmbientColor(gold_rgb)
pyramid_glyph_property.SetDiffuseColor(yellow_rgb)
pyramid_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
pyramid_glyph_property.SetSpecular(0.5)
pyramid_glyph_property.SetDiffuse(0.7)
pyramid_glyph_property.SetAmbient(0.5)
pyramid_glyph_property.SetSpecularPower(20.0)
pyramid_glyph_property.SetOpacity(1.0)
pyramid_glyph_mapper = vtkGlyph3DMapper()
pyramid_glyph_mapper.SetInputData(pyramid_grid)
pyramid_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
pyramid_glyph_mapper.ScalingOn()
pyramid_glyph_mapper.ScalarVisibilityOff()
pyramid_glyph_actor = vtkActor()
pyramid_glyph_actor.SetMapper(pyramid_glyph_mapper)
pyramid_glyph_actor.SetProperty(pyramid_glyph_property)

# Plinth
pyramid_nb = pyramid_grid.GetBounds()
pyramid_nd = (pyramid_nb[1] - pyramid_nb[0], pyramid_nb[3] - pyramid_nb[2], pyramid_nb[5] - pyramid_nb[4])
pyramid_thick = pyramid_nd[2] * 0.01
pyramid_plinth_source = vtkCubeSource()
pyramid_plinth_source.SetCenter((pyramid_nb[1] + pyramid_nb[0]) / 2.0,
                                pyramid_nb[2] - pyramid_thick / 2.0 - 0.05,
                                (pyramid_nb[5] + pyramid_nb[4]) / 2.0)
pyramid_plinth_source.SetXLength(pyramid_nd[0] + pyramid_nd[0] * 0.5)
pyramid_plinth_source.SetYLength(pyramid_thick)
pyramid_plinth_source.SetZLength(pyramid_nd[2] + pyramid_nd[2] * 0.5)
pyramid_plinth_property = vtkProperty()
pyramid_plinth_property.SetAmbientColor(steel_blue_rgb)
pyramid_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
pyramid_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
pyramid_plinth_property.SetSpecular(0.5)
pyramid_plinth_property.SetDiffuse(0.7)
pyramid_plinth_property.SetAmbient(0.5)
pyramid_plinth_property.SetSpecularPower(20.0)
pyramid_plinth_property.SetOpacity(0.8)
pyramid_plinth_property.EdgeVisibilityOn()
pyramid_plinth_property.SetLineWidth(1)
pyramid_plinth_mapper = vtkPolyDataMapper()
pyramid_plinth_mapper.SetInputConnection(pyramid_plinth_source.GetOutputPort())
pyramid_plinth_actor = vtkActor()
pyramid_plinth_actor.SetMapper(pyramid_plinth_mapper)
pyramid_plinth_actor.SetProperty(pyramid_plinth_property)

pyramid_text_actor = vtkTextActor()
pyramid_text_actor.SetInput("Pyramid")
pyramid_text_actor.GetTextProperty().SetFontSize(12)
pyramid_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
pyramid_text_actor.GetTextProperty().SetJustificationToCentered()
pyramid_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pyramid_text_actor.SetPosition(0.5, 0.01)

pyramid_renderer = vtkRenderer()
pyramid_renderer.AddActor(pyramid_actor)
pyramid_renderer.AddActor(pyramid_label_actor)
pyramid_renderer.AddActor(pyramid_glyph_actor)
pyramid_renderer.AddActor(pyramid_plinth_actor)
pyramid_renderer.AddViewProp(pyramid_text_actor)
pyramid_renderer.SetBackground(background_rgb)
pyramid_renderer.SetViewport(1 / num_cols, 0 / num_rows, 2 / num_cols, 1 / num_rows)

# ---------------------------------------------------------------------------
# Cell 14: Pentagonal Prism (row 3, col 2) — 3D surface
# ---------------------------------------------------------------------------
sf_pp = 4.0
pentagonal_prism_cell = vtkPentagonalPrism()
pentagonal_prism_cell.GetPoints().SetPoint(0, 11 / sf_pp, 10 / sf_pp, 10 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(1, 13 / sf_pp, 10 / sf_pp, 10 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(2, 14 / sf_pp, 12 / sf_pp, 10 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(3, 12 / sf_pp, 14 / sf_pp, 10 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(4, 10 / sf_pp, 12 / sf_pp, 10 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(5, 11 / sf_pp, 10 / sf_pp, 14 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(6, 13 / sf_pp, 10 / sf_pp, 14 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(7, 14 / sf_pp, 12 / sf_pp, 14 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(8, 12 / sf_pp, 14 / sf_pp, 14 / sf_pp)
pentagonal_prism_cell.GetPoints().SetPoint(9, 10 / sf_pp, 12 / sf_pp, 14 / sf_pp)
for i in range(10):
    pentagonal_prism_cell.GetPointIds().SetId(i, i)
pentagonal_prism_grid = vtkUnstructuredGrid()
pentagonal_prism_grid.SetPoints(pentagonal_prism_cell.GetPoints())
pentagonal_prism_grid.InsertNextCell(pentagonal_prism_cell.GetCellType(), pentagonal_prism_cell.GetPointIds())

# 3D rotation
pentagonal_prism_rot = vtkTransform()
pentagonal_prism_rot.RotateX(-20)
pentagonal_prism_rot.RotateY(20)
pentagonal_prism_rtf = vtkTransformFilter()
pentagonal_prism_rtf.SetTransform(pentagonal_prism_rot)
pentagonal_prism_rtf.SetInputData(pentagonal_prism_grid)
pentagonal_prism_rtf.Update()
pentagonal_prism_grid.SetPoints(pentagonal_prism_rtf.GetOutput().GetPoints())

# Center
pentagonal_prism_bounds = pentagonal_prism_grid.GetBounds()
pentagonal_prism_pts = pentagonal_prism_grid.GetPoints()
pentagonal_prism_new_pts = vtkPoints()
pentagonal_prism_new_pts.SetNumberOfPoints(pentagonal_prism_pts.GetNumberOfPoints())
for i in range(pentagonal_prism_pts.GetNumberOfPoints()):
    px, py, pz = pentagonal_prism_pts.GetPoint(i)
    pentagonal_prism_new_pts.SetPoint(i, px - (pentagonal_prism_bounds[0] + pentagonal_prism_bounds[1]) / 2.0,
                                      py - (pentagonal_prism_bounds[2] + pentagonal_prism_bounds[3]) / 2.0,
                                      pz - (pentagonal_prism_bounds[4] + pentagonal_prism_bounds[5]) / 2.0)
pentagonal_prism_grid.SetPoints(pentagonal_prism_new_pts)

pentagonal_prism_surface_property = vtkProperty()
pentagonal_prism_surface_property.SetAmbientColor(dark_salmon_rgb)
pentagonal_prism_surface_property.SetDiffuseColor(seashell_rgb)
pentagonal_prism_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
pentagonal_prism_surface_property.SetSpecular(0.5)
pentagonal_prism_surface_property.SetDiffuse(0.7)
pentagonal_prism_surface_property.SetAmbient(0.5)
pentagonal_prism_surface_property.SetSpecularPower(20.0)
pentagonal_prism_surface_property.SetOpacity(0.9)
pentagonal_prism_surface_property.EdgeVisibilityOn()
pentagonal_prism_surface_property.SetLineWidth(3)

pentagonal_prism_mapper = vtkDataSetMapper()
pentagonal_prism_mapper.SetInputData(pentagonal_prism_grid)
pentagonal_prism_actor = vtkActor()
pentagonal_prism_actor.SetMapper(pentagonal_prism_mapper)
pentagonal_prism_actor.SetProperty(pentagonal_prism_surface_property)

pentagonal_prism_label_text_property = vtkTextProperty()
pentagonal_prism_label_text_property.BoldOn()
pentagonal_prism_label_text_property.ShadowOn()
pentagonal_prism_label_text_property.SetJustificationToCentered()
pentagonal_prism_label_text_property.SetColor(deep_pink_rgb)
pentagonal_prism_label_text_property.SetFontSize(14)
pentagonal_prism_label_mapper = vtkLabeledDataMapper()
pentagonal_prism_label_mapper.SetInputData(pentagonal_prism_grid)
pentagonal_prism_label_mapper.SetLabelTextProperty(pentagonal_prism_label_text_property)
pentagonal_prism_label_actor = vtkActor2D()
pentagonal_prism_label_actor.SetMapper(pentagonal_prism_label_mapper)

pentagonal_prism_glyph_property = vtkProperty()
pentagonal_prism_glyph_property.SetAmbientColor(gold_rgb)
pentagonal_prism_glyph_property.SetDiffuseColor(yellow_rgb)
pentagonal_prism_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
pentagonal_prism_glyph_property.SetSpecular(0.5)
pentagonal_prism_glyph_property.SetDiffuse(0.7)
pentagonal_prism_glyph_property.SetAmbient(0.5)
pentagonal_prism_glyph_property.SetSpecularPower(20.0)
pentagonal_prism_glyph_property.SetOpacity(1.0)
pentagonal_prism_glyph_mapper = vtkGlyph3DMapper()
pentagonal_prism_glyph_mapper.SetInputData(pentagonal_prism_grid)
pentagonal_prism_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
pentagonal_prism_glyph_mapper.ScalingOn()
pentagonal_prism_glyph_mapper.ScalarVisibilityOff()
pentagonal_prism_glyph_actor = vtkActor()
pentagonal_prism_glyph_actor.SetMapper(pentagonal_prism_glyph_mapper)
pentagonal_prism_glyph_actor.SetProperty(pentagonal_prism_glyph_property)

# Plinth
pentagonal_prism_nb = pentagonal_prism_grid.GetBounds()
pentagonal_prism_nd = (pentagonal_prism_nb[1] - pentagonal_prism_nb[0], pentagonal_prism_nb[3] - pentagonal_prism_nb[2], pentagonal_prism_nb[5] - pentagonal_prism_nb[4])
pentagonal_prism_thick = pentagonal_prism_nd[2] * 0.01
pentagonal_prism_plinth_source = vtkCubeSource()
pentagonal_prism_plinth_source.SetCenter((pentagonal_prism_nb[1] + pentagonal_prism_nb[0]) / 2.0,
                                         pentagonal_prism_nb[2] - pentagonal_prism_thick / 2.0 - 0.05,
                                         (pentagonal_prism_nb[5] + pentagonal_prism_nb[4]) / 2.0)
pentagonal_prism_plinth_source.SetXLength(pentagonal_prism_nd[0] + pentagonal_prism_nd[0] * 0.5)
pentagonal_prism_plinth_source.SetYLength(pentagonal_prism_thick)
pentagonal_prism_plinth_source.SetZLength(pentagonal_prism_nd[2] + pentagonal_prism_nd[2] * 0.5)
pentagonal_prism_plinth_property = vtkProperty()
pentagonal_prism_plinth_property.SetAmbientColor(steel_blue_rgb)
pentagonal_prism_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
pentagonal_prism_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
pentagonal_prism_plinth_property.SetSpecular(0.5)
pentagonal_prism_plinth_property.SetDiffuse(0.7)
pentagonal_prism_plinth_property.SetAmbient(0.5)
pentagonal_prism_plinth_property.SetSpecularPower(20.0)
pentagonal_prism_plinth_property.SetOpacity(0.8)
pentagonal_prism_plinth_property.EdgeVisibilityOn()
pentagonal_prism_plinth_property.SetLineWidth(1)
pentagonal_prism_plinth_mapper = vtkPolyDataMapper()
pentagonal_prism_plinth_mapper.SetInputConnection(pentagonal_prism_plinth_source.GetOutputPort())
pentagonal_prism_plinth_actor = vtkActor()
pentagonal_prism_plinth_actor.SetMapper(pentagonal_prism_plinth_mapper)
pentagonal_prism_plinth_actor.SetProperty(pentagonal_prism_plinth_property)

pentagonal_prism_text_actor = vtkTextActor()
pentagonal_prism_text_actor.SetInput("Pentagonal Prism")
pentagonal_prism_text_actor.GetTextProperty().SetFontSize(12)
pentagonal_prism_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
pentagonal_prism_text_actor.GetTextProperty().SetJustificationToCentered()
pentagonal_prism_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pentagonal_prism_text_actor.SetPosition(0.5, 0.01)

pentagonal_prism_renderer = vtkRenderer()
pentagonal_prism_renderer.AddActor(pentagonal_prism_actor)
pentagonal_prism_renderer.AddActor(pentagonal_prism_label_actor)
pentagonal_prism_renderer.AddActor(pentagonal_prism_glyph_actor)
pentagonal_prism_renderer.AddActor(pentagonal_prism_plinth_actor)
pentagonal_prism_renderer.AddViewProp(pentagonal_prism_text_actor)
pentagonal_prism_renderer.SetBackground(background_rgb)
pentagonal_prism_renderer.SetViewport(2 / num_cols, 0 / num_rows, 3 / num_cols, 1 / num_rows)

# ---------------------------------------------------------------------------
# Cell 15: Hexagonal Prism (row 3, col 3) — 3D surface
# ---------------------------------------------------------------------------
sf_hp = 4.0
hexagonal_prism_cell = vtkHexagonalPrism()
hexagonal_prism_cell.GetPoints().SetPoint(0, 11 / sf_hp, 10 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(1, 13 / sf_hp, 10 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(2, 14 / sf_hp, 12 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(3, 13 / sf_hp, 14 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(4, 11 / sf_hp, 14 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(5, 10 / sf_hp, 12 / sf_hp, 10 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(6, 11 / sf_hp, 10 / sf_hp, 14 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(7, 13 / sf_hp, 10 / sf_hp, 14 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(8, 14 / sf_hp, 12 / sf_hp, 14 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(9, 13 / sf_hp, 14 / sf_hp, 14 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(10, 11 / sf_hp, 14 / sf_hp, 14 / sf_hp)
hexagonal_prism_cell.GetPoints().SetPoint(11, 10 / sf_hp, 12 / sf_hp, 14 / sf_hp)
for i in range(12):
    hexagonal_prism_cell.GetPointIds().SetId(i, i)
hexagonal_prism_grid = vtkUnstructuredGrid()
hexagonal_prism_grid.SetPoints(hexagonal_prism_cell.GetPoints())
hexagonal_prism_grid.InsertNextCell(hexagonal_prism_cell.GetCellType(), hexagonal_prism_cell.GetPointIds())

# 3D rotation
hexagonal_prism_rot = vtkTransform()
hexagonal_prism_rot.RotateX(-20)
hexagonal_prism_rot.RotateY(20)
hexagonal_prism_rtf = vtkTransformFilter()
hexagonal_prism_rtf.SetTransform(hexagonal_prism_rot)
hexagonal_prism_rtf.SetInputData(hexagonal_prism_grid)
hexagonal_prism_rtf.Update()
hexagonal_prism_grid.SetPoints(hexagonal_prism_rtf.GetOutput().GetPoints())

# Center
hexagonal_prism_bounds = hexagonal_prism_grid.GetBounds()
hexagonal_prism_pts = hexagonal_prism_grid.GetPoints()
hexagonal_prism_new_pts = vtkPoints()
hexagonal_prism_new_pts.SetNumberOfPoints(hexagonal_prism_pts.GetNumberOfPoints())
for i in range(hexagonal_prism_pts.GetNumberOfPoints()):
    px, py, pz = hexagonal_prism_pts.GetPoint(i)
    hexagonal_prism_new_pts.SetPoint(i, px - (hexagonal_prism_bounds[0] + hexagonal_prism_bounds[1]) / 2.0,
                                     py - (hexagonal_prism_bounds[2] + hexagonal_prism_bounds[3]) / 2.0,
                                     pz - (hexagonal_prism_bounds[4] + hexagonal_prism_bounds[5]) / 2.0)
hexagonal_prism_grid.SetPoints(hexagonal_prism_new_pts)

hexagonal_prism_surface_property = vtkProperty()
hexagonal_prism_surface_property.SetAmbientColor(dark_salmon_rgb)
hexagonal_prism_surface_property.SetDiffuseColor(seashell_rgb)
hexagonal_prism_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
hexagonal_prism_surface_property.SetSpecular(0.5)
hexagonal_prism_surface_property.SetDiffuse(0.7)
hexagonal_prism_surface_property.SetAmbient(0.5)
hexagonal_prism_surface_property.SetSpecularPower(20.0)
hexagonal_prism_surface_property.SetOpacity(0.9)
hexagonal_prism_surface_property.EdgeVisibilityOn()
hexagonal_prism_surface_property.SetLineWidth(3)

hexagonal_prism_mapper = vtkDataSetMapper()
hexagonal_prism_mapper.SetInputData(hexagonal_prism_grid)
hexagonal_prism_actor = vtkActor()
hexagonal_prism_actor.SetMapper(hexagonal_prism_mapper)
hexagonal_prism_actor.SetProperty(hexagonal_prism_surface_property)

hexagonal_prism_label_text_property = vtkTextProperty()
hexagonal_prism_label_text_property.BoldOn()
hexagonal_prism_label_text_property.ShadowOn()
hexagonal_prism_label_text_property.SetJustificationToCentered()
hexagonal_prism_label_text_property.SetColor(deep_pink_rgb)
hexagonal_prism_label_text_property.SetFontSize(14)
hexagonal_prism_label_mapper = vtkLabeledDataMapper()
hexagonal_prism_label_mapper.SetInputData(hexagonal_prism_grid)
hexagonal_prism_label_mapper.SetLabelTextProperty(hexagonal_prism_label_text_property)
hexagonal_prism_label_actor = vtkActor2D()
hexagonal_prism_label_actor.SetMapper(hexagonal_prism_label_mapper)

hexagonal_prism_glyph_property = vtkProperty()
hexagonal_prism_glyph_property.SetAmbientColor(gold_rgb)
hexagonal_prism_glyph_property.SetDiffuseColor(yellow_rgb)
hexagonal_prism_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
hexagonal_prism_glyph_property.SetSpecular(0.5)
hexagonal_prism_glyph_property.SetDiffuse(0.7)
hexagonal_prism_glyph_property.SetAmbient(0.5)
hexagonal_prism_glyph_property.SetSpecularPower(20.0)
hexagonal_prism_glyph_property.SetOpacity(1.0)
hexagonal_prism_glyph_mapper = vtkGlyph3DMapper()
hexagonal_prism_glyph_mapper.SetInputData(hexagonal_prism_grid)
hexagonal_prism_glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
hexagonal_prism_glyph_mapper.ScalingOn()
hexagonal_prism_glyph_mapper.ScalarVisibilityOff()
hexagonal_prism_glyph_actor = vtkActor()
hexagonal_prism_glyph_actor.SetMapper(hexagonal_prism_glyph_mapper)
hexagonal_prism_glyph_actor.SetProperty(hexagonal_prism_glyph_property)

# Plinth
hexagonal_prism_nb = hexagonal_prism_grid.GetBounds()
hexagonal_prism_nd = (hexagonal_prism_nb[1] - hexagonal_prism_nb[0], hexagonal_prism_nb[3] - hexagonal_prism_nb[2], hexagonal_prism_nb[5] - hexagonal_prism_nb[4])
hexagonal_prism_thick = hexagonal_prism_nd[2] * 0.01
hexagonal_prism_plinth_source = vtkCubeSource()
hexagonal_prism_plinth_source.SetCenter((hexagonal_prism_nb[1] + hexagonal_prism_nb[0]) / 2.0,
                                        hexagonal_prism_nb[2] - hexagonal_prism_thick / 2.0 - 0.05,
                                        (hexagonal_prism_nb[5] + hexagonal_prism_nb[4]) / 2.0)
hexagonal_prism_plinth_source.SetXLength(hexagonal_prism_nd[0] + hexagonal_prism_nd[0] * 0.5)
hexagonal_prism_plinth_source.SetYLength(hexagonal_prism_thick)
hexagonal_prism_plinth_source.SetZLength(hexagonal_prism_nd[2] + hexagonal_prism_nd[2] * 0.5)
hexagonal_prism_plinth_property = vtkProperty()
hexagonal_prism_plinth_property.SetAmbientColor(steel_blue_rgb)
hexagonal_prism_plinth_property.SetDiffuseColor(light_steel_blue_rgb)
hexagonal_prism_plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
hexagonal_prism_plinth_property.SetSpecular(0.5)
hexagonal_prism_plinth_property.SetDiffuse(0.7)
hexagonal_prism_plinth_property.SetAmbient(0.5)
hexagonal_prism_plinth_property.SetSpecularPower(20.0)
hexagonal_prism_plinth_property.SetOpacity(0.8)
hexagonal_prism_plinth_property.EdgeVisibilityOn()
hexagonal_prism_plinth_property.SetLineWidth(1)
hexagonal_prism_plinth_mapper = vtkPolyDataMapper()
hexagonal_prism_plinth_mapper.SetInputConnection(hexagonal_prism_plinth_source.GetOutputPort())
hexagonal_prism_plinth_actor = vtkActor()
hexagonal_prism_plinth_actor.SetMapper(hexagonal_prism_plinth_mapper)
hexagonal_prism_plinth_actor.SetProperty(hexagonal_prism_plinth_property)

hexagonal_prism_text_actor = vtkTextActor()
hexagonal_prism_text_actor.SetInput("Hexagonal Prism")
hexagonal_prism_text_actor.GetTextProperty().SetFontSize(12)
hexagonal_prism_text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
hexagonal_prism_text_actor.GetTextProperty().SetJustificationToCentered()
hexagonal_prism_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
hexagonal_prism_text_actor.SetPosition(0.5, 0.01)

hexagonal_prism_renderer = vtkRenderer()
hexagonal_prism_renderer.AddActor(hexagonal_prism_actor)
hexagonal_prism_renderer.AddActor(hexagonal_prism_label_actor)
hexagonal_prism_renderer.AddActor(hexagonal_prism_glyph_actor)
hexagonal_prism_renderer.AddActor(hexagonal_prism_plinth_actor)
hexagonal_prism_renderer.AddViewProp(hexagonal_prism_text_actor)
hexagonal_prism_renderer.SetBackground(background_rgb)
hexagonal_prism_renderer.SetViewport(3 / num_cols, 0 / num_rows, 4 / num_cols, 1 / num_rows)

# ---------------------------------------------------------------------------
# Render window
# ---------------------------------------------------------------------------
render_window = vtkRenderWindow()
render_window.AddRenderer(vertex_renderer)
render_window.AddRenderer(poly_vertex_renderer)
render_window.AddRenderer(line_cell_renderer)
render_window.AddRenderer(poly_line_renderer)
render_window.AddRenderer(triangle_renderer)
render_window.AddRenderer(triangle_strip_renderer)
render_window.AddRenderer(polygon_renderer)
render_window.AddRenderer(pixel_renderer)
render_window.AddRenderer(quad_renderer)
render_window.AddRenderer(tetra_renderer)
render_window.AddRenderer(voxel_renderer)
render_window.AddRenderer(hexahedron_renderer)
render_window.AddRenderer(wedge_renderer)
render_window.AddRenderer(pyramid_renderer)
render_window.AddRenderer(pentagonal_prism_renderer)
render_window.AddRenderer(hexagonal_prism_renderer)
render_window.SetWindowName("linear cells demo")
render_window.SetMultiSamples(0)
render_window.SetSize(1200, 1200)

# ---------------------------------------------------------------------------
# Interactor
# ---------------------------------------------------------------------------
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# ---------------------------------------------------------------------------
# Scene: configure cameras for each viewport
# ---------------------------------------------------------------------------
vertex_renderer.ResetCamera()
vertex_renderer.GetActiveCamera().Zoom(1.4)

poly_vertex_renderer.ResetCamera()
poly_vertex_renderer.GetActiveCamera().Zoom(1.4)

line_cell_renderer.ResetCamera()
line_cell_renderer.GetActiveCamera().Zoom(1.4)

poly_line_renderer.ResetCamera()
poly_line_renderer.GetActiveCamera().Zoom(1.4)

triangle_renderer.ResetCamera()
triangle_renderer.GetActiveCamera().Zoom(1.4)

triangle_strip_renderer.ResetCamera()
triangle_strip_renderer.GetActiveCamera().Zoom(1.4)

polygon_renderer.ResetCamera()
polygon_renderer.GetActiveCamera().Zoom(1.4)

pixel_renderer.ResetCamera()
pixel_renderer.GetActiveCamera().Zoom(1.4)

quad_renderer.ResetCamera()
quad_renderer.GetActiveCamera().Zoom(1.4)

tetra_renderer.ResetCamera()
tetra_renderer.GetActiveCamera().Zoom(1.4)

voxel_renderer.ResetCamera()
voxel_renderer.GetActiveCamera().Zoom(1.4)

hexahedron_renderer.ResetCamera()
hexahedron_renderer.GetActiveCamera().Zoom(1.4)

wedge_renderer.ResetCamera()
wedge_renderer.GetActiveCamera().Zoom(1.4)

pyramid_renderer.ResetCamera()
pyramid_renderer.GetActiveCamera().Zoom(1.4)

pentagonal_prism_renderer.ResetCamera()
pentagonal_prism_renderer.GetActiveCamera().Zoom(1.4)

hexagonal_prism_renderer.ResetCamera()
hexagonal_prism_renderer.GetActiveCamera().Zoom(1.4)

render_window_interactor.Initialize()
render_window_interactor.Start()
