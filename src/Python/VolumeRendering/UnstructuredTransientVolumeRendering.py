#!/usr/bin/env python

# Volume render a transient unstructured grid from vtkTimeSourceExample.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkFiltersGeneral import (
    vtkDataSetTriangleFilter,
    vtkTimeSourceExample,
)
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkUnstructuredGridVolumeRayCastMapper

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# TimeSourceExample: produces an unstructured grid that changes over time.
# The time range is [0, 1] with time-varying point scalars ("Point Label").
time_source = vtkTimeSourceExample()
time_source.SetGrowing(1)

# Request the first time step and update the pipeline.
# Use the modern API: set UPDATE_TIME_STEP on the output information object.
time_source.UpdateInformation()
time_key = vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP()
time_source.GetOutputInformation(0).Set(time_key, 0.0)
time_source.Update()

# TriangleFilter: tetrahedralize the unstructured grid for volume rendering.
# vtkUnstructuredGridVolumeRayCastMapper requires tetrahedral cells.
triangle_filter = vtkDataSetTriangleFilter()
triangle_filter.SetInputConnection(time_source.GetOutputPort())
triangle_filter.SetTetrahedraOnly(1)
triangle_filter.Update()

# Set the active scalar array for volume rendering
triangle_filter.GetOutput().GetPointData().SetActiveScalars("Point Label")
scalar_range = triangle_filter.GetOutput().GetPointData().GetScalars().GetRange()

# OpacityFunction: map scalar values to opacity
opacity = vtkPiecewiseFunction()
opacity.AddPoint(scalar_range[0], 0.0)
opacity.AddPoint(scalar_range[1], 0.8)

# ColorFunction: map scalar values to color (blue → red)
color_func = vtkColorTransferFunction()
color_func.SetColorSpaceToHSV()
color_func.HSVWrapOff()
color_func.AddRGBPoint(scalar_range[0], 0.0, 0.0, 1.0)
color_func.AddRGBPoint(scalar_range[1], 1.0, 0.0, 0.0)

# VolumeProperty: combine opacity and color transfer functions
volume_property = vtkVolumeProperty()
volume_property.SetScalarOpacity(opacity)
volume_property.SetColor(color_func)
volume_property.ShadeOff()
volume_property.SetInterpolationTypeToLinear()

# VolumeMapper: ray-cast the unstructured grid
volume_mapper = vtkUnstructuredGridVolumeRayCastMapper()
volume_mapper.SetInputConnection(triangle_filter.GetOutputPort())

# Volume: pair the mapper and property
volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# ScalarBar: legend showing the color mapping
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(color_func)
scalar_bar.SetOrientationToVertical()
scalar_bar.SetPosition(0.85, 0.1)
scalar_bar.SetPosition2(0.1, 0.8)

# TextActor: display the current time step
text_actor = vtkTextActor()
text_actor.SetInput("time = 0.00")
text_actor.GetTextProperty().SetFontSize(18)
text_actor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
text_actor.SetPosition(10, 10)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(scalar_bar)
renderer.AddActor(text_actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("UnstructuredTransientVolumeRendering")


class TimeAnimationCallback:
    """Advance through time steps using a repeating timer."""

    def __init__(self, source, tri_filter, text, num_steps=10):
        self.source = source
        self.tri_filter = tri_filter
        self.text = text
        self.num_steps = num_steps
        self.current_step = 0
        self.timer_id = None

    def execute(self, obj, event):
        t = self.current_step / self.num_steps
        self.text.SetInput(f"time = {t:.2f}")

        self.source.GetOutputInformation(0).Set(
            vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), t
        )
        self.source.Modified()
        self.tri_filter.Update()
        self.tri_filter.GetOutput().GetPointData().SetActiveScalars("Point Label")

        obj.GetRenderWindow().Render()

        self.current_step += 1
        if self.current_step > self.num_steps:
            if self.timer_id is not None:
                obj.DestroyTimer(self.timer_id)


# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Timer callback: animate through time steps
cb = TimeAnimationCallback(time_source, triangle_filter, text_actor, num_steps=10)
render_window_interactor.AddObserver("TimerEvent", cb.execute)

# Launch the interactive visualization
render_window_interactor.Initialize()
cb.timer_id = render_window_interactor.CreateRepeatingTimer(500)
render_window_interactor.Start()
