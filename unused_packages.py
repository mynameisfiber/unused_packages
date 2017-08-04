#!/usr/bin/env python3

from lib import dpkg
from lib.utils import picklecache

import os
from datetime import datetime
from operator import itemgetter

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, *args, **kwargs):
        return x


def package_recent_atime(package):
    return max(f.st_atime for f in package.values())


@picklecache("_dpkg_cache.pkl", name='package_info', default=dict)
def find_package_information(packages, package_info=None):
    for cached_package in package_info.keys():
        if cached_package not in packages:
            package_info.pop(cached_package)

    for package in tqdm(packages, "Enumerating Files"):
        if package in package_info:
            continue
        p = {}
        for package_file in dpkg.package_files(package):
            try:
                p[package_file] = os.stat(package_file)
            except FileNotFoundError:
                pass
            except PermissionError as e:
                print(("Permission Denied, try running as root "
                       "for more accurate results: {}").format(e))
        package_info[package] = p
    return package_info


if __name__ == "__main__":
    packages = set(dpkg.installed_packages())
    package_info = find_package_information(packages)

    packages_atime = [(p, package_recent_atime(v))
                      for p, v in package_info.items()]
    packages_atime.sort(key=itemgetter(1), reverse=True)
    now = datetime.now()
    for package, atime in packages_atime:
        dt = now - datetime.fromtimestamp(atime)
        print("{}, {}, {}".format(package, str(dt), package.desc))
