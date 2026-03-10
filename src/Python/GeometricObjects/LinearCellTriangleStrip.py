#!/usr/bin/env python

# Render a single triangle strip linear cell with vertex-ordering labels and
# gold sphere glyphs at the vertices.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkTriangleStrip,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
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
deep_pink_rgb = (1.0, 0.078, 0.576)
background_rgb = (0.690, 0.769, 0.871)

# Cell: Triangle Strip with 10 points
sf = 3.0
points = vtkPoints()
points.InsertNextPoint(0 / sf, 0 / sf, 0)
points.InsertNextPoint(1 / sf, -0.1 / sf, 0)
points.InsertNextPoint(0.5 / sf, 1 / sf, 0)
points.InsertNextPoint(2.0 / sf, -0.1 / sf, 0)
points.InsertNextPoint(1.5 / sf, 0.8 / sf, 0)
points.InsertNextPoint(3.0 / sf, 0 / sf, 0)
points.InsertNextPoint(2.5 / sf, 0.9 / sf, 0)
points.InsertNextPoint(4.0 / sf, -0.2 / sf, 0)
points.InsertNextPoint(3.5 / sf, 0.8 / sf, 0)
points.InsertNextPoint(4.5 / sf, 1.1 / sf, 0)

cell = vtkTriangleStrip()
cell.GetPointIds().SetNumberOfIds(10)
for i in range(10):
    cell.GetPointIds().SetId(i, i)

# Unstructured grid
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

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

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(label_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("LinearCellTriangleStrip")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
