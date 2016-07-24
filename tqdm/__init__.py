from ._tqdm import tqdm as _tqdm
from ._tqdm_notebook import tqdm_notebook as _tqdm_notebook
from ._tqdm import trange
from ._tqdm_gui import tqdm_gui
from ._tqdm_gui import tgrange
from ._tqdm_pandas import tqdm_pandas
from ._main import main
from ._main import TqdmKeyError
from ._main import TqdmTypeError
from ._version import __version__  # NOQA

try:
    from IPython import get_ipython
    from IPython.terminal.interactiveshell import TerminalInteractiveShell as TIShell
    ip = get_ipython()
    if ip is not None and not isinstance(ip, TIShell):
        # Then we might be in ipython notebook. Check.
        from IPython import display
        # WARNING: terrible hack below
        display.display_javascript("""IPython.notebook.kernel.execute(
                'from IPython import get_ipython;get_ipython().has_js=True');""",
                 raw=True)
        try:
            from ipywidgets import FloatProgress, Text
        except ImportError:
            from IPython.html.widgets import FloatProgress, Text
except (ImportError, AssertionError):
    # Not using IPython notebook. Default to text displays
    pass


__all__ = ['tqdm', 'tqdm_gui', 'trange', 'tgrange', 'tqdm_pandas',
           'tqdm_notebook', 'tnrange', 'main', 'TqdmKeyError', 'TqdmTypeError',
           '_tqdm', '_tqdm_notebook', '__version__']

def tqdm(*args, **kwargs):
    if _has_js():
        # This is the deferred notebook check, detailed above.
        return _tqdm_notebook(*args, **kwargs)
    return _tqdm(*args, **kwargs)
# Hack to make tab-complete documentation work in ipython notebook
tqdm.__doc__ = _tqdm.__init__.__doc__


def tqdm_notebook(*args, **kwargs):  # pragma: no cover
    """See tqdm._tqdm_notebook.tqdm_notebook for full documentation"""
    from ._tqdm_notebook import tqdm_notebook as _tqdm_notebook
    return _tqdm_notebook(*args, **kwargs)


def tnrange(*args, **kwargs):  # pragma: no cover
    """
    A shortcut for tqdm_notebook(xrange(*args), **kwargs).
    On Python3+ range is used instead of xrange.
    """
    from ._tqdm_notebook import tnrange as _tnrange
    return _tnrange(*args, **kwargs)


def _has_js():
    """Checks the ip object for has_js.
    ``ip = IPython.get_ipython()`` from import stage.
    This check has to be deferred to after the import because
    the javascript doesn't execute until the cell is executed, so
    immediately checking whether it worked will always return false.
    Luckily most use cases in notebook will use separate cells for
    the import statement and the loop.
    """
    return hasattr(ip, 'has_js')
