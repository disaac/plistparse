"""

"""

import json
import logging
import plistlib
import re
import sys

import click

from plistparse import __version__

__author__ = "Daniel"
__copyright__ = "Daniel"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from plistparse.plistparse import parse`,
# when using this Python module as a library.


def parse(plist):
    """Parse plist and filter the data

    Args:
      plist (file): plist file to parse

    Returns:
      string or list or dict: parsed plist
    """

    # this coverts bytes to a string so that it can be dumped as JSON
    if isinstance(plist, bytes):
        try:
            # Even though its bytes, try to decode it as utf-8
            return plist.decode("utf-8")
        except UnicodeDecodeError:
            pass

        # if it can't be decoded as utf-8, try to extract strings from the binary data
        ms = re.findall(b"[\x20-\x7F]{4,}", plist)
        if (
            len(ms) and False
        ):  # adding 'and False' here for now to disable this feature.
            # It makes the outputted structure unpredictable and not sure if it's useful
            # if theres extracted strings, return them as a list
            # AND the raw str() 'encoded' bytes
            return {
                "__raw": str(plist),
                "__strings": f"{[s.decode('utf-8') for s in ms]}",
            }
        else:
            return str(plist)
    elif isinstance(plist, list):
        return [parse(x) for x in plist]
    elif isinstance(plist, dict):
        return {k: parse(v) for k, v in plist.items()}
    else:
        return plist


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def setup_logging(loglevel, stream="stderr"):
    """Setup basic logging

    Args:
      loglevel (levelname): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logginglevel = getattr(logging, loglevel.upper())
    sysstream = getattr(sys, stream.lower())
    logging.basicConfig(
        level=logginglevel,
        stream=sysstream,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(fname, out, oformat, iformat, loglevel):
    """Main entry point allowing external calls

    Instead of returning the value from :func:`parse`, it prints the result to the
    ``stdout`` or ``out`` file.

    Args:
        see :click:`options`
    """
    setup_logging(loglevel, "stderr")
    _logger.debug("Starting plist parsing...")
    if fname is not sys.stdin:
        fn = fname
    else:
        fn = fname.buffer
    if iformat == "xml":
        try:
            plist = plistlib.load(
                fn, fmt=plistlib.FMT_XML if iformat == "xml" else None
            )
        except Exception as e:
            _logger.error(f"Error loading plist file: {fn} exception: {e}")
            raise
        if oformat == "json":
            try:
                click.echo(json.dumps(parse(plist), indent=4), file=out)
            except Exception as e:
                _logger.error(
                    f"Error outputting oformat: {oformat} iformat: {iformat} plist: {e}"
                )
                raise
        if oformat == "xml":
            try:
                click.echo(plistlib.dumps(parse(plist)), file=out)
            except Exception as e:
                _logger.error(
                    f"Error outputting oformat: {oformat} iformat: {iformat} plist: {e}"
                )
                raise
    if iformat == "json":
        if oformat == "xml":
            try:
                click.echo(
                    plistlib.dumps(json.load(fn), fmt=plistlib.FMT_XML), file=out
                )
            except Exception as e:
                _logger.error(
                    f"Error outputting oformat: {oformat} iformat: {iformat} plist: {e}"
                )
                raise
        elif oformat == "json":
            try:
                click.echo(
                    json.dumps(
                        parse(json.load(fn)),
                        indent=4,
                    ),
                    file=out,
                )
            except Exception as e:
                _logger.error(
                    f"Error outputting oformat: {oformat} iformat: {iformat} plist: {e}"
                )
                raise
    _logger.debug("Ending plist parsing")


@click.version_option(__version__, "--version", "-V")
@click.command()
@click.option(
    "--fname",
    "-f",
    help="Filename of the plist, omit to read from STDIN.",
    type=click.File("rb", lazy=False),
    default=sys.stdin,
)
@click.option(
    "--out",
    "-o",
    help="File to write the Output to, omit to display on screen.",
    type=click.File("ab"),
    default=sys.stdout,
)
@click.option(
    "--iformat",
    "-I",
    help="Format of input either json or xml",
    type=click.Choice(["json", "xml"], case_sensitive=False),
    default="xml",
)
@click.option(
    "--oformat",
    "-O",
    help="Format of output either json or xml",
    type=click.Choice(["json", "xml"], case_sensitive=False),
    default="json",
)
@click.option(
    "--loglevel",
    "-L",
    help="Log level for logging messages.",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"], case_sensitive=False
    ),
    default="info",
)
def run(fname, out, oformat, iformat, loglevel):
    """Processes the plist file from stdout or a file depending on provided options."""
    main(fname, out, oformat, iformat, loglevel)


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m plistparse.plistparse
    #
    run()
