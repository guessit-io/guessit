"""Custom Hatchling metadata hook.

Builds the PyPI long description (``readme``) by concatenating ``README.md``
and ``CHANGELOG.md``, reproducing the behaviour of the former ``setup.py``.
"""
import os

from hatchling.metadata.plugin.interface import MetadataHookInterface


class CustomMetadataHook(MetadataHookInterface):
    """Assemble the long description from README.md + CHANGELOG.md."""

    def update(self, metadata):
        with open(os.path.join(self.root, 'README.md'), encoding='utf-8') as readme_file:
            readme = readme_file.read()
        with open(os.path.join(self.root, 'CHANGELOG.md'), encoding='utf-8') as changelog_file:
            changelog = changelog_file.read()

        metadata['readme'] = {
            'content-type': 'text/markdown',
            'text': readme + '\n\n' + changelog,
        }
