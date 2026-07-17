#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import krita

releases = list(krita.releases('krita-x64-{}.zip'))
