#!/usr/bin/env python

# Read an OpenFOAM case with face zones and render pressure on face zone.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOGeometry import vtkOpenFOAMReader
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))


def find_block_by_name(mb, name):
    """Recursively find a named block in a multi-block dataset."""
    if mb is None:
        return None
    for i in range(mb.GetNumberOfBlocks()):
        meta = mb.GetMetaData(i)
        if meta and meta.Get(vtkMultiBlockDataSet.NAME()) == name:
            return mb.GetBlock(i)
        child = vtkMultiBlockDataSet.SafeDownCast(mb.GetBlock(i))
        if child:
            result = find_block_by_name(child, name)
            if result:
                return result
    return None


def find_first_polydata(mb):
    """Recursively find the first vtkPolyData in a multi-block dataset."""
    if mb is None:
        return None
    for i in range(mb.GetNumberOfBlocks()):
        obj = mb.GetBlock(i)
        if obj and obj.GetClassName() == "vtkPolyData":
            return obj
        child = vtkMultiBlockDataSet.SafeDownCast(obj)
        if child:
            result = find_first_polydata(child)
            if result:
                return result
    return None


# Read OpenFOAM case with face zones
foam_reader = vtkOpenFOAMReader()
foam_reader.SetFileName(os.path.join(data_dir, "OpenFOAM", "squareBend", "squareBend.foam"))
foam_reader.SetTimeValue(100)
foam_reader.ReadZonesOn()
foam_reader.CopyDataToCellZonesOn()
foam_reader.DisableAllPatchArrays()
foam_reader.Update()

# Find zone blocks
all_blocks = foam_reader.GetOutput()
zone_blocks = find_block_by_name(all_blocks, "zones")
fzone = find_first_polydata(vtkMultiBlockDataSet.SafeDownCast(zone_blocks))

fzone.GetCellData().SetScalars(fzone.GetCellData().GetArray("p"))

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputData(fzone)
poly_mapper.ScalarVisibilityOn()
poly_mapper.SetColorModeToMapScalars()
poly_mapper.SetScalarRange(-40, 80)

# Actor
foam_actor = vtkActor()
foam_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(foam_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("open foam reader face zone")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
