#!/usr/bin/env python

# Demonstrate a camera model built from cones, cubes, arrows, and spheres
# using vtkRotationalExtrusionFilter, vtkImplicitModeller, vtkWarpTo, and
# various transforms to create azimuth, elevation, roll, and DOP arrows.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendFilter, vtkContourFilter
from vtkmodules.vtkFiltersGeneral import (
    vtkTransformFilter,
    vtkTransformPolyDataFilter,
    vtkWarpTo,
)
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Camera model: cone + cube
camera_cone = vtkConeSource()
camera_cone.SetHeight(1.5)
camera_cone.SetResolution(12)
camera_cone.SetRadius(0.4)

camera_cube = vtkCubeSource()
camera_cube.SetXLength(1.5)
camera_cube.SetZLength(0.8)
camera_cube.SetCenter(0.4, 0, 0)

camera_append = vtkAppendFilter()
camera_append.AddInputConnection(camera_cone.GetOutputPort())
camera_append.AddInputConnection(camera_cube.GetOutputPort())

# Arrow polygon for implicit modelling
arrow_poly = vtkPolyData()
arrow_cells = vtkCellArray()
arrow_points = vtkPoints()
arrow_points.InsertNextPoint(0, 1, 0)
arrow_points.InsertNextPoint(8, 1, 0)
arrow_points.InsertNextPoint(8, 2, 0)
arrow_points.InsertNextPoint(10, 0.01, 0)
arrow_points.InsertNextPoint(8, -2, 0)
arrow_points.InsertNextPoint(8, -1, 0)
arrow_points.InsertNextPoint(0, -1, 0)
arrow_cells.InsertNextCell(7)
arrow_cells.InsertCellPoint(0)
arrow_cells.InsertCellPoint(1)
arrow_cells.InsertCellPoint(2)
arrow_cells.InsertCellPoint(3)
arrow_cells.InsertCellPoint(4)
arrow_cells.InsertCellPoint(5)
arrow_cells.InsertCellPoint(6)
arrow_poly.SetPoints(arrow_points)
arrow_poly.SetPolys(arrow_cells)

# Half-arrow for DOP
half_arrow_poly = vtkPolyData()
half_arrow_cells = vtkCellArray()
half_arrow_points = vtkPoints()
half_arrow_points.InsertNextPoint(0, 1, 0)
half_arrow_points.InsertNextPoint(8, 1, 0)
half_arrow_points.InsertNextPoint(8, 2, 0)
half_arrow_points.InsertNextPoint(10, 0.01, 0)
half_arrow_cells.InsertNextCell(4)
half_arrow_cells.InsertCellPoint(0)
half_arrow_cells.InsertCellPoint(1)
half_arrow_cells.InsertCellPoint(2)
half_arrow_cells.InsertCellPoint(3)
half_arrow_poly.SetPoints(half_arrow_points)
half_arrow_poly.SetLines(half_arrow_cells)

# Implicit model of arrow -> contour -> warp -> transform
arrow_im = vtkImplicitModeller()
arrow_im.SetInputData(arrow_poly)
arrow_im.SetSampleDimensions(50, 20, 8)

arrow_contour = vtkContourFilter()
arrow_contour.SetInputConnection(arrow_im.GetOutputPort())
arrow_contour.SetValue(0, 0.2)

arrow_warp = vtkWarpTo()
arrow_warp.SetInputConnection(arrow_contour.GetOutputPort())
arrow_warp.SetPosition(5, 0, 5)
arrow_warp.SetScaleFactor(0.85)
arrow_warp.AbsoluteOn()

arrow_transform = vtkTransform()
arrow_transform.RotateY(60)
arrow_transform.Translate(-1.33198, 0, -1.479)
arrow_transform.Scale(1, 0.5, 1)

arrow_transform_filter = vtkTransformFilter()
arrow_transform_filter.SetInputConnection(arrow_warp.GetOutputPort())
arrow_transform_filter.SetTransform(arrow_transform)

# Direction of projection (DOP) arrow via rotational extrusion
arrow_transform_2 = vtkTransform()
arrow_transform_2.Scale(1, 0.6, 1)
arrow_transform_2.RotateY(90)

arrow_transform_filter_2 = vtkTransformPolyDataFilter()
arrow_transform_filter_2.SetInputData(half_arrow_poly)
arrow_transform_filter_2.SetTransform(arrow_transform_2)

arrow_extrusion = vtkRotationalExtrusionFilter()
arrow_extrusion.SetInputConnection(arrow_transform_filter_2.GetOutputPort())
arrow_extrusion.CappingOff()
arrow_extrusion.SetResolution(30)

# Focal point sphere
focal_sphere = vtkSphereSource()
focal_sphere.SetRadius(0.5)

# Roll arrows (yellow)
arrow_warp_2 = vtkWarpTo()
arrow_warp_2.SetInputConnection(arrow_contour.GetOutputPort())
arrow_warp_2.SetPosition(5, 0, 2.5)
arrow_warp_2.SetScaleFactor(0.95)
arrow_warp_2.AbsoluteOn()

arrow_transform_3 = vtkTransform()
arrow_transform_3.Translate(-2.50358, 0, -1.70408)
arrow_transform_3.Scale(0.5, 0.3, 1)

arrow_transform_filter_3 = vtkTransformFilter()
arrow_transform_filter_3.SetInputConnection(arrow_warp_2.GetOutputPort())
arrow_transform_filter_3.SetTransform(arrow_transform_3)

# Mapper and actor pairs
camera_mapper = vtkDataSetMapper()
camera_mapper.SetInputConnection(camera_append.GetOutputPort())
camera_actor = vtkLODActor()
camera_actor.SetMapper(camera_mapper)
camera_actor.SetScale(2, 2, 2)

arrow_mapper = vtkDataSetMapper()
arrow_mapper.SetInputConnection(arrow_transform_filter.GetOutputPort())
arrow_mapper.ScalarVisibilityOff()

# Azimuth arrows (red)
a1_actor = vtkLODActor()
a1_actor.SetMapper(arrow_mapper)
a1_actor.RotateZ(180)
a1_actor.SetPosition(1, 0, -1)
a1_actor.GetProperty().SetColor(1, 0.3, 0.3)
a1_actor.GetProperty().SetSpecularColor(1, 1, 1)
a1_actor.GetProperty().SetSpecular(0.3)
a1_actor.GetProperty().SetSpecularPower(20)
a1_actor.GetProperty().SetAmbient(0.2)
a1_actor.GetProperty().SetDiffuse(0.8)

a2_actor = vtkLODActor()
a2_actor.SetMapper(arrow_mapper)
a2_actor.RotateZ(180)
a2_actor.RotateX(180)
a2_actor.SetPosition(1, 0, 1)
a2_actor.GetProperty().SetColor(1, 0.3, 0.3)
a2_actor.GetProperty().SetSpecularColor(1, 1, 1)
a2_actor.GetProperty().SetSpecular(0.3)
a2_actor.GetProperty().SetSpecularPower(20)
a2_actor.GetProperty().SetAmbient(0.2)
a2_actor.GetProperty().SetDiffuse(0.8)

# Elevation arrows (green)
a3_actor = vtkLODActor()
a3_actor.SetMapper(arrow_mapper)
a3_actor.RotateZ(180)
a3_actor.RotateX(90)
a3_actor.SetPosition(1, -1, 0)
a3_actor.GetProperty().SetColor(0.3, 1, 0.3)
a3_actor.GetProperty().SetSpecularColor(1, 1, 1)
a3_actor.GetProperty().SetSpecular(0.3)
a3_actor.GetProperty().SetSpecularPower(20)
a3_actor.GetProperty().SetAmbient(0.2)
a3_actor.GetProperty().SetDiffuse(0.8)

a4_actor = vtkLODActor()
a4_actor.SetMapper(arrow_mapper)
a4_actor.RotateZ(180)
a4_actor.RotateX(-90)
a4_actor.SetPosition(1, 1, 0)
a4_actor.GetProperty().SetColor(0.3, 1, 0.3)
a4_actor.GetProperty().SetSpecularColor(1, 1, 1)
a4_actor.GetProperty().SetSpecular(0.3)
a4_actor.GetProperty().SetSpecularPower(20)
a4_actor.GetProperty().SetAmbient(0.2)
a4_actor.GetProperty().SetDiffuse(0.8)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(arrow_extrusion.GetOutputPort())
a5_actor = vtkLODActor()
a5_actor.SetMapper(spike_mapper)
a5_actor.SetScale(0.3, 0.3, 0.6)
a5_actor.RotateY(90)
a5_actor.SetPosition(-2, 0, 0)
a5_actor.GetProperty().SetColor(1, 0.3, 1)
a5_actor.GetProperty().SetAmbient(0.2)
a5_actor.GetProperty().SetDiffuse(0.8)

fp_mapper = vtkPolyDataMapper()
fp_mapper.SetInputConnection(focal_sphere.GetOutputPort())
fp_actor = vtkLODActor()
fp_actor.SetMapper(fp_mapper)
fp_actor.SetPosition(-9, 0, 0)
fp_actor.GetProperty().SetSpecularColor(1, 1, 1)
fp_actor.GetProperty().SetSpecular(0.3)
fp_actor.GetProperty().SetAmbient(0.2)
fp_actor.GetProperty().SetDiffuse(0.8)
fp_actor.GetProperty().SetSpecularPower(20)

arrow_mapper_2 = vtkDataSetMapper()
arrow_mapper_2.SetInputConnection(arrow_transform_filter_3.GetOutputPort())
arrow_mapper_2.ScalarVisibilityOff()
a6_actor = vtkLODActor()
a6_actor.SetMapper(arrow_mapper_2)
a6_actor.RotateZ(90)
a6_actor.SetPosition(-4, 0, 0)
a6_actor.SetScale(1.5, 1.5, 1.5)
a6_actor.GetProperty().SetColor(1, 1, 0.3)
a6_actor.GetProperty().SetSpecularColor(1, 1, 1)
a6_actor.GetProperty().SetSpecular(0.3)
a6_actor.GetProperty().SetSpecularPower(20)
a6_actor.GetProperty().SetAmbient(0.2)
a6_actor.GetProperty().SetDiffuse(0.8)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(camera_actor)
renderer.AddActor(a1_actor)
renderer.AddActor(a2_actor)
renderer.AddActor(a3_actor)
renderer.AddActor(a4_actor)
renderer.AddActor(a5_actor)
renderer.AddActor(a6_actor)
renderer.AddActor(fp_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("camera")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Zoom(1.5)
camera.Azimuth(150)
camera.Elevation(30)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
