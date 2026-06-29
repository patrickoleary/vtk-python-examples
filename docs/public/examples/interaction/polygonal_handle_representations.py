#!/usr/bin/env python
# Demonstrate various polygonal handle representations on a terrain surface.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersSources import vtkGlyphSource2D, vtkSphereSource
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkInteractionWidgets import (
    vtkHandleWidget,
    vtkOrientedPolygonalHandleRepresentation3D,
    vtkPointHandleRepresentation3D,
    vtkPolygonalHandleRepresentation3D,
    vtkPolygonalSurfacePointPlacer,
)
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

# Filters
resample = vtkImageResample()
resample.SetInputConnection(dem_reader.GetOutputPort())
resample.SetDimensionality(2)
resample.SetAxisMagnificationFactor(0, 1)
resample.SetAxisMagnificationFactor(1, 1)

surface = vtkImageDataGeometryFilter()
surface.SetInputConnection(resample.GetOutputPort())

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(surface.GetOutputPort())
triangle_filter.Update()

warp = vtkWarpScalar()
warp.SetInputConnection(triangle_filter.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)
warp.Update()

lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

poly_normals = vtkPolyDataNormals()
poly_normals.SetInputConnection(warp.GetOutputPort())
poly_normals.SetFeatureAngle(60)
poly_normals.SplittingOff()
poly_normals.ComputeCellNormalsOn()
poly_normals.Update()

normals_output = poly_normals.GetOutput()

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(poly_normals.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(lookup_table)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polygonal handle representations")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget 1: Vertex glyph (shape=1, color=(1/3, 2/3, 1))
vertex_glyph = vtkGlyphSource2D()
vertex_glyph.SetGlyphType(1)
vertex_glyph.SetScale(600)
vertex_glyph.Update()

vertex_rep = vtkOrientedPolygonalHandleRepresentation3D()
vertex_rep.SetHandle(vertex_glyph.GetOutput())
vertex_rep.SetWorldPosition((561909, 5.11921e+06, 4381.48))
vertex_rep.GetProperty().SetColor(1.0 / 3.0, 2.0 / 3.0, 1.0)
vertex_rep.GetProperty().SetLineWidth(1.0)
vertex_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
vertex_rep.SetLabelVisibility(1)
vertex_rep.SetLabelText("Vertex")

vertex_widget = vtkHandleWidget()
vertex_widget.SetInteractor(interactor)
vertex_widget.SetRepresentation(vertex_rep)
vertex_widget.EnabledOn()

# Widget 2: Dash glyph (shape=2, color=(2/3, 5/6, 0))
dash_glyph = vtkGlyphSource2D()
dash_glyph.SetGlyphType(2)
dash_glyph.SetScale(600)
dash_glyph.Update()

dash_rep = vtkOrientedPolygonalHandleRepresentation3D()
dash_rep.SetHandle(dash_glyph.GetOutput())
dash_rep.SetWorldPosition((559400, 5.11064e+06, 2323.25))
dash_rep.GetProperty().SetColor(2.0 / 3.0, 5.0 / 6.0, 0.0)
dash_rep.GetProperty().SetLineWidth(1.0)
dash_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
dash_rep.SetLabelVisibility(1)
dash_rep.SetLabelText("Dash")

dash_widget = vtkHandleWidget()
dash_widget.SetInteractor(interactor)
dash_widget.SetRepresentation(dash_rep)
dash_widget.EnabledOn()

# Widget 3: Cross glyph (shape=3, color=(0, 1, 1))
cross_glyph = vtkGlyphSource2D()
cross_glyph.SetGlyphType(3)
cross_glyph.SetScale(600)
cross_glyph.Update()

cross_rep = vtkOrientedPolygonalHandleRepresentation3D()
cross_rep.SetHandle(cross_glyph.GetOutput())
cross_rep.SetWorldPosition((563531, 5.11924e+06, 5202.51))
cross_rep.GetProperty().SetColor(0.0, 1.0, 1.0)
cross_rep.GetProperty().SetLineWidth(1.0)
cross_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
cross_rep.SetLabelVisibility(1)
cross_rep.SetLabelText("cross")

cross_widget = vtkHandleWidget()
cross_widget.SetInteractor(interactor)
cross_widget.SetRepresentation(cross_rep)
cross_widget.EnabledOn()

# Widget 4: Thick cross glyph (shape=4, color=(0, 1/6, 0))
thick_cross_glyph = vtkGlyphSource2D()
thick_cross_glyph.SetGlyphType(4)
thick_cross_glyph.SetScale(600)
thick_cross_glyph.Update()

thick_cross_rep = vtkOrientedPolygonalHandleRepresentation3D()
thick_cross_rep.SetHandle(thick_cross_glyph.GetOutput())
thick_cross_rep.SetWorldPosition((563300, 5.11729e+06, 4865.47))
thick_cross_rep.GetProperty().SetColor(0.0, 1.0 / 6.0, 0.0)
thick_cross_rep.GetProperty().SetLineWidth(1.0)
thick_cross_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
thick_cross_rep.SetLabelVisibility(1)
thick_cross_rep.SetLabelText("Thick Cross")

thick_cross_widget = vtkHandleWidget()
thick_cross_widget.SetInteractor(interactor)
thick_cross_widget.SetRepresentation(thick_cross_rep)
thick_cross_widget.EnabledOn()

# Widget 5: Triangle glyph (shape=5, color=(1/3, 1/3, 1))
triangle_glyph = vtkGlyphSource2D()
triangle_glyph.SetGlyphType(5)
triangle_glyph.SetScale(600)
triangle_glyph.Update()

triangle_rep = vtkOrientedPolygonalHandleRepresentation3D()
triangle_rep.SetHandle(triangle_glyph.GetOutput())
triangle_rep.SetWorldPosition((564392, 5.11248e+06, 3936.91))
triangle_rep.GetProperty().SetColor(1.0 / 3.0, 1.0 / 3.0, 1.0)
triangle_rep.GetProperty().SetLineWidth(1.0)
triangle_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
triangle_rep.SetLabelVisibility(1)
triangle_rep.SetLabelText("triangle")

triangle_widget = vtkHandleWidget()
triangle_widget.SetInteractor(interactor)
triangle_widget.SetRepresentation(triangle_rep)
triangle_widget.EnabledOn()

# Widget 6: Square glyph (shape=6, color=(2/3, 1/2, 0))
square_glyph = vtkGlyphSource2D()
square_glyph.SetGlyphType(6)
square_glyph.SetScale(600)
square_glyph.Update()

square_rep = vtkOrientedPolygonalHandleRepresentation3D()
square_rep.SetHandle(square_glyph.GetOutput())
square_rep.SetWorldPosition((563715, 5.11484e+06, 4345.68))
square_rep.GetProperty().SetColor(2.0 / 3.0, 1.0 / 2.0, 0.0)
square_rep.GetProperty().SetLineWidth(1.0)
square_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
square_rep.SetLabelVisibility(1)
square_rep.SetLabelText("square")

square_widget = vtkHandleWidget()
square_widget.SetInteractor(interactor)
square_widget.SetRepresentation(square_rep)
square_widget.EnabledOn()

# Widget 7: Circle glyph (shape=7, color=(0, 2/3, 1))
circle_glyph = vtkGlyphSource2D()
circle_glyph.SetGlyphType(7)
circle_glyph.SetScale(600)
circle_glyph.Update()

circle_rep = vtkOrientedPolygonalHandleRepresentation3D()
circle_rep.SetHandle(circle_glyph.GetOutput())
circle_rep.SetWorldPosition((564705, 5.10849e+06, 2335.16))
circle_rep.GetProperty().SetColor(0.0, 2.0 / 3.0, 1.0)
circle_rep.GetProperty().SetLineWidth(1.0)
circle_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
circle_rep.SetLabelVisibility(1)
circle_rep.SetLabelText("circle")

circle_widget = vtkHandleWidget()
circle_widget.SetInteractor(interactor)
circle_widget.SetRepresentation(circle_rep)
circle_widget.EnabledOn()

# Widget 8: Diamond glyph (shape=8, color=(0, 5/6, 0))
diamond_glyph = vtkGlyphSource2D()
diamond_glyph.SetGlyphType(8)
diamond_glyph.SetScale(600)
diamond_glyph.Update()

diamond_rep = vtkOrientedPolygonalHandleRepresentation3D()
diamond_rep.SetHandle(diamond_glyph.GetOutput())
diamond_rep.SetWorldPosition((560823, 5.1202e+06, 3783.94))
diamond_rep.GetProperty().SetColor(0.0, 5.0 / 6.0, 0.0)
diamond_rep.GetProperty().SetLineWidth(1.0)
diamond_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
diamond_rep.SetLabelVisibility(1)
diamond_rep.SetLabelText("diamond")

diamond_widget = vtkHandleWidget()
diamond_widget.SetInteractor(interactor)
diamond_widget.SetRepresentation(diamond_rep)
diamond_widget.EnabledOn()

# Widget 9: Arrow glyph (shape=9, color=(1/3, 1, 1))
arrow_glyph = vtkGlyphSource2D()
arrow_glyph.SetGlyphType(9)
arrow_glyph.SetScale(600)
arrow_glyph.Update()

arrow_rep = vtkOrientedPolygonalHandleRepresentation3D()
arrow_rep.SetHandle(arrow_glyph.GetOutput())
arrow_rep.SetWorldPosition((559637, 5.12068e+06, 2718.66))
arrow_rep.GetProperty().SetColor(1.0 / 3.0, 1.0, 1.0)
arrow_rep.GetProperty().SetLineWidth(1.0)
arrow_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
arrow_rep.SetLabelVisibility(1)
arrow_rep.SetLabelText("arrow")

arrow_widget = vtkHandleWidget()
arrow_widget.SetInteractor(interactor)
arrow_widget.SetRepresentation(arrow_rep)
arrow_widget.EnabledOn()

# Widget 10: Thick arrow glyph (shape=10, color=(2/3, 1/6, 0))
thick_arrow_glyph = vtkGlyphSource2D()
thick_arrow_glyph.SetGlyphType(10)
thick_arrow_glyph.SetScale(600)
thick_arrow_glyph.Update()

thick_arrow_rep = vtkOrientedPolygonalHandleRepresentation3D()
thick_arrow_rep.SetHandle(thick_arrow_glyph.GetOutput())
thick_arrow_rep.SetWorldPosition((560597, 5.10817e+06, 3582.44))
thick_arrow_rep.GetProperty().SetColor(2.0 / 3.0, 1.0 / 6.0, 0.0)
thick_arrow_rep.GetProperty().SetLineWidth(1.0)
thick_arrow_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
thick_arrow_rep.SetLabelVisibility(1)
thick_arrow_rep.SetLabelText("thickArrow")

thick_arrow_widget = vtkHandleWidget()
thick_arrow_widget.SetInteractor(interactor)
thick_arrow_widget.SetRepresentation(thick_arrow_rep)
thick_arrow_widget.EnabledOn()

# Widget 11: Hooked arrow glyph (shape=11, color=(0, 1/3, 1))
hooked_arrow_glyph = vtkGlyphSource2D()
hooked_arrow_glyph.SetGlyphType(11)
hooked_arrow_glyph.SetScale(600)
hooked_arrow_glyph.Update()

hooked_arrow_rep = vtkOrientedPolygonalHandleRepresentation3D()
hooked_arrow_rep.SetHandle(hooked_arrow_glyph.GetOutput())
hooked_arrow_rep.SetWorldPosition((558266, 5.12137e+06, 2559.14))
hooked_arrow_rep.GetProperty().SetColor(0.0, 1.0 / 3.0, 1.0)
hooked_arrow_rep.GetProperty().SetLineWidth(1.0)
hooked_arrow_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
hooked_arrow_rep.SetLabelVisibility(1)
hooked_arrow_rep.SetLabelText("hookedArrow")

hooked_arrow_widget = vtkHandleWidget()
hooked_arrow_widget.SetInteractor(interactor)
hooked_arrow_widget.SetRepresentation(hooked_arrow_rep)
hooked_arrow_widget.EnabledOn()

# Widget 12: Edge arrow glyph (shape=12, color=(0, 1/2, 0))
edge_arrow_glyph = vtkGlyphSource2D()
edge_arrow_glyph.SetGlyphType(12)
edge_arrow_glyph.SetScale(600)
edge_arrow_glyph.Update()

edge_arrow_rep = vtkOrientedPolygonalHandleRepresentation3D()
edge_arrow_rep.SetHandle(edge_arrow_glyph.GetOutput())
edge_arrow_rep.SetWorldPosition((568869, 5.11028e+06, 2026.57))
edge_arrow_rep.GetProperty().SetColor(0.0, 1.0 / 2.0, 0.0)
edge_arrow_rep.GetProperty().SetLineWidth(1.0)
edge_arrow_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
edge_arrow_rep.SetLabelVisibility(1)
edge_arrow_rep.SetLabelText("EdgeArrow")

edge_arrow_widget = vtkHandleWidget()
edge_arrow_widget.SetInteractor(interactor)
edge_arrow_widget.SetRepresentation(edge_arrow_rep)
edge_arrow_widget.EnabledOn()

# Widget 13: Sphere constrained to surface (shape=12, color=(0, 1/2, 0))
constrained_sphere = vtkSphereSource()
constrained_sphere.SetThetaResolution(10)
constrained_sphere.SetPhiResolution(10)
constrained_sphere.SetRadius(300.0)
constrained_sphere.Update()

constrained_rep = vtkPolygonalHandleRepresentation3D()
constrained_rep.SetHandle(constrained_sphere.GetOutput())
constrained_rep.SetWorldPosition((561753, 5.11577e+06, 3183))

constrained_placer = vtkPolygonalSurfacePointPlacer()
constrained_placer.AddProp(dem_actor)
constrained_placer.GetPolys().AddItem(normals_output)
constrained_placer.SetDistanceOffset(100.0)
constrained_rep.SetPointPlacer(constrained_placer)

constrained_rep.GetProperty().SetColor(0.0, 1.0 / 2.0, 0.0)
constrained_rep.GetProperty().SetLineWidth(1.0)
constrained_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)
constrained_rep.SetLabelVisibility(1)
constrained_rep.SetLabelText("Sphere constrained to surface")

constrained_widget = vtkHandleWidget()
constrained_widget.SetInteractor(interactor)
constrained_widget.SetRepresentation(constrained_rep)
constrained_widget.EnableAxisConstraintOff()
constrained_widget.EnabledOn()

# Widget 14: Crosshair point handle (shape=13, color=(1/3, 2/3, 1))
crosshair_rep = vtkPointHandleRepresentation3D()
crosshair_rep.SetWorldPosition((562692, 5.11521e+06, 3355.65))
crosshair_rep.GetProperty().SetColor(1.0 / 3.0, 2.0 / 3.0, 1.0)
crosshair_rep.GetProperty().SetLineWidth(1.0)
crosshair_rep.GetSelectedProperty().SetColor(1.0, 0.0, 0.0)

crosshair_widget = vtkHandleWidget()
crosshair_widget.SetInteractor(interactor)
crosshair_widget.SetRepresentation(crosshair_rep)
crosshair_widget.EnabledOn()

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
