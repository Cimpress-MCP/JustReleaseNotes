import os
from setuptools import setup

description = "Release notes generator package"
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.rst')).read()
except:
    long_description = description

setup(name='JustReleaseNotes',
      version='0.1.8',
      description='Release notes generator package',
      long_description=long_description,
      url='https://github.com/Cimpress-MCP/JustReleaseNotes',
      author='Ivan Stanishev, Rafal Nowosielski',
      author_email='ivan@stanishev.info, rafal@nowosielski.link',
      license='Apache License 2.0',
      packages=['JustReleaseNotes', 'JustReleaseNotes.artifacters', 'JustReleaseNotes.issuers',
                'JustReleaseNotes.artifacters.versioners','JustReleaseNotes.writers', 'JustReleaseNotes.sourcers',
                'JustReleaseNotes.utils'],
      install_requires=[
          'requests',
          'gitpython'
      ],
      zip_safe=False,
      entry_points="""
      [console_scripts]
      just_release = JustReleaseNotes.command_line:main
      """
)
