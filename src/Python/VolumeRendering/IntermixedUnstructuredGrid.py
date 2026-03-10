#!/usr/bin/env python

# Intermixed volume rendering of an unstructured grid with a polygonal contour.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkThreshold
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkUnstructuredGridVolumeRayCastMapper

# Colors (normalized RGB)
green_bkg_rgb = (0.098, 0.400, 0.200)

# Data: locate the datasets
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
iron_prot_file = str(data_dir / "ironProt.vtk")
neghip_file = str(data_dir / "neghip.slc")

# Source 1: read the iron protein data for volume rendering
reader = vtkStructuredPointsReader()
reader.SetFileName(iron_prot_file)

# Source 2: read the neghip data for polygonal contouring
reader2 = vtkSLCReader()
reader2.SetFileName(neghip_file)

# Threshold: convert from vtkImageData to vtkUnstructuredGrid,
# remove cells where all values are below 80
thresh = vtkThreshold()
thresh.SetInputConnection(reader.GetOutputPort())
thresh.SetUpperThreshold(80)
thresh.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
thresh.SetAllScalars(False)

# Triangulate: convert to triangles for the unstructured grid mapper
trifilter = vtkDataSetTriangleFilter()
trifilter.SetInputConnection(thresh.GetOutputPort())

# Transfer functions: map scalar value to opacity and color
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(80, 0.0)
opacity_transfer_function.AddPoint(120, 0.2)
opacity_transfer_function.AddPoint(255, 0.2)

color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(80.0, 0.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(120.0, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(160.0, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(200.0, 0.0, 1.0, 0.0)
color_transfer_function.AddRGBPoint(255.0, 0.0, 1.0, 1.0)

# VolumeProperty: describe how the volume data will look
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)
volume_property.ShadeOff()
volume_property.SetInterpolationTypeToLinear()

# VolumeMapper: unstructured grid ray cast mapper
volume_mapper = vtkUnstructuredGridVolumeRayCastMapper()
volume_mapper.SetInputConnection(trifilter.GetOutputPort())

# Volume: holds the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Contour: extract isosurface from the neghip data
contour = vtkContourFilter()
contour.SetInputConnection(reader2.GetOutputPort())
contour.SetValue(0, 80)

# Mapper: map contour output to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

# Actor: polygonal contour surface
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer: assemble the scene with both volume and polygonal data
renderer = vtkRenderer()
renderer.AddViewProp(contour_actor)
renderer.AddVolume(volume)
renderer.SetBackground(green_bkg_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 512)
render_window.SetWindowName("IntermixedUnstructuredGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
