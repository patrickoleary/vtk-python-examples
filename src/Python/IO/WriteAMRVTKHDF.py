#!/usr/bin/env python

# Build a two-level overlapping AMR dataset with a Gaussian pulse scalar
# field, write it to the VTKHDF file format using vtkHDFWriter, read it
# back with vtkHDFReader, and render the block outlines and iso-surface.

import math
import tempfile
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkAMRBox,
    vtkOverlappingAMR,
    vtkUniformGrid,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOHDF import vtkHDFReader, vtkHDFWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.000, 0.843, 0.000)
peach_puff_rgb = (1.000, 0.855, 0.725)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Output path: write to a temporary directory
output_path = str(Path(tempfile.mkdtemp()) / "amr_gaussian_pulse.vtkhdf")

# Gaussian pulse centered at (5, 5, 5) with standard deviation 2
center = (5.0, 5.0, 5.0)
sigma = 2.0


def gaussian_pulse(x, y, z):
    """Evaluate a 3D Gaussian pulse."""
    dx, dy, dz = x - center[0], y - center[1], z - center[2]
    return math.exp(-(dx * dx + dy * dy + dz * dz) / (2.0 * sigma * sigma))


def fill_scalars(grid, origin, spacing, dims):
    """Compute Gaussian pulse values at every point of a uniform grid."""
    scalars = vtkFloatArray()
    scalars.SetName("Gaussian-Pulse")
    scalars.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
    idx = 0
    for k in range(dims[2]):
        for j in range(dims[1]):
            for i in range(dims[0]):
                x = origin[0] + spacing[0] * i
                y = origin[1] + spacing[1] * j
                z = origin[2] + spacing[2] * k
                scalars.SetValue(idx, gaussian_pulse(x, y, z))
                idx += 1
    grid.GetPointData().SetScalars(scalars)


# AMR: two-level overlapping adaptive mesh refinement
# Level 0: one coarse block covering [0, 10]^3
# Level 1: two refined blocks around the pulse center
amr = vtkOverlappingAMR()
amr.Initialize([1, 2])

dims = [11, 11, 11]

# Level 0, Block 0: coarse grid, spacing 1.0
ug0 = vtkUniformGrid()
ug0.SetOrigin(0.0, 0.0, 0.0)
ug0.SetSpacing(1.0, 1.0, 1.0)
ug0.SetDimensions(dims)
fill_scalars(ug0, (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), dims)
box0 = vtkAMRBox()
amr.SetAMRBox(0, 0, box0)
amr.SetDataSet(0, 0, ug0)

# Level 1, Block 0: refined grid at origin, spacing 0.5
ug1 = vtkUniformGrid()
ug1.SetOrigin(0.0, 0.0, 0.0)
ug1.SetSpacing(0.5, 0.5, 0.5)
ug1.SetDimensions(dims)
fill_scalars(ug1, (0.0, 0.0, 0.0), (0.5, 0.5, 0.5), dims)
box1 = vtkAMRBox()
amr.SetAMRBox(1, 0, box1)
amr.SetDataSet(1, 0, ug1)

# Level 1, Block 1: refined grid at (3, 3, 3), spacing 0.5
ug2 = vtkUniformGrid()
ug2.SetOrigin(3.0, 3.0, 3.0)
ug2.SetSpacing(0.5, 0.5, 0.5)
ug2.SetDimensions(dims)
fill_scalars(ug2, (3.0, 3.0, 3.0), (0.5, 0.5, 0.5), dims)
box2 = vtkAMRBox()
amr.SetAMRBox(1, 1, box2)
amr.SetDataSet(1, 1, ug2)
amr.SetRefinementRatio(0, 2)

# Write: save the AMR dataset to a VTKHDF file
writer = vtkHDFWriter()
writer.SetInputData(amr)
writer.SetFileName(output_path)
writer.SetOverwrite(True)
writer.Write()
print(f"Wrote {output_path}")

# Read: load the VTKHDF file back to verify the round-trip
reader = vtkHDFReader()
reader.SetFileName(output_path)
reader.Update()
print(f"Read back: {reader.GetOutput().GetClassName()}")

# Outline: show block bounding boxes of the original AMR data
outline = vtkOutlineFilter()
outline.SetInputData(amr)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(gold_rgb)
outline_actor.GetProperty().SetLineWidth(2)

# Contour: extract an iso-surface at the half-maximum of the Gaussian pulse
contour = vtkContourFilter()
contour.SetInputData(amr)
contour.SetNumberOfContours(1)
contour.SetValue(0, 0.5)

contour_geometry = vtkCompositeDataGeometryFilter()
contour_geometry.SetInputConnection(contour.GetOutputPort())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_geometry.GetOutputPort())
contour_mapper.SetScalarRange(0.0, 1.0)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WriteAMRVTKHDF")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
