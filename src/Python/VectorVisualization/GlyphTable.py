#!/usr/bin/env python

# Use a glyph table to vary glyph shape by scalar value.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkElevationFilter,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_gray = (0.663, 0.663, 0.663)

# Source: generate a 2D wavelet image with scalar data
rt = vtkRTAnalyticSource()
rt.SetWholeExtent(-2, 2, -2, 2, 0, 0)

# Filter: compute gradient of RTData to produce a vector attribute
grad = vtkImageGradient()
grad.SetDimensionality(3)
grad.SetInputConnection(rt.GetOutputPort())

# Filter: add an elevation scalar that varies smoothly across the domain
elev = vtkElevationFilter()
elev.SetLowPoint(-2, -2, 0)
elev.SetHighPoint(2, 2, 0)
elev.SetInputConnection(grad.GetOutputPort())

# Source: three glyph shapes for the glyph table
cube = vtkCubeSource()
cube.SetXLength(0.5)
cube.SetYLength(1)
cube.SetZLength(2)

sphere = vtkSphereSource()
sphere.SetRadius(0.25)

cone = vtkConeSource()
cone.SetRadius(0.25)
cone.SetHeight(0.5)

# Filter: place oriented glyphs, selecting shape from the table by scalar
glyph = vtkGlyph3D()
glyph.SetInputConnection(elev.GetOutputPort())
glyph.SetSourceConnection(0, cube.GetOutputPort())
glyph.SetSourceConnection(1, sphere.GetOutputPort())
glyph.SetSourceConnection(2, cone.GetOutputPort())
glyph.ScalingOn()
glyph.SetScaleModeToScaleByScalar()
glyph.SetVectorModeToUseVector()
glyph.OrientOn()
glyph.SetScaleFactor(1)
glyph.SetRange(0, 1)
glyph.SetIndexModeToScalar()
glyph.SetInputArrayToProcess(0, 0, 0, 0, "Elevation")
glyph.SetInputArrayToProcess(1, 0, 0, 0, "RTDataGradient")

# Mapper: color glyphs by Elevation
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()
mapper.SelectColorArray("Elevation")

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_gray)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("GlyphTable")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
