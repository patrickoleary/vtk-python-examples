#!/usr/bin/env python

# Clip a sphere with a plane and cap the open boundary by converting
# the boundary edge loop into a filled polygon using vtkFeatureEdges
# and vtkStripper.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkFeatureEdges,
    vtkStripper,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
steel_blue_background_rgb = (0.275, 0.510, 0.706)
tomato_rgb = (1.000, 0.388, 0.278)
banana_rgb = (0.890, 0.812, 0.341)

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(11)
sphere.Update()

# Clip plane: diagonal plane through the sphere center
clip_plane = vtkPlane()
clip_plane.SetOrigin(sphere.GetOutput().GetCenter())
clip_plane.SetNormal(1.0, -1.0, -1.0)

# Clip: remove the portion on the positive side of the plane
clipper = vtkClipPolyData()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetClipFunction(clip_plane)
clipper.SetValue(0)
clipper.Update()

clipped_poly = clipper.GetOutput()

# Mapper: clipped surface
clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputData(clipped_poly)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetDiffuseColor(tomato_rgb)
clip_actor.GetProperty().SetInterpolationToFlat()
clip_actor.GetProperty().EdgeVisibilityOn()

# FeatureEdges: extract the boundary edge loop of the clipped surface
boundary_edges = vtkFeatureEdges()
boundary_edges.SetInputData(clipped_poly)
boundary_edges.BoundaryEdgesOn()
boundary_edges.FeatureEdgesOff()
boundary_edges.NonManifoldEdgesOff()
boundary_edges.ManifoldEdgesOff()

# Stripper: join boundary edges into continuous polylines
boundary_strips = vtkStripper()
boundary_strips.SetInputConnection(boundary_edges.GetOutputPort())
boundary_strips.Update()

# Cap: convert the polyline loop into a filled polygon
boundary_poly = vtkPolyData()
boundary_poly.SetPoints(boundary_strips.GetOutput().GetPoints())
boundary_poly.SetPolys(boundary_strips.GetOutput().GetLines())

boundary_mapper = vtkPolyDataMapper()
boundary_mapper.SetInputData(boundary_poly)

boundary_actor = vtkActor()
boundary_actor.SetMapper(boundary_mapper)
boundary_actor.GetProperty().SetDiffuseColor(banana_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(boundary_actor)
renderer.SetBackground(steel_blue_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CapClip")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
