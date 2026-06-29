#!/usr/bin/env python

# Demonstrate vtkGeometryFilter on degenerated hexahedrons (tetrahedra
# stored as hexahedra with repeated point IDs), with red backfaces to
# detect missing external faces.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read degenerated hexahedron mesh
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "degenerated-hexahedrons.vtu"))

# Geometry filter
geom_filter = vtkGeometryFilter()
geom_filter.SetInputConnection(reader.GetOutputPort())

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geom_filter.GetOutputPort())

# Red backface property to detect missing external faces
backface_prop = vtkProperty()
backface_prop.SetColor(255, 0, 0)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetBackfaceProperty(backface_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("filter degenerated cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
cam = renderer.GetActiveCamera()
cam.Azimuth(-90)

interactor.Initialize()
interactor.Start()
