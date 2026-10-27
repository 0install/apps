import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import msys2

# MSYS2 split gcc-libs into libgcc, libstdc++, etc. (built from the same sources, sharing a version) in 16.2.0-4
# Not available for clangarm64, which uses LLVM's runtime libraries instead
releases = msys2.releases('libgcc', repos=['ucrt64'])
