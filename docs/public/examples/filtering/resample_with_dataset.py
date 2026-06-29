#!/usr/bin/env python

# Resample a clipped, transformed wavelet multi-block dataset onto
# another wavelet source using vtkResampleWithDataSet.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkMultiBlockDataSet,
    vtkSphere,
)
from vtkmodules.vtkCommonExecutionModel import vtkExtentTranslator
from vtkmodules.vtkFiltersCore import vtkResampleWithDataSet
from vtkmodules.vtkFiltersGeneral import (
    vtkRandomAttributeGenerator,
    vtkTableBasedClipDataSet,
    vtkTransformFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource  # moved in VTK 9.6
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

number_of_input_blocks = 3
number_of_source_blocks = 5

# --- Build input multi-block dataset ---

input_mb = vtkMultiBlockDataSet()
input_mb.SetNumberOfBlocks(number_of_input_blocks)

input_translator = vtkExtentTranslator()
input_translator.SetWholeExtent(-16, 16, -16, 16, -16, 16)
input_translator.SetNumberOfPieces(number_of_input_blocks)
input_translator.SetSplitModeToBlock()

input_wavelet = vtkRTAnalyticSource()
input_wavelet.SetWholeExtent(-16, 16, -16, 16, -16, 16)
input_wavelet.SetCenter(0, 0, 0)

cylinder = vtkCylinder()
cylinder.SetCenter(0, 0, 0)
cylinder.SetRadius(15)
cylinder.SetAxis(0, 1, 0)

clip_cyl = vtkTableBasedClipDataSet()
clip_cyl.SetClipFunction(cylinder)
clip_cyl.InsideOutOn()

clip_sphere = vtkSphere()
clip_sphere.SetCenter(0, 0, 4)
clip_sphere.SetRadius(12)

clip_sphr = vtkTableBasedClipDataSet()
clip_sphr.SetInputConnection(clip_cyl.GetOutputPort())
clip_sphr.SetClipFunction(clip_sphere)

transform = vtkTransform()
transform.RotateZ(45)

trans_filter = vtkTransformFilter()
trans_filter.SetInputConnection(clip_sphr.GetOutputPort())
trans_filter.SetTransform(transform)

random_attrs = vtkRandomAttributeGenerator()
random_attrs.SetInputConnection(trans_filter.GetOutputPort())
random_attrs.GeneratePointScalarsOn()
random_attrs.GeneratePointVectorsOn()
random_attrs.GeneratePointTensorsOn()
random_attrs.GenerateCellScalarsOn()
random_attrs.GenerateCellVectorsOn()
random_attrs.GenerateCellTensorsOn()
random_attrs.GenerateFieldArrayOn()
random_attrs.SetNumberOfTuples(100)

for i in range(number_of_input_blocks):
    block_extent = [0] * 6
    input_translator.SetPiece(i)
    input_translator.PieceToExtent()
    block_extent = list(input_translator.GetExtent())
    input_wavelet.UpdateExtent(block_extent)
    clip_cyl.SetInputData(input_wavelet.GetOutputDataObject(0))
    random_attrs.Update()
    block = random_attrs.GetOutputDataObject(0).NewInstance()
    block.DeepCopy(random_attrs.GetOutputDataObject(0))
    input_mb.SetBlock(i, block)
    block.UnRegister(None)

# --- Build source multi-block dataset ---

source_mb = vtkMultiBlockDataSet()
source_mb.SetNumberOfBlocks(number_of_source_blocks)

source_translator = vtkExtentTranslator()
source_translator.SetWholeExtent(-22, 22, -22, 22, -16, 16)
source_translator.SetNumberOfPieces(number_of_source_blocks)
source_translator.SetSplitModeToBlock()

source_wavelet = vtkRTAnalyticSource()
source_wavelet.SetWholeExtent(-22, 22, -22, 22, -16, 16)
source_wavelet.SetCenter(0, 0, 0)

for i in range(number_of_source_blocks):
    block_extent = [0] * 6
    source_translator.SetPiece(i)
    source_translator.PieceToExtent()
    block_extent = list(source_translator.GetExtent())
    source_wavelet.UpdateExtent(block_extent)
    block = source_wavelet.GetOutputDataObject(0).NewInstance()
    block.DeepCopy(source_wavelet.GetOutputDataObject(0))
    source_mb.SetBlock(i, block)
    block.UnRegister(None)

# Resample input onto source
resample = vtkResampleWithDataSet()
resample.SetInputData(input_mb)
resample.SetSourceData(source_mb)
resample.PassCellArraysOn()
resample.PassPointArraysOn()
resample.Update()

# Extract geometry for rendering
to_poly = vtkCompositeDataGeometryFilter()
to_poly.SetInputData(resample.GetOutputDataObject(0))
to_poly.Update()

scalar_range = to_poly.GetOutput().GetPointData().GetArray("RTData").GetRange()

# Mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(to_poly.GetOutputPort())
mapper.SetScalarRange(scalar_range)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("resample with dataset")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
