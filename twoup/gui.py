from __future__ import unicode_literals

import glob
import sys
import time
from PIL import Image, ImageTk
from Tkinter import Tk, Label, LEFT, Y


class Gui(object):
    """
    Encapsulates the GUI reading and display code.
    Specific to SumatraPDF on Windows right now.
    """

    def __init__(self, base_path):
        self.base_path = base_path

    def detect_windows(self):
        """
        Works out what windows are available and which is the main window
        by detecting which one moves its page.
        """
        # Internal import so the rest can be used on Linux
        from pywinauto import Desktop, findwindows
        # Get the initial list of PDF windows
        windows = [
            Desktop().window(handle=window_handle)
            for window_handle in
            findwindows.find_windows(title_re=r".* \- SumatraPDF$")
        ]
        if not windows:
            print("No PDF windows detected")
            sys.exit(1)
        if len(windows) == 1:
            return windows[0], []
        # Wait until one moves its page, then declare that the main one
        last_pages = {}
        main_window = None
        print("Waiting to detect main window from: %s" % windows)
        while not main_window:
            for window in windows:
                new_page = self.get_window_page(window)
                if window in last_pages and last_pages[window] != new_page:
                    main_window = window
                    break
                last_pages[window] = new_page
            time.sleep(0.1)
        # OK, we have the main one, return
        print("Got main window: %s" % main_window)
        return main_window, [window for window in windows if window is not main_window]

    def get_window_page(self, window):
        """
        Given a window, returns the page number it is on, or None if it cannot be
        detected.
        """
        seen_page = False
        for descendant in window.descendants():
            if descendant.window_text() == "Page:":
                seen_page = True
            elif seen_page and descendant.class_name() == "Edit" and descendant.window_text().isdigit():
                return int(descendant.window_text())
        return None


    def set_window_page(self, window, page):
        """
        Sets a window's page to the given page number
        """
        seen_page = False
        for descendant in window.descendants():
            if descendant.window_text() == "Page:":
                seen_page = True
            elif seen_page and descendant.class_name() == "Edit" and descendant.window_text().isdigit():
                descendant.set_text(page)
                descendant.type_keys("{ENTER}")
                return

    def page_loop(self, main_window, other_windows):
        """
        Copies page navigation from main_window to all other_windows.
        It has to focus each window to do this, so it can flicker.
        """
        old_page = self.get_window_page(main_window)
        while True:
            new_page = self.get_window_page(main_window)
            if new_page is None:
                print("Main window exited")
                sys.exit(1)
            if new_page != old_page:
                print("Page changed to %s" % new_page)
                for other_window in other_windows:
                    self.set_window_page(other_window, new_page)
                main_window.set_focus()
            # Loop
            old_page = new_page
            time.sleep(0.1)

    def run_tk(self):
        """
        Runs a TK-based viewer with current slide and next slide
        """
        # Detect PDF windows
        main_window, other_windows = self.detect_windows()
        # Make main window
        root = Tk()
        root.title("viewer")
        # Load images into memory
        images = [
            ImageTk.PhotoImage(Image.open(filename))
            for filename in
            glob.glob("./pngs/*.svg.png")
        ]
        # Add current and next image labels
        current = Label(root, image=images[0])
        current.pack(side=LEFT, fill=Y)
        next = Label(root, image=images[1])
        next.pack(side=LEFT, fill=Y)
        # Add a continuous task to poll which page to flip to
        def task():
            page = self.get_window_page(main_window) - 1
            if page < len(images):
                current.configure(image = images[page])
                current.image = images[page]
                if page < len(images) - 1:
                    next.configure(image = images[page+1])
                    next.image = images[page+1]
            root.after(200, task)
        root.after(200, task)
        # Run TK
        root.mainloop()
