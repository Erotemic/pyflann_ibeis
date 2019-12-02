#!/usr/bin/env python
"""
Create a base docker image for building pyflann_ibeis
"""
from __future__ import absolute_import, division, print_function
import os
from os.path import join
import ubelt as ub


def main():
    ROOT = join(os.getcwd())
    # ROOT = '.'
    os.chdir(ROOT)

    NAME = 'pyhesaff'
    VERSION = '0.1.0'
    DOCKER_TAG = '{}-{}'.format(NAME, VERSION )

    QUAY_REPO = 'quay.io/erotemic/manylinux-for'
    DOCKER_URI = '{QUAY_REPO}:{DOCKER_TAG}'.format(**locals())

    dockerfile_fpath = join(ROOT, 'Dockerfile')
    # This docker code is very specific for building linux binaries.
    # We will need to do a bit of refactoring to handle OSX and windows.
    # But the goal is to get at least one OS working end-to-end.

    """
    Notes:
        docker run --rm -it quay.io/pypa/manylinux2010_x86_64 /bin/bash
    """
    docker_code = ub.codeblock(
        '''
        FROM quay.io/pypa/manylinux2010_x86_64
        # FROM quay.io/skvark/manylinux1_x86_64

        RUN yum install lz4-devel -y

        RUN MB_PYTHON_TAG=cp27-cp27m  && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m pip install setuptools pip virtualenv -U && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m virtualenv ./venv-$MB_PYTHON_TAG && \
            source ./venv-$MB_PYTHON_TAG/bin/activate && \
            pip install scikit-build cmake ninja

        RUN MB_PYTHON_TAG=cp27-cp27mu  && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m pip install setuptools pip virtualenv -U && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m virtualenv ./venv-$MB_PYTHON_TAG && \
            source ./venv-$MB_PYTHON_TAG/bin/activate && \
            pip install scikit-build cmake ninja

        RUN MB_PYTHON_TAG=cp35-cp35m  && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m pip install setuptools pip virtualenv -U && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m virtualenv ./venv-$MB_PYTHON_TAG && \
            source ./venv-$MB_PYTHON_TAG/bin/activate && \
            pip install scikit-build cmake ninja

        RUN MB_PYTHON_TAG=cp36-cp36m  && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m pip install setuptools pip virtualenv -U && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m virtualenv ./venv-$MB_PYTHON_TAG && \
            source ./venv-$MB_PYTHON_TAG/bin/activate && \
            pip install scikit-build cmake ninja

        RUN MB_PYTHON_TAG=cp37-cp37m  && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m pip install setuptools pip virtualenv -U && \
            /opt/python/$MB_PYTHON_TAG/bin/python -m virtualenv ./venv-$MB_PYTHON_TAG && \
            source ./venv-$MB_PYTHON_TAG/bin/activate && \
            pip install scikit-build cmake ninja
        ''')

    try:
        print(ub.color_text('\n--- DOCKER CODE ---', 'white'))
        print(ub.highlight_code(docker_code, 'docker'))
        print(ub.color_text('--- END DOCKER CODE ---\n', 'white'))
    except Exception:
        pass
    with open(dockerfile_fpath, 'w') as file:
        file.write(docker_code)

    docker_build_cli = ' '.join([
        'docker', 'build',
        # '--build-arg PY_VER={}'.format(PY_VER),
        '--tag {}'.format(DOCKER_TAG),
        '-f {}'.format(dockerfile_fpath),
        '.'
    ])
    print('docker_build_cli = {!r}'.format(docker_build_cli))
    info = ub.cmd(docker_build_cli, verbose=3, shell=True)

    if info['ret'] != 0:
        print(ub.color_text('\n--- FAILURE ---', 'red'))
        print('Failed command:')
        print(info['command'])
        print(info['err'])
        print('NOTE: sometimes reruning the command manually works')
        raise Exception('Building docker failed with exit code {}'.format(info['ret']))
    else:
        print(ub.color_text('\n--- SUCCESS ---', 'green'))

    print(ub.highlight_code(ub.codeblock(
        r'''
        # Finished creating the docker image.
        # To test / export / publish you can do something like this:


        # Test that we can get a bash terminal
        docker run -v -it {DOCKER_TAG} bash

        docker save -o ${ROOT}/{DOCKER_TAG}.docker.tar {DOCKER_TAG}

        # To publish to quay

        source $(secret_loader.sh)
        echo "QUAY_USERNAME = $QUAY_USERNAME"
        docker login -u $QUAY_USERNAME -p $QUAY_PASSWORD quay.io


        docker tag {DOCKER_TAG} {DOCKER_URI}
        docker push {DOCKER_URI}

        ''').format(NAME=NAME, ROOT=ROOT, DOCKER_TAG=DOCKER_TAG,
                    DOCKER_URI=DOCKER_URI), 'bash'))

    print('DOCKER_TAG = {!r}'.format(DOCKER_TAG))
    print('dockerfile_fpath = {!r}'.format(dockerfile_fpath))

    # push_cmd = 'docker push quay.io/erotemic/manylinux-opencv:manylinux1_x86_64-opencv4.1.0-py3.6'
    # print('push_cmd = {!r}'.format(push_cmd))
    # print(push_cmd)

    PUBLISH = 0
    if PUBLISH:
        cmd1 = 'docker tag {DOCKER_TAG} {DOCKER_URI}'.format(**locals())
        cmd2 = 'docker push {DOCKER_URI}'.format(**locals())
        print('-- <push cmds> ---')
        print(cmd1)
        print(cmd2)
        print('-- </push cmds> ---')


if __name__ == '__main__':
    """
    CommandLine:
        python ~/code/flann/dev/docker/make_base_image.py
    """
    main()
