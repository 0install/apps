#os=Linux
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import blender

releases = blender.releases('linux-x64.tar.xz')
