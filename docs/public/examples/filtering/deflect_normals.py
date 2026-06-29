#!/usr/bin/env python

# Demonstrate vtkDeflectNormals by computing gradients on a wavelet source,
# then deflecting normals using both a user-defined normal and point data
# normals, shown side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersGeneral import (
    vtkDeflectNormals,
    vtkGradientFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create wavelet source (2D slice)
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-100, 100, -100, 100, 0, 0)

# Compute gradient
gradient = vtkGradientFilter()
gradient.SetInputConnection(wavelet.GetOutputPort())
gradient.SetResultArrayName("Deflector")

# Extract surface
surface = vtkGeometryFilter()
surface.SetInputConnection(gradient.GetOutputPort())

# Left viewport: user normal deflection
deflect_0 = vtkDeflectNormals()
deflect_0.SetInputConnection(surface.GetOutputPort())
deflect_0.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Deflector"
)
deflect_0.SetScaleFactor(0.2)
deflect_0.UseUserNormalOn()
deflect_0.SetUserNormal(0.0, 0.0, 1.0)

mapper_0 = vtkPolyDataMapper()
mapper_0.ScalarVisibilityOff()
mapper_0.SetInputConnection(deflect_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(actor_0)

# Right viewport: point data normal deflection
deflect_1 = vtkDeflectNormals()
deflect_1.SetInputConnection(surface.GetOutputPort())
deflect_1.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Deflector"
)
deflect_1.SetScaleFactor(0.8)
deflect_1.UseUserNormalOff()

mapper_1 = vtkPolyDataMapper()
mapper_1.ScalarVisibilityOff()
mapper_1.SetInputConnection(deflect_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddActor(actor_1)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("deflect normals")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
