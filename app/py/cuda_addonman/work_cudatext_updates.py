import sys
import os
import re
import platform
import tempfile
import webbrowser
import cudatext as app
from .work_remote import *

p = sys.platform
X64 = platform.architecture()[0]=='64bit'
##p = 'win32'
##X64 = False

DOWNLOAD_PAGE = \
    'https://sourceforge.net/projects/cudatext/files/release/Linux/' if p.startswith('linux')\
    else 'https://sourceforge.net/projects/cudatext/files/release/Windows/' if p.startswith('win')\
    else 'https://sourceforge.net/projects/cudatext/files/release/macOS/' if p=='darwin'\
    else 'https://sourceforge.net/projects/cudatext/files/release/FreeBSD/' if p.startswith('freebsd')\
    else '?'

if p=='darwin':
    TEXT_CPU = ''
else:
    TEXT_CPU = '64' if X64 else '(386|32)'

DOWNLOAD_REGEX = \
    ' href="(\w+://[\w\.]+/projects/cudatext/files/release/\w+/cudatext-[\w\-]+?'+TEXT_CPU+'[\w\-]*?-([\d\.]+?)\.(zip|dmg|tar\.xz)/download)"'



def versions_ordered(s1, s2):
    """
    compare "1.10.0" and "1.9.0" correctly
    """
    n1 = list(map(int, s1.split('.')))
    n2 = list(map(int, s2.split('.')))
    return n1<=n2


def check_cudatext():

    fn = os.path.join(tempfile.gettempdir(), 'cudatext_download.html')
    app.msg_status('Downloading: '+DOWNLOAD_PAGE, True)
    get_url(DOWNLOAD_PAGE, fn, True)
    app.msg_status('')

    if not os.path.isfile(fn):
        app.msg_status('Cannot download: '+DOWNLOAD_PAGE)
        return

    text = open(fn, encoding='utf8').read()
    items = re.findall(DOWNLOAD_REGEX, text)
    if not items:
        app.msg_status('Cannot find download links')
        return

    items = sorted(items, key=lambda i:i[1], reverse=True)
    print('Found links:')
    for i in items:
        print('  '+i[0])

    url = items[0][0]
    ver_inet = items[0][1]
    ver_local = app.app_exe_version()

    if versions_ordered(ver_inet, ver_local):
        app.msg_box('Latest CudaText is already here.\nHere: %s\nInternet: %s'
                   %(ver_local, ver_inet), app.MB_OK+app.MB_ICONINFO)
        return

    if app.msg_box('Newer CudaText is available.\nHere: %s\nInternet: %s\n\nOpen download URL in browser?'
                  %(ver_local, ver_inet), app.MB_YESNO+app.MB_ICONINFO) == app.ID_YES:
        webbrowser.open_new_tab(url)
        print('Opened download URL')
