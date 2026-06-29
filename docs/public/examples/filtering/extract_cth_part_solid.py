#!/usr/bin/env python

# Demonstrate vtkExtractCTHPart with solid geometry generation by reading
# a rectilinear grid with CTH volume fraction data, extracting solid
# geometry for each part, and iterating composite output blocks.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import (
    vtkAlgorithm,
    vtkCompositeDataPipeline,
)
from vtkmodules.vtkFiltersParallel import vtkExtractCTHPart
from vtkmodules.vtkIOXML import vtkXMLRectilinearGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Use composite data pipeline with multiblock datasets
algorithm = vtkAlgorithm()
pipeline = vtkCompositeDataPipeline()
algorithm.SetDefaultExecutivePrototype(pipeline)

# Read CTH data
reader = vtkXMLRectilinearGridReader()
reader.SetFileName(os.path.join(data_dir, "cth.vtr"))
reader.UpdateInformation()
reader.SetCellArrayStatus("X Velocity", 0)
reader.SetCellArrayStatus("Y Velocity", 0)
reader.SetCellArrayStatus("Z Velocity", 0)
reader.SetCellArrayStatus("Mass for Armor Plate", 0)
reader.SetCellArrayStatus("Mass for Body, Nose", 0)

# Extract CTH parts with solid geometry
extract = vtkExtractCTHPart()
extract.SetInputConnection(reader.GetOutputPort())
extract.AddVolumeArrayName("Volume Fraction for Armor Plate")
extract.AddVolumeArrayName("Volume Fraction for Body, Nose")
extract.SetClipPlane(None)
extract.GenerateSolidGeometryOn()

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(256)
lookup_table.SetHueRange(0.6667, 0)
lookup_table.SetSaturationRange(1, 1)
lookup_table.SetValueRange(1, 1)
lookup_table.SetTableRange(0, 1)
lookup_table.SetVectorComponent(0)
lookup_table.Build()

extract.Update()
composite_data = extract.GetOutput()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.33, 0.35, 0.43)

# Block 0: Armor Plate.
curr_data_0 = composite_data.GetBlock(0)
mapper_0 = vtkDataSetMapper()
mapper_0.SetInputData(curr_data_0)
mapper_0.SetScalarRange(0, 1)
mapper_0.UseLookupTableScalarRangeOn()
mapper_0.SetScalarVisibility(1)
mapper_0.SetScalarModeToUsePointFieldData()
mapper_0.SelectColorArray("Part Index")
mapper_0.SetLookupTable(lookup_table)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetRepresentationToSurface()
actor_0.GetProperty().SetInterpolationToGouraud()
actor_0.GetProperty().SetAmbient(0)
actor_0.GetProperty().SetDiffuse(1)
actor_0.GetProperty().SetSpecular(0)
actor_0.GetProperty().SetSpecularPower(1)
actor_0.GetProperty().SetSpecularColor(1, 1, 1)
renderer.AddActor(actor_0)

# Block 1: Body, Nose.
curr_data_1 = composite_data.GetBlock(1)
mapper_1 = vtkDataSetMapper()
mapper_1.SetInputData(curr_data_1)
mapper_1.SetScalarRange(0, 1)
mapper_1.UseLookupTableScalarRangeOn()
mapper_1.SetScalarVisibility(1)
mapper_1.SetScalarModeToUsePointFieldData()
mapper_1.SelectColorArray("Part Index")
mapper_1.SetLookupTable(lookup_table)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetRepresentationToSurface()
actor_1.GetProperty().SetInterpolationToGouraud()
actor_1.GetProperty().SetAmbient(0)
actor_1.GetProperty().SetDiffuse(1)
actor_1.GetProperty().SetSpecular(0)
actor_1.GetProperty().SetSpecularPower(1)
actor_1.GetProperty().SetSpecularColor(1, 1, 1)
renderer.AddActor(actor_1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract cth part solid")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

algorithm.SetDefaultExecutivePrototype(None)

interactor.Initialize()
interactor.Start()
