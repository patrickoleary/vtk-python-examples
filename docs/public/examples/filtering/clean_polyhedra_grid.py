#!/usr/bin/env python

# Clean a polyhedra grid converted from PLOT3D data using
# vtkStaticCleanUnstructuredGrid with various tolerance settings.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkFiltersCore import (
    vtkConvertToPolyhedra,
    vtkStaticCleanUnstructuredGrid,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load PLOT3D multi-block data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
pl3d_output = plot3d_reader.GetOutput().GetBlock(0)

# Convert to unstructured grid
ext_sphere = vtkSphere()
ext_sphere.SetCenter(0, 0, 0)
ext_sphere.SetRadius(1000)
extract_geometry = vtkExtractGeometry()
extract_geometry.SetInputData(pl3d_output)
extract_geometry.SetImplicitFunction(ext_sphere)
extract_geometry.Update()
sample = extract_geometry.GetOutput()

# Convert mesh to polyhedra
convert_0 = vtkConvertToPolyhedra()
convert_0.SetInputData(sample)
convert_0.Update()

# Clean with zero tolerance
clean_0 = vtkStaticCleanUnstructuredGrid()
clean_0.SetInputConnection(convert_0.GetOutputPort())
clean_0.ToleranceIsAbsoluteOn()
clean_0.SetTolerance(0.0)
clean_0.RemoveUnusedPointsOff()
clean_0.Update()

print(f"Cleaning grid with: {sample.GetNumberOfPoints()} points and {sample.GetNumberOfCells()} cells")
print(f"Zero tolerance: {clean_0.GetOutput().GetNumberOfPoints()} points, {clean_0.GetOutput().GetNumberOfCells()} cells")

# Shrink with factor 0.999 and clean with non-zero tolerance
shrink = vtkShrinkFilter()
shrink.SetInputData(sample)
shrink.SetShrinkFactor(0.999)
shrink.Update()

convert_1 = vtkConvertToPolyhedra()
convert_1.SetInputConnection(shrink.GetOutputPort())

clean_1 = vtkStaticCleanUnstructuredGrid()
clean_1.SetInputConnection(convert_1.GetOutputPort())
clean_1.ToleranceIsAbsoluteOn()
clean_1.SetAbsoluteTolerance(0.01)
clean_1.ProduceMergeMapOn()
clean_1.AveragePointDataOff()
clean_1.Update()

print(f"Non-zero tolerance: {clean_1.GetOutput().GetNumberOfPoints()} points, {clean_1.GetOutput().GetNumberOfCells()} cells")

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(clean_1.GetOutputPort())
mapper.SetScalarRange(sample.GetPointData().GetScalars().GetRange())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToFlat()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("clean polyhedra grid")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
