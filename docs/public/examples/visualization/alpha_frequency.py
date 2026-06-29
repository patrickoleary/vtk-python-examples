#!/usr/bin/env python

# Linearly extrude letter glyphs to visualize character frequency in a text file.

import os
import re
from collections import Counter
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
peacock = (0.200, 0.631, 0.788)
silver = (0.753, 0.753, 0.753)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "Gettysburg.txt"

# Read the file and calculate the frequency of each letter
with open(file_path) as f:
    freq = Counter()
    for line in f:
        cleaned = re.sub(r"[\d_]", "", line.strip().lower())
        freq += Counter(re.findall(r"\w", cleaned, re.UNICODE))
max_freq = max(freq.values())

# Letter A (freq=102)
text_a = vtkVectorText()
text_a.SetText("A")

extrude_a = vtkLinearExtrusionFilter()
extrude_a.SetInputConnection(text_a.GetOutputPort())
extrude_a.SetExtrusionTypeToVectorExtrusion()
extrude_a.SetVector(0, 0, 1.0)
extrude_a.SetScaleFactor(float(freq["a"]) / max_freq * 2.50)

mapper_a = vtkPolyDataMapper()
mapper_a.SetInputConnection(extrude_a.GetOutputPort())
mapper_a.ScalarVisibilityOff()

actor_a = vtkActor()
actor_a.SetMapper(mapper_a)
actor_a.GetProperty().SetColor(peacock)
actor_a.SetPosition(0.0, 0.0, 0.0)

# Letter B (freq=14)
text_b = vtkVectorText()
text_b.SetText("B")

extrude_b = vtkLinearExtrusionFilter()
extrude_b.SetInputConnection(text_b.GetOutputPort())
extrude_b.SetExtrusionTypeToVectorExtrusion()
extrude_b.SetVector(0, 0, 1.0)
extrude_b.SetScaleFactor(float(freq["b"]) / max_freq * 2.50)

mapper_b = vtkPolyDataMapper()
mapper_b.SetInputConnection(extrude_b.GetOutputPort())
mapper_b.ScalarVisibilityOff()

actor_b = vtkActor()
actor_b.SetMapper(mapper_b)
actor_b.GetProperty().SetColor(peacock)
actor_b.SetPosition(1.5, 0.0, 0.0)

# Letter C (freq=31)
text_c = vtkVectorText()
text_c.SetText("C")

extrude_c = vtkLinearExtrusionFilter()
extrude_c.SetInputConnection(text_c.GetOutputPort())
extrude_c.SetExtrusionTypeToVectorExtrusion()
extrude_c.SetVector(0, 0, 1.0)
extrude_c.SetScaleFactor(float(freq["c"]) / max_freq * 2.50)

mapper_c = vtkPolyDataMapper()
mapper_c.SetInputConnection(extrude_c.GetOutputPort())
mapper_c.ScalarVisibilityOff()

actor_c = vtkActor()
actor_c.SetMapper(mapper_c)
actor_c.GetProperty().SetColor(peacock)
actor_c.SetPosition(3.0, 0.0, 0.0)

# Letter D (freq=58)
text_d = vtkVectorText()
text_d.SetText("D")

extrude_d = vtkLinearExtrusionFilter()
extrude_d.SetInputConnection(text_d.GetOutputPort())
extrude_d.SetExtrusionTypeToVectorExtrusion()
extrude_d.SetVector(0, 0, 1.0)
extrude_d.SetScaleFactor(float(freq["d"]) / max_freq * 2.50)

mapper_d = vtkPolyDataMapper()
mapper_d.SetInputConnection(extrude_d.GetOutputPort())
mapper_d.ScalarVisibilityOff()

actor_d = vtkActor()
actor_d.SetMapper(mapper_d)
actor_d.GetProperty().SetColor(peacock)
actor_d.SetPosition(4.5, 0.0, 0.0)

# Letter E (freq=165)
text_e = vtkVectorText()
text_e.SetText("E")

extrude_e = vtkLinearExtrusionFilter()
extrude_e.SetInputConnection(text_e.GetOutputPort())
extrude_e.SetExtrusionTypeToVectorExtrusion()
extrude_e.SetVector(0, 0, 1.0)
extrude_e.SetScaleFactor(float(freq["e"]) / max_freq * 2.50)

mapper_e = vtkPolyDataMapper()
mapper_e.SetInputConnection(extrude_e.GetOutputPort())
mapper_e.ScalarVisibilityOff()

actor_e = vtkActor()
actor_e.SetMapper(mapper_e)
actor_e.GetProperty().SetColor(peacock)
actor_e.SetPosition(6.0, 0.0, 0.0)

# Letter F (freq=27)
text_f = vtkVectorText()
text_f.SetText("F")

extrude_f = vtkLinearExtrusionFilter()
extrude_f.SetInputConnection(text_f.GetOutputPort())
extrude_f.SetExtrusionTypeToVectorExtrusion()
extrude_f.SetVector(0, 0, 1.0)
extrude_f.SetScaleFactor(float(freq["f"]) / max_freq * 2.50)

mapper_f = vtkPolyDataMapper()
mapper_f.SetInputConnection(extrude_f.GetOutputPort())
mapper_f.ScalarVisibilityOff()

actor_f = vtkActor()
actor_f.SetMapper(mapper_f)
actor_f.GetProperty().SetColor(peacock)
actor_f.SetPosition(7.5, 0.0, 0.0)

# Letter G (freq=28)
text_g = vtkVectorText()
text_g.SetText("G")

extrude_g = vtkLinearExtrusionFilter()
extrude_g.SetInputConnection(text_g.GetOutputPort())
extrude_g.SetExtrusionTypeToVectorExtrusion()
extrude_g.SetVector(0, 0, 1.0)
extrude_g.SetScaleFactor(float(freq["g"]) / max_freq * 2.50)

mapper_g = vtkPolyDataMapper()
mapper_g.SetInputConnection(extrude_g.GetOutputPort())
mapper_g.ScalarVisibilityOff()

actor_g = vtkActor()
actor_g.SetMapper(mapper_g)
actor_g.GetProperty().SetColor(peacock)
actor_g.SetPosition(9.0, 0.0, 0.0)

# Letter H (freq=80)
text_h = vtkVectorText()
text_h.SetText("H")

extrude_h = vtkLinearExtrusionFilter()
extrude_h.SetInputConnection(text_h.GetOutputPort())
extrude_h.SetExtrusionTypeToVectorExtrusion()
extrude_h.SetVector(0, 0, 1.0)
extrude_h.SetScaleFactor(float(freq["h"]) / max_freq * 2.50)

mapper_h = vtkPolyDataMapper()
mapper_h.SetInputConnection(extrude_h.GetOutputPort())
mapper_h.ScalarVisibilityOff()

actor_h = vtkActor()
actor_h.SetMapper(mapper_h)
actor_h.GetProperty().SetColor(peacock)
actor_h.SetPosition(10.5, 0.0, 0.0)

# Letter I (freq=68)
text_i = vtkVectorText()
text_i.SetText("I")

extrude_i = vtkLinearExtrusionFilter()
extrude_i.SetInputConnection(text_i.GetOutputPort())
extrude_i.SetExtrusionTypeToVectorExtrusion()
extrude_i.SetVector(0, 0, 1.0)
extrude_i.SetScaleFactor(float(freq["i"]) / max_freq * 2.50)

mapper_i = vtkPolyDataMapper()
mapper_i.SetInputConnection(extrude_i.GetOutputPort())
mapper_i.ScalarVisibilityOff()

actor_i = vtkActor()
actor_i.SetMapper(mapper_i)
actor_i.GetProperty().SetColor(peacock)
actor_i.SetPosition(12.0, 0.0, 0.0)

# Letter J (freq=0)
text_j = vtkVectorText()
text_j.SetText("J")

extrude_j = vtkLinearExtrusionFilter()
extrude_j.SetInputConnection(text_j.GetOutputPort())
extrude_j.SetExtrusionTypeToVectorExtrusion()
extrude_j.SetVector(0, 0, 1.0)
extrude_j.SetScaleFactor(float(freq["j"]) / max_freq * 2.50)

mapper_j = vtkPolyDataMapper()
mapper_j.SetInputConnection(extrude_j.GetOutputPort())
mapper_j.ScalarVisibilityOff()

actor_j = vtkActor()
actor_j.SetMapper(mapper_j)
actor_j.GetProperty().SetColor(peacock)
actor_j.VisibilityOff()
actor_j.SetPosition(13.5, 0.0, 0.0)

# Letter K (freq=3)
text_k = vtkVectorText()
text_k.SetText("K")

extrude_k = vtkLinearExtrusionFilter()
extrude_k.SetInputConnection(text_k.GetOutputPort())
extrude_k.SetExtrusionTypeToVectorExtrusion()
extrude_k.SetVector(0, 0, 1.0)
extrude_k.SetScaleFactor(float(freq["k"]) / max_freq * 2.50)

mapper_k = vtkPolyDataMapper()
mapper_k.SetInputConnection(extrude_k.GetOutputPort())
mapper_k.ScalarVisibilityOff()

actor_k = vtkActor()
actor_k.SetMapper(mapper_k)
actor_k.GetProperty().SetColor(peacock)
actor_k.SetPosition(15.0, 0.0, 0.0)

# Letter L (freq=42)
text_l = vtkVectorText()
text_l.SetText("L")

extrude_l = vtkLinearExtrusionFilter()
extrude_l.SetInputConnection(text_l.GetOutputPort())
extrude_l.SetExtrusionTypeToVectorExtrusion()
extrude_l.SetVector(0, 0, 1.0)
extrude_l.SetScaleFactor(float(freq["l"]) / max_freq * 2.50)

mapper_l = vtkPolyDataMapper()
mapper_l.SetInputConnection(extrude_l.GetOutputPort())
mapper_l.ScalarVisibilityOff()

actor_l = vtkActor()
actor_l.SetMapper(mapper_l)
actor_l.GetProperty().SetColor(peacock)
actor_l.SetPosition(16.5, 0.0, 0.0)

# Letter M (freq=13)
text_m = vtkVectorText()
text_m.SetText("M")

extrude_m = vtkLinearExtrusionFilter()
extrude_m.SetInputConnection(text_m.GetOutputPort())
extrude_m.SetExtrusionTypeToVectorExtrusion()
extrude_m.SetVector(0, 0, 1.0)
extrude_m.SetScaleFactor(float(freq["m"]) / max_freq * 2.50)

mapper_m = vtkPolyDataMapper()
mapper_m.SetInputConnection(extrude_m.GetOutputPort())
mapper_m.ScalarVisibilityOff()

actor_m = vtkActor()
actor_m.SetMapper(mapper_m)
actor_m.GetProperty().SetColor(peacock)
actor_m.SetPosition(18.0, 0.0, 0.0)

# Letter N (freq=77)
text_n = vtkVectorText()
text_n.SetText("N")

extrude_n = vtkLinearExtrusionFilter()
extrude_n.SetInputConnection(text_n.GetOutputPort())
extrude_n.SetExtrusionTypeToVectorExtrusion()
extrude_n.SetVector(0, 0, 1.0)
extrude_n.SetScaleFactor(float(freq["n"]) / max_freq * 2.50)

mapper_n = vtkPolyDataMapper()
mapper_n.SetInputConnection(extrude_n.GetOutputPort())
mapper_n.ScalarVisibilityOff()

actor_n = vtkActor()
actor_n.SetMapper(mapper_n)
actor_n.GetProperty().SetColor(peacock)
actor_n.SetPosition(0.0, -3.0, 0.0)

# Letter O (freq=93)
text_o = vtkVectorText()
text_o.SetText("O")

extrude_o = vtkLinearExtrusionFilter()
extrude_o.SetInputConnection(text_o.GetOutputPort())
extrude_o.SetExtrusionTypeToVectorExtrusion()
extrude_o.SetVector(0, 0, 1.0)
extrude_o.SetScaleFactor(float(freq["o"]) / max_freq * 2.50)

mapper_o = vtkPolyDataMapper()
mapper_o.SetInputConnection(extrude_o.GetOutputPort())
mapper_o.ScalarVisibilityOff()

actor_o = vtkActor()
actor_o.SetMapper(mapper_o)
actor_o.GetProperty().SetColor(peacock)
actor_o.SetPosition(1.5, -3.0, 0.0)

# Letter P (freq=15)
text_p = vtkVectorText()
text_p.SetText("P")

extrude_p = vtkLinearExtrusionFilter()
extrude_p.SetInputConnection(text_p.GetOutputPort())
extrude_p.SetExtrusionTypeToVectorExtrusion()
extrude_p.SetVector(0, 0, 1.0)
extrude_p.SetScaleFactor(float(freq["p"]) / max_freq * 2.50)

mapper_p = vtkPolyDataMapper()
mapper_p.SetInputConnection(extrude_p.GetOutputPort())
mapper_p.ScalarVisibilityOff()

actor_p = vtkActor()
actor_p.SetMapper(mapper_p)
actor_p.GetProperty().SetColor(peacock)
actor_p.SetPosition(3.0, -3.0, 0.0)

# Letter Q (freq=1)
text_q = vtkVectorText()
text_q.SetText("Q")

extrude_q = vtkLinearExtrusionFilter()
extrude_q.SetInputConnection(text_q.GetOutputPort())
extrude_q.SetExtrusionTypeToVectorExtrusion()
extrude_q.SetVector(0, 0, 1.0)
extrude_q.SetScaleFactor(float(freq["q"]) / max_freq * 2.50)

mapper_q = vtkPolyDataMapper()
mapper_q.SetInputConnection(extrude_q.GetOutputPort())
mapper_q.ScalarVisibilityOff()

actor_q = vtkActor()
actor_q.SetMapper(mapper_q)
actor_q.GetProperty().SetColor(peacock)
actor_q.SetPosition(4.5, -3.0, 0.0)

# Letter R (freq=79)
text_r = vtkVectorText()
text_r.SetText("R")

extrude_r = vtkLinearExtrusionFilter()
extrude_r.SetInputConnection(text_r.GetOutputPort())
extrude_r.SetExtrusionTypeToVectorExtrusion()
extrude_r.SetVector(0, 0, 1.0)
extrude_r.SetScaleFactor(float(freq["r"]) / max_freq * 2.50)

mapper_r = vtkPolyDataMapper()
mapper_r.SetInputConnection(extrude_r.GetOutputPort())
mapper_r.ScalarVisibilityOff()

actor_r = vtkActor()
actor_r.SetMapper(mapper_r)
actor_r.GetProperty().SetColor(peacock)
actor_r.SetPosition(6.0, -3.0, 0.0)

# Letter S (freq=44)
text_s = vtkVectorText()
text_s.SetText("S")

extrude_s = vtkLinearExtrusionFilter()
extrude_s.SetInputConnection(text_s.GetOutputPort())
extrude_s.SetExtrusionTypeToVectorExtrusion()
extrude_s.SetVector(0, 0, 1.0)
extrude_s.SetScaleFactor(float(freq["s"]) / max_freq * 2.50)

mapper_s = vtkPolyDataMapper()
mapper_s.SetInputConnection(extrude_s.GetOutputPort())
mapper_s.ScalarVisibilityOff()

actor_s = vtkActor()
actor_s.SetMapper(mapper_s)
actor_s.GetProperty().SetColor(peacock)
actor_s.SetPosition(7.5, -3.0, 0.0)

# Letter T (freq=126)
text_t = vtkVectorText()
text_t.SetText("T")

extrude_t = vtkLinearExtrusionFilter()
extrude_t.SetInputConnection(text_t.GetOutputPort())
extrude_t.SetExtrusionTypeToVectorExtrusion()
extrude_t.SetVector(0, 0, 1.0)
extrude_t.SetScaleFactor(float(freq["t"]) / max_freq * 2.50)

mapper_t = vtkPolyDataMapper()
mapper_t.SetInputConnection(extrude_t.GetOutputPort())
mapper_t.ScalarVisibilityOff()

actor_t = vtkActor()
actor_t.SetMapper(mapper_t)
actor_t.GetProperty().SetColor(peacock)
actor_t.SetPosition(9.0, -3.0, 0.0)

# Letter U (freq=21)
text_u = vtkVectorText()
text_u.SetText("U")

extrude_u = vtkLinearExtrusionFilter()
extrude_u.SetInputConnection(text_u.GetOutputPort())
extrude_u.SetExtrusionTypeToVectorExtrusion()
extrude_u.SetVector(0, 0, 1.0)
extrude_u.SetScaleFactor(float(freq["u"]) / max_freq * 2.50)

mapper_u = vtkPolyDataMapper()
mapper_u.SetInputConnection(extrude_u.GetOutputPort())
mapper_u.ScalarVisibilityOff()

actor_u = vtkActor()
actor_u.SetMapper(mapper_u)
actor_u.GetProperty().SetColor(peacock)
actor_u.SetPosition(10.5, -3.0, 0.0)

# Letter V (freq=24)
text_v = vtkVectorText()
text_v.SetText("V")

extrude_v = vtkLinearExtrusionFilter()
extrude_v.SetInputConnection(text_v.GetOutputPort())
extrude_v.SetExtrusionTypeToVectorExtrusion()
extrude_v.SetVector(0, 0, 1.0)
extrude_v.SetScaleFactor(float(freq["v"]) / max_freq * 2.50)

mapper_v = vtkPolyDataMapper()
mapper_v.SetInputConnection(extrude_v.GetOutputPort())
mapper_v.ScalarVisibilityOff()

actor_v = vtkActor()
actor_v.SetMapper(mapper_v)
actor_v.GetProperty().SetColor(peacock)
actor_v.SetPosition(12.0, -3.0, 0.0)

# Letter W (freq=28)
text_w = vtkVectorText()
text_w.SetText("W")

extrude_w = vtkLinearExtrusionFilter()
extrude_w.SetInputConnection(text_w.GetOutputPort())
extrude_w.SetExtrusionTypeToVectorExtrusion()
extrude_w.SetVector(0, 0, 1.0)
extrude_w.SetScaleFactor(float(freq["w"]) / max_freq * 2.50)

mapper_w = vtkPolyDataMapper()
mapper_w.SetInputConnection(extrude_w.GetOutputPort())
mapper_w.ScalarVisibilityOff()

actor_w = vtkActor()
actor_w.SetMapper(mapper_w)
actor_w.GetProperty().SetColor(peacock)
actor_w.SetPosition(13.5, -3.0, 0.0)

# Letter X (freq=0)
text_x = vtkVectorText()
text_x.SetText("X")

extrude_x = vtkLinearExtrusionFilter()
extrude_x.SetInputConnection(text_x.GetOutputPort())
extrude_x.SetExtrusionTypeToVectorExtrusion()
extrude_x.SetVector(0, 0, 1.0)
extrude_x.SetScaleFactor(float(freq["x"]) / max_freq * 2.50)

mapper_x = vtkPolyDataMapper()
mapper_x.SetInputConnection(extrude_x.GetOutputPort())
mapper_x.ScalarVisibilityOff()

actor_x = vtkActor()
actor_x.SetMapper(mapper_x)
actor_x.GetProperty().SetColor(peacock)
actor_x.VisibilityOff()
actor_x.SetPosition(15.0, -3.0, 0.0)

# Letter Y (freq=10)
text_y = vtkVectorText()
text_y.SetText("Y")

extrude_y = vtkLinearExtrusionFilter()
extrude_y.SetInputConnection(text_y.GetOutputPort())
extrude_y.SetExtrusionTypeToVectorExtrusion()
extrude_y.SetVector(0, 0, 1.0)
extrude_y.SetScaleFactor(float(freq["y"]) / max_freq * 2.50)

mapper_y = vtkPolyDataMapper()
mapper_y.SetInputConnection(extrude_y.GetOutputPort())
mapper_y.ScalarVisibilityOff()

actor_y = vtkActor()
actor_y.SetMapper(mapper_y)
actor_y.GetProperty().SetColor(peacock)
actor_y.SetPosition(16.5, -3.0, 0.0)

# Letter Z (freq=0)
text_z = vtkVectorText()
text_z.SetText("Z")

extrude_z = vtkLinearExtrusionFilter()
extrude_z.SetInputConnection(text_z.GetOutputPort())
extrude_z.SetExtrusionTypeToVectorExtrusion()
extrude_z.SetVector(0, 0, 1.0)
extrude_z.SetScaleFactor(float(freq["z"]) / max_freq * 2.50)

mapper_z = vtkPolyDataMapper()
mapper_z.SetInputConnection(extrude_z.GetOutputPort())
mapper_z.ScalarVisibilityOff()

actor_z = vtkActor()
actor_z.SetMapper(mapper_z)
actor_z.GetProperty().SetColor(peacock)
actor_z.VisibilityOff()
actor_z.SetPosition(18.0, -3.0, 0.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor_a)
renderer.AddActor(actor_b)
renderer.AddActor(actor_c)
renderer.AddActor(actor_d)
renderer.AddActor(actor_e)
renderer.AddActor(actor_f)
renderer.AddActor(actor_g)
renderer.AddActor(actor_h)
renderer.AddActor(actor_i)
renderer.AddActor(actor_j)
renderer.AddActor(actor_k)
renderer.AddActor(actor_l)
renderer.AddActor(actor_m)
renderer.AddActor(actor_n)
renderer.AddActor(actor_o)
renderer.AddActor(actor_p)
renderer.AddActor(actor_q)
renderer.AddActor(actor_r)
renderer.AddActor(actor_s)
renderer.AddActor(actor_t)
renderer.AddActor(actor_u)
renderer.AddActor(actor_v)
renderer.AddActor(actor_w)
renderer.AddActor(actor_x)
renderer.AddActor(actor_y)
renderer.AddActor(actor_z)
renderer.SetBackground(silver)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30.0)
renderer.GetActiveCamera().Azimuth(-30.0)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("alpha frequency")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
