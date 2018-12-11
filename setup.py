import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
# get version information
exec(open('openrem/remapp/version.py').read())

requires = [
    'django>=1.8,<1.9',
    'django-filter >= 0.10,<0.15',
    'pytz >= 0a',
    'humanize',
    'pydicom == 0.9.9',
    'django-pagination',
    'xlsxwriter',
    'celery >= 3.1',
    'argparse >= 1.2.1',
    'django-qsstats-magic',
    'python-dateutil',
    'django-solo',
    'django-crispy-forms',
    'pandas',
    'xlrd',
    'testfixtures >= 6.0',
    'mock',
    'django-debug-toolbar <= 1.9.1',
    'django-js-reverse',
    'requests'
    ]

setup(
    name='OpenREM',
    version=__version__,
    packages=['openrem'],
    include_package_data=True,
    install_requires = requires,
    scripts=[
        'openrem/scripts/openrem_rdsr.py',
        'openrem/scripts/openrem_mg.py',
        'openrem/scripts/openrem_dx.py',
        'openrem/scripts/openrem_ctphilips.py',
        'openrem/scripts/openrem_cttoshiba.py',
        'openrem/scripts/openrem_ptsizecsv.py',
        'openrem/scripts/openrem_store.py',
        'openrem/scripts/openrem_qr.py',
    ],
    license='GPLv3 with additional permissions',
    # description='Radiation Exposure Monitoring for physicists',
    description='Developer beta only',
    long_description=README,
    url='https://openrem.org/',
    author='Ed McDonagh',
    author_email='ed@openrem.org',
    long_description_content_type="text/x-rst",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Physics',
        ],
)
