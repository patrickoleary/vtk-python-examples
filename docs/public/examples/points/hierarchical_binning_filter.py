#!/usr/bin/env python

# Demonstrate vtkHierarchicalBinningFilter and vtkExtractHierarchicalBins
# by binning a bounded random point source, extracting a specific bin,
# and rendering extracted points with the bin outline.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkExtractHierarchicalBins,
    vtkHierarchicalBinningFilter,
)
from vtkmodules.vtkFiltersSources import vtkOutlineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 1000000
bin_num = 16
math = vtkMath()
math.RandomSeed(31415)

# Create bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Hierarchical binning
hierarchical_binning = vtkHierarchicalBinningFilter()
hierarchical_binning.SetInputConnection(points.GetOutputPort())
hierarchical_binning.AutomaticOff()
hierarchical_binning.SetDivisions(2, 2, 2)
hierarchical_binning.SetBounds(points.GetOutput().GetBounds())

timer = vtkTimerLog()
timer.StartTimer()
hierarchical_binning.Update()
timer.StopTimer()
print("Points processed: {0}".format(n_pts))
print("   Time to bin: {0}".format(timer.GetElapsedTime()))

# Extract a specific bin
extract_bin = vtkExtractHierarchicalBins()
extract_bin.SetInputConnection(hierarchical_binning.GetOutputPort())
extract_bin.SetBinningFilter(hierarchical_binning)
extract_bin.SetLevel(1000)
extract_bin.Update()
extract_bin.SetBin(1000000000)
extract_bin.SetLevel(-1)
extract_bin.SetBin(bin_num)
extract_bin.Update()

bin_mapper = vtkPointGaussianMapper()
bin_mapper.SetInputConnection(extract_bin.GetOutputPort())
bin_mapper.EmissiveOff()
bin_mapper.SetScaleFactor(0.0)

bin_actor = vtkActor()
bin_actor.SetMapper(bin_mapper)

# Outline of the full point set
outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Outline of the extracted bin
bin_bounds = [0, 0, 0, 0, 0, 0]
hierarchical_binning.GetBinBounds(bin_num, bin_bounds)
bin_outline = vtkOutlineSource()
bin_outline.SetBounds(bin_bounds)

bin_outline_mapper = vtkPolyDataMapper()
bin_outline_mapper.SetInputConnection(bin_outline.GetOutputPort())

bin_outline_actor = vtkActor()
bin_outline_actor.SetMapper(bin_outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(bin_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(bin_outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("hierarchical binning filter")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(1, 1, 1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
