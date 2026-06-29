#!/usr/bin/env python

# Read EnSight office binary case file, compute streamlines with cone glyphs.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "office_bin.case"))
ensight_reader.Update()

# Outline from block 0
outline_filter = vtkStructuredGridOutlineFilter()
outline_filter.SetInputData(ensight_reader.GetOutput().GetBlock(0))

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Streamlines from block 0
stream_tracer = vtkStreamTracer()
stream_tracer.SetInputData(ensight_reader.GetOutput().GetBlock(0))
stream_tracer.SetStartPosition(0.1, 2.1, 0.5)
stream_tracer.SetMaximumPropagation(500)
stream_tracer.SetInitialIntegrationStep(0.1)
stream_tracer.SetIntegrationDirectionToForward()

# Cone glyphs
cone_source = vtkConeSource()
cone_source.SetResolution(8)

glyph_filter = vtkGlyph3D()
glyph_filter.SetInputConnection(stream_tracer.GetOutputPort())
glyph_filter.SetSourceConnection(cone_source.GetOutputPort())
glyph_filter.SetScaleFactor(3)
glyph_filter.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "vectors")
glyph_filter.SetScaleModeToScaleByVector()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph_filter.GetOutputPort())
glyph_mapper.SetScalarRange(ensight_reader.GetOutput().GetBlock(0).GetScalarRange())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.4, 0.4, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight office bin")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
