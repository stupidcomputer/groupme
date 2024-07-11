from distutils.core import setup

setup(
    name="groupme_sync",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'groupme_sync = groupme_sync:main',
        ]
    }
)