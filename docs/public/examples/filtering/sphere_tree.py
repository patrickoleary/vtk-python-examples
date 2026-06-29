#!/usr/bin/env python

# Visualize sphere trees built from structured and unstructured grids
# using vtkSphereTreeFilter with glyph rendering in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkCommonExecutionModel import vtkSphereTree
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkSphereTreeFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkImageDataToPointSet
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 25

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)

# Convert image data to structured grid
convert = vtkImageDataToPointSet()
convert.SetInputConnection(sample.GetOutputPort())

# Sphere tree filter on structured grid (level 0)
sphere_tree_filter = vtkSphereTreeFilter()
sphere_tree_filter.SetInputConnection(convert.GetOutputPort())
sphere_tree_filter.SetLevel(0)

# Glyph source for sphere tree visualization
glyph_source = vtkSphereSource()
glyph_source.SetPhiResolution(8)
glyph_source.SetThetaResolution(16)
glyph_source.SetRadius(1)

sphere_tree_glyphs = vtkGlyph3D()
sphere_tree_glyphs.SetInputConnection(sphere_tree_filter.GetOutputPort())
sphere_tree_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

sphere_tree_mapper = vtkPolyDataMapper()
sphere_tree_mapper.SetInputConnection(sphere_tree_glyphs.GetOutputPort())
sphere_tree_mapper.ScalarVisibilityOff()

sphere_tree_actor = vtkActor()
sphere_tree_actor.SetMapper(sphere_tree_mapper)
sphere_tree_actor.GetProperty().SetColor(1, 1, 1)

# Outline for structured grid
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Convert image data to unstructured grid via extraction
extraction_sphere = vtkSphere()
extraction_sphere.SetRadius(100)
extraction_sphere.SetCenter(0, 0, 0)

extract = vtkExtractGeometry()
extract.SetImplicitFunction(extraction_sphere)
extract.SetInputConnection(sample.GetOutputPort())
extract.Update()

# Build an explicit sphere tree on the unstructured grid
unstructured_tree = vtkSphereTree()
unstructured_tree.BuildHierarchyOn()
unstructured_tree.Build(extract.GetOutput())

# Sphere tree filter on unstructured grid
unstructured_tree_filter = vtkSphereTreeFilter()
unstructured_tree_filter.SetSphereTree(unstructured_tree)
unstructured_tree_filter.SetLevel(0)

unstructured_tree_glyphs = vtkGlyph3D()
unstructured_tree_glyphs.SetInputConnection(unstructured_tree_filter.GetOutputPort())
unstructured_tree_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

unstructured_tree_mapper = vtkPolyDataMapper()
unstructured_tree_mapper.SetInputConnection(unstructured_tree_glyphs.GetOutputPort())
unstructured_tree_mapper.ScalarVisibilityOff()

unstructured_tree_actor = vtkActor()
unstructured_tree_actor.SetMapper(unstructured_tree_mapper)
unstructured_tree_actor.GetProperty().SetColor(1, 1, 1)

# Outline for unstructured grid
u_outline = vtkOutlineFilter()
u_outline.SetInputConnection(sample.GetOutputPort())

u_outline_mapper = vtkPolyDataMapper()
u_outline_mapper.SetInputConnection(u_outline.GetOutputPort())

u_outline_actor = vtkActor()
u_outline_actor.SetMapper(u_outline_mapper)

# Two viewports: structured (left), unstructured (right)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(sphere_tree_actor)
renderer_0.AddActor(outline_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(unstructured_tree_actor)
renderer_1.AddActor(u_outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("sphere tree")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
