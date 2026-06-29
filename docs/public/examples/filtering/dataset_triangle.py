#!/usr/bin/env python

# Triangulate a clipped region of CT head image data using
# vtkDataSetTriangleFilter and display with extracted edges.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkExtractEdges
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageClip
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read CT head data
reader = vtkImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 64)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)
reader.SetDataSpacing(1.6, 1.6, 1.5)

# Clip a small subregion
clipper = vtkImageClip()
clipper.SetInputConnection(reader.GetOutputPort())
clipper.SetOutputWholeExtent(30, 36, 30, 36, 30, 36)

# Triangulate the dataset
tris = vtkDataSetTriangleFilter()
tris.SetInputConnection(clipper.GetOutputPort())

# Extract surface geometry
geom = vtkGeometryFilter()
geom.SetInputConnection(tris.GetOutputPort())

# Extract edges for wireframe overlay
edges = vtkExtractEdges()
edges.SetInputConnection(tris.GetOutputPort())

# Surface mapper
mapper_surface = vtkPolyDataMapper()
mapper_surface.SetInputConnection(geom.GetOutputPort())
mapper_surface.ScalarVisibilityOn()
mapper_surface.SetScalarRange(0, 1200)

# Edge mapper
mapper_edges = vtkPolyDataMapper()
mapper_edges.SetInputConnection(edges.GetOutputPort())
mapper_edges.SetResolveCoincidentTopologyToPolygonOffset()
mapper_edges.SetResolveCoincidentTopologyLineOffsetParameters(0, -7)

# Actors
actor_surface = vtkActor()
actor_surface.SetMapper(mapper_surface)

actor_edges = vtkActor()
actor_edges.SetMapper(mapper_edges)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_surface)
renderer.AddActor(actor_edges)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("dataset triangle")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
