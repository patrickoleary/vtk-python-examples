#!/usr/bin/env python

# Test vtkTransformCoordinateSystems with 2D glyphs on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkGlyph2D
from vtkmodules.vtkFiltersSources import (
    vtkGlyphSource2D,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTransformCoordinateSystems,
)

# Renderer (created early: xform.SetViewport requires renderer)
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)

# Sphere source
sphere = vtkSphereSource()
sphere.SetPhiResolution(10)
sphere.SetThetaResolution(20)

# Transform world to display coordinates
xform = vtkTransformCoordinateSystems()
xform.SetInputConnection(sphere.GetOutputPort())
xform.SetInputCoordinateSystemToWorld()
xform.SetOutputCoordinateSystemToDisplay()
xform.SetViewport(renderer)

# Glyph source
glyph_source = vtkGlyphSource2D()
glyph_source.SetGlyphTypeToCircle()
glyph_source.SetScale(20)
glyph_source.FilledOff()
glyph_source.CrossOn()
glyph_source.Update()

# Create glyphs
glyph_2d = vtkGlyph2D()
glyph_2d.SetInputConnection(xform.GetOutputPort())
glyph_2d.SetSourceData(0, glyph_source.GetOutput())
glyph_2d.SetScaleModeToDataScalingOff()

mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(glyph_2d.GetOutputPort())

glyph_actor = vtkActor2D()
glyph_actor.SetMapper(mapper)

renderer.AddActor(glyph_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("transform coordinate systems")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
