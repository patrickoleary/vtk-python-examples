#!/usr/bin/env python

# Demonstrate vtkEarthSource and vtkTexturedSphereSource with an earth
# texture map overlay.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersHybrid import vtkEarthSource
from vtkmodules.vtkFiltersSources import vtkTexturedSphereSource
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Textured sphere for earth surface
tss = vtkTexturedSphereSource()
tss.SetThetaResolution(18)
tss.SetPhiResolution(9)

earth_mapper = vtkPolyDataMapper()
earth_mapper.SetInputConnection(tss.GetOutputPort())

earth_actor = vtkActor()
earth_actor.SetMapper(earth_mapper)

# Load texture map
texture = vtkTexture()
pnm_reader = vtkPNMReader()
pnm_reader.SetFileName(os.path.join(data_dir, "earth.ppm"))
texture.SetInputConnection(pnm_reader.GetOutputPort())
texture.InterpolateOn()
earth_actor.SetTexture(texture)

# Earth source for coastline outlines
es = vtkEarthSource()
es.SetRadius(0.501)
es.SetOnRatio(2)

earth2_mapper = vtkPolyDataMapper()
earth2_mapper.SetInputConnection(es.GetOutputPort())

earth2_actor = vtkActor()
earth2_actor.SetMapper(earth2_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(earth_actor)
renderer.AddActor(earth2_actor)
renderer.SetBackground(0, 0, 0.1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("earth")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

interactor.Initialize()
interactor.Start()
