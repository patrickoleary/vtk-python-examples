#!/usr/bin/env python

# Test vtkStructuredGridLIC2D with an X-direction slice.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkImageData, vtkStructuredGrid
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)
from vtkmodules.vtkRenderingLICOpenGL2 import vtkStructuredGridLIC2D

# Parameters
magnification = 8
num_steps = 100
slice_dir = 0  # X slice
slice_idx = 98
zoom_factor = 3.0

# Read structured grid data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkXMLStructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "timestep_0_15.vts"))
reader.Update()

# Determine VOI based on slice direction
extent = list(reader.GetOutput().GetExtent())
voi = list(extent)

# X slice (YZ plane)
voi[0] = voi[1] = max(extent[0], min(extent[0] + slice_idx, extent[1]))

# Extract slice
extract_voi = vtkExtractGrid()
extract_voi.SetInputConnection(reader.GetOutputPort())
extract_voi.SetVOI(voi)

# Renderer
renderer = vtkRenderer()

# Render window (functional exception: Render() needed for OpenGL context)
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.Render()

# Read noise texture
noise_reader = vtkPNGReader()
noise_reader.SetFileName(os.path.join(data_dir, "noise.png"))

# Apply structured grid LIC
lic_filter = vtkStructuredGridLIC2D()
if lic_filter.SetContext(render_window) == 0:
    print("WARNING: Required OpenGL extensions not supported, skipping.")
else:
    lic_filter.SetInputConnection(extract_voi.GetOutputPort())
    lic_filter.SetInputConnection(1, noise_reader.GetOutputPort(0))
    lic_filter.SetSteps(num_steps)
    lic_filter.SetStepSize(0.01 / magnification)
    lic_filter.SetMagnification(magnification)

    # Process single partition
    lic_filter.UpdatePiece(0, 1, 0)
    if lic_filter.GetFBOSuccess() == 0 or lic_filter.GetLICSuccess() == 0:
        print("WARNING: LIC computation failed, skipping.")
    else:
        # Get LIC image output
        lic_image = vtkImageData()
        lic_image.ShallowCopy(lic_filter.GetOutputDataObject(1))

        scalar_range = lic_image.GetPointData().GetScalars().GetRange()

        # Scale to unsigned char for texture
        caster = vtkImageShiftScale()
        caster.SetInputData(lic_image)
        caster.SetOutputScalarTypeToUnsignedChar()
        caster.SetShift(-scalar_range[0])
        if scalar_range[1] - scalar_range[0] > 0:
            caster.SetScale(255.0 / (scalar_range[1] - scalar_range[0]))
        caster.Update()

        texture = vtkTexture()
        texture.SetInputConnection(caster.GetOutputPort())

        # Get geometry output
        lic_geometry = vtkStructuredGrid()
        lic_geometry.ShallowCopy(lic_filter.GetOutput(0))

        surface_filter = vtkDataSetSurfaceFilter()
        surface_filter.SetInputData(lic_geometry)

        surface_mapper = vtkPolyDataMapper()
        surface_mapper.SetInputConnection(surface_filter.GetOutputPort())
        surface_mapper.SetScalarVisibility(0)

        surface_actor = vtkActor()
        surface_actor.SetMapper(surface_mapper)
        surface_actor.SetTexture(texture)
        renderer.AddActor(surface_actor)

    # Scene
    renderer.SetBackground(0.2, 0.1, 0.2)
    renderer.ResetCamera()
    camera = renderer.GetActiveCamera()
    camera.Zoom(zoom_factor)
    camera.Azimuth(90)

    render_window.SetWindowName("structuredgrid lic2 dx slice")

    # Interactor
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    interactor.Initialize()
    interactor.Start()
