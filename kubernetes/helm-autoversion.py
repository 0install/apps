import sys
import subprocess
import re

def helm(version, args):
    return ['0install', 'run', '--version', version, 'https://apps.0install.net/kubernetes/helm'] + args

def get_version():
    version_dependant_commands = ['list', 'ls', 'get', 'status', 'history', 'hist', 'install', 'upgrade', 'test', 'rollback', 'delete', 'del']
    if any(x in version_dependant_commands for x in sys.argv[1:]):
        try:
            process = subprocess.run(helm('..!3-pre', ['version', '--server']), check=True, stdout=subprocess.PIPE, universal_newlines=True)
        except subprocess.CalledProcessError as ex:
            sys.exit(ex.returncode)
        result = re.search(r'SemVer:"v(?P<version>[^"]*)"', process.stdout)
        if result:
            return result.group('version')
    return '..!3-pre'

sys.exit(subprocess.call(helm(get_version(), sys.argv[1:])))
