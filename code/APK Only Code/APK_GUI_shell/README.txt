#setup for windows/python 2.7.x:
pip uninstall Pillow
pip uninstall PIL
pip install Pillow
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew kivy.deps.gstreamer --extra-index-url https://kivy.org/downloads/packages/simple/
python -m pip install kivy

# The following should now work:
# $ python
# $>>> import PIL
# $>>> import kivy

# Test layers.py:
# $ python layers.py
# Notice 'layers.png' updating.

# Test GUI_shell.py:
# $ python GUI_shell.py
# Currently it does not update like the '.png' image.