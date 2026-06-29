#!/usr/bin/env python

# Read NIFTI files, write and re-read to verify, then display in two viewports.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import (
    vtkNIFTIImageReader,
    vtkNIFTIImageWriter,
)
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

# Verify read-write-read roundtrip for minimal.nii.gz
inpath_1 = os.path.join(data_dir, "minimal.nii.gz")
outpath_1 = os.path.join(temp_dir, "out_minimal.nii.gz")

nifti_reader_1 = vtkNIFTIImageReader()
nifti_reader_1.SetFileName(inpath_1)
nifti_reader_1.TimeAsVectorOn()
nifti_reader_1.Update()

nifti_writer_1 = vtkNIFTIImageWriter()
nifti_writer_1.SetInputConnection(nifti_reader_1.GetOutputPort())
nifti_writer_1.SetFileName(outpath_1)
nifti_writer_1.SetNIFTIHeader(nifti_reader_1.GetNIFTIHeader())
nifti_writer_1.SetQFac(nifti_reader_1.GetQFac())
nifti_writer_1.SetTimeDimension(nifti_reader_1.GetTimeDimension())
nifti_writer_1.SetQFormMatrix(nifti_reader_1.GetQFormMatrix())
nifti_writer_1.SetSFormMatrix(nifti_reader_1.GetSFormMatrix())
nifti_writer_1.Write()

reread_1 = vtkNIFTIImageReader()
reread_1.SetFileName(outpath_1)
reread_1.TimeAsVectorOn()
reread_1.Update()

diff_1 = vtkImageMathematics()
diff_1.SetOperationToSubtract()
diff_1.SetInputConnection(0, nifti_reader_1.GetOutputPort())
diff_1.SetInputConnection(1, reread_1.GetOutputPort())
diff_1.Update()
diff_range_1 = diff_1.GetOutput().GetScalarRange()
diff_err_1 = diff_range_1[0] ** 2 + diff_range_1[1] ** 2
assert diff_err_1 == 0, "Input minimal.nii.gz differs from output out_minimal.nii.gz"

# Verify read-write-read roundtrip for minimal.img.gz
inpath_2 = os.path.join(data_dir, "minimal.img.gz")
outpath_2 = os.path.join(temp_dir, "out_minimal.hdr")

nifti_reader_2 = vtkNIFTIImageReader()
nifti_reader_2.SetFileName(inpath_2)
nifti_reader_2.TimeAsVectorOn()
nifti_reader_2.Update()

nifti_writer_2 = vtkNIFTIImageWriter()
nifti_writer_2.SetInputConnection(nifti_reader_2.GetOutputPort())
nifti_writer_2.SetFileName(outpath_2)
nifti_writer_2.SetNIFTIHeader(nifti_reader_2.GetNIFTIHeader())
nifti_writer_2.SetQFac(nifti_reader_2.GetQFac())
nifti_writer_2.SetTimeDimension(nifti_reader_2.GetTimeDimension())
nifti_writer_2.SetQFormMatrix(nifti_reader_2.GetQFormMatrix())
nifti_writer_2.SetSFormMatrix(nifti_reader_2.GetSFormMatrix())
nifti_writer_2.Write()

reread_2 = vtkNIFTIImageReader()
reread_2.SetFileName(outpath_2)
reread_2.TimeAsVectorOn()
reread_2.Update()

diff_2 = vtkImageMathematics()
diff_2.SetOperationToSubtract()
diff_2.SetInputConnection(0, nifti_reader_2.GetOutputPort())
diff_2.SetInputConnection(1, reread_2.GetOutputPort())
diff_2.Update()
diff_range_2 = diff_2.GetOutput().GetScalarRange()
diff_err_2 = diff_range_2[0] ** 2 + diff_range_2[1] ** 2
assert diff_err_2 == 0, "Input minimal.img.gz differs from output out_minimal.hdr"

# Display the avg152T1 NIFTI image in two viewports
disp_reader = vtkNIFTIImageReader()
disp_reader.SetFileName(os.path.join(data_dir, "avg152T1_RL_nifti.nii.gz"))
disp_reader.Update()

size = disp_reader.GetOutput().GetDimensions()
center = disp_reader.GetOutput().GetCenter()
spacing = disp_reader.GetOutput().GetSpacing()

# Adjust centers for even/odd dimensions
center_1 = list(center)
center_2 = list(center)
if size[2] % 2 == 1:
    center_1[2] = center[2] + 0.5 * spacing[2]
if size[0] % 2 == 1:
    center_2[0] = center[0] + 0.5 * spacing[0]

vrange = disp_reader.GetOutput().GetScalarRange()

# Axial view
axial_mapper = vtkImageSliceMapper()
axial_mapper.BorderOn()
axial_mapper.SliceAtFocalPointOn()
axial_mapper.SliceFacesCameraOn()
axial_mapper.SetInputConnection(disp_reader.GetOutputPort())

axial_slice = vtkImageSlice()
axial_slice.SetMapper(axial_mapper)
axial_slice.GetProperty().SetColorWindow(vrange[1] - vrange[0])
axial_slice.GetProperty().SetColorLevel(0.5 * (vrange[0] + vrange[1]))

# Sagittal view
sagittal_mapper = vtkImageSliceMapper()
sagittal_mapper.BorderOn()
sagittal_mapper.SliceAtFocalPointOn()
sagittal_mapper.SliceFacesCameraOn()
sagittal_mapper.SetInputConnection(disp_reader.GetOutputPort())

sagittal_slice = vtkImageSlice()
sagittal_slice.SetMapper(sagittal_mapper)
sagittal_slice.GetProperty().SetColorWindow(vrange[1] - vrange[0])
sagittal_slice.GetProperty().SetColorLevel(0.5 * (vrange[0] + vrange[1]))

# Two viewports
ratio = size[0] * 1.0 / (size[0] + size[2])

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, ratio, 1.0)
renderer_0.AddViewProp(axial_slice)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(ratio, 0.0, 1.0, 1.0)
renderer_1.AddViewProp(sagittal_slice)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("nifti reader writer")
render_window.SetMultiSamples(0)
render_window.SetSize((size[0] + size[2]) // 2 * 2, size[1] // 2 * 2)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(0.5 * spacing[1] * size[1])
camera_0.SetFocalPoint(center_1[0], center_1[1], center_1[2])
camera_0.SetPosition(center_1[0], center_1[1], center_1[2] - 100.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.5 * spacing[1] * size[1])
camera_1.SetFocalPoint(center_2[0], center_2[1], center_2[2])
camera_1.SetPosition(center_2[0] + 100.0, center_2[1], center_2[2])

interactor.Initialize()
interactor.Start()

# Clean up temp files
for f in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, f))
os.rmdir(temp_dir)
