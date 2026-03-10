#!/usr/bin/env python

# Convert labeled voxels from a segmented volume into colored cubes.  Each
# label in the range 1–29 is thresholded, converted to surface geometry, and
# displayed with scalar coloring.

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
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageWrapPad
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

# Label range to display
start_label = 1
end_label = 29

# Reader: load the labeled frog-tissue volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "Frog" / "frogtissue.mhd"))
reader.Update()

# Pad: extend the volume by one voxel so point data can become cell data
extent = reader.GetOutput().GetExtent()
pad = vtkImageWrapPad()
pad.SetInputConnection(reader.GetOutputPort())
pad.SetOutputWholeExtent(
    extent[0], extent[1] + 1,
    extent[2], extent[3] + 1,
    extent[4], extent[5] + 1,
)
pad.Update()

# Copy point scalars into cell scalars
pad.GetOutput().GetCellData().SetScalars(
    reader.GetOutput().GetPointData().GetScalars()
)

# Threshold: select cells whose scalar lies within the label range
selector = vtkThreshold()
selector.SetInputArrayToProcess(
    0, 0, 0,
    vtkDataObject().FIELD_ASSOCIATION_CELLS,
    vtkDataSetAttributes().SCALARS,
)
selector.SetInputConnection(pad.GetOutputPort())
selector.SetLowerThreshold(start_label)
selector.SetUpperThreshold(end_label)
selector.Update()

# Transform: shift geometry by half a voxel so cubes align with labels
transform = vtkTransform()
transform.Translate(-0.5, -0.5, -0.5)

transform_filter = vtkTransformFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(selector.GetOutputPort())

# GeometryFilter: convert unstructured grid to polydata for rendering
geometry = vtkGeometryFilter()
geometry.SetInputConnection(transform_filter.GetOutputPort())

# Mapper: color cubes by their label value
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetScalarRange(start_label, end_label)
mapper.SetScalarModeToUseCellData()
mapper.SetColorModeToMapScalars()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("GenerateCubesFromLabels")
render_window.Render()

# Camera: position for a clear view of the frog anatomy
camera = renderer.GetActiveCamera()
camera.SetPosition(42.301174, 939.893457, -124.005030)
camera.SetFocalPoint(224.697134, 221.301653, 146.823706)
camera.SetViewUp(0.262286, -0.281321, -0.923073)
camera.SetDistance(789.297581)
camera.SetClippingRange(168.744328, 1509.660206)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
