#!/usr/bin/env python

# Read transient data from a VTK HDF file and animate through the time
# steps using a repeating timer callback.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOHDF import vtkHDFReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load transient VTK HDF data
reader = vtkHDFReader()
reader.SetFileName(str(data_dir / "warping_spheres.vtkhdf"))
reader.Update()

# Color transfer function: blue-white-red diverging colormap
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(-30.0, 0.086, 0.004, 0.298)
ctf.AddRGBPoint(-14.0, 0.400, 0.700, 0.900)
ctf.AddRGBPoint(  0.0, 1.000, 1.000, 1.000)
ctf.AddRGBPoint(  2.3, 0.700, 0.100, 0.100)

# Mapper: color the composite surface by SpatioTemporalHarmonics field
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetLookupTable(ctf)
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("SpatioTemporalHarmonics")

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(background_rgb)
renderer.UseHiddenLineRemovalOn()
renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("TransientHDFReaderApp")
render_window.SetSize(1024, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())


# Animation callback: step through time on each timer event.
# A class is required because VTK observer callbacks must be callable
# objects that retain a reference to the reader and interactor.
class AnimationCallback:
    def __init__(self, hdf_reader, interactor):
        self.reader = hdf_reader
        self.interactor = interactor

    def __call__(self, caller, event):
        current = self.reader.GetStep()
        total = self.reader.GetNumberOfSteps()
        self.reader.SetStep(0 if current == total - 1 else current + 1)
        self.reader.Update()
        self.interactor.Render()


# Initialize must happen before adding observers and creating timers
render_window_interactor.Initialize()
render_window_interactor.AddObserver(
    "TimerEvent", AnimationCallback(reader, render_window_interactor))
render_window_interactor.CreateRepeatingTimer(50)

# Launch the interactive visualization
render_window_interactor.Start()
