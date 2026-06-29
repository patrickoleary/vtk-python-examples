#!/usr/bin/env python

# Demonstrate vtkExplodeDataSet by reading an image dataset with material
# labels, exploding it into partitions by cell scalar, and rendering
# each partition with a different color.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersGeneral import vtkExplodeDataSet
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkPolyDataMapper,
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

# Get the cell scalar array name
array_name = reader.GetOutput().GetCellData().GetArray(0).GetName()

# Explode dataset by cell scalars
explode = vtkExplodeDataSet()
explode.SetInputConnection(reader.GetOutputPort())
explode.SetInputArrayToProcess(array_name, 1)  # 1 = CELL association
explode.Update()

# Extract geometry from the partitioned dataset collection
geometry = vtkCompositeDataGeometryFilter()
geometry.SetInputConnection(explode.GetOutputPort())

# Mapper and actor
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
render_window.SetWindowName("explode dataset")

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
