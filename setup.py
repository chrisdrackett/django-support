from setuptools import setup, find_packages
 
setup(
    name='django-support',
    version='0.2',
    description='Support filters/tags/etc. for django.',
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    author='Chris Drackett',
    author_email='chris@drackett.com',
    url = "https://github.com/chrisdrackett/django-support",
    license='BSD',
    packages=find_packages(),
    package_data = {
        'support': [
            'templates/support/*.html'
        ],
    },
    include_package_data=True
)