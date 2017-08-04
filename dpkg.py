import os
from shlex import quote
from collections import namedtuple

Package = namedtuple('Package', 'name version arch desc'.split())
Package.__str__ = lambda x: "{} [{}]".format(x.name, x.version)


def _run_command(cmd):
    stdout = os.popen(cmd, mode='r')
    return [line.strip() for line in stdout]


def installed_packages():
    output = _run_command('dpkg-query -l')
    for line in output:
        if line.startswith("ii"):
            fields = line.split(maxsplit=4)
            yield Package(*fields[1:])


def package_files(package):
    output = _run_command('dpkg-query -L "{}"'.format(quote(package.name)))
    for line in output:
        if line != '/.':
            yield line


if __name__ == "__main__":
    for package in installed_packages():
        print(package.name, package.version)
