# rustup publishes no GitHub releases, only version tags; the binaries live on
# static.rust-lang.org. Tags carry no date, so the template omits {released}.
import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': tag['name']
} for tag in github.tags('rust-lang/rustup') if re.match(r'^\d+\.\d+\.\d+$', tag['name'])]
