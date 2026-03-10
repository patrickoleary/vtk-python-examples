#!/usr/bin/env python

# Generate smoothed surface models from a labeled segmentation volume using
# vtkDiscreteFlyingEdges3D.  Each label produces a separate isosurface that
# is smoothed with a windowed sinc filter and displayed in a single scene.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkDataSetAttributes,
)
from vtkmodules.vtkFiltersCore import (
    vtkMaskFields,
    vtkThreshold,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingStatistics import vtkImageAccumulate
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_blue_rgb = (0.282, 0.239, 0.545)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Label range and smoothing parameters
start_label = 1
end_label = 29
smoothing_iterations = 15
pass_band = 0.001
feature_angle = 120.0

# Reader: load the labeled frog-tissue volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "Frog" / "frogtissue.mhd"))

# Histogram: determine which labels are present in the volume
histogram = vtkImageAccumulate()
histogram.SetInputConnection(reader.GetOutputPort())
histogram.SetComponentExtent(0, end_label, 0, 0, 0, 0)
histogram.SetComponentOrigin(0, 0, 0)
histogram.SetComponentSpacing(1, 1, 1)
histogram.Update()

# DiscreteFlyingEdges3D: generate isosurfaces for each label value
discrete_cubes = vtkDiscreteFlyingEdges3D()
discrete_cubes.SetInputConnection(reader.GetOutputPort())
discrete_cubes.GenerateValues(end_label - start_label + 1, start_label, end_label)

# Smoother: smooth the label surfaces while preserving boundaries
smoother = vtkWindowedSincPolyDataFilter()
smoother.SetInputConnection(discrete_cubes.GetOutputPort())
smoother.SetNumberOfIterations(smoothing_iterations)
smoother.BoundarySmoothingOff()
smoother.FeatureEdgeSmoothingOff()
smoother.SetFeatureAngle(feature_angle)
smoother.SetPassBand(pass_band)
smoother.NonManifoldSmoothingOn()
smoother.NormalizeCoordinatesOn()
smoother.Update()

# Renderer: assemble all label surfaces into one scene
renderer = vtkRenderer()
renderer.SetBackground(dark_slate_blue_rgb)

for i in range(start_label, end_label + 1):
    # Skip labels that are not present in the volume
    frequency = histogram.GetOutput().GetPointData().GetScalars().GetTuple1(i)
    if frequency == 0.0:
        continue

    # ---- Threshold: isolate the current label ----
    selector = vtkThreshold()
    selector.SetInputConnection(smoother.GetOutputPort())
    selector.SetInputArrayToProcess(
        0, 0, 0,
        vtkDataObject().FIELD_ASSOCIATION_POINTS,
        vtkDataSetAttributes().SCALARS,
    )
    selector.SetLowerThreshold(i)
    selector.SetUpperThreshold(i)

    # ---- MaskFields: strip scalar arrays for clean geometry ----
    scalars_off = vtkMaskFields()
    scalars_off.SetInputConnection(selector.GetOutputPort())
    scalars_off.CopyAttributeOff(vtkMaskFields().POINT_DATA, vtkDataSetAttributes().SCALARS)
    scalars_off.CopyAttributeOff(vtkMaskFields().CELL_DATA, vtkDataSetAttributes().SCALARS)

    # ---- GeometryFilter: convert to polydata for rendering ----
    geometry = vtkGeometryFilter()
    geometry.SetInputConnection(scalars_off.GetOutputPort())

    # ---- Mapper: map the surface geometry ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(geometry.GetOutputPort())
    mapper.ScalarVisibilityOff()

    # ---- Actor: add to the scene with a unique color per label ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    hue = (i - start_label) / (end_label - start_label)
    actor.GetProperty().SetColor(
        0.5 + 0.5 * abs(2.0 * hue - 1.0),
        0.7 * (1.0 - hue),
        0.7 * hue,
    )
    renderer.AddActor(actor)

# Camera: position for a clear view of the frog anatomy
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(-90)
camera.Azimuth(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("GenerateModelsFromLabels")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Initialize()
interactor.Start()
