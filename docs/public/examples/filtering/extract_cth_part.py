#!/usr/bin/env python

# Demonstrate vtkExtractCTHPart by reading a rectilinear grid with CTH
# volume fraction data and extracting isosurfaces for armor plate and
# body/nose parts, rendered with a lookup table.

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
    vtkCompositePolyDataMapper,
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

# Extract CTH parts
extract = vtkExtractCTHPart()
extract.SetInputConnection(reader.GetOutputPort())
extract.AddVolumeArrayName("Volume Fraction for Armor Plate")
extract.AddVolumeArrayName("Volume Fraction for Body, Nose")
extract.SetClipPlane(None)

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(256)
lookup_table.SetHueRange(0.6667, 0)
lookup_table.SetSaturationRange(1, 1)
lookup_table.SetValueRange(1, 1)
lookup_table.SetTableRange(0, 1)
lookup_table.SetVectorComponent(0)
lookup_table.Build()

# Composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(extract.GetOutputPort())
mapper.SetScalarRange(0, 1)
mapper.UseLookupTableScalarRangeOn()
mapper.SetScalarVisibility(1)
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Part Index")
mapper.SetLookupTable(lookup_table)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().SetInterpolationToGouraud()
actor.GetProperty().SetAmbient(0)
actor.GetProperty().SetDiffuse(1)
actor.GetProperty().SetSpecular(0)
actor.GetProperty().SetSpecularPower(1)
actor.GetProperty().SetSpecularColor(1, 1, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.33, 0.35, 0.43)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract cth part")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

algorithm.SetDefaultExecutivePrototype(None)

interactor.Initialize()
interactor.Start()
