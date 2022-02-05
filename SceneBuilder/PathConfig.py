import shutil, os

def find_app_paths():
    blender = shutil.which("blender")
    maxima = shutil.which("maxima")

    if not blender:
        blender = '/Applications/Blender.app/Contents/MacOS/Blender'
    if not maxima:
        maxima = "/opt/homebrew/bin/maxima"
    # TODO: Include Linux/Windows support.
    return (blender, maxima)

