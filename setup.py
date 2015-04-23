from setuptools import setup

setup(name='GitReleaseNotes',
      version='0.1',
      description='Release notes generator tool',
      url='https://github.com/Cimpress-MCP/GitReleaseNotes',
      author='Ivan Stanishev, Rafal Nowosielski',
      author_email='ivan@stanishev.net',
      license='Apache 2.0',
      packages=['GitReleaseNotes'],
      install_requires=[
          'requests',
		  'gitpython'
      ],
      zip_safe=False)