#!/usr/bin/env python
from distutils.core import setup

setup(
        name='samklang-media',
        version="0.1.1",
        author='Sigurd Gartmann',
        author_email='sigurdga-samklang@sigurdga.no',
        url='http://github.com/sigurdga/samklang-media',
        description='Uploading and file storage for samklang',
        long_description=open('README.txt').read(),
        license="AGPL",
        packages = ['samklang_media', 'samklang_media.templatetags', 'samklang_media.migrations'],
        package_data = {'samklang_media': ['templates/samklang_media/*.html', 'locale/*/LC_MESSAGES/django.*o', 'static/js/*.js']},
        classifiers=[
                "Development Status :: 3 - Alpha",
                "License :: OSI Approved :: GNU Affero General Public License v3",
                "Intended Audience :: Developers",
                "Framework :: Django",
                "Environment :: Web Environment",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                ]
        )
