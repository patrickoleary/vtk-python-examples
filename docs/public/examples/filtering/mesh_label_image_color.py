#!/usr/bin/env python

# Read a label image in Meta format, mesh a single label with discrete
# flying edges, smooth the surface, and color vertices by smoothing error.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dim_gray_rgb = (0.412, 0.412, 0.412)

# Data: locate the labels.mhd file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
label_index = 31

# Reader: load the label image in Meta format
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "labels.mhd"))
reader.Update()

# Extract VOI: select the region of interest
extract_voi = vtkExtractVOI()
extract_voi.SetInputConnection(reader.GetOutputPort())
extract_voi.SetVOI(0, 517, 0, 228, 0, 392)
extract_voi.SetSampleRate(1, 1, 1)
extract_voi.Update()

# Contour: extract a surface mesh for the selected label
contour_filter = vtkDiscreteFlyingEdges3D()
contour_filter.SetInputConnection(extract_voi.GetOutputPort())
contour_filter.SetValue(0, label_index)
contour_filter.Update()

# Smoother: smooth the mesh and generate error scalars
smooth_filter = vtkWindowedSincPolyDataFilter()
smooth_filter.SetInputConnection(contour_filter.GetOutputPort())
smooth_filter.SetNumberOfIterations(30)
smooth_filter.NonManifoldSmoothingOn()
smooth_filter.NormalizeCoordinatesOn()
smooth_filter.GenerateErrorScalarsOn()
smooth_filter.Update()

smoothing_error_range = smooth_filter.GetOutput().GetPointData().GetScalars().GetRange()

# Lookup table: green-to-red diverging color map for smoothing error
color_transfer = vtkColorTransferFunction()
color_transfer.SetColorSpaceToDiverging()
color_transfer.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
color_transfer.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
color_transfer.AddRGBPoint(1.0, 0.758, 0.214, 0.233)

lut_size = 256
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(lut_size)
lookup_table.Build()
for i in range(lut_size):
    rgba = list(color_transfer.GetColor(float(i) / lut_size))
    rgba.append(1)
    lookup_table.SetTableValue(i, rgba)

# Normals: compute cell normals for better lighting
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(smooth_filter.GetOutputPort())
normals_filter.ComputeCellNormalsOn()
normals_filter.ComputePointNormalsOff()
normals_filter.ConsistencyOn()
normals_filter.AutoOrientNormalsOn()
normals_filter.SetFeatureAngle(60.0)

# Mapper: map the smoothed mesh to graphics primitives colored by error
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals_filter.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(smoothing_error_range)
mapper.SetScalarModeToUsePointData()
mapper.SetLookupTable(lookup_table)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(dim_gray_rgb)
renderer.AddActor(actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mesh label image color")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
