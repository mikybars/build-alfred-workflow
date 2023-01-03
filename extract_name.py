#!/usr/bin/env python

import os
import plistlib
import re
import string
import sys
from unicodedata import normalize


# Characters permitted in workflow filenames
OK_CHARS = set(string.ascii_letters + string.digits + '-.')


def safename(name):
    """Make name filesystem and web-safe."""
    if isinstance(name, str):
        name = unicode(name, 'utf-8')

    # remove non-ASCII
    normalized = normalize('NFD', name).encode('us-ascii', errors='ignore')
    clean = [c if c in OK_CHARS else '-' for c in normalized]

    return re.sub(r'-+', '-', ''.join(clean)).strip('-')


def main():
    if len(sys.argv) < 2:
        print('Please provide a info.plist')
        sys.exit(1)

    info_plist = sys.argv[1]

    if not os.path.exists(info_plist):
        print('info.plist not found')
        sys.exit(2)

    info = plistlib.readPlist(info_plist)

    if 'name' not in info:
        print('Name key not found')
        sys.exit(3)

    workflow_file = safename(info['name'])

    custom_version = os.environ.get("CUSTOM_VERSION")
    if custom_version:
        info['version'] = custom_version
        plistlib.writePlist(info, info_plist)

    if 'version' in info:
        workflow_file += '-{}'.format(safename(info['version']))
    workflow_file += '.alfredworkflow'

    print(workflow_file)


if __name__ == '__main__':
    main()
