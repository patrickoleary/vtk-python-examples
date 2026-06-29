#!/usr/bin/env python

# Probe a random HyperTreeGrid with a wavelet dataset and
# color the result by tree depth.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkHyperTreeGridProbeFilter
from vtkmodules.vtkFiltersSources import vtkRandomHyperTreeGridSource
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: random HyperTreeGrid
htg_source = vtkRandomHyperTreeGridSource()
htg_source.SetDimensions(5, 5, 5)
htg_source.SetOutputBounds(-10, 10, -10, 10, -10, 10)
htg_source.SetSeed(0)
htg_source.SetMaxDepth(4)
htg_source.SetSplitFraction(0.4)

# Source: wavelet as probing geometry
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)

# Filter: probe the HyperTreeGrid with the wavelet
prober = vtkHyperTreeGridProbeFilter()
prober.SetInputConnection(wavelet.GetOutputPort())
prober.SetSourceConnection(htg_source.GetOutputPort())
prober.SetPassPointArrays(True)
prober.SetUseImplicitArrays(False)
prober.Update()
prober.GetOutput().GetPointData().SetActiveScalars("Depth")

# Lookup table for tree depth
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(6)
lookup_table.SetTableRange(0, 5)

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(prober.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetLookupTable(lookup_table)
mapper.UseLookupTableScalarRangeOn()
mapper.SetScalarModeToUsePointData()
mapper.ColorByArrayComponent("Depth", 0)
mapper.InterpolateScalarsBeforeMappingOn()

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hypertreegrid probe")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-15, -15, -15)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
