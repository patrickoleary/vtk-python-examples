#!/usr/bin/env python

# Test vtkImageDataLIC2D with probed vector data and a noise texture.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math
import os

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkFiltersCore import vtkProbeFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOLegacy import vtkGenericDataObjectReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLICOpenGL2 import vtkImageDataLIC2D

# Parameters
magnification = 5
num_partitions = 5
num_steps = 40
resolution = 10

# Read data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkGenericDataObjectReader()
reader.SetFileName(os.path.join(data_dir, "SurfaceVectors.vtk"))
reader.Update()

dataset = reader.GetUnstructuredGridOutput()
bounds = dataset.GetBounds()

# Determine data orientation
# XY plane (bounds[4] == bounds[5])
comp = [0, 1, 2]
if bounds[0] == bounds[1]:
    comp = [1, 2, 0]
elif bounds[2] == bounds[3]:
    comp = [0, 2, 1]

width = int(math.ceil((bounds[2 * comp[0] + 1] - bounds[2 * comp[0]]) * resolution))
height = int(math.ceil((bounds[2 * comp[1] + 1] - bounds[2 * comp[1]]) * resolution))

dims = [0, 0, 0]
dims[comp[0]] = width
dims[comp[1]] = height
dims[comp[2]] = 1

spacing = [0.0, 0.0, 0.0]
spacing[comp[0]] = (bounds[2 * comp[0] + 1] - bounds[2 * comp[0]]) / float(width)
spacing[comp[1]] = (bounds[2 * comp[1] + 1] - bounds[2 * comp[1]]) / float(height)
spacing[comp[2]] = 1.0

origin = [bounds[0], bounds[2], bounds[4]]

out_width = magnification * width
out_height = magnification * height

# Create probe image data
probe_data = vtkImageData()
probe_data.SetOrigin(origin)
probe_data.SetDimensions(dims)
probe_data.SetSpacing(spacing)

probe = vtkProbeFilter()
probe.SetSourceConnection(reader.GetOutputPort())
probe.SetInputData(probe_data)
probe.Update()

# Read noise texture
noise_reader = vtkPNGReader()
noise_reader.SetFileName(os.path.join(data_dir, "noise.png"))
noise_reader.Update()

noise = noise_reader.GetOutput()
char_values = noise.GetPointData().GetScalars()
num_tuples = char_values.GetNumberOfTuples()

# Convert noise from unsigned char to float
float_values = vtkFloatArray()
float_values.SetNumberOfComponents(2)
float_values.SetNumberOfTuples(num_tuples)
float_values.SetName("noise")
for i in range(num_tuples * 2):
    comp_idx = i % 2
    tup_idx = i // 2
    float_values.SetComponent(tup_idx, comp_idx, char_values.GetComponent(tup_idx, comp_idx) / 255.0)

noise.GetPointData().RemoveArray(0)
noise.GetPointData().SetScalars(float_values)

# Create rendering context
render_window = vtkRenderWindow()
render_window.Render()

# Create and run the LIC filter
lic_filter = vtkImageDataLIC2D()
if lic_filter.SetContext(render_window) == 0:
    print("WARNING: Required OpenGL not supported, skipping.")
else:
    lic_filter.SetSteps(num_steps)
    lic_filter.SetStepSize(0.8 / magnification)
    lic_filter.SetMagnification(magnification)
    lic_filter.SetInputConnection(0, probe.GetOutputPort(0))
    lic_filter.SetInputData(1, noise)
    lic_filter.UpdateInformation()

    # Assemble LIC result from partitions
    lic_data_size = out_width * out_height
    lic_data = vtkFloatArray()
    lic_data.SetNumberOfComponents(3)
    lic_data.SetNumberOfTuples(lic_data_size)

    for kk in range(num_partitions):
        lic_filter.UpdatePiece(kk, num_partitions, 0)
        lic_piece = lic_filter.GetOutput()
        lic_scalars = lic_piece.GetPointData().GetScalars()
        piece_ext = list(lic_piece.GetExtent())

        # Copy piece into full array
        pw = piece_ext[2 * comp[0] + 1] - piece_ext[2 * comp[0]] + 1
        ph = piece_ext[2 * comp[1] + 1] - piece_ext[2 * comp[1]] + 1
        for j in range(ph):
            for i in range(pw):
                src_idx = j * pw + i
                dst_x = piece_ext[2 * comp[0]] + i
                dst_y = piece_ext[2 * comp[1]] + j
                dst_idx = dst_y * out_width + dst_x
                if 0 <= dst_idx < lic_data_size and src_idx < lic_scalars.GetNumberOfTuples():
                    for c in range(3):
                        lic_data.SetComponent(dst_idx, c, lic_scalars.GetComponent(src_idx, c))

    # Convert to unsigned char for display
    lic_png = vtkUnsignedCharArray()
    lic_png.SetNumberOfComponents(3)
    lic_png.SetNumberOfTuples(lic_data_size)
    for i in range(lic_data_size):
        for c in range(3):
            lic_png.SetComponent(i, c, int(lic_data.GetComponent(i, c) * 255.0))

    # Wrap into image data for display
    out_spacing = [
        spacing[comp[0]] / magnification,
        spacing[comp[1]] / magnification,
        1.0,
    ]

    png_data = vtkImageData()
    png_data.SetDimensions(out_width, out_height, 1)
    png_data.SetSpacing(out_spacing)
    png_data.SetOrigin(origin)
    png_data.GetPointData().SetScalars(lic_png)

    # Display using standard rendering pipeline
    renderer = vtkRenderer()
    renderer.GetActiveCamera().ParallelProjectionOn()

    image_actor = vtkImageActor()
    image_actor.GetMapper().SetInputData(png_data)
    renderer.AddActor(image_actor)

    render_window.AddRenderer(renderer)
    render_window.SetWindowName("imagedata lic2d")

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    renderer.ResetCamera()
    interactor.Initialize()
    interactor.Start()
