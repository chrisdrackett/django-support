from distutils.core import setup, find_packages
 
setup(
    name='django-support',
    version='0.1',
    description='Support filters/tags/etc. for django.',
    author='Chris Drackett',
    author_email='chris@drackett.com',
    url = "https://github.com/chrisdrackett/django-support",
    packages=find_packages(),
    package_data = {
        'support': [
            'templates/support/*.html'
        ],
    },
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)