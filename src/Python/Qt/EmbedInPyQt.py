#!/usr/bin/env python

# Embed a VTK render window inside a PyQt6 application.

import sys

import vtkmodules.qt

vtkmodules.qt.QVTKRWIBase = "QOpenGLWidget"

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from PyQt6.QtCore import qInstallMessageHandler
from PyQt6.QtWidgets import QApplication, QMainWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
)


def qt_message_handler(mode, context, message):
    if "QPainter" not in message:
        print(message)


qInstallMessageHandler(qt_message_handler)

# Application: create the Qt application
app = QApplication(sys.argv)

# MainWindow: top-level window with embedded VTK widget
window = QMainWindow()
window.setWindowTitle("EmbedInPyQt")
vtk_widget = QVTKRenderWindowInteractor(window)
window.setCentralWidget(vtk_widget)

# Source: generate a sphere
source = vtkSphereSource()
source.SetRadius(0.5)
source.SetThetaResolution(32)
source.SetPhiResolution(32)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)
renderer.ResetCamera()

# RenderWindow: connect the VTK widget render window to the renderer
render_window = vtk_widget.GetRenderWindow()
render_window.AddRenderer(renderer)

window.resize(800, 600)
window.show()

vtk_widget.Initialize()
render_window.Render()

sys.exit(app.exec())