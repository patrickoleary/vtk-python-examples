#!/usr/bin/env python

# Elliptical Gaussian splatting to reconstruct a face surface from oriented points.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkMaskPoints,
    vtkPolyDataNormals,
)
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
flesh = (1.000, 0.490, 0.250)
turquoise = (0.251, 0.878, 0.816)
wheat = (0.961, 0.871, 0.702)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "fran_cut.vtk")

# Reader: load the face mesh
fran = vtkPolyDataReader()
fran.SetFileName(file_name)

# Filter: compute surface normals
fran_normals = vtkPolyDataNormals()
fran_normals.SetInputConnection(fran.GetOutputPort())

# Filter: subsample every 8th point for splatting
mask = vtkMaskPoints()
mask.SetInputConnection(fran_normals.GetOutputPort())
mask.SetOnRatio(8)

# Filter: splat subsampled oriented points into a 100^3 volume
splatter = vtkGaussianSplatter()
splatter.SetInputConnection(mask.GetOutputPort())
splatter.SetSampleDimensions(100, 100, 100)
splatter.SetEccentricity(2.5)
splatter.NormalWarpingOn()
splatter.SetScaleFactor(1.0)
splatter.SetRadius(0.025)

# Filter: extract an isosurface from the splatted volume
contour = vtkContourFilter()
contour.SetInputConnection(splatter.GetOutputPort())
contour.SetValue(0, 0.25)

# Mapper: map the reconstructed surface to graphics primitives
splat_mapper = vtkPolyDataMapper()
splat_mapper.SetInputConnection(contour.GetOutputPort())
splat_mapper.ScalarVisibilityOff()

# Actor: display the reconstructed surface
splat_actor = vtkActor()
splat_actor.SetMapper(splat_mapper)
splat_actor.GetProperty().SetColor(flesh)

# Mapper: map the original wireframe mesh to graphics primitives
wireframe_mapper = vtkPolyDataMapper()
wireframe_mapper.SetInputConnection(fran.GetOutputPort())
wireframe_mapper.ScalarVisibilityOff()

# Actor: display the original mesh as wireframe overlay
wireframe_actor = vtkActor()
wireframe_actor.SetMapper(wireframe_mapper)
wireframe_actor.GetProperty().SetRepresentationToWireframe()
wireframe_actor.GetProperty().SetColor(turquoise)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(wireframe_actor)
renderer.AddActor(splat_actor)
renderer.SetBackground(wheat)
cam = renderer.GetActiveCamera()
cam.SetClippingRange(0.0332682, 1.66341)
cam.SetFocalPoint(0.0511519, -0.127555, -0.0554379)
cam.SetPosition(0.516567, -0.124763, -0.349538)
cam.SetViewAngle(18.1279)
cam.SetViewUp(-0.013125, 0.99985, -0.0112779)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("SplatFace")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
