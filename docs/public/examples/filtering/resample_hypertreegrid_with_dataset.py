#!/usr/bin/env python

# Resample a pre-configured HyperTreeGrid with a wavelet dataset
# using vtkResampleWithDataSet, colored by tree depth.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkResampleWithDataSet
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridPreConfiguredSource
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: pre-configured HyperTreeGrid
htg_source = vtkHyperTreeGridPreConfiguredSource()
htg_source.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.CUSTOM)
htg_source.SetCustomArchitecture(vtkHyperTreeGridPreConfiguredSource.UNBALANCED)
htg_source.SetCustomDim(3)
htg_source.SetCustomFactor(2)
htg_source.SetCustomDepth(6)
htg_source.SetCustomSubdivisions(3, 3, 2)
htg_source.SetCustomExtent(-10, 10, -10, 10, -10, 10)

# Source: wavelet as probing geometry
wavelet = vtkRTAnalyticSource()

# Filter: resample the HyperTreeGrid onto the wavelet
prober = vtkResampleWithDataSet()
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
render_window.SetWindowName("resample hypertreegrid with dataset")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-15, -15, -15)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
