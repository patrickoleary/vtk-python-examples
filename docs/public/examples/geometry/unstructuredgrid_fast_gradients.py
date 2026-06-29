#!/usr/bin/env python

# Compute fast approximation gradients on an unstructured grid and visualize with glyphs.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkGlyph3D,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersGeneral import vtkGradientFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
grid_reader = vtkUnstructuredGridReader()
grid_reader.SetFileName(os.path.join(data_dir, "uGridEx.vtk"))

# Extract edges and create tubes
edges = vtkExtractEdges()
edges.SetInputConnection(grid_reader.GetOutputPort())

tubes = vtkTubeFilter()
tubes.SetInputConnection(edges.GetOutputPort())
tubes.SetRadius(0.0625)
tubes.SetVaryRadiusToVaryRadiusOff()
tubes.SetNumberOfSides(32)

tubes_mapper = vtkPolyDataMapper()
tubes_mapper.SetInputConnection(tubes.GetOutputPort())
tubes_mapper.SetScalarRange(0.0, 26.0)

tubes_actor = vtkActor()
tubes_actor.SetMapper(tubes_mapper)

# Compute gradients with fast approximation
gradients = vtkGradientFilter()
gradients.SetInputConnection(grid_reader.GetOutputPort())
gradients.FasterApproximationOn()

# Assign gradients as vectors
vectors = vtkAssignAttribute()
vectors.SetInputConnection(gradients.GetOutputPort())
vectors.Assign("Gradients", "VECTORS", "POINT_DATA")

# Arrow glyphs
arrow = vtkArrowSource()

glyphs = vtkGlyph3D()
glyphs.SetInputConnection(0, vectors.GetOutputPort())
glyphs.SetInputConnection(1, arrow.GetOutputPort())
glyphs.ScalingOn()
glyphs.SetScaleModeToScaleByVector()
glyphs.SetScaleFactor(0.25)
glyphs.OrientOn()
glyphs.ClampingOff()
glyphs.SetVectorModeToUseVector()
glyphs.SetIndexModeToOff()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyphs.GetOutputPort())
glyph_mapper.ScalarVisibilityOff()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(tubes_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.328125, 0.347656, 0.425781)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("unstructuredgrid fast gradients")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 500)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(-80.0)
camera.OrthogonalizeViewUp()
camera.Azimuth(135.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
