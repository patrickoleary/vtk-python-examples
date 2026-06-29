#!/usr/bin/env python

# Demonstrate order-independent translucent rendering pass with glyphed spheres and an opaque plane.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkOrderIndependentTranslucentPass,
    vtkRenderStepsPass,
)

# Sphere glyph source
sphere = vtkSphereSource()
sphere.SetRadius(1)
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetThetaResolution(10)
sphere.SetPhiResolution(10)
sphere.SetLatLongTessellation(0)

# Image grid source
grid = vtkImageGridSource()
grid.SetGridSpacing(1, 1, 1)
grid.SetGridOrigin(0, 0, 0)
grid.SetLineValue(1.0)
grid.SetFillValue(0.5)
grid.SetDataScalarTypeToUnsignedChar()
grid.SetDataExtent(0, 10, 0, 10, 0, 10)
grid.SetDataSpacing(0.1, 0.1, 0.1)
grid.SetDataOrigin(0.0, 0.0, 0.0)
grid.Update()

scalar_range = grid.GetOutput().GetPointData().GetScalars().GetRange()

# Glyph spheres on grid
glyph = vtkGlyph3D()
glyph.SetInputConnection(0, grid.GetOutputPort(0))
glyph.SetSourceConnection(sphere.GetOutputPort(0))
glyph.SetScaling(1)
glyph.SetScaleModeToScaleByScalar()
glyph.SetColorModeToColorByScale()
glyph.SetScaleFactor(0.05)
glyph.SetRange(scalar_range)
glyph.SetOrient(0)
glyph.SetClamping(0)
glyph.SetVectorModeToUseVector()
glyph.SetIndexModeToOff()
glyph.SetGeneratePointIds(0)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort(0))

lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.SetRange(scalar_range)
mapper.SetLookupTable(lut)
mapper.SetScalarRange(scalar_range)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.2)
actor.GetProperty().SetColor(0.0, 1.0, 0.0)
actor.GetProperty().SetBackfaceCulling(1)
actor.GetProperty().SetFrontfaceCulling(0)

# Opaque plane
plane = vtkPlaneSource()
plane.SetCenter(0.5, 0.5, 0.5)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(0, plane.GetOutputPort(0))

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetOpacity(1.0)
plane_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
plane_actor.GetProperty().SetBackfaceCulling(0)
plane_actor.GetProperty().SetFrontfaceCulling(0)

# Renderer with order-independent translucent pass
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.5, 0.0)
renderer.AddActor(actor)
renderer.AddActor(plane_actor)

basic_passes = vtkRenderStepsPass()
peeling = vtkOrderIndependentTranslucentPass()
peeling.SetTranslucentPass(basic_passes.GetTranslucentPass())
basic_passes.SetTranslucentPass(peeling)
renderer.SetPass(basic_passes)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("order independent translucent pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
