## Render SBGN
from IPython.display import Image, display_png
import tempfile

import IPython
from IPython.core.display import HTML
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from libsbgnpy import render, utils
sbgn = utils.read_from_file("Repressilator_PD_v7.sbgn")
f_png = tempfile.NamedTemporaryFile(suffix=".png")
render.render_sbgn(sbgn, image_file=f_png.name,
                   file_format="png")
display_png(Image(f_png.name, width=500))