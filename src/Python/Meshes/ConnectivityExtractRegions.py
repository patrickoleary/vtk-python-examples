#!/usr/bin/env python

# Extract connected regions from a mesh containing two separate spheres
# using vtkConnectivityFilter. Each connected region is colored by its
# region ID.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkConnectivityFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source 1: sphere at the origin
sphere1 = vtkSphereSource()
sphere1.SetCenter(-1.5, 0.0, 0.0)
sphere1.SetRadius(1.0)
sphere1.SetThetaResolution(20)
sphere1.SetPhiResolution(20)

# Source 2: sphere offset to the right
sphere2 = vtkSphereSource()
sphere2.SetCenter(1.5, 0.0, 0.0)
sphere2.SetRadius(1.0)
sphere2.SetThetaResolution(20)
sphere2.SetPhiResolution(20)

# Append: combine both spheres into one polydata
appender = vtkAppendPolyData()
appender.AddInputConnection(sphere1.GetOutputPort())
appender.AddInputConnection(sphere2.GetOutputPort())

# ConnectivityFilter: label each connected region
connectivity = vtkConnectivityFilter()
connectivity.SetInputConnection(appender.GetOutputPort())
connectivity.SetExtractionModeToAllRegions()
connectivity.ColorRegionsOn()
connectivity.Update()

# Mapper: color by region ID
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(connectivity.GetOutputPort())
mapper.SetScalarRange(0, 1)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ConnectivityExtractRegions")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
