#!/usr/bin/env python

# Visualize sphere tree extraction modes (point, line, plane) across three
# data types (image, structured grid, unstructured grid) in a 3x3 grid
# of viewports using vtkSphereTreeFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
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

resolution = 10

# Glyph source for sphere tree visualization
glyph_source = vtkSphereSource()
glyph_source.SetPhiResolution(6)
glyph_source.SetThetaResolution(12)
glyph_source.SetRadius(1)

# Source: sample a sphere implicit function (image data)
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

image = vtkSampleFunction()
image.SetImplicitFunction(sphere)
image.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
image.SetSampleDimensions(resolution, resolution, resolution)
image.Update()

# Convert image data to structured grid
sgrid = vtkImageDataToPointSet()
sgrid.SetInputConnection(image.GetOutputPort())
sgrid.Update()

# Convert image data to unstructured grid
extraction_sphere = vtkSphere()
extraction_sphere.SetRadius(100)
extraction_sphere.SetCenter(0, 0, 0)

extract = vtkExtractGeometry()
extract.SetImplicitFunction(extraction_sphere)
extract.SetInputConnection(image.GetOutputPort())
extract.Update()

# Row 0 (image), Col 0 (point): image_point
image_point_filter = vtkSphereTreeFilter()
image_point_filter.SetInputConnection(image.GetOutputPort())
image_point_filter.SetExtractionModeToPoint()
image_point_filter.SetPoint(0, 0, 0)

image_point_glyphs = vtkGlyph3D()
image_point_glyphs.SetInputConnection(image_point_filter.GetOutputPort())
image_point_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

image_point_mapper = vtkPolyDataMapper()
image_point_mapper.SetInputConnection(image_point_glyphs.GetOutputPort())
image_point_mapper.ScalarVisibilityOff()

image_point_actor = vtkActor()
image_point_actor.SetMapper(image_point_mapper)
image_point_actor.GetProperty().SetColor(1, 1, 1)

image_point_outline = vtkOutlineFilter()
image_point_outline.SetInputConnection(image.GetOutputPort())

image_point_outline_mapper = vtkPolyDataMapper()
image_point_outline_mapper.SetInputConnection(image_point_outline.GetOutputPort())

image_point_outline_actor = vtkActor()
image_point_outline_actor.SetMapper(image_point_outline_mapper)

image_point_renderer = vtkRenderer()
image_point_renderer.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0 / 3.0)
image_point_renderer.SetBackground(0, 0, 0)
image_point_renderer.AddActor(image_point_actor)
image_point_renderer.AddActor(image_point_outline_actor)

# Row 0 (image), Col 1 (line): image_line
image_line_filter = vtkSphereTreeFilter()
image_line_filter.SetInputConnection(image.GetOutputPort())
image_line_filter.SetExtractionModeToLine()
image_line_filter.SetPoint(0, 0, 0)
image_line_filter.SetRay(1, 1, 1)

image_line_glyphs = vtkGlyph3D()
image_line_glyphs.SetInputConnection(image_line_filter.GetOutputPort())
image_line_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

image_line_mapper = vtkPolyDataMapper()
image_line_mapper.SetInputConnection(image_line_glyphs.GetOutputPort())
image_line_mapper.ScalarVisibilityOff()

image_line_actor = vtkActor()
image_line_actor.SetMapper(image_line_mapper)
image_line_actor.GetProperty().SetColor(1, 1, 1)

image_line_outline = vtkOutlineFilter()
image_line_outline.SetInputConnection(image.GetOutputPort())

image_line_outline_mapper = vtkPolyDataMapper()
image_line_outline_mapper.SetInputConnection(image_line_outline.GetOutputPort())

image_line_outline_actor = vtkActor()
image_line_outline_actor.SetMapper(image_line_outline_mapper)

image_line_renderer = vtkRenderer()
image_line_renderer.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0 / 3.0)
image_line_renderer.SetBackground(0, 0, 0)
image_line_renderer.AddActor(image_line_actor)
image_line_renderer.AddActor(image_line_outline_actor)

# Row 0 (image), Col 2 (plane): image_plane
image_plane_filter = vtkSphereTreeFilter()
image_plane_filter.SetInputConnection(image.GetOutputPort())
image_plane_filter.SetExtractionModeToPlane()
image_plane_filter.SetPoint(0, 0, 0)
image_plane_filter.SetNormal(1, 1, 1)

image_plane_glyphs = vtkGlyph3D()
image_plane_glyphs.SetInputConnection(image_plane_filter.GetOutputPort())
image_plane_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

image_plane_mapper = vtkPolyDataMapper()
image_plane_mapper.SetInputConnection(image_plane_glyphs.GetOutputPort())
image_plane_mapper.ScalarVisibilityOff()

image_plane_actor = vtkActor()
image_plane_actor.SetMapper(image_plane_mapper)
image_plane_actor.GetProperty().SetColor(1, 1, 1)

image_plane_outline = vtkOutlineFilter()
image_plane_outline.SetInputConnection(image.GetOutputPort())

image_plane_outline_mapper = vtkPolyDataMapper()
image_plane_outline_mapper.SetInputConnection(image_plane_outline.GetOutputPort())

image_plane_outline_actor = vtkActor()
image_plane_outline_actor.SetMapper(image_plane_outline_mapper)

image_plane_renderer = vtkRenderer()
image_plane_renderer.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0 / 3.0)
image_plane_renderer.SetBackground(0, 0, 0)
image_plane_renderer.AddActor(image_plane_actor)
image_plane_renderer.AddActor(image_plane_outline_actor)

# Row 1 (structured grid), Col 0 (point): sgrid_point
sgrid_point_filter = vtkSphereTreeFilter()
sgrid_point_filter.SetInputConnection(sgrid.GetOutputPort())
sgrid_point_filter.SetExtractionModeToPoint()
sgrid_point_filter.SetPoint(0, 0, 0)

sgrid_point_glyphs = vtkGlyph3D()
sgrid_point_glyphs.SetInputConnection(sgrid_point_filter.GetOutputPort())
sgrid_point_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

sgrid_point_mapper = vtkPolyDataMapper()
sgrid_point_mapper.SetInputConnection(sgrid_point_glyphs.GetOutputPort())
sgrid_point_mapper.ScalarVisibilityOff()

sgrid_point_actor = vtkActor()
sgrid_point_actor.SetMapper(sgrid_point_mapper)
sgrid_point_actor.GetProperty().SetColor(1, 1, 1)

sgrid_point_outline = vtkOutlineFilter()
sgrid_point_outline.SetInputConnection(sgrid.GetOutputPort())

sgrid_point_outline_mapper = vtkPolyDataMapper()
sgrid_point_outline_mapper.SetInputConnection(sgrid_point_outline.GetOutputPort())

sgrid_point_outline_actor = vtkActor()
sgrid_point_outline_actor.SetMapper(sgrid_point_outline_mapper)

sgrid_point_renderer = vtkRenderer()
sgrid_point_renderer.SetViewport(0.0, 1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)
sgrid_point_renderer.SetBackground(0, 0, 0)
sgrid_point_renderer.AddActor(sgrid_point_actor)
sgrid_point_renderer.AddActor(sgrid_point_outline_actor)

# Row 1 (structured grid), Col 1 (line): sgrid_line
sgrid_line_filter = vtkSphereTreeFilter()
sgrid_line_filter.SetInputConnection(sgrid.GetOutputPort())
sgrid_line_filter.SetExtractionModeToLine()
sgrid_line_filter.SetPoint(0, 0, 0)
sgrid_line_filter.SetRay(1, 1, 1)

sgrid_line_glyphs = vtkGlyph3D()
sgrid_line_glyphs.SetInputConnection(sgrid_line_filter.GetOutputPort())
sgrid_line_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

sgrid_line_mapper = vtkPolyDataMapper()
sgrid_line_mapper.SetInputConnection(sgrid_line_glyphs.GetOutputPort())
sgrid_line_mapper.ScalarVisibilityOff()

sgrid_line_actor = vtkActor()
sgrid_line_actor.SetMapper(sgrid_line_mapper)
sgrid_line_actor.GetProperty().SetColor(1, 1, 1)

sgrid_line_outline = vtkOutlineFilter()
sgrid_line_outline.SetInputConnection(sgrid.GetOutputPort())

sgrid_line_outline_mapper = vtkPolyDataMapper()
sgrid_line_outline_mapper.SetInputConnection(sgrid_line_outline.GetOutputPort())

sgrid_line_outline_actor = vtkActor()
sgrid_line_outline_actor.SetMapper(sgrid_line_outline_mapper)

sgrid_line_renderer = vtkRenderer()
sgrid_line_renderer.SetViewport(1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)
sgrid_line_renderer.SetBackground(0, 0, 0)
sgrid_line_renderer.AddActor(sgrid_line_actor)
sgrid_line_renderer.AddActor(sgrid_line_outline_actor)

# Row 1 (structured grid), Col 2 (plane): sgrid_plane
sgrid_plane_filter = vtkSphereTreeFilter()
sgrid_plane_filter.SetInputConnection(sgrid.GetOutputPort())
sgrid_plane_filter.SetExtractionModeToPlane()
sgrid_plane_filter.SetPoint(0, 0, 0)
sgrid_plane_filter.SetNormal(1, 1, 1)

sgrid_plane_glyphs = vtkGlyph3D()
sgrid_plane_glyphs.SetInputConnection(sgrid_plane_filter.GetOutputPort())
sgrid_plane_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

sgrid_plane_mapper = vtkPolyDataMapper()
sgrid_plane_mapper.SetInputConnection(sgrid_plane_glyphs.GetOutputPort())
sgrid_plane_mapper.ScalarVisibilityOff()

sgrid_plane_actor = vtkActor()
sgrid_plane_actor.SetMapper(sgrid_plane_mapper)
sgrid_plane_actor.GetProperty().SetColor(1, 1, 1)

sgrid_plane_outline = vtkOutlineFilter()
sgrid_plane_outline.SetInputConnection(sgrid.GetOutputPort())

sgrid_plane_outline_mapper = vtkPolyDataMapper()
sgrid_plane_outline_mapper.SetInputConnection(sgrid_plane_outline.GetOutputPort())

sgrid_plane_outline_actor = vtkActor()
sgrid_plane_outline_actor.SetMapper(sgrid_plane_outline_mapper)

sgrid_plane_renderer = vtkRenderer()
sgrid_plane_renderer.SetViewport(2.0 / 3.0, 1.0 / 3.0, 1.0, 2.0 / 3.0)
sgrid_plane_renderer.SetBackground(0, 0, 0)
sgrid_plane_renderer.AddActor(sgrid_plane_actor)
sgrid_plane_renderer.AddActor(sgrid_plane_outline_actor)

# Row 2 (unstructured grid), Col 0 (point): ugrid_point
ugrid_point_filter = vtkSphereTreeFilter()
ugrid_point_filter.SetInputConnection(extract.GetOutputPort())
ugrid_point_filter.SetExtractionModeToPoint()
ugrid_point_filter.SetPoint(0, 0, 0)

ugrid_point_glyphs = vtkGlyph3D()
ugrid_point_glyphs.SetInputConnection(ugrid_point_filter.GetOutputPort())
ugrid_point_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

ugrid_point_mapper = vtkPolyDataMapper()
ugrid_point_mapper.SetInputConnection(ugrid_point_glyphs.GetOutputPort())
ugrid_point_mapper.ScalarVisibilityOff()

ugrid_point_actor = vtkActor()
ugrid_point_actor.SetMapper(ugrid_point_mapper)
ugrid_point_actor.GetProperty().SetColor(1, 1, 1)

ugrid_point_outline = vtkOutlineFilter()
ugrid_point_outline.SetInputConnection(extract.GetOutputPort())

ugrid_point_outline_mapper = vtkPolyDataMapper()
ugrid_point_outline_mapper.SetInputConnection(ugrid_point_outline.GetOutputPort())

ugrid_point_outline_actor = vtkActor()
ugrid_point_outline_actor.SetMapper(ugrid_point_outline_mapper)

ugrid_point_renderer = vtkRenderer()
ugrid_point_renderer.SetViewport(0.0, 2.0 / 3.0, 1.0 / 3.0, 1.0)
ugrid_point_renderer.SetBackground(0, 0, 0)
ugrid_point_renderer.AddActor(ugrid_point_actor)
ugrid_point_renderer.AddActor(ugrid_point_outline_actor)

# Row 2 (unstructured grid), Col 1 (line): ugrid_line
ugrid_line_filter = vtkSphereTreeFilter()
ugrid_line_filter.SetInputConnection(extract.GetOutputPort())
ugrid_line_filter.SetExtractionModeToLine()
ugrid_line_filter.SetPoint(0, 0, 0)
ugrid_line_filter.SetRay(1, 1, 1)

ugrid_line_glyphs = vtkGlyph3D()
ugrid_line_glyphs.SetInputConnection(ugrid_line_filter.GetOutputPort())
ugrid_line_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

ugrid_line_mapper = vtkPolyDataMapper()
ugrid_line_mapper.SetInputConnection(ugrid_line_glyphs.GetOutputPort())
ugrid_line_mapper.ScalarVisibilityOff()

ugrid_line_actor = vtkActor()
ugrid_line_actor.SetMapper(ugrid_line_mapper)
ugrid_line_actor.GetProperty().SetColor(1, 1, 1)

ugrid_line_outline = vtkOutlineFilter()
ugrid_line_outline.SetInputConnection(extract.GetOutputPort())

ugrid_line_outline_mapper = vtkPolyDataMapper()
ugrid_line_outline_mapper.SetInputConnection(ugrid_line_outline.GetOutputPort())

ugrid_line_outline_actor = vtkActor()
ugrid_line_outline_actor.SetMapper(ugrid_line_outline_mapper)

ugrid_line_renderer = vtkRenderer()
ugrid_line_renderer.SetViewport(1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0, 1.0)
ugrid_line_renderer.SetBackground(0, 0, 0)
ugrid_line_renderer.AddActor(ugrid_line_actor)
ugrid_line_renderer.AddActor(ugrid_line_outline_actor)

# Row 2 (unstructured grid), Col 2 (plane): ugrid_plane
ugrid_plane_filter = vtkSphereTreeFilter()
ugrid_plane_filter.SetInputConnection(extract.GetOutputPort())
ugrid_plane_filter.SetExtractionModeToPlane()
ugrid_plane_filter.SetPoint(0, 0, 0)
ugrid_plane_filter.SetNormal(1, 1, 1)

ugrid_plane_glyphs = vtkGlyph3D()
ugrid_plane_glyphs.SetInputConnection(ugrid_plane_filter.GetOutputPort())
ugrid_plane_glyphs.SetSourceConnection(glyph_source.GetOutputPort())

ugrid_plane_mapper = vtkPolyDataMapper()
ugrid_plane_mapper.SetInputConnection(ugrid_plane_glyphs.GetOutputPort())
ugrid_plane_mapper.ScalarVisibilityOff()

ugrid_plane_actor = vtkActor()
ugrid_plane_actor.SetMapper(ugrid_plane_mapper)
ugrid_plane_actor.GetProperty().SetColor(1, 1, 1)

ugrid_plane_outline = vtkOutlineFilter()
ugrid_plane_outline.SetInputConnection(extract.GetOutputPort())

ugrid_plane_outline_mapper = vtkPolyDataMapper()
ugrid_plane_outline_mapper.SetInputConnection(ugrid_plane_outline.GetOutputPort())

ugrid_plane_outline_actor = vtkActor()
ugrid_plane_outline_actor.SetMapper(ugrid_plane_outline_mapper)

ugrid_plane_renderer = vtkRenderer()
ugrid_plane_renderer.SetViewport(2.0 / 3.0, 2.0 / 3.0, 1.0, 1.0)
ugrid_plane_renderer.SetBackground(0, 0, 0)
ugrid_plane_renderer.AddActor(ugrid_plane_actor)
ugrid_plane_renderer.AddActor(ugrid_plane_outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(image_point_renderer)
render_window.AddRenderer(image_line_renderer)
render_window.AddRenderer(image_plane_renderer)
render_window.AddRenderer(sgrid_point_renderer)
render_window.AddRenderer(sgrid_line_renderer)
render_window.AddRenderer(sgrid_plane_renderer)
render_window.AddRenderer(ugrid_point_renderer)
render_window.AddRenderer(ugrid_line_renderer)
render_window.AddRenderer(ugrid_plane_renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("sphere tree extraction modes")

# Scene
image_point_renderer.ResetCamera()
image_line_renderer.ResetCamera()
image_plane_renderer.ResetCamera()
sgrid_point_renderer.ResetCamera()
sgrid_line_renderer.ResetCamera()
sgrid_plane_renderer.ResetCamera()
ugrid_point_renderer.ResetCamera()
ugrid_line_renderer.ResetCamera()
ugrid_plane_renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
