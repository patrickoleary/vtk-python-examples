#!/usr/bin/env python

# Demonstrate vtkRecoverGeometryWireframe restoring original cell
# edges on a non-linearly subdivided quadratic tetra surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersGeometry import (
    vtkDataSetSurfaceFilter,
    vtkRecoverGeometryWireframe,
)
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read quadratic tetra mesh
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "quadraticTetra01.vtu"))

# Extract surface with pass-through cell IDs
ds_surface = vtkDataSetSurfaceFilter()
ds_surface.SetInputConnection(reader.GetOutputPort())
ds_surface.PassThroughCellIdsOn()
ds_surface.SetOriginalCellIdsName("MyOriginalCellIds")
ds_surface.SetNonlinearSubdivisionLevel(2)
ds_surface.Update()

# Recover wireframe from original cell IDs
recover = vtkRecoverGeometryWireframe()
recover.SetInputData(ds_surface.GetOutput())
recover.SetCellIdsAttribute("MyOriginalCellIds")
recover.Update()

# Mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(recover.GetOutput())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().SetEdgeVisibility(True)
actor.GetProperty().SetEdgeColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.ResetCamera()

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("recover wireframe")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
