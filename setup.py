from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
	user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

	def initialize_options(self):
		TestCommand.initialize_options(self)
		self.pytest_args = list()

	def finalize_options(self):
		TestCommand.finalize_options(self)
		self.test_args = list()
		self.test_suite = True

	def run_tests(self):
		import pytest
		import sys
		errno = pytest.main(self.pytest_args)
		sys.exit(errno)

setup(
		name = 'solarcity_mqtt',
		version = '0.1',
		description = 'Python library for eavesdropping Solar City gateway data and send it to a mqtt server',
		long_description = 'Python library for eavesdropping Solar City gateway data and send it to a mqtt server',
		maintainer = 'Kevin Rauwolf',
		url = 'https://github.com/squidpickles/solarcity_mqtt',
		license = 'BSD License',
		packages = ['solarcity_mqtt', ],
		install_requires = ['configparser', 'paho-mqtt', 'watchdog'],
		tests_require = ['pytest', ],
		keywords = ['SolarCity', ],
		cmdclass = {'test': PyTest, },
		classifiers = [
			'Development Status :: 3 - Alpha',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: BSD License',
			'Natural Language :: English',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Topic :: Home Automation',
			'Topic :: Software Development :: Libraries',
		],
)
