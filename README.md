scanpkg
=======

Windows alternative for dpkg-scanpackages (mainly created for cydia repos, but should work with other Debian repos)

Dependencies
============

```
click
patool
Git command line tools
```

Installation
============
`pip install scanpkg`

or

```
git clone https://github.com/mstg/scanpkg
cd scanpkg
python setup.py install
```

Usage
=====
```
Usage: scanpkg [OPTIONS]

  dpkg-scanpackages alternative for windows (mainly created for Cydia
  repos)

Options:
  -v INTEGER   Verbose scanpkg
  -dir TEXT    Directory to scan  [required]
  --help       Show this message and exit.
```
