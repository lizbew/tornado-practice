from __future__ import print_function
import os.path
import shlex, subprocess

BASE_PATH = 
r'D:\Tools\adt-bundle-windows-x86_64-20131030\sdk\platform-tools'


def get_apk_path(pkg):
    cmd_line = 'adb shell pm path {0}'.format(pkg)
    args = shlex.split(cmd_line)
    ret = subprocess.check_output(args)
    if len(ret) > 0:
        return ret.split(':')[1].strip()
    else:
        print('Not found package {0}'.format(pkg))
        return None
def pull_apk_file(apk_path):
    print('getting apk %s'%(os.path.basename(apk_path),))
    args = shlex.split('adb pull "{0}" "{1}"'.format(apk_path, 
os.path.join(BASE_PATH, os.path.basename(apk_path))))
    subprocess.check_call(args)
    
def uninstall_apk(pkg):
    cmd_line = 'adb shell pm uninstall {0}'.format(pkg)
    args = shlex.split(cmd_line)
    print(args)
    subprocess.check_call(args)

def get_uns_apk():
    lines = open(os.path.join(BASE_PATH, 'apks.txt')).readlines()
    for apk in lines:
        if len(apk) > 0:
            apk_path = get_apk_path(apk)
            if apk_path:
                pull_apk_file(apk_path)
                uninstall_apk(apk)

if __name__ == '__main__':
    get_uns_apk()

