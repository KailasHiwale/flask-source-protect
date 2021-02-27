#!/bin/python3

'''
:created on: Feb 25th, 2021
:author: kailas_hiwale
:summery: This is a setup file for cythonization of python source code in
    order to protect source by compiling it to native shared object files (.so)
    and to take advantage of improved execution speed after binary conversion.
:steps:
    1. Takes source path and reindent source code in case of mix indentation.
    2. Collect extentions, compiles and generates build and distribution files.
    3. Remove unwanted extentions. i.e removes .py, .o & .c files from dist.
'''
import os
import subprocess
from setuptools import setup, find_packages
from Cython.Build import cythonize

EXCLUDE = {
	'exclude_files': [
		'src/test.py',
	],
	'exclude_dir': [
		'src/static',
		'src/pkg2',
	],
}

PATHS = {
	'src_path': 'src',
	'build': 'build',
	'dist': 'dist',
}


def reindent(path):
    '''
    Function performs reindentation on source code.

    :param str path: source code path
    :return: boolean value 1 on sucess & 0 on failure
    :rtype: boolean
    '''
    try:
        # subprocess.call(['reindent', '-r', '-n', 'src'])
        os.popen('reindent -r -n {}'.format(path))
        return 1
    except Exception as e:
        print(e)
        return 0


def lst_ext_paths(root_dir, exclude):
    '''
    Function lists files and dir for compilation.

    :param str root_dir: source directory path
    :param dict exclude: dictionry consist of files and dirs to be 
        excluded from compilation.
    :return: list with extentions.
    :rtype: list
    '''
    ext_paths = []
    for root, dirs, files in os.walk(root_dir):
        if root in exclude['exclude_dir']:
            continue
        for filename in files:
            if os.path.splitext(filename)[1] != '.py':
                continue
            file_path = os.path.join(root, filename)
            if file_path in exclude['exclude_files']:
                continue
            ext_paths.append(file_path)

    return ext_paths


def rm_ext(paths):
    '''
    Function removes unwanted extentions. i.e removes .py, .o & .c files
    from dist.

    :param dict paths: dictionary with source and distribution paths
    :return: boolean value 1 on sucess & 0 on failure
    :rtype: boolean
    '''
    try:
        src = paths['src_path'] 
        os.popen('find {}/ -name \'*.c\' -type f -delete'.format(src))
        os.popen('find {}/ -name \'*.so\' -type f -delete'.format(src))

        build = paths['build']
        if os.path.isdir(build):
            os.popen('find {}/ -name \'*.c\' -type f -delete'.format(build))
            os.popen('find {}/ -name \'*.py\' -not -name \'run.py\' -not -name \'__init__.py\' -type f -delete'.format(build))

        dist = paths['dist']
        if os.path.isdir(dist):
            spath = os.path.join(dist, os.listdir('dist')[0])
            dpath = os.path.join(dist, src)
            unzip = ['unzip', '-o', spath, '-d', dpath]
            subprocess.call(unzip)
            os.popen('find {}/ -name \'*.c\' -type f -delete'.format(dist))
            os.popen('find {}/ -name \'*.py\' -not -name \'run.py\' -not -name \'__init__.py\' -type f -delete'.format(dist))
        
        return 1
    except Exception as e:
        print(e)
        return 0


if __name__ == '__main__':
    #1 reindention of source code
    if reindent(PATHS['src_path']):
        print('Source reindentation done!!')
    #2 setup, compilation and packaging of the source code
    setup(
        metadata_version='0.1',
        name=PATHS['src_path'],
        version='0.1.1',
        summary='source protection with cython',
        author='Kailas Hiwale',
        author_email='hiwale.kb@gmail.com',
        license='UNKNOWN',
        platform='UNKNOWN',
        packages=find_packages(),
        ext_modules=cythonize(
            lst_ext_paths(PATHS['src_path'], EXCLUDE),
            compiler_directives={'always_allow_keywords': True, 'language_level': 3}
        ),
    )
    print('Source compilation and packaging done!!')
    #3 remove extra files
    if rm_ext(PATHS):
        print('Extra extentions removal done!!')