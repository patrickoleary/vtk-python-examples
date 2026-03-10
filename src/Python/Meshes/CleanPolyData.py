#!/usr/bin/env python

# Remove duplicate points and degenerate cells from a mesh using
# vtkCleanPolyData. The same sphere is appended to itself three times,
# tripling the point and cell count. The left viewport shows the
# uncleaned mesh with visible z-fighting from overlapping faces; the
# right viewport shows the cleaned mesh reduced back to a single copy.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCleanPolyData,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
alice_blue_rgb = (0.941, 0.973, 1.000)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Source: a single sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)

# Append: combine the same sphere three times (triples points and cells)
appender = vtkAppendPolyData()
appender.AddInputConnection(sphere.GetOutputPort())
appender.AddInputConnection(sphere.GetOutputPort())
appender.AddInputConnection(sphere.GetOutputPort())
appender.Update()

# Clean: merge duplicate points and remove degenerate cells
cleaner = vtkCleanPolyData()
cleaner.SetInputConnection(appender.GetOutputPort())
cleaner.SetTolerance(0.0)
cleaner.Update()

dirty_data = appender.GetOutput()
clean_data = cleaner.GetOutput()
print(f"Before: {dirty_data.GetNumberOfPoints()} points, "
      f"{dirty_data.GetNumberOfCells()} cells")
print(f"After:  {clean_data.GetNumberOfPoints()} points, "
      f"{clean_data.GetNumberOfCells()} cells")

# Mapper: uncleaned mesh (triplicated faces cause z-fighting)
dirty_mapper = vtkPolyDataMapper()
dirty_mapper.SetInputConnection(appender.GetOutputPort())
dirty_mapper.ScalarVisibilityOff()

dirty_actor = vtkActor()
dirty_actor.SetMapper(dirty_mapper)
dirty_actor.GetProperty().SetColor(alice_blue_rgb)
dirty_actor.GetProperty().EdgeVisibilityOn()
dirty_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Mapper: cleaned mesh (single copy, clean edges)
clean_mapper = vtkPolyDataMapper()
clean_mapper.SetInputConnection(cleaner.GetOutputPort())
clean_mapper.ScalarVisibilityOff()

clean_actor = vtkActor()
clean_actor.SetMapper(clean_mapper)
clean_actor.GetProperty().SetColor(alice_blue_rgb)
clean_actor.GetProperty().EdgeVisibilityOn()
clean_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Text: show point/cell counts in each viewport
dirty_text = vtkTextActor()
dirty_text.SetInput(f"Points: {dirty_data.GetNumberOfPoints()}\n"
                    f"Cells: {dirty_data.GetNumberOfCells()}")
dirty_text.GetTextProperty().SetFontSize(16)
dirty_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
dirty_text.SetPosition(10, 10)

clean_text = vtkTextActor()
clean_text.SetInput(f"Points: {clean_data.GetNumberOfPoints()}\n"
                    f"Cells: {clean_data.GetNumberOfCells()}")
clean_text.GetTextProperty().SetFontSize(16)
clean_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
clean_text.SetPosition(10, 10)

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, 0, 3)
camera.SetFocalPoint(0, 0, 0)

# Left renderer: uncleaned mesh with z-fighting
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(dirty_actor)
left_renderer.AddActor(dirty_text)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: cleaned mesh
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(clean_actor)
right_renderer.AddActor(clean_text)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CleanPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
