#!/usr/bin/env python

# Create a spring by rotationally extruding a circular cross-section
# with translation and delta-radius to form a helix.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burlywood_background_rgb = (0.871, 0.722, 0.529)
powder_blue_rgb = (0.690, 0.878, 0.902)

# Source: define a circular cross-section for the spring wire
points = vtkPoints()
points.InsertPoint(0, 1.0, 0.0, 0.0)
points.InsertPoint(1, 1.0732, 0.0, -0.1768)
points.InsertPoint(2, 1.25, 0.0, -0.25)
points.InsertPoint(3, 1.4268, 0.0, -0.1768)
points.InsertPoint(4, 1.5, 0.0, 0.00)
points.InsertPoint(5, 1.4268, 0.0, 0.1768)
points.InsertPoint(6, 1.25, 0.0, 0.25)
points.InsertPoint(7, 1.0732, 0.0, 0.1768)

poly = vtkCellArray()
poly.InsertNextCell(8)
poly.InsertCellPoint(0)
poly.InsertCellPoint(1)
poly.InsertCellPoint(2)
poly.InsertCellPoint(3)
poly.InsertCellPoint(4)
poly.InsertCellPoint(5)
poly.InsertCellPoint(6)
poly.InsertCellPoint(7)

profile = vtkPolyData()
profile.SetPoints(points)
profile.SetPolys(poly)

# Filter: rotationally extrude with translation and radius change to form a helix
extrude = vtkRotationalExtrusionFilter()
extrude.SetInputData(profile)
extrude.SetResolution(360)
extrude.SetTranslation(6)
extrude.SetDeltaRadius(1.0)
extrude.SetAngle(2160.0)

# Filter: compute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(extrude.GetOutputPort())
normals.SetFeatureAngle(60)

# Mapper: map the spring surface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

# Actor: the spring with specular highlights
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(powder_blue_rgb)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetSpecularPower(20)
actor.GetProperty().BackfaceCullingOn()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(burlywood_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(90)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Spring")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
