
from setuptools import setup, find_packages


setup(
    name = "django-socketio",
    version = __import__("django_socketio").__version__,
    author = "Stephen McDonald",
    author_email = "steve@jupo.org",
    description = ("A Django app providing the features required to use "
                   "websockets with Django via Socket.IO"),
    long_description = open("README.rst").read(),
    url = "http://github.com/stephenmcd/django-socketio",
    py_modules=["django_socketio",],
    install_requires=["gevent-socketio", "sphinx-me"],
    zip_safe = False,
    include_package_data = True,
    packages = find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ]
)
