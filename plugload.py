#Created by: Ali B Othman
#Version : 1.1.0

import sys, os
from importlib import machinery
import tokenize
import easylogging

PluginFolder = "plugins"
MainModule = "__init__"
Version = "1.1.0"

pl = {}
easylogging.logname('Ploader')

####################################### Functions from (imp) lib ####################################
PY_SOURCE = 1
PY_COMPILED = 2
C_EXTENSION = 3


def find_module(name, path=None):
    """**DEPRECATED**

    Search for a module.

    If path is omitted or None, search for a built-in, frozen or special
    module and continue search in sys.path. The module name cannot
    contain '.'; to search for a submodule of a package, pass the
    submodule name and the package's __path__.
	
	Note : This function from (imp) library

    """
    if not isinstance(name, str):
        raise TypeError("'name' must be a str, not {}".format(type(name)))
    elif not isinstance(path, (type(None), list)):
        # Backwards-compatibility
        raise RuntimeError("'path' must be None or a list, "
                           "not {}".format(type(path)))

    if path is None:
        if is_builtin(name):
            return None, None, ('', '', C_BUILTIN)
        elif is_frozen(name):
            return None, None, ('', '', PY_FROZEN)
        else:
            path = sys.path

    for entry in path:
        package_directory = os.path.join(entry, name)
        for suffix in ['.py', machinery.BYTECODE_SUFFIXES[0]]:
            package_file_name = '__init__' + suffix
            file_path = os.path.join(package_directory, package_file_name)
            if os.path.isfile(file_path):
                return None, package_directory, ('', '', PKG_DIRECTORY)
        for suffix, mode, type_ in get_suffixes():
            file_name = name + suffix
            file_path = os.path.join(entry, file_name)
            if os.path.isfile(file_path):
                break
        else:
            continue
        break  # Break out of outer loop when breaking out of inner loop.
    else:
        raise ImportError(_ERR_MSG.format(name), name=name)

    encoding = None
    if 'b' not in mode:
        with open(file_path, 'rb') as file:
            encoding = tokenize.detect_encoding(file.readline)[0]
    file = open(file_path, mode, encoding=encoding)
    return file, file_path, (suffix, mode, type_)

def get_suffixes():
    """**DEPRECATED**

	Note : This function from (imp) library

    """
    extensions = [(s, 'rb', C_EXTENSION) for s in machinery.EXTENSION_SUFFIXES]
    source = [(s, 'r', PY_SOURCE) for s in machinery.SOURCE_SUFFIXES]
    bytecode = [(s, 'rb', PY_COMPILED) for s in machinery.BYTECODE_SUFFIXES]

    return extensions + source + bytecode
####################################### End (imp) functions #########################################
def plugi(file, filename, details):

	suffix, mode, type_ = details
	libname = filename.split('\\')
	lib_name = libname[-2]
	pl[filename] = lib_name

def getPlugins():
    plugins = []
    if not PluginFolder in os.listdir() or not os.path.isdir(PluginFolder):
    	os.mkdir(PluginFolder)
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue

        info = find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    for i in plugins:
	    plugi(*i['info'])

def run():
	getPlugins()
	for i in pl:
		easylogging.info('Loading plugin : %s' % (pl[i]))
		try:
		    f = open(i, 'r')
		    exec(f.read())
		except :
			easylogging.error('Failed load plugin : %s' % (pl[i]))

		finally:
		    f.close()

if __name__ == '__main__':
    run()


