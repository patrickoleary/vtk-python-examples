### Description

This example displays all 21 parametric surfaces arranged in a 5 × 5 grid inside a single renderer. Each surface is normalized to a consistent size and labelled. It follows the VTK pipeline structure:

**Source → Mapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) renders each surface in navajo white, scaled to a uniform size and positioned on a 5-column grid with `SetPosition()` and `SetScale()`.
- [vtkMinimalStandardRandomSequence](https://www.vtk.org/doc/nightly/html/classvtkMinimalStandardRandomSequence.html) provides minimal standard random sequence functionality.
- [vtkParametricBohemianDome](https://www.vtk.org/doc/nightly/html/classvtkParametricBohemianDome.html) provides parametric bohemian dome functionality.
- [vtkParametricBour](https://www.vtk.org/doc/nightly/html/classvtkParametricBour.html) provides parametric bour functionality.
- [vtkParametricBoy](https://www.vtk.org/doc/nightly/html/classvtkParametricBoy.html) provides parametric boy functionality.
- [vtkParametricCatalanMinimal](https://www.vtk.org/doc/nightly/html/classvtkParametricCatalanMinimal.html) provides parametric catalan minimal functionality.
- [vtkParametricConicSpiral](https://www.vtk.org/doc/nightly/html/classvtkParametricConicSpiral.html) provides parametric conic spiral functionality.
- [vtkParametricCrossCap](https://www.vtk.org/doc/nightly/html/classvtkParametricCrossCap.html) provides parametric cross cap functionality.
- [vtkParametricDini](https://www.vtk.org/doc/nightly/html/classvtkParametricDini.html) provides parametric dini functionality.
- [vtkParametricEllipsoid](https://www.vtk.org/doc/nightly/html/classvtkParametricEllipsoid.html) provides parametric ellipsoid functionality.
- [vtkParametricEnneper](https://www.vtk.org/doc/nightly/html/classvtkParametricEnneper.html) provides parametric enneper functionality.
- [vtkParametricFigure8Klein](https://www.vtk.org/doc/nightly/html/classvtkParametricFigure8Klein.html) provides parametric figure8klein functionality.
- [vtkParametricFunctionSource](https://www.vtk.org/doc/nightly/html/classvtkParametricFunctionSource.html) samples each parametric function to produce polygonal output.
- [vtkParametricHenneberg](https://www.vtk.org/doc/nightly/html/classvtkParametricHenneberg.html) provides parametric henneberg functionality.
- [vtkParametricKlein](https://www.vtk.org/doc/nightly/html/classvtkParametricKlein.html) provides parametric klein functionality.
- [vtkParametricKuen](https://www.vtk.org/doc/nightly/html/classvtkParametricKuen.html) provides parametric kuen functionality.
- [vtkParametricMobius](https://www.vtk.org/doc/nightly/html/classvtkParametricMobius.html) provides parametric mobius functionality.
- [vtkParametricPluckerConoid](https://www.vtk.org/doc/nightly/html/classvtkParametricPluckerConoid.html) provides parametric plucker conoid functionality.
- [vtkParametricPseudosphere](https://www.vtk.org/doc/nightly/html/classvtkParametricPseudosphere.html) provides parametric pseudosphere functionality.
- [vtkParametricRandomHills](https://www.vtk.org/doc/nightly/html/classvtkParametricRandomHills.html) provides parametric random hills functionality.
- [vtkParametricRoman](https://www.vtk.org/doc/nightly/html/classvtkParametricRoman.html) provides parametric roman functionality.
- [vtkParametricSpline](https://www.vtk.org/doc/nightly/html/classvtkParametricSpline.html) provides parametric spline functionality.
- [vtkParametricSuperEllipsoid](https://www.vtk.org/doc/nightly/html/classvtkParametricSuperEllipsoid.html) provides parametric super ellipsoid functionality.
- [vtkParametricSuperToroid](https://www.vtk.org/doc/nightly/html/classvtkParametricSuperToroid.html) provides parametric super toroid functionality.
- [vtkParametricTorus](https://www.vtk.org/doc/nightly/html/classvtkParametricTorus.html) provides parametric torus functionality.
- [vtkPoints](https://www.vtk.org/doc/nightly/html/classvtkPoints.html) stores 3D point coordinates.
- [vtkPolyDataMapper](https://www.vtk.org/doc/nightly/html/classvtkPolyDataMapper.html) maps each surface geometry to graphics primitives.
- [vtkTextActor](https://www.vtk.org/doc/nightly/html/classvtkTextActor.html) overlays text in the viewport.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene with a midnight blue background.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
