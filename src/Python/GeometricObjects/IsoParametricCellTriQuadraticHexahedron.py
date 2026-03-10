#!/usr/bin/env python

# Render a single tri-quadratic hexahedron isoparametric cell with
# vertex-ordering labels, gold sphere glyphs at the vertices, and a
# translucent plinth.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkTriQuadraticHexahedron,
    vtkUnstructuredGrid,
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

# Cell: build from parametric coordinates
cell = vtkTriQuadraticHexahedron()
pc = cell.GetParametricCoords()
for i in range(cell.GetNumberOfPoints()):
    cell.GetPointIds().SetId(i, i)
    cell.GetPoints().SetPoint(i, pc[3 * i], pc[3 * i + 1], pc[3 * i + 2])

# Unstructured grid
grid = vtkUnstructuredGrid()
grid.SetPoints(cell.GetPoints())
grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

# Rotate for 3D viewing
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

# Cell surface property
cell_surface_property = vtkProperty()
cell_surface_property.SetAmbientColor(dark_salmon_rgb)
cell_surface_property.SetDiffuseColor(seashell_rgb)
cell_surface_property.SetSpecularColor(1.0, 1.0, 1.0)
cell_surface_property.SetSpecular(0.5)
cell_surface_property.SetDiffuse(0.7)
cell_surface_property.SetAmbient(0.5)
cell_surface_property.SetSpecularPower(20.0)
cell_surface_property.SetOpacity(0.9)
cell_surface_property.EdgeVisibilityOn()
cell_surface_property.SetLineWidth(3)

mapper = vtkDataSetMapper()
mapper.SetInputData(grid)
actor = vtkActor()
actor.SetMapper(mapper)
actor.SetProperty(cell_surface_property)

# Vertex labels
label_text_property = vtkTextProperty()
label_text_property.BoldOn()
label_text_property.ShadowOn()
label_text_property.SetJustificationToCentered()
label_text_property.SetColor(deep_pink_rgb)
label_text_property.SetFontSize(14)

label_mapper = vtkLabeledDataMapper()
label_mapper.SetInputData(grid)
label_mapper.SetLabelTextProperty(label_text_property)
label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Vertex glyphs: gold spheres
sphere = vtkSphereSource()
sphere.SetPhiResolution(21)
sphere.SetThetaResolution(21)
sphere.SetRadius(0.04)

glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputData(grid)
glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
glyph_mapper.ScalingOn()
glyph_mapper.ScalarVisibilityOff()

point_glyph_property = vtkProperty()
point_glyph_property.SetAmbientColor(gold_rgb)
point_glyph_property.SetDiffuseColor(yellow_rgb)
point_glyph_property.SetSpecularColor(1.0, 1.0, 1.0)
point_glyph_property.SetSpecular(0.5)
point_glyph_property.SetDiffuse(0.7)
point_glyph_property.SetAmbient(0.5)
point_glyph_property.SetSpecularPower(20.0)
point_glyph_property.SetOpacity(1.0)

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.SetProperty(point_glyph_property)

# Plinth: translucent platform beneath the 3D cell
nb = grid.GetBounds()
nd = (nb[1] - nb[0], nb[3] - nb[2], nb[5] - nb[4])
thick = nd[2] * 0.01
plinth_source = vtkCubeSource()
plinth_source.SetCenter((nb[1] + nb[0]) / 2.0, nb[2] - thick / 2.0 - 0.05, (nb[5] + nb[4]) / 2.0)
plinth_source.SetXLength(nd[0] + nd[0] * 0.5)
plinth_source.SetYLength(thick)
plinth_source.SetZLength(nd[2] + nd[2] * 0.5)

plinth_property = vtkProperty()
plinth_property.SetAmbientColor(steel_blue_rgb)
plinth_property.SetDiffuseColor(light_steel_blue_rgb)
plinth_property.SetSpecularColor(1.0, 1.0, 1.0)
plinth_property.SetSpecular(0.5)
plinth_property.SetDiffuse(0.7)
plinth_property.SetAmbient(0.5)
plinth_property.SetSpecularPower(20.0)
plinth_property.SetOpacity(0.8)
plinth_property.EdgeVisibilityOn()
plinth_property.SetLineWidth(1)

plinth_mapper = vtkPolyDataMapper()
plinth_mapper.SetInputConnection(plinth_source.GetOutputPort())
plinth_actor = vtkActor()
plinth_actor.SetMapper(plinth_mapper)
plinth_actor.SetProperty(plinth_property)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(label_actor)
renderer.AddActor(glyph_actor)
renderer.AddActor(plinth_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("IsoParametricCellTriQuadraticHexahedron")

# Interactor
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window_interactor.Initialize()
render_window_interactor.Start()
