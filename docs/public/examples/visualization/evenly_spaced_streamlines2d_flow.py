#!/usr/bin/env python

# Demonstrate vtkEvenlySpacedStreamlines2D generating evenly spaced
# streamlines from a 2D vector field read from a multi-block dataset.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersFlowPaths import vtkEvenlySpacedStreamlines2D
from vtkmodules.vtkIOXML import vtkXMLMultiBlockDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read multi-block data
reader = vtkXMLMultiBlockDataReader()
reader.SetFileName(os.path.join(data_dir, "clt.vtm"))
reader.Update()

# Evenly spaced streamlines
stream = vtkEvenlySpacedStreamlines2D()
stream.SetInputConnection(reader.GetOutputPort())
stream.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "result")
stream.SetInitialIntegrationStep(0.2)
stream.SetClosedLoopMaximumDistance(0.2)
stream.SetMaximumNumberOfSteps(2000)
stream.SetSeparatingDistance(2)
stream.SetSeparatingDistanceRatio(0.3)
stream.SetStartPosition(0, 0, 200)

# Mapper
stream_mapper = vtkDataSetMapper()
stream_mapper.SetInputConnection(stream.GetOutputPort())
stream_mapper.ScalarVisibilityOff()

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)
stream_actor.GetProperty().SetColor(0, 0, 0)
stream_actor.GetProperty().SetLineWidth(1.0)
stream_actor.SetPosition(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(stream_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.SetWindowName("evenly spaced streamlines2d flow")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
