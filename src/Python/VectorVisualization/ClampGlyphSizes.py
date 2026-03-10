#!/usr/bin/env python

# Demonstrate range clamping with vtkGlyph3D to enforce minimum glyph sizes.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkElevationFilter,
    vtkGlyph3D,
)
from vtkmodules.vtkFiltersSources import vtkConeSource
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
midnight_blue = (0.098, 0.098, 0.439)

# Source: generate a 2D wavelet image with scalar data
rt = vtkRTAnalyticSource()
rt.SetWholeExtent(-2, 2, -2, 2, 0, 0)

# Filter: compute gradient of RTData to produce a vector attribute
grad = vtkImageGradient()
grad.SetDimensionality(3)
grad.SetInputConnection(rt.GetOutputPort())

# Filter: add an elevation scalar that varies smoothly across the domain
elev = vtkElevationFilter()
elev.SetLowPoint(-2, 0, 0)
elev.SetHighPoint(2, 0, 0)
elev.SetInputConnection(grad.GetOutputPort())

# Source: cone geometry used as the glyph shape
cone = vtkConeSource()
cone.SetRadius(0.1)
cone.SetHeight(0.5)

# Filter: place oriented and scaled cone glyphs at each point
glyph = vtkGlyph3D()
glyph.SetInputConnection(elev.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.ScalingOn()
glyph.SetScaleModeToScaleByScalar()
glyph.SetVectorModeToUseVector()
glyph.OrientOn()
glyph.ClampingOn()
glyph.SetScaleFactor(1)
glyph.SetRange(-0.5, 1)
glyph.SetInputArrayToProcess(0, 0, 0, 0, "Elevation")
glyph.SetInputArrayToProcess(1, 0, 0, 0, "RTDataGradient")
glyph.SetInputArrayToProcess(3, 0, 0, 0, "RTData")
glyph.Update()

# Mapper: color glyphs by RTData
coloring_by = "RTData"
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(
    glyph.GetOutputDataObject(0).GetPointData().GetArray(coloring_by).GetRange()
)
mapper.SelectColorArray(coloring_by)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ClampGlyphSizes")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
