#!/usr/bin/env python

# Test vtkRenderLargeImage with a camera window center offset,
# displaying the magnified result using vtkImageSliceMapper.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersHybrid import vtkRenderLargeImage
from vtkmodules.vtkIOImport import vtk3DSImporter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkImageSlice, vtkImageSliceMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Scene render window (offscreen source)
renderer_scene = vtkRenderer()
render_window_scene = vtkRenderWindow()
render_window_scene.AddRenderer(renderer_scene)

# Import 3DS scene
importer = vtk3DSImporter()
importer.SetRenderWindow(render_window_scene)
importer.ComputeNormalsOn()
importer.SetFileName(os.path.join(data_dir, "iflamigm.3ds"))
importer.Update()

importer.GetRenderer().SetBackground(0.1, 0.2, 0.4)
importer.GetRenderWindow().SetSize(150, 150)

# Get the renderer created by the importer
ren_collection = render_window_scene.GetRenderers()
ren_collection.InitTraversal()
ren = ren_collection.GetNextItem()

# Change view up to +z with window center offset
ren.GetActiveCamera().SetWindowCenter(-0.2, 0.3)
ren.GetActiveCamera().SetPosition(0, 1, 0)
ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
ren.GetActiveCamera().SetViewUp(0, 0, 1)
ren.ResetCamera()
ren.GetActiveCamera().Dolly(1.4)
renderer_scene.ResetCameraClippingRange()

# Render large image
render_large = vtkRenderLargeImage()
render_large.SetInput(renderer_scene)
render_large.SetMagnification(3)
render_large.Update()

# Display using vtkImageSliceMapper + vtkImageSlice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(render_large.GetOutputPort())

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)
image_slice.GetProperty().SetColorWindow(255)
image_slice.GetProperty().SetColorLevel(127.5)

# Viewer renderer
renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("large image offset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
