#!/usr/bin/env python

# Demonstrate vtkQuadraturePointsGenerator and vtkQuadraturePointInterpolator
# by reading a quadratic unstructured grid, generating quadrature scheme
# dictionaries, interpolating fields, warping, clipping, thresholding,
# and rendering quadrature points as glyphs alongside the warped surface.

import math
import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import (
    vtkQuadraturePointInterpolator,
    vtkQuadraturePointsGenerator,
    vtkQuadratureSchemeDictionaryGenerator,
    vtkWarpVector,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read quadratic unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "Quadratic", "CylinderQuadratic.vtk"))
reader.Update()

input_data = reader.GetOutput()

# Generate warp vector from point coordinates
n_pts = input_data.GetNumberOfPoints()
pts_data = input_data.GetPoints().GetData()
bounds = [0.0] * 6
input_data.GetPoints().GetBounds(bounds)
zmax = bounds[5]
zmin = bounds[4]
zmid = (zmax + zmin) / 4.0

warp_arr = vtkDoubleArray()
warp_arr.SetName("warp")
warp_arr.SetNumberOfComponents(3)
warp_arr.SetNumberOfTuples(n_pts)

thresh_arr = vtkDoubleArray()
thresh_arr.SetName("threshold")
thresh_arr.SetNumberOfComponents(1)
thresh_arr.SetNumberOfTuples(n_pts)

for i in range(n_pts):
    pt = pts_data.GetTuple3(i)
    zs = (pt[2] - zmid) / (zmax - zmid) if (zmax - zmid) != 0 else 0
    fzs = zs * zs * zs
    mod_r = math.sqrt(pt[0] * pt[0] + pt[1] * pt[1])
    if mod_r > 0:
        rx = (pt[0] / mod_r) * fzs
        ry = (pt[1] / mod_r) * fzs
    else:
        rx = 0
        ry = 0
    warp_arr.SetTuple3(i, rx, ry, 0.0)
    thresh_arr.SetTuple1(i, ry)

input_data.GetPointData().AddArray(warp_arr)
input_data.GetPointData().AddArray(thresh_arr)
input_data.GetPointData().SetActiveVectors("warp")
input_data.GetPointData().SetActiveScalars("threshold")

# Generate quadrature scheme dictionary
dict_gen = vtkQuadratureSchemeDictionaryGenerator()
dict_gen.SetInputData(input_data)

# Interpolate fields to quadrature points
interp = vtkQuadraturePointInterpolator()
interp.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "QuadratureOffset"
)
interp.SetInputConnection(dict_gen.GetOutputPort())

# Warp by vector
warper = vtkWarpVector()
warper.SetInputConnection(interp.GetOutputPort())
warper.SetScaleFactor(0.02)

# Generate quadrature points
point_gen = vtkQuadraturePointsGenerator()
point_gen.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "QuadratureOffset"
)
point_gen.SetInputConnection(warper.GetOutputPort())
point_gen.Update()

# Glyph the quadrature points
glyph_sphere = vtkSphereSource()
glyph_sphere.SetRadius(0.0008)

glyphs = vtkGlyph3D()
glyphs.SetInputConnection(point_gen.GetOutputPort())
glyphs.SetSourceConnection(glyph_sphere.GetOutputPort())
glyphs.ScalingOff()
glyphs.SetColorModeToColorByScalar()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyphs.GetOutputPort())
glyph_mapper.SetColorModeToMapScalars()
glyph_mapper.SetScalarModeToUsePointData()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Extract warped surface for reference
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(warper.GetOutputPort())

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface.GetOutputPort())
surface_mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
surface_actor.GetProperty().SetRepresentationToWireframe()
surface_actor.SetMapper(surface_mapper)

# Left viewport: glyphs only
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(glyph_actor)
renderer_0.SetBackground(0.328125, 0.347656, 0.425781)

# Right viewport: glyphs + wireframe surface
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddActor(glyph_actor)
renderer_1.AddActor(surface_actor)
renderer_1.SetBackground(0.328125, 0.347656, 0.425781)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(800, 400)
render_window.SetWindowName("quadrature points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
camera_0 = renderer_0.GetActiveCamera()
camera_0.Elevation(95.0)
camera_0.SetViewUp(0.0, 0.0, 1.0)
camera_0.Azimuth(180.0)

renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
