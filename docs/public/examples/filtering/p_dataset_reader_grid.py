#!/usr/bin/env python

# Write and read parallel datasets (structured grid, image data, polydata) and render them.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersParallel import vtkTransmitStructuredDataPiece
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOParallel import (
    vtkMultiBlockPLOT3DReader,
    vtkPDataSetReader,
    vtkPDataSetWriter,
)
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkParallelCore import vtkDummyController
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
temp_dir = tempfile.mkdtemp()

dummy_controller = vtkDummyController()

# ====== Structured Grid ======
# Source
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.Update()

grid_transmit = vtkTransmitStructuredDataPiece()
grid_transmit.SetController(dummy_controller)
grid_transmit.SetInputData(plot3d_reader.GetOutput().GetBlock(0))

grid_writer = vtkPDataSetWriter()
grid_writer.SetFileName(os.path.join(temp_dir, "comb.pvtk"))
grid_writer.SetInputConnection(grid_transmit.GetOutputPort())
grid_writer.SetNumberOfPieces(4)
grid_writer.Write()

grid_reader = vtkPDataSetReader()
grid_reader.SetFileName(os.path.join(temp_dir, "comb.pvtk"))

# Filter
grid_surface = vtkDataSetSurfaceFilter()
grid_surface.SetInputConnection(grid_reader.GetOutputPort())

# Mapper
grid_mapper = vtkPolyDataMapper()
grid_mapper.SetInputConnection(grid_surface.GetOutputPort())
grid_mapper.SetNumberOfPieces(2)
grid_mapper.SetPiece(0)
grid_mapper.SetGhostLevel(1)
grid_mapper.Update()

# Actor
grid_actor = vtkActor()
grid_actor.SetMapper(grid_mapper)
grid_actor.SetPosition(-5, 0, -29)

# Clean up structured grid temp files
path = os.path.join(temp_dir, "comb.pvtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "comb.0.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "comb.1.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "comb.2.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "comb.3.vtk")
if os.path.exists(path):
    os.remove(path)

# ====== ImageData ======
# Source
mandelbrot_source = vtkImageMandelbrotSource()
mandelbrot_source.SetWholeExtent(0, 9, 0, 9, 0, 9)
mandelbrot_source.SetSampleCX(0.1, 0.1, 0.1, 0.1)
mandelbrot_source.SetMaximumNumberOfIterations(10)

image_transmit = vtkTransmitStructuredDataPiece()
image_transmit.SetController(dummy_controller)
image_transmit.SetInputConnection(mandelbrot_source.GetOutputPort())

image_writer = vtkPDataSetWriter()
image_writer.SetFileName(os.path.join(temp_dir, "fractal.pvtk"))
image_writer.SetInputConnection(image_transmit.GetOutputPort())
image_writer.SetNumberOfPieces(4)
image_writer.Write()

image_reader = vtkPDataSetReader()
image_reader.SetFileName(os.path.join(temp_dir, "fractal.pvtk"))

# Filter
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(image_reader.GetOutputPort())
contour_filter.SetValue(0, 4)

# Mapper
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_filter.GetOutputPort())
contour_mapper.SetNumberOfPieces(3)
contour_mapper.SetPiece(0)
contour_mapper.SetGhostLevel(0)
contour_mapper.Update()
contour_mapper.GetInput().RemoveGhostCells()

# Actor
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.SetScale(5, 5, 5)
contour_actor.SetPosition(6, 6, 6)

# Clean up fractal temp files
path = os.path.join(temp_dir, "fractal.pvtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "fractal.0.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "fractal.1.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "fractal.2.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "fractal.3.vtk")
if os.path.exists(path):
    os.remove(path)

# ====== PolyData ======
# Source
sphere_source = vtkSphereSource()
sphere_source.SetRadius(2)

sphere_writer = vtkPDataSetWriter()
sphere_writer.SetFileName(os.path.join(temp_dir, "sphere.pvtk"))
sphere_writer.SetInputConnection(sphere_source.GetOutputPort())
sphere_writer.SetNumberOfPieces(4)
sphere_writer.Write()

sphere_reader = vtkPDataSetReader()
sphere_reader.SetFileName(os.path.join(temp_dir, "sphere.pvtk"))

# Mapper
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_reader.GetOutputPort())
sphere_mapper.SetNumberOfPieces(2)
sphere_mapper.SetPiece(0)
sphere_mapper.SetGhostLevel(1)
sphere_mapper.Update()

# Actor
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetPosition(6, 6, 6)

# Clean up sphere temp files
path = os.path.join(temp_dir, "sphere.pvtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "sphere.0.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "sphere.1.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "sphere.2.vtk")
if os.path.exists(path):
    os.remove(path)
path = os.path.join(temp_dir, "sphere.3.vtk")
if os.path.exists(path):
    os.remove(path)

os.rmdir(temp_dir)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(grid_actor)
renderer.AddActor(contour_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("p dataset reader grid")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(20)
camera.Elevation(40)
renderer.ResetCamera()
camera.Zoom(1.2)

interactor.Initialize()
interactor.Start()
