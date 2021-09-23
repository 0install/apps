#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import blender

releases = blender.releases('windows-x64.zip')
