# Some Python imports (needed for the code below) - you can leave these alone
import os
from repo import paths
import subprocess, shutil
from os.path import join


# The URL of the directory which will host the repository (feeds, keys, stylesheets and catalogue).
REPOSITORY_BASE_URL = "https://apps.0install.net/"

# The GPG secret key which 0repo should use to sign the generated feeds and any
# Git commits it makes. The fingerprint preceeded by "0x" is the most precise
# way to identity a key (see "HOW TO SPECIFY A USER ID" in the gpg(1) man-page
# for other options).
GPG_SIGNING_KEY = None if os.getenv('NO_SIGN') else "0x88C8A1F375928691D7365C0259AA3927C24E4E1E"

# If set, XML feeds in the "incoming" directory and any Git pull requests must be signed by one of
# these keys, otherwise they will be rejected. For local use, this can be set to None so that the
# files don't need to be signed.
CONTRIBUTOR_GPG_KEYS = None

# Prompt about old implementations that remain in the "testing" stability level for too long.
# Set this to False if you intend to permanently mark releases as testing, e.g., release candidates.
TRACK_TESTING_IMPLS = False


#### Feed hosting ####

# Copy everything in './public' to REPOSITORY_BASE_URL
# e.g. so that public/catalog.xml can be downloaded as REPOSITORY_BASE_URL/catalog.xml
# 'files' is the set of files maintained by 0repo, which may be useful if you want to
# sync just those, commit them to Git, etc. Pathnames are relative to 'public', which is
# also the current directory.
# 'message' can be used if you want to log the reason for the update.
def upload_public_dir(files, message):
	subprocess.check_call(['git', 'config', 'user.name', 'apps.0install.net'])
	subprocess.check_call(['git', 'config', 'user.email', 'webmaster@0install.net'])
	subprocess.check_call(['git', 'add', '--', 'archives.db'] + files)
	changed = subprocess.call(['git', 'diff', '--exit-code', '--stat', 'HEAD'])
	if changed:
		subprocess.check_call(['git', 'commit', '-m', message])
		print("Changes to public committed. Remember to push!")
	else:
		print("No changes to public.")

#### Archive hosting ####

# The URL of the directory containing the archives.
# Note that uploaders can choose whether to store archives within 0repo or externally.
# This setting does not affect external archives, only archives managed by 0repo.
ARCHIVES_BASE_URL = "https://github.com/0install/apps/releases/download/archives/"

# Where to keep copies of the archives we upload.
LOCAL_ARCHIVES_BACKUP_DIR = "archive-backups/"

# At what URL under ARCHIVES_BASE_URL should this NEW file/archive be served?
# Note: Changing this does not affect archives which have already been uploaded; to relocate an existing archive, edit archives.db instead.
# Note: There may be multiple archives/files for a single version, so you probably want to keep archive_basename in the final URL.
def get_archive_rel_url(archive_basename, impl):
	return archive_basename

def guess_mime_type(name):
	if name.endswith('.zip'): return 'application/zip'
	elif name.endswith('.tar'): return 'application/x-tar'
	elif name.endswith('.tar.gz') or name.endswith('.tgz'): return 'application/x-compressed-tar'
	elif name.endswith('.tar.bz2') or name.endswith('.tbz2') or name.endswith('.tbz'): return 'application/x-bzip-compressed-tar'
	elif name.endswith('.tar.lzma') or name.endswith('.tlzma'): return 'application/x-lzma-compressed-tar'
	elif name.endswith('.tar.xz') or name.endswith('.txz'): return 'application/x-xz-compressed-tar'
	elif name.endswith('.gem'): return 'application/x-ruby-gem'
	elif name.endswith('.7z'): return 'application/x-7z-compressed'
	elif name.endswith('.cab'): return 'application/vnd.ms-cab-compressed'
	elif name.endswith('.msi'): return 'application/x-msi'
	elif name.endswith('.deb'): return 'application/x-deb'
	elif name.endswith('.rpm'): return 'application/x-rpm'
	elif name.endswith('.dmg'): return 'application/x-apple-diskimage'
	else: return 'application/zip'

# Upload these new archives to the file server.
# For each archive in the list:
#   archive.source_path = path to local archive to be uploaded (in LOCAL_ARCHIVES_BACKUP_DIR)
#   archive.rel_url = result from get_archive_rel_url() above
# If any target files already exist, overwrite them (we will retry if uploading fails part way through).
def upload_archives(archives):
	if os.getenv('GITHUB_TOKEN') and GPG_SIGNING_KEY:
		from urllib import request
		for archive in archives:
			print("Uploading " + archive.rel_url)
			with open(archive.source_path, 'br') as file:
				request.urlopen(request.Request(
                    # We use a single dummy "Release" on GitHub to host archives managed by 0repo.
                    # Note: In this repository most feeds point to externally hosted archives
					'https://uploads.github.com/repos/0install/apps/releases/22408464/assets?name=' + archive.rel_url,
					file.read(),
					headers={
						'Content-Type': guess_mime_type(archive.rel_url),
						'Accept': 'application/vnd.github.v3+json',
						'Authorization': 'token ' + os.environ['GITHUB_TOKEN']
					}
				)).read()

# Recalculate the manifest digests specified for local archives in incoming feeds to ensure the are correct.
# You can set this to False if you trust all contributors to create correct feeds.
CHECK_DIGESTS = False

#### Custom checks and rules ####

# When adding a new implementation to the repository, this function is called to check that
# it meets the repository policies. Return a string explaining the problem, if any.
def check_new_impl(impl):
	# Must have a release date
	released = impl.metadata.get('released', None)
	if not released:
		return "Missing 'released' attribute"

	# Must have a license
	license = impl.metadata.get('license', None)
	if not license:
		return "Missing 'license' attribute"

	return None


#### Repository Layout (advanced) ####

# uri_rel_path is the part of the feed's URL following REPOSITORY_BASE_URL.
# Where should it be placed within "feeds"? By default, these are the same.
# You might want to change this if you have a strange naming scheme (e.g. feed
# URLs ending in "/" or without an extension). The result must end in '.xml'.
def get_feeds_rel_path(uri_rel_path):
	return uri_rel_path.replace('/', os.sep)

# A source feed "feeds/games/my-game.xml" has a relative path of
# "games/my-game.xml". Where should the corresponding generated (signed) feed
# be placed under "public"? The default (and recommended) setting is to keep it
# the same, so we would generate "public/games/my-game.xml" in this case.
def get_public_rel_path(feeds_rel_path):
	return feeds_rel_path

# is_excluded_from_catalog controls wether a specific feed should be excluded from
# the generated catalog. By default this excludes any feed that has been marked as
# replaced by another feed.
# feed_root = the feed's XML data
# dir_rel_path = the relative path of the directory of the catalog being generated
def is_excluded_from_catalog(feed_root, dir_rel_path):
	def get_tag(tag_name):
		return feed_root.getElementsByTagName(tag_name)
	def has_tag(tag_name):
		return get_tag(tag_name).length > 0
	def has_main(tag_name):
		return any(tag.hasAttribute('main') for tag in get_tag(tag_name))
	def has_command(command_name):
		return any(tag.getAttribute('name') == command_name for tag in get_tag('command'))
	def is_executable():
		return has_main('group') or has_main('implementation') or has_main('package-implementation') or has_command('run') or has_tag('entry-point')
	def excluded_from_toplevel():
		return not is_executable() or feed_root.getAttribute('uri').startswith('https://apps.0install.net/lib/') or feed_root.getAttribute('uri').endswith('runtime.xml') or feed_root.getAttribute('uri').startswith('https://apps.0install.net/dotnet/clr') or feed_root.getAttribute('uri').startswith('https://apps.0install.net/0install/0install')

	return has_tag('replaced-by') or has_tag('feed-for') or (dir_rel_path == '' and excluded_from_toplevel())

# When 0install fetches a feed http://.../prog.xml, it looks for the GPG key at http://.../KEY.gpg.
# Normally, 0repo should place a symlink to the key in the same directory as the feed file (from get_public_rel_path); use "." for that.
GPG_PUBLIC_KEY_DIRECTORY = "."

# This for archives uploaded and managed by 0repo itself.
def check_uploaded_archive(archive, url): pass

# As check_uploaded_archive, but for external archives.
def check_external_archive(archive, url): pass
