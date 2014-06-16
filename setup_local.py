import importlib
import os, os.path
import traceback
import sys

def print_usage():
    print """
    Usage:
        python setup_local.py
        python setup_local.py clean

    Note: This script will attempt to set up Selenium and BeautifulSoup in the local directory of a linux device.
          Any step that fails can be performed manually with a little googling.
    """


def setup_module(name, url):
    installed = False
    try:
        importlib.import_module(name)
        installed = True
    except Exception as ex:
        pass
    if not installed:
        tar_file = name+".tar.gz"
        unpack_head = name+"_untar"
        try:
            if not os.path.isfile(tar_file):
                print "Downloading %s..."%name
                os.system("wget -q -O %s %s"%(tar_file, url))
            if not os.path.isdir(unpack_head):
                print "Unpacking %s..."%name
                os.mkdir(unpack_head)
                os.system("tar -zxvf %s -C %s"%(tar_file, unpack_head))
            unpacked = os.listdir(unpack_head)[0]
            unpack_path = os.path.join(unpack_head, unpacked)
            build_path = os.path.join(unpack_path,"build")
            if not os.path.isdir(build_path):
                print "Building %s..."%name
                os.chdir(unpack_path)
                os.system("python setup.py build")
                os.chdir("../..")
            if not os.path.isdir(name):
                print "Making local path..."
                build = os.listdir(build_path)[0]
                build = os.path.join(build_path, build)
                build = os.path.join(build, name)
                if os.path.isdir(build):
                    os.system("mv "+build+" "+name)
                elif os.path.isfile(build+".py"):
                    os.system("mv "+build+".py "+name+".py")
                else:
                    raise("Invalid build!")
            try:
                importlib.import_module(name)
                installed = True
            except Exception as ex:
                pass
        except Exception as ex:
            print "!!! Error in install file. !!!"
            traceback.print_exc()

        if installed:
            print "Cleaning up %s local install."%name
            os.system("rm "+tar_file)
            os.system("rm -r "+unpack_head)
        else:
            print "!!! %s NOT successfully installed! !!!"%name
            return False
    if installed:
        print "%s Installed."%name
        return True

def setup_beautifulsoup():
    name = "BeautifulSoup"
    url = "https://pypi.python.org/packages/source/B/BeautifulSoup/BeautifulSoup-3.2.1.tar.gz"
    return setup_module(name, url)

def setup_selenium():
    name = "selenium"
    url = "https://pypi.python.org/packages/source/s/selenium/selenium-2.42.1.tar.gz"
    return setup_module(name, url)

def clean():
    os.system("rm BeautifulSoup.*")
    os.system("rm -r selenium")

if __name__=="__main__":
    if len(sys.argv)==2:
        if sys.argv[1]!="clean":
            print_usage()
            exit()
        clean()
    elif len(sys.argv)!=1:
        print_usage()
    else:
        if not setup_beautifulsoup():
            exit()
        setup_selenium()
