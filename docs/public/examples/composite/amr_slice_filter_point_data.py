#!/usr/bin/env python

# Demonstrate vtkAMRSliceFilter on synthetic point data generated from
# vtkRTAnalyticSource converted to AMR via vtkImageToAMR, with a
# diverging color map showing only leaf-level blocks.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import (
    vtkCompositeDataSet,
    vtkDataObjectTreeIterator,
    vtkOverlappingAMR,
)
from vtkmodules.vtkFiltersAMR import vtkAMRSliceFilter, vtkImageToAMR
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkCompositeDataDisplayAttributes,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Synthetic wavelet source (point data)
img_src = vtkRTAnalyticSource()

# Convert image to AMR with 3 levels
amr = vtkImageToAMR()
amr.SetInputConnection(img_src.GetOutputPort())
amr.SetNumberOfLevels(3)

# Slice AMR along Y-normal
slicer = vtkAMRSliceFilter()
slicer.SetInputConnection(amr.GetOutputPort())
slicer.SetNormal(1)
slicer.SetOffsetFromOrigin(10)
slicer.SetMaxResolution(2)

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(slicer.GetOutputPort())
surface.Update()

# Diverging color map: red -> blue
colormap = vtkColorTransferFunction()
colormap.SetColorSpaceToDiverging()
colormap.AddRGBPoint(0.0, 1.0, 0.0, 0.0)
colormap.AddRGBPoint(1.0, 0.0, 0.0, 1.0)

lookup_table = vtkLookupTable()
lookup_table.SetNumberOfColors(256)
for i in range(lookup_table.GetNumberOfColors()):
    color = [0.0, 0.0, 0.0]
    colormap.GetColor(float(i) / lookup_table.GetNumberOfColors(), color)
    lookup_table.SetTableValue(i, color[0], color[1], color[2], 1.0)
lookup_table.Build()

# Composite mapper with point field data coloring
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetLookupTable(lookup_table)
mapper.SetScalarRange(37.3531, 276.829)
mapper.SetScalarModeToUsePointFieldData()
mapper.SetInterpolateScalarsBeforeMapping(1)
mapper.SelectColorArray("RTData")

display_attributes = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Count non-leaf nodes to hide them
overlapping_amr = vtkOverlappingAMR.SafeDownCast(slicer.GetOutputDataObject(0))
non_leaf_nodes = 0
if overlapping_amr:
    for level_idx in range(overlapping_amr.GetNumberOfLevels()):
        if level_idx < 2:
            non_leaf_nodes += overlapping_amr.GetNumberOfBlocks(level_idx)

# Only show leaf nodes
composite_input = vtkCompositeDataSet.SafeDownCast(surface.GetOutputDataObject(0))
if composite_input:
    tree_iter = vtkDataObjectTreeIterator()
    tree_iter.SetDataSet(composite_input)
    tree_iter.SkipEmptyNodesOn()
    tree_iter.VisitOnlyLeavesOn()
    count = 0
    tree_iter.InitTraversal()
    while not tree_iter.IsDoneWithTraversal():
        flat_index = tree_iter.GetCurrentFlatIndex()
        mapper.SetBlockVisibility(flat_index, count > non_leaf_nodes)
        count += 1
        tree_iter.GoToNextItem()

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("amr slice filter point data")

# Scene
renderer.GetActiveCamera().SetPosition(15, 0, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
