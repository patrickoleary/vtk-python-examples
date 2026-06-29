#!/usr/bin/env python

# Demonstrate vtkGradientFilter by computing gradients, vorticity,
# Q-criterion, and divergence on a structured grid dataset, then
# visualizing the gradient vectors as arrow glyphs.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersGeneral import vtkGradientFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read structured grid
reader = vtkStructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "SampleStructGrid.vtk"))
reader.Update()
grid = reader.GetOutput()

# Create a synthetic 3-component vector field from point coordinates.
# Component j at point i = point[(j + offset) % 3], with offset = 1.
# This produces a field whose gradient and vorticity are analytically known.
offset = 1
num_points = grid.GetNumberOfPoints()
linear_field = vtkDoubleArray()
linear_field.SetNumberOfComponents(3)
linear_field.SetNumberOfTuples(num_points)
linear_field.SetName("LinearField")
for i in range(num_points):
    pt = grid.GetPoint(i)
    linear_field.SetTuple3(i, pt[(0 + offset) % 3], pt[(1 + offset) % 3], pt[(2 + offset) % 3])
grid.GetPointData().AddArray(linear_field)

# Compute gradient with vorticity, Q-criterion, and divergence
gradient = vtkGradientFilter()
gradient.SetInputData(grid)
gradient.SetInputScalars(vtkDataObject.FIELD_ASSOCIATION_POINTS, "LinearField")
gradient.SetResultArrayName("Gradient")
gradient.SetComputeVorticity(1)
gradient.SetComputeQCriterion(1)
gradient.SetComputeDivergence(1)
gradient.Update()

# Mask a subset of points for glyph display
mask = vtkMaskPoints()
mask.SetInputConnection(gradient.GetOutputPort())
mask.RandomModeOff()
mask.SetOnRatio(5)

# Create arrow glyphs for gradient vectors
arrow = vtkArrowSource()

glyph = vtkGlyph3D()
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetInputConnection(mask.GetOutputPort())
glyph.SetVectorModeToUseVector()
glyph.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Vorticity")
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.05)
glyph.SetColorModeToColorByScalar()

glyph.Update()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.ScalarVisibilityOn()
glyph_mapper.SetScalarRange(glyph.GetOutput().GetScalarRange())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(glyph_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("gradient and vorticity")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(120)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
