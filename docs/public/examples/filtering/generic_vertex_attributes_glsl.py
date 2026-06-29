#!/usr/bin/env python

# Test custom GLSL shader replacements on a sphere with random vectors.
# Modern replacement for the removed LoadMaterialFromString API.
# Uses vtkShaderProperty.AddVertexShaderReplacement /
# AddFragmentShaderReplacement to inject custom GLSL code.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere with random vectors
sphere_source = vtkSphereSource()
sphere_source.SetRadius(5)
sphere_source.SetPhiResolution(20)
sphere_source.SetThetaResolution(20)

random_vectors = vtkBrownianPoints()
random_vectors.SetMinimumSpeed(0)
random_vectors.SetMaximumSpeed(1)
random_vectors.SetInputConnection(sphere_source.GetOutputPort())

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(random_vectors.GetOutputPort())
sphere_mapper.MapDataArrayToVertexAttribute("genAttrVector", "BrownianVectors", 0, -1)

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Use vtkShaderProperty to inject custom GLSL code
sp = sphere_actor.GetShaderProperty()

sp.AddVertexShaderReplacement(
    "//VTK::Color::Dec",
    True,
    "//VTK::Color::Dec\n"
    "in vec3 genAttrVector;\n"
    "out vec4 myColor;\n",
    False,
)

sp.AddVertexShaderReplacement(
    "//VTK::Color::Impl",
    True,
    "//VTK::Color::Impl\n"
    "  myColor = vec4(normalize(genAttrVector), 1.0);\n",
    False,
)

sp.AddFragmentShaderReplacement(
    "//VTK::Color::Dec",
    True,
    "//VTK::Color::Dec\n"
    "in vec4 myColor;\n",
    False,
)

sp.AddFragmentShaderReplacement(
    "//VTK::Color::Impl",
    True,
    "//VTK::Color::Impl\n"
    "  ambientColor = myColor.rgb;\n"
    "  diffuseColor = myColor.rgb;\n"
    "  opacity = myColor.a;\n",
    False,
)

renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("generic vertex attributes glsl")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# First render initializes OpenGL context for shader compilation
render_window.Render()

renderer.GetActiveCamera().Azimuth(-50)
renderer.GetActiveCamera().Roll(70)

interactor.Initialize()
interactor.Start()
