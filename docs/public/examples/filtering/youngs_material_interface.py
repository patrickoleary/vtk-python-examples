#!/usr/bin/env python

# Demonstrate vtkYoungsMaterialInterface by reading a 2D UCD dataset with
# volume fraction and normal data, thresholding by material, reconstructing
# interfaces, and rendering the wireframe mesh with surface interfaces.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import (
    vtkCompositeDataSet,
    vtkDataObject,
    vtkDataSetAttributes,
    vtkMultiBlockDataSet,
)
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeneral import vtkYoungsMaterialInterface
from vtkmodules.vtkIOGeometry import vtkAVSucdReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read AVS UCD data
reader = vtkAVSucdReader()
reader.SetFileName(os.path.join(data_dir, "UCD2D", "UCD_00005.inp"))
reader.Update()

mesh = reader.GetOutput()
cell_data = mesh.GetCellData()

# Create normal vectors from norme[0] and norme[1]
cell_data.SetActiveScalars("norme[0]")
norm_x = cell_data.GetScalars()
cell_data.SetActiveScalars("norme[1]")
norm_y = cell_data.GetScalars()
n = norm_x.GetNumberOfTuples()

norm = vtkDoubleArray()
norm.SetNumberOfComponents(3)
norm.SetNumberOfTuples(n)
norm.SetName("norme")
for i in range(n):
    norm.SetTuple3(i, norm_x.GetTuple1(i), norm_y.GetTuple1(i), 0.0)
cell_data.SetVectors(norm)

# Extract submesh for material 2
cell_data.SetActiveScalars("Material Id")
threshold_2 = vtkThreshold()
threshold_2.SetInputData(mesh)
threshold_2.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, vtkDataSetAttributes.SCALARS
)
threshold_2.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
threshold_2.SetLowerThreshold(2.0)
threshold_2.Update()
mesh_mat_2 = threshold_2.GetOutput()

# Extract submesh for material 3
threshold_3 = vtkThreshold()
threshold_3.SetInputData(mesh)
threshold_3.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, vtkDataSetAttributes.SCALARS
)
threshold_3.SetThresholdFunction(vtkThreshold.THRESHOLD_UPPER)
threshold_3.SetUpperThreshold(3.0)
threshold_3.Update()
mesh_mat_3 = threshold_3.GetOutput()

# Make multiblock from extracted submeshes
mesh_mb = vtkMultiBlockDataSet()
mesh_mb.SetNumberOfBlocks(2)
mesh_mb.GetMetaData(0).Set(vtkCompositeDataSet.NAME(), "Material 2")
mesh_mb.SetBlock(0, mesh_mat_2)
mesh_mb.GetMetaData(1).Set(vtkCompositeDataSet.NAME(), "Material 3")
mesh_mb.SetBlock(1, mesh_mat_3)

# Wireframe actor for material 2 mesh
mat_range = cell_data.GetScalars().GetRange()
mesh_mapper = vtkDataSetMapper()
mesh_mapper.SetInputData(mesh_mat_2)
mesh_mapper.SetScalarRange(mat_range)
mesh_mapper.SetScalarModeToUseCellData()
mesh_mapper.SetColorModeToMapScalars()
mesh_mapper.ScalarVisibilityOn()
mesh_mapper.SetResolveCoincidentTopologyPolygonOffsetParameters(0, 1)
mesh_mapper.SetResolveCoincidentTopologyToPolygonOffset()

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetRepresentationToWireframe()

# Reconstruct Youngs material interface
cell_data.SetActiveScalars("frac_pres[1]")
youngs = vtkYoungsMaterialInterface()
youngs.SetInputData(mesh_mb)
youngs.SetNumberOfMaterials(2)
youngs.SetMaterialVolumeFractionArray(0, "frac_pres[1]")
youngs.SetMaterialVolumeFractionArray(1, "frac_pres[2]")
youngs.SetMaterialNormalArray(0, "norme")
youngs.SetMaterialNormalArray(1, "norme")
youngs.SetVolumeFractionRange(0.001, 0.999)
youngs.FillMaterialOn()
youngs.RemoveAllMaterialBlockMappings()
youngs.AddMaterialBlockMapping(-1)
youngs.AddMaterialBlockMapping(1)
youngs.AddMaterialBlockMapping(-2)
youngs.AddMaterialBlockMapping(2)
youngs.UseAllBlocksOff()
youngs.Update()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)
renderer.AddViewProp(mesh_actor)

# Access interface blocks directly.
# Output is a 2-level multiblock: 2 input blocks x 2 materials.
# Flat indices: root=0, block0=1, leaf(0,0)=2, leaf(0,1)=3, block1=4, leaf(1,0)=5, leaf(1,1)=6.
output_mb = youngs.GetOutput()
sub_block_0 = output_mb.GetBlock(0)
sub_block_1 = output_mb.GetBlock(1)

# Block 0: flat index 2 → b_comp = 0.0
interface_ds_0 = sub_block_0.GetBlock(0)
interface_mapper_0 = vtkDataSetMapper()
interface_mapper_0.SetInputDataObject(interface_ds_0)
interface_mapper_0.ScalarVisibilityOff()
interface_mapper_0.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 100)
interface_mapper_0.SetResolveCoincidentTopologyToPolygonOffset()
interface_actor_0 = vtkActor()
interface_actor_0.SetMapper(interface_mapper_0)
interface_actor_0.GetProperty().SetColor(0.0, 1.0, 0.0)
interface_actor_0.GetProperty().SetRepresentationToSurface()
renderer.AddViewProp(interface_actor_0)

# Block 1: flat index 3 → b_comp = 1.0
interface_ds_1 = sub_block_0.GetBlock(1)
interface_mapper_1 = vtkDataSetMapper()
interface_mapper_1.SetInputDataObject(interface_ds_1)
interface_mapper_1.ScalarVisibilityOff()
interface_mapper_1.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 100)
interface_mapper_1.SetResolveCoincidentTopologyToPolygonOffset()
interface_actor_1 = vtkActor()
interface_actor_1.SetMapper(interface_mapper_1)
interface_actor_1.GetProperty().SetColor(0.0, 0.0, 1.0)
interface_actor_1.GetProperty().SetRepresentationToSurface()
renderer.AddViewProp(interface_actor_1)

# Block 2: flat index 5 → b_comp = 1.0
interface_ds_2 = sub_block_1.GetBlock(0)
interface_mapper_2 = vtkDataSetMapper()
interface_mapper_2.SetInputDataObject(interface_ds_2)
interface_mapper_2.ScalarVisibilityOff()
interface_mapper_2.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 100)
interface_mapper_2.SetResolveCoincidentTopologyToPolygonOffset()
interface_actor_2 = vtkActor()
interface_actor_2.SetMapper(interface_mapper_2)
interface_actor_2.GetProperty().SetColor(0.0, 0.0, 1.0)
interface_actor_2.GetProperty().SetRepresentationToSurface()
renderer.AddViewProp(interface_actor_2)

# Block 3: flat index 6 → b_comp = 1.0
interface_ds_3 = sub_block_1.GetBlock(1)
interface_mapper_3 = vtkDataSetMapper()
interface_mapper_3.SetInputDataObject(interface_ds_3)
interface_mapper_3.ScalarVisibilityOff()
interface_mapper_3.SetResolveCoincidentTopologyPolygonOffsetParameters(1, 100)
interface_mapper_3.SetResolveCoincidentTopologyToPolygonOffset()
interface_actor_3 = vtkActor()
interface_actor_3.SetMapper(interface_mapper_3)
interface_actor_3.GetProperty().SetColor(0.0, 0.0, 1.0)
interface_actor_3.GetProperty().SetRepresentationToSurface()
renderer.AddViewProp(interface_actor_3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 200)
render_window.SetMultiSamples(0)
render_window.SetWindowName("youngs material interface")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
