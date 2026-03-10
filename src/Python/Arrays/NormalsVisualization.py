#!/usr/bin/env python

# Visualize surface normals as arrow glyphs on a sphere, colored by
# the normal Z component to show directional variation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a sphere with normals
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.Update()

# Extract the Z component of each normal for scalar coloring
polydata = sphere.GetOutput()
normals = polydata.GetPointData().GetNormals()
num_points = polydata.GetNumberOfPoints()

z_component = vtkFloatArray()
z_component.SetName("NormalZ")
z_component.SetNumberOfTuples(num_points)
for i in range(num_points):
    nz = normals.GetTuple3(i)[2]
    z_component.SetValue(i, nz)
polydata.GetPointData().AddArray(z_component)
polydata.GetPointData().SetActiveScalars("NormalZ")

# Arrow source: glyph shape for normals
arrow = vtkArrowSource()
arrow.SetTipResolution(16)
arrow.SetShaftResolution(16)

# Glyph: place an arrow at each point oriented along the surface normal
glyph = vtkGlyph3D()
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetInputData(polydata)
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByScalar()
glyph.SetScaleFactor(0.15)
glyph.OrientOn()
glyph.SetColorModeToColorByScalar()

# Lookup table: map normal Z values to a diverging color ramp
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.SetRange(-1.0, 1.0)
lut.Build()

# Mapper: map the arrow glyphs to graphics primitives
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.SetLookupTable(lut)
glyph_mapper.SetScalarRange(-1.0, 1.0)

# Actor: assign the glyph geometry
glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Mapper: map the sphere surface
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputData(polydata)
sphere_mapper.ScalarVisibilityOff()

# Actor: assign the sphere with semi-transparent appearance
back_face = vtkProperty()
back_face.SetColor(tomato_rgb)
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(peach_puff_rgb)
sphere_actor.GetProperty().SetOpacity(0.4)
sphere_actor.SetBackfaceProperty(back_face)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("NormalsVisualization")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
