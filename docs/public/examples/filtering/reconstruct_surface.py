#!/usr/bin/env python

# Test vtkSurfaceReconstructionFilter on point cloud data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkReverseSense,
)
from vtkmodules.vtkFiltersSources import vtkProgrammableSource
from vtkmodules.vtkImagingHybrid import vtkSurfaceReconstructionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read points from file using a programmable source
point_source = vtkProgrammableSource()

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

def read_points():
    fp = open(os.path.join(data_dir, "cactus.3337.pts"), "r")
    points = vtkPoints()
    while True:
        line = fp.readline().split()
        if len(line) == 0:
            break
        if line[0] == "p":
            points.InsertNextPoint(float(line[1]), float(line[2]), float(line[3]))
    point_source.GetPolyDataOutput().SetPoints(points)

point_source.SetExecuteMethod(read_points)

# Construct the surface and create isosurface
surface_reconstruction = vtkSurfaceReconstructionFilter()
surface_reconstruction.SetInputConnection(point_source.GetOutputPort())

contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(surface_reconstruction.GetOutputPort())
contour_filter.SetValue(0, 0.0)

reverse = vtkReverseSense()
reverse.SetInputConnection(contour_filter.GetOutputPort())
reverse.ReverseCellsOn()
reverse.ReverseNormalsOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reverse.GetOutputPort())
mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(mapper)
surface_actor.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)
surface_actor.GetProperty().SetSpecularColor(1, 1, 1)
surface_actor.GetProperty().SetSpecular(.4)
surface_actor.GetProperty().SetSpecularPower(50)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("reconstruct surface")

# Scene
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(20)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
