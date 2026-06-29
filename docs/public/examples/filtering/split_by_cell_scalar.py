#!/usr/bin/env python

# Demonstrate vtkSplitByCellScalarFilter by reading an image dataset with
# material labels, splitting it into blocks by cell scalar, and rendering
# the multi-block output with composite mapper.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkFiltersGeneral import vtkSplitByCellScalarFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read image data with material labels
reader = vtkXMLImageDataReader()
reader.SetFileName(os.path.join(data_dir, "waveletMaterial.vti"))
reader.Update()

# Split by cell scalar
split = vtkSplitByCellScalarFilter()
split.SetInputData(reader.GetOutput())
split.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, vtkDataSetAttributes.SCALARS
)
split.Update()

# Extract geometry for rendering
geometry = vtkCompositeDataGeometryFilter()
geometry.SetInputConnection(split.GetOutputPort())

# Render with composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("split by cell scalar")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
