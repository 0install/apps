#os=Linux
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import robo3t

releases = robo3t.releases('.tar.gz')
