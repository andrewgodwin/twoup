twoup
=====

An SVG-based presentation toolset. Works with presentations composed of
individual SVG files in a directory, and builds them either to PDF or
to a set of PNG files.

Also includes a custom GUI which runs alongside a PDF presenting program and
shows a presenter view with the current and next slides.

![Viewer example image](/docs/viewer.png?raw=true "Viewer example")

Usage
-----

The compilation into PDF/PNG is triggered like so::

    cd /path/to/slides
    twoup build

This requires ``inkscape`` and ``pdftk`` to be installed and available
in the PATH. I usually run it from either Linux or the Windows Linux Subsystem.

The presenter view is triggered with::

    cd /path/to/slides
    twoup gui

This currently requires you to have the ``pywinauto`` library, be running on
Windows, and be using the SumatraPDF reader.

Why?
----

I make and run presentations off of both Linux and Windows, and when I
started speaking that meant very few options of program. Now, I stick with
SVG slides out of both laziness and a love for Inkscape's drawing tools.
