#!/usr/bin/env python

# Display all 21 parametric surfaces arranged in a 5 × 5 grid of viewports,
# each with its own renderer.  Each surface is normalized, centered, and
# labelled with a 2D text title pinned to the bottom of the viewport.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import (
    vtkParametricBohemianDome,
    vtkParametricBour,
    vtkParametricBoy,
    vtkParametricCatalanMinimal,
    vtkParametricConicSpiral,
    vtkParametricCrossCap,
    vtkParametricDini,
    vtkParametricEllipsoid,
    vtkParametricEnneper,
    vtkParametricFigure8Klein,
    vtkParametricHenneberg,
    vtkParametricKlein,
    vtkParametricKuen,
    vtkParametricMobius,
    vtkParametricPluckerConoid,
    vtkParametricPseudosphere,
    vtkParametricRandomHills,
    vtkParametricRoman,
    vtkParametricSpline,
    vtkParametricSuperEllipsoid,
    vtkParametricSuperToroid,
    vtkParametricTorus,
)
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
navajo_white_rgb = (1.0, 0.871, 0.678)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# ---------------------------------------------------------------------------
# Build parametric function instances (alphabetical order).
# Some require custom parameter settings.
# ---------------------------------------------------------------------------
bohemian_dome = vtkParametricBohemianDome()
bohemian_dome.SetA(5.0)
bohemian_dome.SetB(1.0)
bohemian_dome.SetC(2.0)

ellipsoid = vtkParametricEllipsoid()
ellipsoid.SetXRadius(0.5)
ellipsoid.SetYRadius(2.0)

kuen = vtkParametricKuen()
kuen.SetDeltaV0(0.001)

mobius = vtkParametricMobius()
mobius.SetRadius(2.0)
mobius.SetMinimumV(-0.5)
mobius.SetMaximumV(0.5)

random_hills = vtkParametricRandomHills()
random_hills.AllowRandomGenerationOn()
random_hills.SetRandomSeed(1)
random_hills.SetNumberOfHills(30)

spline = vtkParametricSpline()
spline_points = vtkPoints()
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
for _ in range(10):
    xyz = [0.0] * 3
    for j in range(3):
        xyz[j] = rng.GetRangeValue(-1.0, 1.0)
        rng.Next()
    spline_points.InsertNextPoint(xyz)
spline.SetPoints(spline_points)

super_ellipsoid = vtkParametricSuperEllipsoid()
super_ellipsoid.SetN1(0.5)
super_ellipsoid.SetN2(0.4)

super_toroid = vtkParametricSuperToroid()
super_toroid.SetN1(0.5)
super_toroid.SetN2(3.0)

# ---------------------------------------------------------------------------
# Viewport grid: 5 columns × 5 rows (25 cells, 22 filled)
# ---------------------------------------------------------------------------
num_cols = 5
num_rows = 5

# ---------------------------------------------------------------------------
# Sources: sample each parametric function to produce polygonal output
# ---------------------------------------------------------------------------
bohemian_dome_source = vtkParametricFunctionSource()
bohemian_dome_source.SetParametricFunction(bohemian_dome)
bohemian_dome_source.SetUResolution(51)
bohemian_dome_source.SetVResolution(51)
bohemian_dome_source.SetWResolution(51)
bohemian_dome_source.Update()

bour_fn = vtkParametricBour()
bour_source = vtkParametricFunctionSource()
bour_source.SetParametricFunction(bour_fn)
bour_source.SetUResolution(51)
bour_source.SetVResolution(51)
bour_source.SetWResolution(51)
bour_source.Update()

boy_fn = vtkParametricBoy()
boy_source = vtkParametricFunctionSource()
boy_source.SetParametricFunction(boy_fn)
boy_source.SetUResolution(51)
boy_source.SetVResolution(51)
boy_source.SetWResolution(51)
boy_source.Update()

catalan_fn = vtkParametricCatalanMinimal()
catalan_source = vtkParametricFunctionSource()
catalan_source.SetParametricFunction(catalan_fn)
catalan_source.SetUResolution(51)
catalan_source.SetVResolution(51)
catalan_source.SetWResolution(51)
catalan_source.Update()

conic_fn = vtkParametricConicSpiral()
conic_source = vtkParametricFunctionSource()
conic_source.SetParametricFunction(conic_fn)
conic_source.SetUResolution(51)
conic_source.SetVResolution(51)
conic_source.SetWResolution(51)
conic_source.Update()

crosscap_fn = vtkParametricCrossCap()
crosscap_source = vtkParametricFunctionSource()
crosscap_source.SetParametricFunction(crosscap_fn)
crosscap_source.SetUResolution(51)
crosscap_source.SetVResolution(51)
crosscap_source.SetWResolution(51)
crosscap_source.Update()

dini_fn = vtkParametricDini()
dini_source = vtkParametricFunctionSource()
dini_source.SetParametricFunction(dini_fn)
dini_source.SetUResolution(51)
dini_source.SetVResolution(51)
dini_source.SetWResolution(51)
dini_source.Update()

ellipsoid_source = vtkParametricFunctionSource()
ellipsoid_source.SetParametricFunction(ellipsoid)
ellipsoid_source.SetUResolution(51)
ellipsoid_source.SetVResolution(51)
ellipsoid_source.SetWResolution(51)
ellipsoid_source.Update()

enneper_fn = vtkParametricEnneper()
enneper_source = vtkParametricFunctionSource()
enneper_source.SetParametricFunction(enneper_fn)
enneper_source.SetUResolution(51)
enneper_source.SetVResolution(51)
enneper_source.SetWResolution(51)
enneper_source.Update()

figure8_fn = vtkParametricFigure8Klein()
figure8_source = vtkParametricFunctionSource()
figure8_source.SetParametricFunction(figure8_fn)
figure8_source.SetUResolution(51)
figure8_source.SetVResolution(51)
figure8_source.SetWResolution(51)
figure8_source.Update()

henneberg_fn = vtkParametricHenneberg()
henneberg_source = vtkParametricFunctionSource()
henneberg_source.SetParametricFunction(henneberg_fn)
henneberg_source.SetUResolution(51)
henneberg_source.SetVResolution(51)
henneberg_source.SetWResolution(51)
henneberg_source.Update()

klein_fn = vtkParametricKlein()
klein_source = vtkParametricFunctionSource()
klein_source.SetParametricFunction(klein_fn)
klein_source.SetUResolution(51)
klein_source.SetVResolution(51)
klein_source.SetWResolution(51)
klein_source.Update()

kuen_source = vtkParametricFunctionSource()
kuen_source.SetParametricFunction(kuen)
kuen_source.SetUResolution(51)
kuen_source.SetVResolution(51)
kuen_source.SetWResolution(51)
kuen_source.Update()

mobius_source = vtkParametricFunctionSource()
mobius_source.SetParametricFunction(mobius)
mobius_source.SetUResolution(51)
mobius_source.SetVResolution(51)
mobius_source.SetWResolution(51)
mobius_source.Update()

plucker_fn = vtkParametricPluckerConoid()
plucker_source = vtkParametricFunctionSource()
plucker_source.SetParametricFunction(plucker_fn)
plucker_source.SetUResolution(51)
plucker_source.SetVResolution(51)
plucker_source.SetWResolution(51)
plucker_source.Update()

pseudo_fn = vtkParametricPseudosphere()
pseudo_source = vtkParametricFunctionSource()
pseudo_source.SetParametricFunction(pseudo_fn)
pseudo_source.SetUResolution(51)
pseudo_source.SetVResolution(51)
pseudo_source.SetWResolution(51)
pseudo_source.Update()

random_hills_source = vtkParametricFunctionSource()
random_hills_source.SetParametricFunction(random_hills)
random_hills_source.SetUResolution(51)
random_hills_source.SetVResolution(51)
random_hills_source.SetWResolution(51)
random_hills_source.Update()

roman_fn = vtkParametricRoman()
roman_source = vtkParametricFunctionSource()
roman_source.SetParametricFunction(roman_fn)
roman_source.SetUResolution(51)
roman_source.SetVResolution(51)
roman_source.SetWResolution(51)
roman_source.Update()

spline_source = vtkParametricFunctionSource()
spline_source.SetParametricFunction(spline)
spline_source.SetUResolution(51)
spline_source.SetVResolution(51)
spline_source.SetWResolution(51)
spline_source.Update()

super_ellipsoid_source = vtkParametricFunctionSource()
super_ellipsoid_source.SetParametricFunction(super_ellipsoid)
super_ellipsoid_source.SetUResolution(51)
super_ellipsoid_source.SetVResolution(51)
super_ellipsoid_source.SetWResolution(51)
super_ellipsoid_source.Update()

super_toroid_source = vtkParametricFunctionSource()
super_toroid_source.SetParametricFunction(super_toroid)
super_toroid_source.SetUResolution(51)
super_toroid_source.SetVResolution(51)
super_toroid_source.SetWResolution(51)
super_toroid_source.Update()

torus_fn = vtkParametricTorus()
torus_source = vtkParametricFunctionSource()
torus_source.SetParametricFunction(torus_fn)
torus_source.SetUResolution(51)
torus_source.SetVResolution(51)
torus_source.SetWResolution(51)
torus_source.Update()

# ---------------------------------------------------------------------------
# Normalize: scale and center each surface to fit its viewport cell
# ---------------------------------------------------------------------------
bohemian_dome_bounds = bohemian_dome_source.GetOutput().GetBounds()
bohemian_dome_max_dim = max(bohemian_dome_bounds[1] - bohemian_dome_bounds[0],
                            bohemian_dome_bounds[3] - bohemian_dome_bounds[2],
                            bohemian_dome_bounds[5] - bohemian_dome_bounds[4])
bohemian_dome_scale = 3.0 / bohemian_dome_max_dim if bohemian_dome_max_dim > 0 else 1.0
bohemian_dome_cx = (bohemian_dome_bounds[0] + bohemian_dome_bounds[1]) / 2.0
bohemian_dome_cy = (bohemian_dome_bounds[2] + bohemian_dome_bounds[3]) / 2.0
bohemian_dome_cz = (bohemian_dome_bounds[4] + bohemian_dome_bounds[5]) / 2.0

bour_bounds = bour_source.GetOutput().GetBounds()
bour_max_dim = max(bour_bounds[1] - bour_bounds[0], bour_bounds[3] - bour_bounds[2], bour_bounds[5] - bour_bounds[4])
bour_scale = 3.0 / bour_max_dim if bour_max_dim > 0 else 1.0
bour_cx = (bour_bounds[0] + bour_bounds[1]) / 2.0
bour_cy = (bour_bounds[2] + bour_bounds[3]) / 2.0
bour_cz = (bour_bounds[4] + bour_bounds[5]) / 2.0

boy_bounds = boy_source.GetOutput().GetBounds()
boy_max_dim = max(boy_bounds[1] - boy_bounds[0], boy_bounds[3] - boy_bounds[2], boy_bounds[5] - boy_bounds[4])
boy_scale = 3.0 / boy_max_dim if boy_max_dim > 0 else 1.0
boy_cx = (boy_bounds[0] + boy_bounds[1]) / 2.0
boy_cy = (boy_bounds[2] + boy_bounds[3]) / 2.0
boy_cz = (boy_bounds[4] + boy_bounds[5]) / 2.0

catalan_bounds = catalan_source.GetOutput().GetBounds()
catalan_max_dim = max(catalan_bounds[1] - catalan_bounds[0], catalan_bounds[3] - catalan_bounds[2], catalan_bounds[5] - catalan_bounds[4])
catalan_scale = 3.0 / catalan_max_dim if catalan_max_dim > 0 else 1.0
catalan_cx = (catalan_bounds[0] + catalan_bounds[1]) / 2.0
catalan_cy = (catalan_bounds[2] + catalan_bounds[3]) / 2.0
catalan_cz = (catalan_bounds[4] + catalan_bounds[5]) / 2.0

conic_bounds = conic_source.GetOutput().GetBounds()
conic_max_dim = max(conic_bounds[1] - conic_bounds[0], conic_bounds[3] - conic_bounds[2], conic_bounds[5] - conic_bounds[4])
conic_scale = 3.0 / conic_max_dim if conic_max_dim > 0 else 1.0
conic_cx = (conic_bounds[0] + conic_bounds[1]) / 2.0
conic_cy = (conic_bounds[2] + conic_bounds[3]) / 2.0
conic_cz = (conic_bounds[4] + conic_bounds[5]) / 2.0

crosscap_bounds = crosscap_source.GetOutput().GetBounds()
crosscap_max_dim = max(crosscap_bounds[1] - crosscap_bounds[0], crosscap_bounds[3] - crosscap_bounds[2], crosscap_bounds[5] - crosscap_bounds[4])
crosscap_scale = 3.0 / crosscap_max_dim if crosscap_max_dim > 0 else 1.0
crosscap_cx = (crosscap_bounds[0] + crosscap_bounds[1]) / 2.0
crosscap_cy = (crosscap_bounds[2] + crosscap_bounds[3]) / 2.0
crosscap_cz = (crosscap_bounds[4] + crosscap_bounds[5]) / 2.0

dini_bounds = dini_source.GetOutput().GetBounds()
dini_max_dim = max(dini_bounds[1] - dini_bounds[0], dini_bounds[3] - dini_bounds[2], dini_bounds[5] - dini_bounds[4])
dini_scale = 3.0 / dini_max_dim if dini_max_dim > 0 else 1.0
dini_cx = (dini_bounds[0] + dini_bounds[1]) / 2.0
dini_cy = (dini_bounds[2] + dini_bounds[3]) / 2.0
dini_cz = (dini_bounds[4] + dini_bounds[5]) / 2.0

ellipsoid_bounds = ellipsoid_source.GetOutput().GetBounds()
ellipsoid_max_dim = max(ellipsoid_bounds[1] - ellipsoid_bounds[0], ellipsoid_bounds[3] - ellipsoid_bounds[2], ellipsoid_bounds[5] - ellipsoid_bounds[4])
ellipsoid_scale = 3.0 / ellipsoid_max_dim if ellipsoid_max_dim > 0 else 1.0
ellipsoid_cx = (ellipsoid_bounds[0] + ellipsoid_bounds[1]) / 2.0
ellipsoid_cy = (ellipsoid_bounds[2] + ellipsoid_bounds[3]) / 2.0
ellipsoid_cz = (ellipsoid_bounds[4] + ellipsoid_bounds[5]) / 2.0

enneper_bounds = enneper_source.GetOutput().GetBounds()
enneper_max_dim = max(enneper_bounds[1] - enneper_bounds[0], enneper_bounds[3] - enneper_bounds[2], enneper_bounds[5] - enneper_bounds[4])
enneper_scale = 3.0 / enneper_max_dim if enneper_max_dim > 0 else 1.0
enneper_cx = (enneper_bounds[0] + enneper_bounds[1]) / 2.0
enneper_cy = (enneper_bounds[2] + enneper_bounds[3]) / 2.0
enneper_cz = (enneper_bounds[4] + enneper_bounds[5]) / 2.0

figure8_bounds = figure8_source.GetOutput().GetBounds()
figure8_max_dim = max(figure8_bounds[1] - figure8_bounds[0], figure8_bounds[3] - figure8_bounds[2], figure8_bounds[5] - figure8_bounds[4])
figure8_scale = 3.0 / figure8_max_dim if figure8_max_dim > 0 else 1.0
figure8_cx = (figure8_bounds[0] + figure8_bounds[1]) / 2.0
figure8_cy = (figure8_bounds[2] + figure8_bounds[3]) / 2.0
figure8_cz = (figure8_bounds[4] + figure8_bounds[5]) / 2.0

henneberg_bounds = henneberg_source.GetOutput().GetBounds()
henneberg_max_dim = max(henneberg_bounds[1] - henneberg_bounds[0], henneberg_bounds[3] - henneberg_bounds[2], henneberg_bounds[5] - henneberg_bounds[4])
henneberg_scale = 3.0 / henneberg_max_dim if henneberg_max_dim > 0 else 1.0
henneberg_cx = (henneberg_bounds[0] + henneberg_bounds[1]) / 2.0
henneberg_cy = (henneberg_bounds[2] + henneberg_bounds[3]) / 2.0
henneberg_cz = (henneberg_bounds[4] + henneberg_bounds[5]) / 2.0

klein_bounds = klein_source.GetOutput().GetBounds()
klein_max_dim = max(klein_bounds[1] - klein_bounds[0], klein_bounds[3] - klein_bounds[2], klein_bounds[5] - klein_bounds[4])
klein_scale = 3.0 / klein_max_dim if klein_max_dim > 0 else 1.0
klein_cx = (klein_bounds[0] + klein_bounds[1]) / 2.0
klein_cy = (klein_bounds[2] + klein_bounds[3]) / 2.0
klein_cz = (klein_bounds[4] + klein_bounds[5]) / 2.0

kuen_bounds = kuen_source.GetOutput().GetBounds()
kuen_max_dim = max(kuen_bounds[1] - kuen_bounds[0], kuen_bounds[3] - kuen_bounds[2], kuen_bounds[5] - kuen_bounds[4])
kuen_scale = 3.0 / kuen_max_dim if kuen_max_dim > 0 else 1.0
kuen_cx = (kuen_bounds[0] + kuen_bounds[1]) / 2.0
kuen_cy = (kuen_bounds[2] + kuen_bounds[3]) / 2.0
kuen_cz = (kuen_bounds[4] + kuen_bounds[5]) / 2.0

mobius_bounds = mobius_source.GetOutput().GetBounds()
mobius_max_dim = max(mobius_bounds[1] - mobius_bounds[0], mobius_bounds[3] - mobius_bounds[2], mobius_bounds[5] - mobius_bounds[4])
mobius_scale = 3.0 / mobius_max_dim if mobius_max_dim > 0 else 1.0
mobius_cx = (mobius_bounds[0] + mobius_bounds[1]) / 2.0
mobius_cy = (mobius_bounds[2] + mobius_bounds[3]) / 2.0
mobius_cz = (mobius_bounds[4] + mobius_bounds[5]) / 2.0

plucker_bounds = plucker_source.GetOutput().GetBounds()
plucker_max_dim = max(plucker_bounds[1] - plucker_bounds[0], plucker_bounds[3] - plucker_bounds[2], plucker_bounds[5] - plucker_bounds[4])
plucker_scale = 3.0 / plucker_max_dim if plucker_max_dim > 0 else 1.0
plucker_cx = (plucker_bounds[0] + plucker_bounds[1]) / 2.0
plucker_cy = (plucker_bounds[2] + plucker_bounds[3]) / 2.0
plucker_cz = (plucker_bounds[4] + plucker_bounds[5]) / 2.0

pseudo_bounds = pseudo_source.GetOutput().GetBounds()
pseudo_max_dim = max(pseudo_bounds[1] - pseudo_bounds[0], pseudo_bounds[3] - pseudo_bounds[2], pseudo_bounds[5] - pseudo_bounds[4])
pseudo_scale = 3.0 / pseudo_max_dim if pseudo_max_dim > 0 else 1.0
pseudo_cx = (pseudo_bounds[0] + pseudo_bounds[1]) / 2.0
pseudo_cy = (pseudo_bounds[2] + pseudo_bounds[3]) / 2.0
pseudo_cz = (pseudo_bounds[4] + pseudo_bounds[5]) / 2.0

random_hills_bounds = random_hills_source.GetOutput().GetBounds()
random_hills_max_dim = max(random_hills_bounds[1] - random_hills_bounds[0], random_hills_bounds[3] - random_hills_bounds[2], random_hills_bounds[5] - random_hills_bounds[4])
random_hills_scale = 3.0 / random_hills_max_dim if random_hills_max_dim > 0 else 1.0
random_hills_cx = (random_hills_bounds[0] + random_hills_bounds[1]) / 2.0
random_hills_cy = (random_hills_bounds[2] + random_hills_bounds[3]) / 2.0
random_hills_cz = (random_hills_bounds[4] + random_hills_bounds[5]) / 2.0

roman_bounds = roman_source.GetOutput().GetBounds()
roman_max_dim = max(roman_bounds[1] - roman_bounds[0], roman_bounds[3] - roman_bounds[2], roman_bounds[5] - roman_bounds[4])
roman_scale = 3.0 / roman_max_dim if roman_max_dim > 0 else 1.0
roman_cx = (roman_bounds[0] + roman_bounds[1]) / 2.0
roman_cy = (roman_bounds[2] + roman_bounds[3]) / 2.0
roman_cz = (roman_bounds[4] + roman_bounds[5]) / 2.0

spline_bounds = spline_source.GetOutput().GetBounds()
spline_max_dim = max(spline_bounds[1] - spline_bounds[0], spline_bounds[3] - spline_bounds[2], spline_bounds[5] - spline_bounds[4])
spline_scale = 3.0 / spline_max_dim if spline_max_dim > 0 else 1.0
spline_cx = (spline_bounds[0] + spline_bounds[1]) / 2.0
spline_cy = (spline_bounds[2] + spline_bounds[3]) / 2.0
spline_cz = (spline_bounds[4] + spline_bounds[5]) / 2.0

super_ellipsoid_bounds = super_ellipsoid_source.GetOutput().GetBounds()
super_ellipsoid_max_dim = max(super_ellipsoid_bounds[1] - super_ellipsoid_bounds[0], super_ellipsoid_bounds[3] - super_ellipsoid_bounds[2], super_ellipsoid_bounds[5] - super_ellipsoid_bounds[4])
super_ellipsoid_scale = 3.0 / super_ellipsoid_max_dim if super_ellipsoid_max_dim > 0 else 1.0
super_ellipsoid_cx = (super_ellipsoid_bounds[0] + super_ellipsoid_bounds[1]) / 2.0
super_ellipsoid_cy = (super_ellipsoid_bounds[2] + super_ellipsoid_bounds[3]) / 2.0
super_ellipsoid_cz = (super_ellipsoid_bounds[4] + super_ellipsoid_bounds[5]) / 2.0

super_toroid_bounds = super_toroid_source.GetOutput().GetBounds()
super_toroid_max_dim = max(super_toroid_bounds[1] - super_toroid_bounds[0], super_toroid_bounds[3] - super_toroid_bounds[2], super_toroid_bounds[5] - super_toroid_bounds[4])
super_toroid_scale = 3.0 / super_toroid_max_dim if super_toroid_max_dim > 0 else 1.0
super_toroid_cx = (super_toroid_bounds[0] + super_toroid_bounds[1]) / 2.0
super_toroid_cy = (super_toroid_bounds[2] + super_toroid_bounds[3]) / 2.0
super_toroid_cz = (super_toroid_bounds[4] + super_toroid_bounds[5]) / 2.0

torus_bounds = torus_source.GetOutput().GetBounds()
torus_max_dim = max(torus_bounds[1] - torus_bounds[0], torus_bounds[3] - torus_bounds[2], torus_bounds[5] - torus_bounds[4])
torus_scale = 3.0 / torus_max_dim if torus_max_dim > 0 else 1.0
torus_cx = (torus_bounds[0] + torus_bounds[1]) / 2.0
torus_cy = (torus_bounds[2] + torus_bounds[3]) / 2.0
torus_cz = (torus_bounds[4] + torus_bounds[5]) / 2.0

# ---------------------------------------------------------------------------
# Mappers + Actors (paired together)
# ---------------------------------------------------------------------------
bohemian_dome_mapper = vtkPolyDataMapper()
bohemian_dome_mapper.SetInputConnection(bohemian_dome_source.GetOutputPort())
bohemian_dome_actor = vtkActor()
bohemian_dome_actor.SetMapper(bohemian_dome_mapper)
bohemian_dome_actor.GetProperty().SetColor(navajo_white_rgb)
bohemian_dome_actor.SetScale(bohemian_dome_scale, bohemian_dome_scale, bohemian_dome_scale)
bohemian_dome_actor.SetPosition(-bohemian_dome_cx * bohemian_dome_scale, -bohemian_dome_cy * bohemian_dome_scale, -bohemian_dome_cz * bohemian_dome_scale)

bour_mapper = vtkPolyDataMapper()
bour_mapper.SetInputConnection(bour_source.GetOutputPort())
bour_actor = vtkActor()
bour_actor.SetMapper(bour_mapper)
bour_actor.GetProperty().SetColor(navajo_white_rgb)
bour_actor.SetScale(bour_scale, bour_scale, bour_scale)
bour_actor.SetPosition(-bour_cx * bour_scale, -bour_cy * bour_scale, -bour_cz * bour_scale)

boy_mapper = vtkPolyDataMapper()
boy_mapper.SetInputConnection(boy_source.GetOutputPort())
boy_actor = vtkActor()
boy_actor.SetMapper(boy_mapper)
boy_actor.GetProperty().SetColor(navajo_white_rgb)
boy_actor.SetScale(boy_scale, boy_scale, boy_scale)
boy_actor.SetPosition(-boy_cx * boy_scale, -boy_cy * boy_scale, -boy_cz * boy_scale)

catalan_mapper = vtkPolyDataMapper()
catalan_mapper.SetInputConnection(catalan_source.GetOutputPort())
catalan_actor = vtkActor()
catalan_actor.SetMapper(catalan_mapper)
catalan_actor.GetProperty().SetColor(navajo_white_rgb)
catalan_actor.SetScale(catalan_scale, catalan_scale, catalan_scale)
catalan_actor.SetPosition(-catalan_cx * catalan_scale, -catalan_cy * catalan_scale, -catalan_cz * catalan_scale)

conic_mapper = vtkPolyDataMapper()
conic_mapper.SetInputConnection(conic_source.GetOutputPort())
conic_actor = vtkActor()
conic_actor.SetMapper(conic_mapper)
conic_actor.GetProperty().SetColor(navajo_white_rgb)
conic_actor.SetScale(conic_scale, conic_scale, conic_scale)
conic_actor.SetPosition(-conic_cx * conic_scale, -conic_cy * conic_scale, -conic_cz * conic_scale)

crosscap_mapper = vtkPolyDataMapper()
crosscap_mapper.SetInputConnection(crosscap_source.GetOutputPort())
crosscap_actor = vtkActor()
crosscap_actor.SetMapper(crosscap_mapper)
crosscap_actor.GetProperty().SetColor(navajo_white_rgb)
crosscap_actor.SetScale(crosscap_scale, crosscap_scale, crosscap_scale)
crosscap_actor.SetPosition(-crosscap_cx * crosscap_scale, -crosscap_cy * crosscap_scale, -crosscap_cz * crosscap_scale)

dini_mapper = vtkPolyDataMapper()
dini_mapper.SetInputConnection(dini_source.GetOutputPort())
dini_actor = vtkActor()
dini_actor.SetMapper(dini_mapper)
dini_actor.GetProperty().SetColor(navajo_white_rgb)
dini_actor.SetScale(dini_scale, dini_scale, dini_scale)
dini_actor.SetPosition(-dini_cx * dini_scale, -dini_cy * dini_scale, -dini_cz * dini_scale)

ellipsoid_mapper = vtkPolyDataMapper()
ellipsoid_mapper.SetInputConnection(ellipsoid_source.GetOutputPort())
ellipsoid_actor = vtkActor()
ellipsoid_actor.SetMapper(ellipsoid_mapper)
ellipsoid_actor.GetProperty().SetColor(navajo_white_rgb)
ellipsoid_actor.SetScale(ellipsoid_scale, ellipsoid_scale, ellipsoid_scale)
ellipsoid_actor.SetPosition(-ellipsoid_cx * ellipsoid_scale, -ellipsoid_cy * ellipsoid_scale, -ellipsoid_cz * ellipsoid_scale)

enneper_mapper = vtkPolyDataMapper()
enneper_mapper.SetInputConnection(enneper_source.GetOutputPort())
enneper_actor = vtkActor()
enneper_actor.SetMapper(enneper_mapper)
enneper_actor.GetProperty().SetColor(navajo_white_rgb)
enneper_actor.SetScale(enneper_scale, enneper_scale, enneper_scale)
enneper_actor.SetPosition(-enneper_cx * enneper_scale, -enneper_cy * enneper_scale, -enneper_cz * enneper_scale)

figure8_mapper = vtkPolyDataMapper()
figure8_mapper.SetInputConnection(figure8_source.GetOutputPort())
figure8_actor = vtkActor()
figure8_actor.SetMapper(figure8_mapper)
figure8_actor.GetProperty().SetColor(navajo_white_rgb)
figure8_actor.SetScale(figure8_scale, figure8_scale, figure8_scale)
figure8_actor.SetPosition(-figure8_cx * figure8_scale, -figure8_cy * figure8_scale, -figure8_cz * figure8_scale)

henneberg_mapper = vtkPolyDataMapper()
henneberg_mapper.SetInputConnection(henneberg_source.GetOutputPort())
henneberg_actor = vtkActor()
henneberg_actor.SetMapper(henneberg_mapper)
henneberg_actor.GetProperty().SetColor(navajo_white_rgb)
henneberg_actor.SetScale(henneberg_scale, henneberg_scale, henneberg_scale)
henneberg_actor.SetPosition(-henneberg_cx * henneberg_scale, -henneberg_cy * henneberg_scale, -henneberg_cz * henneberg_scale)

klein_mapper = vtkPolyDataMapper()
klein_mapper.SetInputConnection(klein_source.GetOutputPort())
klein_actor = vtkActor()
klein_actor.SetMapper(klein_mapper)
klein_actor.GetProperty().SetColor(navajo_white_rgb)
klein_actor.SetScale(klein_scale, klein_scale, klein_scale)
klein_actor.SetPosition(-klein_cx * klein_scale, -klein_cy * klein_scale, -klein_cz * klein_scale)

kuen_mapper = vtkPolyDataMapper()
kuen_mapper.SetInputConnection(kuen_source.GetOutputPort())
kuen_actor = vtkActor()
kuen_actor.SetMapper(kuen_mapper)
kuen_actor.GetProperty().SetColor(navajo_white_rgb)
kuen_actor.SetScale(kuen_scale, kuen_scale, kuen_scale)
kuen_actor.SetPosition(-kuen_cx * kuen_scale, -kuen_cy * kuen_scale, -kuen_cz * kuen_scale)

mobius_mapper = vtkPolyDataMapper()
mobius_mapper.SetInputConnection(mobius_source.GetOutputPort())
mobius_actor = vtkActor()
mobius_actor.SetMapper(mobius_mapper)
mobius_actor.GetProperty().SetColor(navajo_white_rgb)
mobius_actor.SetScale(mobius_scale, mobius_scale, mobius_scale)
mobius_actor.SetPosition(-mobius_cx * mobius_scale, -mobius_cy * mobius_scale, -mobius_cz * mobius_scale)

plucker_mapper = vtkPolyDataMapper()
plucker_mapper.SetInputConnection(plucker_source.GetOutputPort())
plucker_actor = vtkActor()
plucker_actor.SetMapper(plucker_mapper)
plucker_actor.GetProperty().SetColor(navajo_white_rgb)
plucker_actor.SetScale(plucker_scale, plucker_scale, plucker_scale)
plucker_actor.SetPosition(-plucker_cx * plucker_scale, -plucker_cy * plucker_scale, -plucker_cz * plucker_scale)

pseudo_mapper = vtkPolyDataMapper()
pseudo_mapper.SetInputConnection(pseudo_source.GetOutputPort())
pseudo_actor = vtkActor()
pseudo_actor.SetMapper(pseudo_mapper)
pseudo_actor.GetProperty().SetColor(navajo_white_rgb)
pseudo_actor.SetScale(pseudo_scale, pseudo_scale, pseudo_scale)
pseudo_actor.SetPosition(-pseudo_cx * pseudo_scale, -pseudo_cy * pseudo_scale, -pseudo_cz * pseudo_scale)

random_hills_mapper = vtkPolyDataMapper()
random_hills_mapper.SetInputConnection(random_hills_source.GetOutputPort())
random_hills_actor = vtkActor()
random_hills_actor.SetMapper(random_hills_mapper)
random_hills_actor.GetProperty().SetColor(navajo_white_rgb)
random_hills_actor.SetScale(random_hills_scale, random_hills_scale, random_hills_scale)
random_hills_actor.SetPosition(-random_hills_cx * random_hills_scale, -random_hills_cy * random_hills_scale, -random_hills_cz * random_hills_scale)

roman_mapper = vtkPolyDataMapper()
roman_mapper.SetInputConnection(roman_source.GetOutputPort())
roman_actor = vtkActor()
roman_actor.SetMapper(roman_mapper)
roman_actor.GetProperty().SetColor(navajo_white_rgb)
roman_actor.SetScale(roman_scale, roman_scale, roman_scale)
roman_actor.SetPosition(-roman_cx * roman_scale, -roman_cy * roman_scale, -roman_cz * roman_scale)

spline_mapper = vtkPolyDataMapper()
spline_mapper.SetInputConnection(spline_source.GetOutputPort())
spline_actor = vtkActor()
spline_actor.SetMapper(spline_mapper)
spline_actor.GetProperty().SetColor(navajo_white_rgb)
spline_actor.SetScale(spline_scale, spline_scale, spline_scale)
spline_actor.SetPosition(-spline_cx * spline_scale, -spline_cy * spline_scale, -spline_cz * spline_scale)

super_ellipsoid_mapper = vtkPolyDataMapper()
super_ellipsoid_mapper.SetInputConnection(super_ellipsoid_source.GetOutputPort())
super_ellipsoid_actor = vtkActor()
super_ellipsoid_actor.SetMapper(super_ellipsoid_mapper)
super_ellipsoid_actor.GetProperty().SetColor(navajo_white_rgb)
super_ellipsoid_actor.SetScale(super_ellipsoid_scale, super_ellipsoid_scale, super_ellipsoid_scale)
super_ellipsoid_actor.SetPosition(-super_ellipsoid_cx * super_ellipsoid_scale, -super_ellipsoid_cy * super_ellipsoid_scale, -super_ellipsoid_cz * super_ellipsoid_scale)

super_toroid_mapper = vtkPolyDataMapper()
super_toroid_mapper.SetInputConnection(super_toroid_source.GetOutputPort())
super_toroid_actor = vtkActor()
super_toroid_actor.SetMapper(super_toroid_mapper)
super_toroid_actor.GetProperty().SetColor(navajo_white_rgb)
super_toroid_actor.SetScale(super_toroid_scale, super_toroid_scale, super_toroid_scale)
super_toroid_actor.SetPosition(-super_toroid_cx * super_toroid_scale, -super_toroid_cy * super_toroid_scale, -super_toroid_cz * super_toroid_scale)

torus_mapper = vtkPolyDataMapper()
torus_mapper.SetInputConnection(torus_source.GetOutputPort())
torus_actor = vtkActor()
torus_actor.SetMapper(torus_mapper)
torus_actor.GetProperty().SetColor(navajo_white_rgb)
torus_actor.SetScale(torus_scale, torus_scale, torus_scale)
torus_actor.SetPosition(-torus_cx * torus_scale, -torus_cy * torus_scale, -torus_cz * torus_scale)

# ---------------------------------------------------------------------------
# Text actors: 2D labels pinned to bottom of each viewport
# ---------------------------------------------------------------------------
bohemian_dome_text = vtkTextActor()
bohemian_dome_text.SetInput("BohemianDome")
bohemian_dome_text.GetTextProperty().SetFontSize(14)
bohemian_dome_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
bohemian_dome_text.GetTextProperty().SetJustificationToCentered()
bohemian_dome_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
bohemian_dome_text.SetPosition(0.5, 0.01)

bour_text = vtkTextActor()
bour_text.SetInput("Bour")
bour_text.GetTextProperty().SetFontSize(14)
bour_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
bour_text.GetTextProperty().SetJustificationToCentered()
bour_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
bour_text.SetPosition(0.5, 0.01)

boy_text = vtkTextActor()
boy_text.SetInput("Boy")
boy_text.GetTextProperty().SetFontSize(14)
boy_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
boy_text.GetTextProperty().SetJustificationToCentered()
boy_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
boy_text.SetPosition(0.5, 0.01)

catalan_text = vtkTextActor()
catalan_text.SetInput("CatalanMinimal")
catalan_text.GetTextProperty().SetFontSize(14)
catalan_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
catalan_text.GetTextProperty().SetJustificationToCentered()
catalan_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
catalan_text.SetPosition(0.5, 0.01)

conic_text = vtkTextActor()
conic_text.SetInput("ConicSpiral")
conic_text.GetTextProperty().SetFontSize(14)
conic_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
conic_text.GetTextProperty().SetJustificationToCentered()
conic_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
conic_text.SetPosition(0.5, 0.01)

crosscap_text = vtkTextActor()
crosscap_text.SetInput("CrossCap")
crosscap_text.GetTextProperty().SetFontSize(14)
crosscap_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
crosscap_text.GetTextProperty().SetJustificationToCentered()
crosscap_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
crosscap_text.SetPosition(0.5, 0.01)

dini_text = vtkTextActor()
dini_text.SetInput("Dini")
dini_text.GetTextProperty().SetFontSize(14)
dini_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
dini_text.GetTextProperty().SetJustificationToCentered()
dini_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
dini_text.SetPosition(0.5, 0.01)

ellipsoid_text = vtkTextActor()
ellipsoid_text.SetInput("Ellipsoid")
ellipsoid_text.GetTextProperty().SetFontSize(14)
ellipsoid_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
ellipsoid_text.GetTextProperty().SetJustificationToCentered()
ellipsoid_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
ellipsoid_text.SetPosition(0.5, 0.01)

enneper_text = vtkTextActor()
enneper_text.SetInput("Enneper")
enneper_text.GetTextProperty().SetFontSize(14)
enneper_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
enneper_text.GetTextProperty().SetJustificationToCentered()
enneper_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
enneper_text.SetPosition(0.5, 0.01)

figure8_text = vtkTextActor()
figure8_text.SetInput("Figure8Klein")
figure8_text.GetTextProperty().SetFontSize(14)
figure8_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
figure8_text.GetTextProperty().SetJustificationToCentered()
figure8_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
figure8_text.SetPosition(0.5, 0.01)

henneberg_text = vtkTextActor()
henneberg_text.SetInput("Henneberg")
henneberg_text.GetTextProperty().SetFontSize(14)
henneberg_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
henneberg_text.GetTextProperty().SetJustificationToCentered()
henneberg_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
henneberg_text.SetPosition(0.5, 0.01)

klein_text = vtkTextActor()
klein_text.SetInput("Klein")
klein_text.GetTextProperty().SetFontSize(14)
klein_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
klein_text.GetTextProperty().SetJustificationToCentered()
klein_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
klein_text.SetPosition(0.5, 0.01)

kuen_text = vtkTextActor()
kuen_text.SetInput("Kuen")
kuen_text.GetTextProperty().SetFontSize(14)
kuen_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
kuen_text.GetTextProperty().SetJustificationToCentered()
kuen_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
kuen_text.SetPosition(0.5, 0.01)

mobius_text = vtkTextActor()
mobius_text.SetInput("Mobius")
mobius_text.GetTextProperty().SetFontSize(14)
mobius_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
mobius_text.GetTextProperty().SetJustificationToCentered()
mobius_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
mobius_text.SetPosition(0.5, 0.01)

plucker_text = vtkTextActor()
plucker_text.SetInput("PluckerConoid")
plucker_text.GetTextProperty().SetFontSize(14)
plucker_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
plucker_text.GetTextProperty().SetJustificationToCentered()
plucker_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
plucker_text.SetPosition(0.5, 0.01)

pseudo_text = vtkTextActor()
pseudo_text.SetInput("Pseudosphere")
pseudo_text.GetTextProperty().SetFontSize(14)
pseudo_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
pseudo_text.GetTextProperty().SetJustificationToCentered()
pseudo_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pseudo_text.SetPosition(0.5, 0.01)

random_hills_text = vtkTextActor()
random_hills_text.SetInput("RandomHills")
random_hills_text.GetTextProperty().SetFontSize(14)
random_hills_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
random_hills_text.GetTextProperty().SetJustificationToCentered()
random_hills_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
random_hills_text.SetPosition(0.5, 0.01)

roman_text = vtkTextActor()
roman_text.SetInput("Roman")
roman_text.GetTextProperty().SetFontSize(14)
roman_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
roman_text.GetTextProperty().SetJustificationToCentered()
roman_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
roman_text.SetPosition(0.5, 0.01)

spline_text = vtkTextActor()
spline_text.SetInput("Spline")
spline_text.GetTextProperty().SetFontSize(14)
spline_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
spline_text.GetTextProperty().SetJustificationToCentered()
spline_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
spline_text.SetPosition(0.5, 0.01)

super_ellipsoid_text = vtkTextActor()
super_ellipsoid_text.SetInput("SuperEllipsoid")
super_ellipsoid_text.GetTextProperty().SetFontSize(14)
super_ellipsoid_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
super_ellipsoid_text.GetTextProperty().SetJustificationToCentered()
super_ellipsoid_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
super_ellipsoid_text.SetPosition(0.5, 0.01)

super_toroid_text = vtkTextActor()
super_toroid_text.SetInput("SuperToroid")
super_toroid_text.GetTextProperty().SetFontSize(14)
super_toroid_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
super_toroid_text.GetTextProperty().SetJustificationToCentered()
super_toroid_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
super_toroid_text.SetPosition(0.5, 0.01)

torus_text = vtkTextActor()
torus_text.SetInput("Torus")
torus_text.GetTextProperty().SetFontSize(14)
torus_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
torus_text.GetTextProperty().SetJustificationToCentered()
torus_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
torus_text.SetPosition(0.5, 0.01)

# ---------------------------------------------------------------------------
# Renderers: one per surface viewport + 3 empty cells
# ---------------------------------------------------------------------------
bohemian_dome_renderer = vtkRenderer()
bohemian_dome_renderer.AddActor(bohemian_dome_actor)
bohemian_dome_renderer.AddViewProp(bohemian_dome_text)
bohemian_dome_renderer.SetBackground(midnight_blue_rgb)
bohemian_dome_renderer.SetViewport(0 / num_cols, 4 / num_rows, 1 / num_cols, 5 / num_rows)

bour_renderer = vtkRenderer()
bour_renderer.AddActor(bour_actor)
bour_renderer.AddViewProp(bour_text)
bour_renderer.SetBackground(midnight_blue_rgb)
bour_renderer.SetViewport(1 / num_cols, 4 / num_rows, 2 / num_cols, 5 / num_rows)

boy_renderer = vtkRenderer()
boy_renderer.AddActor(boy_actor)
boy_renderer.AddViewProp(boy_text)
boy_renderer.SetBackground(midnight_blue_rgb)
boy_renderer.SetViewport(2 / num_cols, 4 / num_rows, 3 / num_cols, 5 / num_rows)

catalan_renderer = vtkRenderer()
catalan_renderer.AddActor(catalan_actor)
catalan_renderer.AddViewProp(catalan_text)
catalan_renderer.SetBackground(midnight_blue_rgb)
catalan_renderer.SetViewport(3 / num_cols, 4 / num_rows, 4 / num_cols, 5 / num_rows)

conic_renderer = vtkRenderer()
conic_renderer.AddActor(conic_actor)
conic_renderer.AddViewProp(conic_text)
conic_renderer.SetBackground(midnight_blue_rgb)
conic_renderer.SetViewport(4 / num_cols, 4 / num_rows, 5 / num_cols, 5 / num_rows)

crosscap_renderer = vtkRenderer()
crosscap_renderer.AddActor(crosscap_actor)
crosscap_renderer.AddViewProp(crosscap_text)
crosscap_renderer.SetBackground(midnight_blue_rgb)
crosscap_renderer.SetViewport(0 / num_cols, 3 / num_rows, 1 / num_cols, 4 / num_rows)

dini_renderer = vtkRenderer()
dini_renderer.AddActor(dini_actor)
dini_renderer.AddViewProp(dini_text)
dini_renderer.SetBackground(midnight_blue_rgb)
dini_renderer.SetViewport(1 / num_cols, 3 / num_rows, 2 / num_cols, 4 / num_rows)

ellipsoid_renderer = vtkRenderer()
ellipsoid_renderer.AddActor(ellipsoid_actor)
ellipsoid_renderer.AddViewProp(ellipsoid_text)
ellipsoid_renderer.SetBackground(midnight_blue_rgb)
ellipsoid_renderer.SetViewport(2 / num_cols, 3 / num_rows, 3 / num_cols, 4 / num_rows)

enneper_renderer = vtkRenderer()
enneper_renderer.AddActor(enneper_actor)
enneper_renderer.AddViewProp(enneper_text)
enneper_renderer.SetBackground(midnight_blue_rgb)
enneper_renderer.SetViewport(3 / num_cols, 3 / num_rows, 4 / num_cols, 4 / num_rows)

figure8_renderer = vtkRenderer()
figure8_renderer.AddActor(figure8_actor)
figure8_renderer.AddViewProp(figure8_text)
figure8_renderer.SetBackground(midnight_blue_rgb)
figure8_renderer.SetViewport(4 / num_cols, 3 / num_rows, 5 / num_cols, 4 / num_rows)

henneberg_renderer = vtkRenderer()
henneberg_renderer.AddActor(henneberg_actor)
henneberg_renderer.AddViewProp(henneberg_text)
henneberg_renderer.SetBackground(midnight_blue_rgb)
henneberg_renderer.SetViewport(0 / num_cols, 2 / num_rows, 1 / num_cols, 3 / num_rows)

klein_renderer = vtkRenderer()
klein_renderer.AddActor(klein_actor)
klein_renderer.AddViewProp(klein_text)
klein_renderer.SetBackground(midnight_blue_rgb)
klein_renderer.SetViewport(1 / num_cols, 2 / num_rows, 2 / num_cols, 3 / num_rows)

kuen_renderer = vtkRenderer()
kuen_renderer.AddActor(kuen_actor)
kuen_renderer.AddViewProp(kuen_text)
kuen_renderer.SetBackground(midnight_blue_rgb)
kuen_renderer.SetViewport(2 / num_cols, 2 / num_rows, 3 / num_cols, 3 / num_rows)

mobius_renderer = vtkRenderer()
mobius_renderer.AddActor(mobius_actor)
mobius_renderer.AddViewProp(mobius_text)
mobius_renderer.SetBackground(midnight_blue_rgb)
mobius_renderer.SetViewport(3 / num_cols, 2 / num_rows, 4 / num_cols, 3 / num_rows)

plucker_renderer = vtkRenderer()
plucker_renderer.AddActor(plucker_actor)
plucker_renderer.AddViewProp(plucker_text)
plucker_renderer.SetBackground(midnight_blue_rgb)
plucker_renderer.SetViewport(4 / num_cols, 2 / num_rows, 5 / num_cols, 3 / num_rows)

pseudo_renderer = vtkRenderer()
pseudo_renderer.AddActor(pseudo_actor)
pseudo_renderer.AddViewProp(pseudo_text)
pseudo_renderer.SetBackground(midnight_blue_rgb)
pseudo_renderer.SetViewport(0 / num_cols, 1 / num_rows, 1 / num_cols, 2 / num_rows)

random_hills_renderer = vtkRenderer()
random_hills_renderer.AddActor(random_hills_actor)
random_hills_renderer.AddViewProp(random_hills_text)
random_hills_renderer.SetBackground(midnight_blue_rgb)
random_hills_renderer.SetViewport(1 / num_cols, 1 / num_rows, 2 / num_cols, 2 / num_rows)

roman_renderer = vtkRenderer()
roman_renderer.AddActor(roman_actor)
roman_renderer.AddViewProp(roman_text)
roman_renderer.SetBackground(midnight_blue_rgb)
roman_renderer.SetViewport(2 / num_cols, 1 / num_rows, 3 / num_cols, 2 / num_rows)

spline_renderer = vtkRenderer()
spline_renderer.AddActor(spline_actor)
spline_renderer.AddViewProp(spline_text)
spline_renderer.SetBackground(midnight_blue_rgb)
spline_renderer.SetViewport(3 / num_cols, 1 / num_rows, 4 / num_cols, 2 / num_rows)

super_ellipsoid_renderer = vtkRenderer()
super_ellipsoid_renderer.AddActor(super_ellipsoid_actor)
super_ellipsoid_renderer.AddViewProp(super_ellipsoid_text)
super_ellipsoid_renderer.SetBackground(midnight_blue_rgb)
super_ellipsoid_renderer.SetViewport(4 / num_cols, 1 / num_rows, 5 / num_cols, 2 / num_rows)

super_toroid_renderer = vtkRenderer()
super_toroid_renderer.AddActor(super_toroid_actor)
super_toroid_renderer.AddViewProp(super_toroid_text)
super_toroid_renderer.SetBackground(midnight_blue_rgb)
super_toroid_renderer.SetViewport(0 / num_cols, 0 / num_rows, 1 / num_cols, 1 / num_rows)

torus_renderer = vtkRenderer()
torus_renderer.AddActor(torus_actor)
torus_renderer.AddViewProp(torus_text)
torus_renderer.SetBackground(midnight_blue_rgb)
torus_renderer.SetViewport(1 / num_cols, 0 / num_rows, 2 / num_cols, 1 / num_rows)

empty_renderer_0 = vtkRenderer()
empty_renderer_0.SetBackground(midnight_blue_rgb)
empty_renderer_0.SetViewport(2 / num_cols, 0 / num_rows, 3 / num_cols, 1 / num_rows)

empty_renderer_1 = vtkRenderer()
empty_renderer_1.SetBackground(midnight_blue_rgb)
empty_renderer_1.SetViewport(3 / num_cols, 0 / num_rows, 4 / num_cols, 1 / num_rows)

empty_renderer_2 = vtkRenderer()
empty_renderer_2.SetBackground(midnight_blue_rgb)
empty_renderer_2.SetViewport(4 / num_cols, 0 / num_rows, 5 / num_cols, 1 / num_rows)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(bohemian_dome_renderer)
render_window.AddRenderer(bour_renderer)
render_window.AddRenderer(boy_renderer)
render_window.AddRenderer(catalan_renderer)
render_window.AddRenderer(conic_renderer)
render_window.AddRenderer(crosscap_renderer)
render_window.AddRenderer(dini_renderer)
render_window.AddRenderer(ellipsoid_renderer)
render_window.AddRenderer(enneper_renderer)
render_window.AddRenderer(figure8_renderer)
render_window.AddRenderer(henneberg_renderer)
render_window.AddRenderer(klein_renderer)
render_window.AddRenderer(kuen_renderer)
render_window.AddRenderer(mobius_renderer)
render_window.AddRenderer(plucker_renderer)
render_window.AddRenderer(pseudo_renderer)
render_window.AddRenderer(random_hills_renderer)
render_window.AddRenderer(roman_renderer)
render_window.AddRenderer(spline_renderer)
render_window.AddRenderer(super_ellipsoid_renderer)
render_window.AddRenderer(super_toroid_renderer)
render_window.AddRenderer(torus_renderer)
render_window.AddRenderer(empty_renderer_0)
render_window.AddRenderer(empty_renderer_1)
render_window.AddRenderer(empty_renderer_2)
render_window.SetWindowName("parametric objects demo")
render_window.SetMultiSamples(0)
render_window.SetSize(1200, 1200)

# Interactor
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure cameras
bohemian_dome_renderer.ResetCamera()
bohemian_dome_renderer.GetActiveCamera().Zoom(1.3)
bour_renderer.ResetCamera()
bour_renderer.GetActiveCamera().Zoom(1.3)
boy_renderer.ResetCamera()
boy_renderer.GetActiveCamera().Zoom(1.3)
catalan_renderer.ResetCamera()
catalan_renderer.GetActiveCamera().Zoom(1.3)
conic_renderer.ResetCamera()
conic_renderer.GetActiveCamera().Zoom(1.3)
crosscap_renderer.ResetCamera()
crosscap_renderer.GetActiveCamera().Zoom(1.3)
dini_renderer.ResetCamera()
dini_renderer.GetActiveCamera().Zoom(1.3)
ellipsoid_renderer.ResetCamera()
ellipsoid_renderer.GetActiveCamera().Zoom(1.3)
enneper_renderer.ResetCamera()
enneper_renderer.GetActiveCamera().Zoom(1.3)
figure8_renderer.ResetCamera()
figure8_renderer.GetActiveCamera().Zoom(1.3)
henneberg_renderer.ResetCamera()
henneberg_renderer.GetActiveCamera().Zoom(1.3)
klein_renderer.ResetCamera()
klein_renderer.GetActiveCamera().Zoom(1.3)
kuen_renderer.ResetCamera()
kuen_renderer.GetActiveCamera().Zoom(1.3)
mobius_renderer.ResetCamera()
mobius_renderer.GetActiveCamera().Zoom(1.3)
plucker_renderer.ResetCamera()
plucker_renderer.GetActiveCamera().Zoom(1.3)
pseudo_renderer.ResetCamera()
pseudo_renderer.GetActiveCamera().Zoom(1.3)
random_hills_renderer.ResetCamera()
random_hills_renderer.GetActiveCamera().Zoom(1.3)
roman_renderer.ResetCamera()
roman_renderer.GetActiveCamera().Zoom(1.3)
spline_renderer.ResetCamera()
spline_renderer.GetActiveCamera().Zoom(1.3)
super_ellipsoid_renderer.ResetCamera()
super_ellipsoid_renderer.GetActiveCamera().Zoom(1.3)
super_toroid_renderer.ResetCamera()
super_toroid_renderer.GetActiveCamera().Zoom(1.3)
torus_renderer.ResetCamera()
torus_renderer.GetActiveCamera().Zoom(1.3)

render_window_interactor.Initialize()
render_window_interactor.Start()
