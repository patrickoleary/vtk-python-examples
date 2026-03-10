#!/usr/bin/env python

# Illustrate camera movement around the focal point (azimuth, elevation, roll).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendFilter,
    vtkContourFilter,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkTransformFilter,
    vtkTransformPolyDataFilter,
    vtkWarpTo,
)
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Colors (normalized RGB)
azimuth_color = (1.000, 0.302, 0.302)
elevation_color = (0.302, 1.000, 0.302)
roll_color = (1.000, 1.000, 0.302)
spike_color = (1.000, 0.302, 1.000)
slate_gray = (0.439, 0.502, 0.565)
white = (1.000, 1.000, 1.000)

# Source: camera model — cone lens + cube body
cam_cone = vtkConeSource()
cam_cone.SetHeight(1.5)
cam_cone.SetResolution(12)
cam_cone.SetRadius(0.4)

cam_cube = vtkCubeSource()
cam_cube.SetXLength(1.5)
cam_cube.SetZLength(0.8)
cam_cube.SetCenter(0.4, 0, 0)

cam_append = vtkAppendFilter()
cam_append.AddInputConnection(cam_cube.GetOutputPort())
cam_append.AddInputConnection(cam_cone.GetOutputPort())

cam_mapper = vtkPolyDataMapper()
cam_mapper.SetInputConnection(cam_append.GetOutputPort())

cam_actor = vtkLODActor()
cam_actor.SetMapper(cam_mapper)
cam_actor.SetScale(2, 2, 2)

# Arrow profile: polygon for implicit modelling
arrow_pd = vtkPolyData()
arrow_pts = vtkPoints()
arrow_pts.InsertNextPoint(0, 1, 0)
arrow_pts.InsertNextPoint(8, 1, 0)
arrow_pts.InsertNextPoint(8, 2, 0)
arrow_pts.InsertNextPoint(10, 0.01, 0)
arrow_pts.InsertNextPoint(8, -2, 0)
arrow_pts.InsertNextPoint(8, -1, 0)
arrow_pts.InsertNextPoint(0, -1, 0)
arrow_ca = vtkCellArray()
arrow_ca.InsertNextCell(7)
for pid in range(7):
    arrow_ca.InsertCellPoint(pid)
arrow_pd.SetPoints(arrow_pts)
arrow_pd.SetPolys(arrow_ca)

# Arrow outline: polyline for rotational extrusion (DOP spike)
arrow_pd2 = vtkPolyData()
arrow_pts2 = vtkPoints()
arrow_pts2.InsertNextPoint(0, 1, 0)
arrow_pts2.InsertNextPoint(8, 1, 0)
arrow_pts2.InsertNextPoint(8, 2, 0)
arrow_pts2.InsertNextPoint(10, 0.01, 0)
arrow_ca2 = vtkCellArray()
arrow_ca2.InsertNextCell(4)
for pid in range(4):
    arrow_ca2.InsertCellPoint(pid)
arrow_pd2.SetPoints(arrow_pts2)
arrow_pd2.SetLines(arrow_ca2)

# Filter: implicit model of the arrow shape
arrow_im = vtkImplicitModeller()
arrow_im.SetInputData(arrow_pd)
arrow_im.SetSampleDimensions(50, 20, 8)

# Filter: extract isosurface from the implicit model
arrow_cf = vtkContourFilter()
arrow_cf.SetInputConnection(arrow_im.GetOutputPort())
arrow_cf.SetValue(0, 0.2)

# Filter: warp the contour into a curved arrow
arrow_wt = vtkWarpTo()
arrow_wt.SetInputConnection(arrow_cf.GetOutputPort())
arrow_wt.SetPosition(5, 0, 5)
arrow_wt.SetScaleFactor(0.85)
arrow_wt.AbsoluteOn()

# Transform: rotate and scale the curved arrow
arrow_t = vtkTransform()
arrow_t.RotateY(60)
arrow_t.Translate(-1.33198, 0, -1.479)
arrow_t.Scale(1, 0.5, 1)

arrow_tf = vtkTransformFilter()
arrow_tf.SetInputConnection(arrow_wt.GetOutputPort())
arrow_tf.SetTransform(arrow_t)

arrow_mapper = vtkDataSetMapper()
arrow_mapper.SetInputConnection(arrow_tf.GetOutputPort())
arrow_mapper.ScalarVisibilityOff()

# Actor: azimuth arrow 1
a1_actor = vtkLODActor()
a1_actor.SetMapper(arrow_mapper)
a1_actor.RotateZ(180)
a1_actor.SetPosition(1, 0, -1)
a1_actor.GetProperty().SetColor(azimuth_color)
a1_actor.GetProperty().SetSpecularColor(white)
a1_actor.GetProperty().SetSpecular(0.3)
a1_actor.GetProperty().SetSpecularPower(20)
a1_actor.GetProperty().SetAmbient(0.2)
a1_actor.GetProperty().SetDiffuse(0.8)

# Actor: azimuth arrow 2
a2_actor = vtkLODActor()
a2_actor.SetMapper(arrow_mapper)
a2_actor.RotateZ(180)
a2_actor.RotateX(180)
a2_actor.SetPosition(1, 0, 1)
a2_actor.GetProperty().SetColor(azimuth_color)
a2_actor.GetProperty().SetSpecularColor(white)
a2_actor.GetProperty().SetSpecular(0.3)
a2_actor.GetProperty().SetSpecularPower(20)
a2_actor.GetProperty().SetAmbient(0.2)
a2_actor.GetProperty().SetDiffuse(0.8)

# Actor: elevation arrow 1
a3_actor = vtkLODActor()
a3_actor.SetMapper(arrow_mapper)
a3_actor.RotateZ(180)
a3_actor.RotateX(90)
a3_actor.SetPosition(1, -1, 0)
a3_actor.GetProperty().SetColor(elevation_color)
a3_actor.GetProperty().SetSpecularColor(white)
a3_actor.GetProperty().SetSpecular(0.3)
a3_actor.GetProperty().SetSpecularPower(20)
a3_actor.GetProperty().SetAmbient(0.2)
a3_actor.GetProperty().SetDiffuse(0.8)

# Actor: elevation arrow 2
a4_actor = vtkLODActor()
a4_actor.SetMapper(arrow_mapper)
a4_actor.RotateZ(180)
a4_actor.RotateX(-90)
a4_actor.SetPosition(1, 1, 0)
a4_actor.GetProperty().SetColor(elevation_color)
a4_actor.GetProperty().SetSpecularColor(white)
a4_actor.GetProperty().SetSpecular(0.3)
a4_actor.GetProperty().SetSpecularPower(20)
a4_actor.GetProperty().SetAmbient(0.2)
a4_actor.GetProperty().SetDiffuse(0.8)

# DOP spike: rotational extrusion of arrow outline
arrow_t2 = vtkTransform()
arrow_t2.Scale(1, 0.6, 1)
arrow_t2.RotateY(90)

arrow_tf2 = vtkTransformPolyDataFilter()
arrow_tf2.SetInputData(arrow_pd2)
arrow_tf2.SetTransform(arrow_t2)

arrow_ref = vtkRotationalExtrusionFilter()
arrow_ref.SetInputConnection(arrow_tf2.GetOutputPort())
arrow_ref.CappingOff()
arrow_ref.SetResolution(30)

spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(arrow_ref.GetOutputPort())

# Actor: direction-of-projection spike
a5_actor = vtkLODActor()
a5_actor.SetMapper(spike_mapper)
a5_actor.SetScale(0.3, 0.3, 0.6)
a5_actor.RotateY(90)
a5_actor.SetPosition(-2, 0, 0)
a5_actor.GetProperty().SetColor(spike_color)
a5_actor.GetProperty().SetAmbient(0.2)
a5_actor.GetProperty().SetDiffuse(0.8)

# Source: focal point sphere
fp_source = vtkSphereSource()
fp_source.SetRadius(0.5)

fp_mapper = vtkPolyDataMapper()
fp_mapper.SetInputConnection(fp_source.GetOutputPort())

fp_actor = vtkLODActor()
fp_actor.SetMapper(fp_mapper)
fp_actor.SetPosition(-9, 0, 0)
fp_actor.GetProperty().SetSpecularColor(white)
fp_actor.GetProperty().SetSpecular(0.3)
fp_actor.GetProperty().SetAmbient(0.2)
fp_actor.GetProperty().SetDiffuse(0.8)
fp_actor.GetProperty().SetSpecularPower(20)

# Roll arrows: warp the contour into tighter curve
arrow_wt2 = vtkWarpTo()
arrow_wt2.SetInputConnection(arrow_cf.GetOutputPort())
arrow_wt2.SetPosition(5, 0, 2.5)
arrow_wt2.SetScaleFactor(0.95)
arrow_wt2.AbsoluteOn()

arrow_t3 = vtkTransform()
arrow_t3.Translate(-2.50358, 0, -1.70408)
arrow_t3.Scale(0.5, 0.3, 1)

arrow_tf3 = vtkTransformFilter()
arrow_tf3.SetInputConnection(arrow_wt2.GetOutputPort())
arrow_tf3.SetTransform(arrow_t3)

arrow_mapper2 = vtkDataSetMapper()
arrow_mapper2.SetInputConnection(arrow_tf3.GetOutputPort())
arrow_mapper2.ScalarVisibilityOff()

# Actor: roll arrow
a6_actor = vtkLODActor()
a6_actor.SetMapper(arrow_mapper2)
a6_actor.RotateZ(90)
a6_actor.SetPosition(-4, 0, 0)
a6_actor.SetScale(1.5, 1.5, 1.5)
a6_actor.GetProperty().SetColor(roll_color)
a6_actor.GetProperty().SetSpecularColor(white)
a6_actor.GetProperty().SetSpecular(0.3)
a6_actor.GetProperty().SetSpecularPower(20)
a6_actor.GetProperty().SetAmbient(0.2)
a6_actor.GetProperty().SetDiffuse(0.8)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cam_actor)
renderer.AddActor(a1_actor)
renderer.AddActor(a2_actor)
renderer.AddActor(a3_actor)
renderer.AddActor(a4_actor)
renderer.AddActor(a5_actor)
renderer.AddActor(a6_actor)
renderer.AddActor(fp_actor)
renderer.SetBackground(slate_gray)

renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(150)
camera.Elevation(30)
camera.Dolly(1.5)
renderer.ResetCameraClippingRange()

# Text: label for azimuth
text_azimuth = vtkTextActor()
text_azimuth.SetInput("Azimuth")
tp = text_azimuth.GetTextProperty()
tp.SetFontFamilyToArial()
tp.ShadowOff()
tp.SetLineSpacing(1.0)
tp.SetFontSize(36)
tp.SetColor(azimuth_color)
text_azimuth.SetDisplayPosition(20, 50)
renderer.AddViewProp(text_azimuth)

# Text: label for elevation
text_elevation = vtkTextActor()
text_elevation.SetInput("Elevation")
tp2 = text_elevation.GetTextProperty()
tp2.SetFontFamilyToArial()
tp2.ShadowOff()
tp2.SetLineSpacing(1.0)
tp2.SetFontSize(36)
tp2.SetColor(elevation_color)
text_elevation.SetDisplayPosition(20, 100)
renderer.AddViewProp(text_elevation)

# Text: label for roll
text_roll = vtkTextActor()
text_roll.SetInput("Roll")
tp3 = text_roll.GetTextProperty()
tp3.SetFontFamilyToArial()
tp3.ShadowOff()
tp3.SetLineSpacing(1.0)
tp3.SetFontSize(36)
tp3.SetColor(roll_color)
text_roll.SetDisplayPosition(20, 150)
renderer.AddViewProp(text_roll)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CameraModel1")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
