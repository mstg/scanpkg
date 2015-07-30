#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Mustafa
# @Date:   2015-07-09 23:52:55
# @Last Modified by:   Mustafa
# @Last Modified time: 2015-07-30 03:20:33

# Exceptions
class scanpkgControlException(Exception):
	pass

class scanpkgDirNotFound(Exception):
	pass

import click, os, shutil, patoolib, sys, subprocess
#sys.tracebacklimit = 0

TEMP_DIR = ".scanpkgtmp"

class scanpkg:
	class control:
		STRING = ""
		def __init__(self, control, deb, origdir):
			MD5sum = subprocess.Popen(["md5sum", deb], stdout=subprocess.PIPE).communicate()[0]
			MD5sum = MD5sum.split(" ", 1)[0]

			if (MD5sum[:1] == "\\"):
				MD5sum = MD5sum[1:]

			MD5sum = "MD5sum: {0}\n".format(MD5sum)

			SHA1 = subprocess.Popen([os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin/sha1sum.exe"), deb], stdout=subprocess.PIPE).communicate()[0]
			SHA1 = SHA1.split(" ", 1)[0]

			if (SHA1[:1] == "\\"):
				SHA1 = SHA1[1:]

			SHA1 = "SHA1: {0}\n".format(SHA1)

			SHA256 = subprocess.Popen([os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin/sha256sum.exe"), deb], stdout=subprocess.PIPE).communicate()[0]
			SHA256 = SHA256.split(" ", 1)[0]

			if (SHA256[:1] == "\\"):
				SHA256 = SHA256[1:]

			SHA256 = "SHA256: {0}\n".format(SHA256)

			Filename = "Filename: {0}/{1}\n".format(os.path.relpath(origdir, os.path.dirname(os.path.realpath(origdir))), os.path.basename(deb))
			Size = "Size: {0}".format(os.path.getsize(deb))

			self.STRING = "{0}{1}{2}{3}{4}{5}\n\n".format(control, MD5sum, SHA1, SHA256, Filename, Size)
			
	@click.command()
	@click.option('-v', default=0, help='Verbose scanpkg')
	@click.option('-dir', help='Directory to scan', required=True)
	@click.pass_context
	def scandebs(self, v, dir):
		"""dpkg-scanpackages alternative for windows (mainly created for Cydia repos)"""
		VERBOSITY = -1
		if v:
			VERBOSITY = 1

		if os.path.isdir(TEMP_DIR):
			shutil.rmtree(TEMP_DIR, ignore_errors=True)

		if os.path.exists("./Packages"):
			os.remove("./Packages")

		if os.path.exists("./Packages.gz"):
			os.remove("./Packages.gz")

		PACKAGE_STRING = ""

		for root, dirs, files in os.walk(dir):
			for file in files:
				if file.endswith(".deb"):
					TEMP_PACKAGE = os.path.join(root, file)
					TEMP_PACKAGE_DIR = os.path.join(TEMP_DIR, os.path.splitext(os.path.join(root, file))[0])
					TEMP_PACKAGE_CONTROL_TAR = os.path.join(TEMP_PACKAGE_DIR, "control.tar.gz")
					TEMP_PACKAGE_CONTROL_FILE = os.path.join(TEMP_PACKAGE_DIR, "control")
					TEMP_PACKAGE_DATA_TAR = os.path.join(TEMP_PACKAGE_DIR, "data.tar.gz")
					if not os.path.isdir(TEMP_PACKAGE_DIR):
						os.makedirs(TEMP_PACKAGE_DIR)


					if v:
						print "Extracted {0}".format(os.path.basename(TEMP_PACKAGE))

					shutil.copyfile(TEMP_PACKAGE, os.path.join(TEMP_PACKAGE_DIR, file))
					TEMP_PACKAGE = os.path.join(TEMP_PACKAGE_DIR, file)

					subprocess.call([os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin/ar.exe"), "-x", TEMP_PACKAGE])

					shutil.move("./control.tar.gz", TEMP_PACKAGE_CONTROL_TAR)
					os.remove("./data.tar.gz")
					os.remove("./debian-binary")

					if not os.path.exists(TEMP_PACKAGE_CONTROL_TAR):
						raise scanpkgControlException("No control file found in {0}".format(TEMP_PACKAGE))
					else:
						patoolib.extract_archive(TEMP_PACKAGE_CONTROL_TAR, outdir=TEMP_PACKAGE_DIR, verbosity=VERBOSITY)
						CONTROL_FILE = open(TEMP_PACKAGE_CONTROL_FILE).read()
						CONTROL_MODIFIED = scanpkg.control(CONTROL_FILE, TEMP_PACKAGE, dir).STRING

						PACKAGE_STRING += CONTROL_MODIFIED

						print "Added file {0}".format(os.path.basename(TEMP_PACKAGE))

		shutil.rmtree(TEMP_DIR, ignore_errors=True)
		with open("./Packages", "w+") as f:
			f.write(PACKAGE_STRING)

		subprocess.call(["gzip", "./Packages"])



def main():
	scanpkg().scandebs()

if __name__ == "__main__":
	main()