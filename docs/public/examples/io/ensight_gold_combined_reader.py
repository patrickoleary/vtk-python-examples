#!/usr/bin/env python

# Read EnSight Gold combined format case files and render with various pipelines.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOEnSight import vtkEnSightGoldCombinedReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# --- Demonstrate reading elements case with point scalars ---
ensight_reader_0 = vtkEnSightGoldCombinedReader()
ensight_reader_0.SetCaseFileName(os.path.join(data_dir, "EnSight", "elements.case"))

geometry_filter_0 = vtkGeometryFilter()
geometry_filter_0.RemoveGhostInterfacesOff()
geometry_filter_0.SetInputConnection(ensight_reader_0.GetOutputPort())

composite_mapper_0 = vtkCompositePolyDataMapper()
composite_mapper_0.SetInputConnection(geometry_filter_0.GetOutputPort())
composite_mapper_0.ColorByArrayComponent("pointScalars", 0)
composite_mapper_0.SetScalarRange(0, 112)

actor_0 = vtkActor()
actor_0.SetMapper(composite_mapper_0)

# --- Demonstrate reading blow1 case with displacement ---
ensight_reader_1 = vtkEnSightGoldCombinedReader()
ensight_reader_1.SetCaseFileName(os.path.join(data_dir, "EnSight", "blow1_ascii.case"))

geometry_filter_1 = vtkGeometryFilter()
geometry_filter_1.RemoveGhostInterfacesOff()
geometry_filter_1.SetInputConnection(ensight_reader_1.GetOutputPort())

composite_mapper_1 = vtkCompositePolyDataMapper()
composite_mapper_1.SetInputConnection(geometry_filter_1.GetOutputPort())
composite_mapper_1.ColorByArrayComponent("displacement", 0)

actor_1 = vtkActor()
actor_1.SetMapper(composite_mapper_1)
actor_1.SetPosition(20, 0, 0)

# --- Demonstrate reading ironProt with contour ---
ensight_reader_2 = vtkEnSightGoldCombinedReader()
ensight_reader_2.SetCaseFileName(os.path.join(data_dir, "EnSight", "ironProt_ascii.case"))

contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(ensight_reader_2.GetOutputPort())
contour_filter.SetNumberOfContours(1)
contour_filter.SetValue(0, 200)
contour_filter.SetComputeScalars(1)

composite_mapper_2 = vtkCompositePolyDataMapper()
composite_mapper_2.SetInputConnection(contour_filter.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(composite_mapper_2)
actor_2.SetPosition(-40, 0, 0)

# --- Demonstrate reading office case with streamlines ---
ensight_reader_3 = vtkEnSightGoldCombinedReader()
ensight_reader_3.SetCaseFileName(os.path.join(data_dir, "EnSight", "office_ascii.case"))

stream_tracer = vtkStreamTracer()
stream_tracer.SetInputConnection(ensight_reader_3.GetOutputPort())
stream_tracer.SetStartPosition(0.1, 2.1, 0.5)
stream_tracer.SetMaximumPropagation(500)
stream_tracer.SetInitialIntegrationStep(0.1)
stream_tracer.SetIntegrationDirectionToForward()

composite_mapper_3 = vtkCompositePolyDataMapper()
composite_mapper_3.SetInputConnection(stream_tracer.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(composite_mapper_3)
actor_3.SetPosition(40, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight gold combined reader")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
