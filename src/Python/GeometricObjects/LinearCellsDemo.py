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

# ---------------------------------------------------------------------------
# Cell definitions: (label, cell_class, point_coords, style, is_3d)
#   cell_class: VTK cell class (or "use_cell_points" sentinel via None coords)
#   point_coords: list of (x,y,z) tuples, or None when cell.GetPoints() is used
#   style: "wireframe" | "surface"
#   is_3d: True → rotate for 3D viewing and add translucent plinth
# ---------------------------------------------------------------------------
cell_defs = [
    # Row 0: Vertex, Poly Vertex, Line, Poly Line
    ("Vertex",            vtkVertex,         [(0, 0, 0)],                                                                                                                                "surface",   False),
    ("Poly Vertex",       vtkPolyVertex,     [(0/1.5, 0/1.5, 0/1.5), (1/1.5, 0/1.5, 0/1.5), (0/1.5, 1/1.5, 0/1.5), (0/1.5, 0/1.5, 1/1.5), (1/1.5, 0/1.5, 0.4/1.5), (0/1.5, 1/1.5, 0.6/1.5)],  "surface",   True),
    ("Line",              vtkLine,           [(0, 0, 0), (0.5, 0.5, 0)],                                                                                                                 "wireframe", False),
    ("Poly Line",         vtkPolyLine,       [(0/2.0, 0.5/2.0, 0), (0.5/2.0, 0/2.0, 0), (1/2.0, 0.3/2.0, 0), (1.5/2.0, 0.4/2.0, 0), (2.0/2.0, 0.4/2.0, 0)],                          "wireframe", False),
    # Row 1: Triangle, Triangle Strip, Polygon, Pixel
    ("Triangle",          vtkTriangle,       [(0, 0, 0), (0.5, 0.5, 0), (0.2, 1, 0)],                                                                                                   "surface",   False),
    ("Triangle Strip",    vtkTriangleStrip,  [(0/3.0, 0/3.0, 0), (1/3.0, -0.1/3.0, 0), (0.5/3.0, 1/3.0, 0), (2.0/3.0, -0.1/3.0, 0), (1.5/3.0, 0.8/3.0, 0), (3.0/3.0, 0/3.0, 0), (2.5/3.0, 0.9/3.0, 0), (4.0/3.0, -0.2/3.0, 0), (3.5/3.0, 0.8/3.0, 0), (4.5/3.0, 1.1/3.0, 0)],  "surface",   False),
    ("Polygon",           vtkPolygon,        [(0, 0, 0), (1, -0.1, 0), (0.8, 0.5, 0), (1, 1, 0), (0.6, 1.2, 0), (0, 0.8, 0)],                                                          "surface",   False),
    ("Pixel",             vtkPixel,          None,                                                                                                                                        "surface",   False),
    # Row 2: Quad, Tetra, Voxel, Hexahedron
    ("Quad",              vtkQuad,           None,                                                                                                                                        "surface",   False),
    ("Tetra",             vtkTetra,          [(0, 0, 0), (1, 0, 0), (1, 0, -1), (0, 1, -1)],                                                                                             "surface",   True),
    ("Voxel",             vtkVoxel,          [(0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,1,1), (1,1,1)],                                                                  "surface",   True),
    ("Hexahedron",        vtkHexahedron,     [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (0,0,1), (1,0,1), (1,1,1), (0,1,1)],                                                                  "surface",   True),
    # Row 3: Wedge, Pyramid, Pentagonal Prism, Hexagonal Prism
    ("Wedge",             vtkWedge,          [(0,0,0), (0,0,1), (0,0.5,0.5), (1,0,0), (1,0,1), (1,0.5,0.5)],                                                                            "surface",   True),
    ("Pyramid",           vtkPyramid,        [(0.5,0,-0.5), (-0.5,0,-0.5), (-0.5,0,0.5), (0.5,0,0.5), (0,1,0)],                                                                         "surface",   True),
    ("Pentagonal Prism",  vtkPentagonalPrism, None,                                                                                                                                      "surface",   True),
    ("Hexagonal Prism",   vtkHexagonalPrism,  None,                                                                                                                                      "surface",   True),
]

# ---------------------------------------------------------------------------
# Viewport grid: 4 columns × 4 rows
# ---------------------------------------------------------------------------
num_cols = 4
num_rows = 4

# Shared sphere source for vertex glyphs
sphere = vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)
sphere.SetRadius(0.04)

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(1200, 1200)
render_window.SetWindowName("LinearCellsDemo")

for idx, (label, cell_class, point_coords, style, is_3d) in enumerate(cell_defs):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    # Viewport rectangle
    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # ---- Build cell and unstructured grid ----
    cell = cell_class()
    n_pts = cell.GetNumberOfPoints()

    if label == "Pixel":
        cell.GetPoints().SetPoint(0, 0, 0, 0)
        cell.GetPoints().SetPoint(1, 1, 0, 0)
        cell.GetPoints().SetPoint(2, 0, 1, 0)
        cell.GetPoints().SetPoint(3, 1, 1, 0)
        for i in range(4):
            cell.GetPointIds().SetId(i, i)
        grid = vtkUnstructuredGrid()
        grid.SetPoints(cell.GetPoints())
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
    elif label == "Quad":
        cell.GetPoints().SetPoint(0, 0, 0, 0)
        cell.GetPoints().SetPoint(1, 1, 0, 0)
        cell.GetPoints().SetPoint(2, 1, 1, 0)
        cell.GetPoints().SetPoint(3, 0, 1, 0)
        for i in range(4):
            cell.GetPointIds().SetId(i, i)
        grid = vtkUnstructuredGrid()
        grid.SetPoints(cell.GetPoints())
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
    elif label == "Pentagonal Prism":
        s = 4.0
        cell.GetPoints().SetPoint(0, 11/s, 10/s, 10/s)
        cell.GetPoints().SetPoint(1, 13/s, 10/s, 10/s)
        cell.GetPoints().SetPoint(2, 14/s, 12/s, 10/s)
        cell.GetPoints().SetPoint(3, 12/s, 14/s, 10/s)
        cell.GetPoints().SetPoint(4, 10/s, 12/s, 10/s)
        cell.GetPoints().SetPoint(5, 11/s, 10/s, 14/s)
        cell.GetPoints().SetPoint(6, 13/s, 10/s, 14/s)
        cell.GetPoints().SetPoint(7, 14/s, 12/s, 14/s)
        cell.GetPoints().SetPoint(8, 12/s, 14/s, 14/s)
        cell.GetPoints().SetPoint(9, 10/s, 12/s, 14/s)
        for i in range(10):
            cell.GetPointIds().SetId(i, i)
        grid = vtkUnstructuredGrid()
        grid.SetPoints(cell.GetPoints())
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
    elif label == "Hexagonal Prism":
        s = 4.0
        cell.GetPoints().SetPoint(0, 11/s, 10/s, 10/s)
        cell.GetPoints().SetPoint(1, 13/s, 10/s, 10/s)
        cell.GetPoints().SetPoint(2, 14/s, 12/s, 10/s)
        cell.GetPoints().SetPoint(3, 13/s, 14/s, 10/s)
        cell.GetPoints().SetPoint(4, 11/s, 14/s, 10/s)
        cell.GetPoints().SetPoint(5, 10/s, 12/s, 10/s)
        cell.GetPoints().SetPoint(6, 11/s, 10/s, 14/s)
        cell.GetPoints().SetPoint(7, 13/s, 10/s, 14/s)
        cell.GetPoints().SetPoint(8, 14/s, 12/s, 14/s)
        cell.GetPoints().SetPoint(9, 13/s, 14/s, 14/s)
        cell.GetPoints().SetPoint(10, 11/s, 14/s, 14/s)
        cell.GetPoints().SetPoint(11, 10/s, 12/s, 14/s)
        for i in range(12):
            cell.GetPointIds().SetId(i, i)
        grid = vtkUnstructuredGrid()
        grid.SetPoints(cell.GetPoints())
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
    else:
        # Generic path: explicit point coordinates supplied in cell_defs
        points = vtkPoints()
        for coord in point_coords:
            points.InsertNextPoint(*coord)
        n_pts = len(point_coords)
        if n_pts != cell.GetNumberOfPoints():
            cell.GetPointIds().SetNumberOfIds(n_pts)
        for i in range(n_pts):
            cell.GetPointIds().SetId(i, i)
        grid = vtkUnstructuredGrid()
        grid.SetPoints(points)
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    # 3D viewing rotation
    if is_3d:
        rot = vtkTransform()
        rot.RotateX(-20)
        rot.RotateY(20)
        rtf = vtkTransformFilter()
        rtf.SetTransform(rot)
        rtf.SetInputData(grid)
        rtf.Update()
        grid.SetPoints(rtf.GetOutput().GetPoints())

    # Center the cell at the origin
    bounds = grid.GetBounds()
    pts = grid.GetPoints()
    new_pts = vtkPoints()
    new_pts.SetNumberOfPoints(pts.GetNumberOfPoints())
    for i in range(pts.GetNumberOfPoints()):
        px, py, pz = pts.GetPoint(i)
        new_pts.SetPoint(i, px - (bounds[0] + bounds[1]) / 2.0,
                         py - (bounds[2] + bounds[3]) / 2.0,
                         pz - (bounds[4] + bounds[5]) / 2.0)
    grid.SetPoints(new_pts)

    # ---- Cell surface / wireframe actor ----
    if style == "wireframe":
        cell_prop = vtkProperty()
        cell_prop.SetRepresentationToWireframe()
        cell_prop.SetLineWidth(2)
        cell_prop.SetOpacity(1)
        cell_prop.SetColor(0.0, 0.0, 0.0)
    else:
        cell_prop = vtkProperty()
        cell_prop.SetAmbientColor(dark_salmon_rgb)
        cell_prop.SetDiffuseColor(seashell_rgb)
        cell_prop.SetSpecularColor(1.0, 1.0, 1.0)
        cell_prop.SetSpecular(0.5)
        cell_prop.SetDiffuse(0.7)
        cell_prop.SetAmbient(0.5)
        cell_prop.SetSpecularPower(20.0)
        cell_prop.SetOpacity(0.9)
        cell_prop.EdgeVisibilityOn()
        cell_prop.SetLineWidth(3)

    mapper = vtkDataSetMapper()
    mapper.SetInputData(grid)
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetProperty(cell_prop)

    # ---- Vertex-ordering labels ----
    label_tp = vtkTextProperty()
    label_tp.BoldOn()
    label_tp.ShadowOn()
    label_tp.SetJustificationToCentered()
    label_tp.SetColor(deep_pink_rgb)
    label_tp.SetFontSize(14)

    label_mapper = vtkLabeledDataMapper()
    label_mapper.SetInputData(grid)
    label_mapper.SetLabelTextProperty(label_tp)
    label_actor = vtkActor2D()
    label_actor.SetMapper(label_mapper)

    # ---- Vertex glyphs: gold spheres ----
    glyph_prop = vtkProperty()
    glyph_prop.SetAmbientColor(gold_rgb)
    glyph_prop.SetDiffuseColor(yellow_rgb)
    glyph_prop.SetSpecularColor(1.0, 1.0, 1.0)
    glyph_prop.SetSpecular(0.5)
    glyph_prop.SetDiffuse(0.7)
    glyph_prop.SetAmbient(0.5)
    glyph_prop.SetSpecularPower(20.0)
    glyph_prop.SetOpacity(1.0)

    glyph_mapper = vtkGlyph3DMapper()
    glyph_mapper.SetInputData(grid)
    glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
    glyph_mapper.ScalingOn()
    glyph_mapper.ScalarVisibilityOff()
    glyph_actor = vtkActor()
    glyph_actor.SetMapper(glyph_mapper)
    glyph_actor.SetProperty(glyph_prop)

    # ---- Renderer for this viewport ----
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(label_actor)
    renderer.AddActor(glyph_actor)

    # Plinth for 3D cells
    if is_3d:
        nb = grid.GetBounds()
        nd = (nb[1] - nb[0], nb[3] - nb[2], nb[5] - nb[4])
        thick = nd[2] * 0.01
        plinth_source = vtkCubeSource()
        plinth_source.SetCenter((nb[1] + nb[0]) / 2.0,
                                nb[2] - thick / 2.0 - 0.05,
                                (nb[5] + nb[4]) / 2.0)
        plinth_source.SetXLength(nd[0] + nd[0] * 0.5)
        plinth_source.SetYLength(thick)
        plinth_source.SetZLength(nd[2] + nd[2] * 0.5)

        plinth_prop = vtkProperty()
        plinth_prop.SetAmbientColor(steel_blue_rgb)
        plinth_prop.SetDiffuseColor(light_steel_blue_rgb)
        plinth_prop.SetSpecularColor(1.0, 1.0, 1.0)
        plinth_prop.SetSpecular(0.5)
        plinth_prop.SetDiffuse(0.7)
        plinth_prop.SetAmbient(0.5)
        plinth_prop.SetSpecularPower(20.0)
        plinth_prop.SetOpacity(0.8)
        plinth_prop.EdgeVisibilityOn()
        plinth_prop.SetLineWidth(1)

        plinth_mapper = vtkPolyDataMapper()
        plinth_mapper.SetInputConnection(plinth_source.GetOutputPort())
        plinth_actor = vtkActor()
        plinth_actor.SetMapper(plinth_mapper)
        plinth_actor.SetProperty(plinth_prop)
        renderer.AddActor(plinth_actor)

    # Title label: 2D text pinned to bottom of viewport
    text_actor = vtkTextActor()
    text_actor.SetInput(label)
    text_actor.GetTextProperty().SetFontSize(12)
    text_actor.GetTextProperty().SetColor(0.0, 0.0, 0.0)
    text_actor.GetTextProperty().SetJustificationToCentered()
    text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
    text_actor.SetPosition(0.5, 0.01)
    renderer.AddViewProp(text_actor)

    renderer.SetBackground(background_rgb)
    renderer.SetViewport(xmin, ymin, xmax, ymax)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.4)

    render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
