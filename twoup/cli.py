import sys
import argparse
import logging
import importlib

from .generator import Generator
from .gui import Gui


class CommandLineInterface(object):
    """
    Acts as the main CLI entry point for running the server.
    """

    description = "SVG slide presentation tool"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=self.description,
        )
        self.parser.add_argument(
            '-d',
            '--dir',
            help='Directory to use as source',
            default=".",
        )
        self.parser.add_argument(
            'command',
            help='The command to run (either build or gui)',
        )

    @classmethod
    def entrypoint(cls):
        """
        Main entrypoint for external starts.
        """
        cls().run(sys.argv[1:])

    def run(self, args):
        """
        Pass in raw argument list and it will decode them
        and run the server.
        """
        # Decode args
        args = self.parser.parse_args(args)
        # Run right command
        if args.command == "build":
            Generator(args.dir).build()
        elif args.command == "gui":
            Gui(args.dir).run_tk()
        else:
            print("No such command: %s" % args.command)
            sys.exit(1)
