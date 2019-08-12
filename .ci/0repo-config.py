# The URL of the directory which will host the repository (feeds, keys, stylesheets and catalogue).
REPOSITORY_BASE_URL = "http://repo.roscidus.com/"

# The GPG secret key which 0repo should use to sign the generated feeds and any
# Git commits it makes. The fingerprint preceeded by "0x" is the most precise
# way to identity a key (see "HOW TO SPECIFY A USER ID" in the gpg(1) man-page
# for other options).
GPG_SIGNING_KEY = None

# If set, XML feeds in the "incoming" directory and any Git pull requests must be signed by one of
# these keys, otherwise they will be rejected. For local use, this can be set to None so that the
# files don't need to be signed.
CONTRIBUTOR_GPG_KEYS = None

# Prompt about old implementations that remain in the "testing" stability level for too long.
# Set this to False if you intend to permanently mark releases as testing, e.g., release candidates.
TRACK_TESTING_IMPLS = False


# Some Python imports (needed for the code below) - you can leave these alone
import os
from repo import paths
import subprocess, shutil
from os.path import join


#### Feed hosting ####

# Copy everything in './public' to REPOSITORY_BASE_URL
# e.g. so that public/catalog.xml can be downloaded as REPOSITORY_BASE_URL/catalog.xml
# 'files' is the set of files maintained by 0repo, which may be useful if you want to
# sync just those, commit them to Git, etc. Pathnames are relative to 'public', which is
# also the current directory.
# 'message' can be used if you want to log the reason for the update.
def upload_public_dir(files, message):
	print "Just a CI run; not uploading"

#### Archive hosting ####

# The URL of the directory containing the archives (which will not be under REPOSITORY_BASE_URL if
# you are hosting archives on a different server). Note that uploaders can choose whether to store
# archives within 0repo or externally. This setting does not affect external archives, only archives
# managed by 0repo.
ARCHIVES_BASE_URL = REPOSITORY_BASE_URL + "archives/"

# Where to keep copies of the archives we upload.
LOCAL_ARCHIVES_BACKUP_DIR = "archive-backups/"

# At what URL under ARCHIVES_BASE_URL should this NEW file/archive be served?
#
# Note: Changing this does not affect archives which have already been uploaded;
#	to relocate an existing archive, edit archives.db instead.
#
# Note: There may be multiple archives/files for a single version, so you
#	probably want to keep archive_basename in the final URL.
def get_archive_rel_url(archive_basename, impl):
	if impl.feed.get_name() > 10:
		program = os.path.basename(impl.feed.url)
	else:
		program = impl.feed.get_name().replace(' ', '-'),
	return "{program}/{archive}".format(
		program = program,
		archive = archive_basename)

# Upload these new archives to the file server.
# For each archive in the list:
#   archive.source_path = path to local archive to be uploaded (in LOCAL_ARCHIVES_BACKUP_DIR)
#   archive.rel_url = result from get_archive_rel_url() above
# If any target files already exist, overwrite them (we will retry if uploading
# fails part way through).
def upload_archives(archives): pass

# Recalculate the manifest digests specified for local archives in incoming feeds to ensure the are correct.
# You can set this to False if you trust all contributors to create correct feeds.
CHECK_DIGESTS = False

#### Custom checks and rules ####

# When adding a new implementation to the repository, this function is called to check that
# it meets the repository policies. Return a string explaining the problem, if any.
def check_new_impl(impl):
	# Example: disallow in-progress version numbers (e.g. "1.2-pre")
	version = impl.get_version()
	if not version[-1].isdigit():
		return "Version number must end in a digit (got {version})".format(version = version)

	# Example: Must has a release date
	released = impl.metadata.get('released', None)
	#if not released:
	#	return "Missing 'released' attribute"

	# Example: Must have a license
	license = impl.metadata.get('license', None)
	if not license:
		return "Missing 'license' attribute"

	# Example: License must be OSI approved
	if not any(fragment in license for fragment in ("OSI Approved", "GPL", "General Public License", "MIT License", "BSD License", "Apache License", "Mozilla Public License", "Python License", "Ruby License")):
		return "Only Open Source software is permitted in this repository"

	return None


#### Repository Layout (advanced) ####

# If you're creating a new repository, you should just use the defaults here.
# If you're switching an existing repository over to 0repo, these settings
# allow you to keep your existing naming scheme.

# uri_rel_path is the part of the feed's URL following REPOSITORY_BASE_URL.
# Where should it be placed within "feeds"? By default, these are the same.
# You might want to change this if you have a strange naming scheme (e.g. feed
# URLs ending in "/" or without an extension). The result must end in '.xml'.
def get_feeds_rel_path(uri_rel_path):
	if uri_rel_path == 'python/python/upstream.xml':
		return 'python/python-upstream.xml'.replace('/', os.sep)
	assert not uri_rel_path.endswith('/'), uri_rel_path
	assert not uri_rel_path.endswith('.xml'), uri_rel_path
	return uri_rel_path.replace('/', os.sep) + '.xml'

# A source feed "feeds/games/my-game.xml" has a relative path of
# "games/my-game.xml". Where should the corresponding generated (signed) feed
# be placed under "public"? The default (and recommended) setting is to keep it
# the same, so we would generate "public/games/my-game.xml" in this case.
#
# When migrating an existing repository with a different scheme, you might need to
# change this function. For example, some repositories save the generated feed
# as "public/games/my-game/feed.xml" and configure Apache to make it appear as
# "http://example.com/games/my-game".
def get_public_rel_path(feeds_rel_path):
	if feeds_rel_path == 'python/python-upstream.xml':
		return 'python/python/upstream.xml'
	assert feeds_rel_path.endswith('.xml')
	return feeds_rel_path[:-4] + '/feed.xml'

# When 0install fetches a feed http://.../prog.xml, it looks for the GPG key
# at http://.../KEY.gpg.
#
# Normally, 0repo should place a symlink to the key in the same directory as
# the feed file (from get_public_rel_path); use "." for that.
#
# If you have one feed per directory (e.g. .../prog/feed.xml with some Apache
# configuration to make them appear as http://.../prog) then 0repo needs to
# place the key in the parent directory ("..") instead.
#
# Finally, if you use mod_rewrite so that all key requests are routed to the
# right place automatically by Apache, you can set this to None and avoid
# generating any symlinks.
GPG_PUBLIC_KEY_DIRECTORY = None

# This for archives uploaded and managed by 0repo itself.
def check_uploaded_archive(archive, url): pass

# As check_uploaded_archive, but for external archives.
def check_external_archive(archive, url): pass
