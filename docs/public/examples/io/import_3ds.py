#!/usr/bin/env python

# Import 3DS, export to OBJ, then re-import the OBJ and render with textures.

import os
import tempfile

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOExport import vtkOBJExporter
from vtkmodules.vtkIOImport import vtk3DSImporter, vtkOBJImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Phase 1: Import 3DS and export as OBJ
render_window_1 = vtkRenderWindow()
renderer_1 = vtkRenderer()
render_window_1.AddRenderer(renderer_1)

ds_importer = vtk3DSImporter()
ds_importer.SetFileName(os.path.join(data_dir, "iflamigm.3ds"))
ds_importer.SetRenderWindow(render_window_1)
ds_importer.Update()

temp_dir = tempfile.mkdtemp()
prefix = os.path.join(temp_dir, "iflamigm")

obj_exporter = vtkOBJExporter()
obj_exporter.SetFilePrefix(prefix)
obj_exporter.SetOBJFileComment("Converted from iflamigm.3ds")
obj_exporter.SetMTLFileComment("Converted from iflamigm.3ds")
obj_exporter.SetActiveRenderer(renderer_1)
obj_exporter.SetRenderWindow(render_window_1)
obj_exporter.Write()

# Phase 2: Re-import the OBJ with textures
obj_importer = vtkOBJImporter()
obj_importer.SetFileName(prefix + ".obj")
obj_importer.SetFileNameMTL(prefix + ".mtl")
obj_importer.SetTexturePath(temp_dir)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.753, 0.753, 0.753)
renderer.GradientBackgroundOn()
renderer.SetBackground2(0.839, 0.839, 0.839)
renderer.UseHiddenLineRemovalOn()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("import 3ds")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

obj_importer.SetRenderWindow(render_window)
obj_importer.Update()

# Enable texture interpolation on imported actors
actors = renderer.GetActors()
actors.InitTraversal()
for _ in range(actors.GetNumberOfItems()):
    actor = actors.GetNextActor()
    if actor.GetTexture():
        actor.GetTexture().InterpolateOn()

interactor.Initialize()
interactor.Start()
