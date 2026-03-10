#!/usr/bin/env python

# Read an STL mesh, voxelize it into a binary stencil mask, write the
# mask to a MetaImage (.mha) file, and visualize the center slice
# alongside the original mesh.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkIOImage import vtkMetaImageWriter
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkPolyDataToImageStencil,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
mesh_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the STL mesh
reader = vtkSTLReader()
reader.SetFileName(str(data_dir / "headMesh.stl"))
reader.Update()
mesh = reader.GetOutput()
bounds = mesh.GetBounds()

# Blank image: create an empty volume covering the mesh bounds with padding
voxel_spacing = 0.5
pixel_padding = 5
origin_shift = pixel_padding * voxel_spacing
spacing = [voxel_spacing, voxel_spacing, voxel_spacing]
origin = [bounds[0] - origin_shift,
          bounds[2] - origin_shift,
          bounds[4] - origin_shift]
extent = [0, int((bounds[1] - bounds[0]) / voxel_spacing) + 2 * pixel_padding,
          0, int((bounds[3] - bounds[2]) / voxel_spacing) + 2 * pixel_padding,
          0, int((bounds[5] - bounds[4]) / voxel_spacing) + 2 * pixel_padding]

blank_image = vtkImageData()
blank_image.SetSpacing(spacing)
blank_image.SetOrigin(origin)
blank_image.SetExtent(extent)
blank_image.AllocateScalars(3, 1)  # VTK_UNSIGNED_CHAR, 1 component
blank_image.GetPointData().GetScalars().Fill(0)

# Stencil: convert the polydata surface into a voxel stencil
poly_to_stencil = vtkPolyDataToImageStencil()
poly_to_stencil.SetInputData(mesh)
poly_to_stencil.SetOutputSpacing(spacing)
poly_to_stencil.SetOutputOrigin(origin)
poly_to_stencil.SetOutputWholeExtent(extent)

# Image stencil: apply the stencil to the blank image to create a binary mask
stencil = vtkImageStencil()
stencil.SetInputData(blank_image)
stencil.SetStencilConnection(poly_to_stencil.GetOutputPort())
stencil.ReverseStencilOn()
stencil.SetBackgroundValue(255)
stencil.Update()

# Writer: save the voxelized mask to a MetaImage file
writer = vtkMetaImageWriter()
writer.SetFileName("ReadSTLWriteMHA.mha")
writer.SetInputData(stencil.GetOutput())
writer.Write()

# Mapper: map the original mesh for overlay
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor: assign the mapped geometry with a semi-transparent appearance
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(mesh_rgb)
actor.GetProperty().SetOpacity(0.3)

# Image actor: display the center Z-slice of the voxelized mask
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputData(stencil.GetOutput())
mid_z = (extent[4] + extent[5]) // 2
image_actor.SetDisplayExtent(extent[0], extent[1],
                             extent[2], extent[3],
                             mid_z, mid_z)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(image_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadSTLWriteMHA")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
