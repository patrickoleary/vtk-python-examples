#!/usr/bin/env python

# Probe a multi-block HyperTreeGrid source with a wavelet dataset,
# coloring the result by tree depth.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersCore import vtkCompositeDataProbeFilter
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridPreConfiguredSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: two HyperTreeGrid blocks with different depths
source_mbds = vtkMultiBlockDataSet()
source_mbds.SetNumberOfBlocks(2)

htg_source_0 = vtkHyperTreeGridPreConfiguredSource()
htg_source_0.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.CUSTOM)
htg_source_0.SetCustomArchitecture(vtkHyperTreeGridPreConfiguredSource.UNBALANCED)
htg_source_0.SetCustomDim(3)
htg_source_0.SetCustomFactor(3)
htg_source_0.SetCustomDepth(5)
htg_source_0.SetCustomSubdivisions(3, 3, 3)
htg_source_0.SetCustomExtent(-10, 0, -10, 10, -10, 10)

htg_source_1 = vtkHyperTreeGridPreConfiguredSource()
htg_source_1.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.CUSTOM)
htg_source_1.SetCustomArchitecture(vtkHyperTreeGridPreConfiguredSource.UNBALANCED)
htg_source_1.SetCustomDim(3)
htg_source_1.SetCustomFactor(3)
htg_source_1.SetCustomDepth(6)
htg_source_1.SetCustomSubdivisions(3, 3, 2)
htg_source_1.SetCustomExtent(0, 10, -10, 10, -10, 10)

htg_source_0.Update()
htg_source_1.Update()

source_mbds.SetBlock(0, htg_source_0.GetOutput())
source_mbds.SetBlock(1, htg_source_1.GetOutput())

# Source: wavelet as the probing geometry
wavelet = vtkRTAnalyticSource()

# Filter: probe the HyperTreeGrid with the wavelet
prober = vtkCompositeDataProbeFilter()
prober.SetInputConnection(wavelet.GetOutputPort())
prober.SetSourceData(source_mbds)
prober.SetPassPointArrays(True)
prober.SetComputeTolerance(False)
prober.SetTolerance(0.0)
prober.Update()
prober.GetOutput().GetPointData().SetActiveScalars("Depth")

# Lookup table for tree depth
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(6)
lookup_table.SetTableRange(0, 5)

# Mapper: color by depth
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
render_window.SetWindowName("composite data probe with hypertreegrid")

# Scene
renderer.GetActiveCamera().SetPosition(-15, -15, -15)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
