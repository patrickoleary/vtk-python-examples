#!/usr/bin/env python

# Demonstrate vtkDiskSource with specified inner and outer radii.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkDiskSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Disk source
disk = vtkDiskSource()
disk.SetInnerRadius(1.0)
disk.SetOuterRadius(2.0)
disk.SetRadialResolution(1)
disk.SetCircumferentialResolution(20)

disk_mapper = vtkPolyDataMapper()
disk_mapper.SetInputConnection(disk.GetOutputPort())

disk_actor = vtkActor()
disk_actor.SetMapper(disk_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(disk_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("disk source")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
