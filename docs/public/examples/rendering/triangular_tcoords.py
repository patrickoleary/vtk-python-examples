#!/usr/bin/env python

# Demonstrate vtkTriangularTCoords and vtkTriangularTexture on a sphere
# with a cube for reference.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkFiltersTexture import vtkTriangularTCoords
from vtkmodules.vtkImagingHybrid import vtkTriangularTexture
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

named_colors = vtkNamedColors()

banana_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("banana", banana_rgb)
tomato_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", tomato_rgb)
slate_grey_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("slate_grey", slate_grey_rgb)

# Triangular texture pattern
a_triangular_texture = vtkTriangularTexture()
a_triangular_texture.SetTexturePattern(2)
a_triangular_texture.SetScaleFactor(1.3)
a_triangular_texture.SetXSize(64)
a_triangular_texture.SetYSize(64)

# Sphere source
a_sphere = vtkSphereSource()
a_sphere.SetThetaResolution(20)
a_sphere.SetPhiResolution(20)

# Generate triangular texture coordinates
t_coords = vtkTriangularTCoords()
t_coords.SetInputConnection(a_sphere.GetOutputPort())

triangle_mapper = vtkPolyDataMapper()
triangle_mapper.SetInputConnection(t_coords.GetOutputPort())

a_texture = vtkTexture()
a_texture.SetInputConnection(a_triangular_texture.GetOutputPort())
a_texture.InterpolateOn()

textured_actor = vtkActor()
textured_actor.SetMapper(triangle_mapper)
textured_actor.SetTexture(a_texture)
textured_actor.GetProperty().BackfaceCullingOn()
textured_actor.GetProperty().SetDiffuseColor(banana_rgb)
textured_actor.GetProperty().SetSpecular(0.4)
textured_actor.GetProperty().SetSpecularPower(40)

# Reference cube
a_cube = vtkCubeSource()
a_cube.SetXLength(0.5)
a_cube.SetYLength(0.5)

a_cube_mapper = vtkPolyDataMapper()
a_cube_mapper.SetInputConnection(a_cube.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(a_cube_mapper)
cube_actor.GetProperty().SetDiffuseColor(tomato_rgb)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(slate_grey_rgb)
renderer.AddActor(cube_actor)
renderer.AddActor(textured_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("triangular tcoords")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
