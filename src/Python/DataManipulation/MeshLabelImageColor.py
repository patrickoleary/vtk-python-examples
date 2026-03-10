#!/usr/bin/env python

# Read a label image in Meta format, mesh a single label with discrete
# flying edges, smooth the surface, and color vertices by smoothing error.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkWindowedSincPolyDataFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dim_gray_rgb = (0.412, 0.412, 0.412)

# Data: locate the labels.mhd file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
label_index = 31

# Reader: load the label image in Meta format
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "labels.mhd"))
reader.Update()

# Extract VOI: select the region of interest
voi = vtkExtractVOI()
voi.SetInputConnection(reader.GetOutputPort())
voi.SetVOI(0, 517, 0, 228, 0, 392)
voi.SetSampleRate(1, 1, 1)
voi.Update()

# Contour: extract a surface mesh for the selected label
contour = vtkDiscreteFlyingEdges3D()
contour.SetInputConnection(voi.GetOutputPort())
contour.SetValue(0, label_index)
contour.Update()

# Smoother: smooth the mesh and generate error scalars
smoother = vtkWindowedSincPolyDataFilter()
smoother.SetInputConnection(contour.GetOutputPort())
smoother.SetNumberOfIterations(30)
smoother.NonManifoldSmoothingOn()
smoother.NormalizeCoordinatesOn()
smoother.GenerateErrorScalarsOn()
smoother.Update()

se_range = smoother.GetOutput().GetPointData().GetScalars().GetRange()

# Lookup table: green-to-red diverging color map for smoothing error
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(1.0, 0.758, 0.214, 0.233)

table_size = 256
lut = vtkLookupTable()
lut.SetNumberOfTableValues(table_size)
lut.Build()
for i in range(table_size):
    rgba = list(ctf.GetColor(float(i) / table_size))
    rgba.append(1)
    lut.SetTableValue(i, rgba)

# Normals: compute cell normals for better lighting
normals = vtkPolyDataNormals()
normals.SetInputConnection(smoother.GetOutputPort())
normals.ComputeCellNormalsOn()
normals.ComputePointNormalsOff()
normals.ConsistencyOn()
normals.AutoOrientNormalsOn()
normals.SetFeatureAngle(60.0)

# Mapper: map the smoothed mesh to graphics primitives colored by error
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(se_range)
mapper.SetScalarModeToUsePointData()
mapper.SetLookupTable(lut)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(dim_gray_rgb)
renderer.AddActor(actor)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("MeshLabelImageColor")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
