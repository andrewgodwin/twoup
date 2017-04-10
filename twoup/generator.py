import sys
import os
import subprocess
import glob


class Generator(object):
    """
    Generates PDF and PNG output from a set of slide SVGs.
    """

    def __init__(self, base_path):
        self.base_path = base_path
        if not os.path.exists(os.path.join(self.base_path, "slide01.svg")):
            raise ValueError("Directory does not appear to contain slides")
        self.type_paths = {
            "pdf": os.path.join(self.base_path, "pdfs"),
            "png": os.path.join(self.base_path, "pngs"),
        }

    def make_singles(self, type):
        """
        Compiles SVGs into PNGs or PDFs.
        """
        assert type in ["png", "pdf"]
        # Make destination directory
        if not os.path.isdir(self.type_paths[type]):
            os.mkdir(self.type_paths[type])
        # Find all SVG files
        seen = set()
        for filename in os.listdir(self.base_path):
            path = os.path.join(self.base_path, filename)
            if path.endswith(".svg"):
                seen.add(filename)
                # See if it has a compiled version that's newer, otherwise
                # compile it
                destination = os.path.join(
                    self.type_paths[type],
                    "%s.%s" % (filename, type),
                )
                if not os.path.exists(destination) or os.stat(destination).st_mtime <= os.stat(path).st_mtime:
                    # Recompile
                    print("Rendering %s to %s" % (filename, type.upper()))
                    if type == "png":
                        subprocess.call(["inkscape", "-z", filename, "-w", "1280", "-e", destination])
                    else:
                        subprocess.call(["inkscape", "-z", filename, "-A", destination])
        # Remove unmatched files
        for filename in os.listdir(self.type_paths[type]):
            original_name = filename[:-4]
            path = os.path.join(self.type_paths[type], filename)
            if original_name not in seen:
                print("Removing outdated %s" % filename)
                os.unlink(path)

    def make_combined_pdf(self):
        """
        Uses pdftk to combine the single pdfs into a single output
        """
        print("Making combined PDF")
        destination = os.path.join(self.base_path, "slides.pdf")
        subprocess.call([
            "pdftk",
            ] + glob.glob("%s/*.svg.pdf" % self.type_paths["pdf"]) + [
            "cat",
            "output",
            destination,
        ])

    def build(self, png=True, pdf=True):
        """
        Main entry point for building the slide set
        """
        if png:
            self.make_singles("png")
        if pdf:
            self.make_singles("pdf")
            self.make_combined_pdf()
