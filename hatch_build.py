"""Custom Hatchling metadata hook.

Builds the PyPI long description (``readme``) by concatenating ``README.md``
and ``CHANGELOG.md``, reproducing the behaviour of the former ``setup.py``.
"""

import os

from hatchling.metadata.plugin.interface import MetadataHookInterface


def _balance_code_fences(text: str) -> str:
    """Make Markdown code fences safe to embed in the PyPI long description.

    Auto-generated changelog entries can carry a closing fence with trailing
    text on the same line, e.g.::

        ``` ([`abc`](https://.../abc))

    CommonMark does not treat such a line as a closing fence (a closing fence
    may only be followed by whitespace), so the code block is never terminated
    and swallows the rest of the document into a single ``<pre>`` block on PyPI.

    Normalise every closing fence onto its own line (moving any trailing text to
    the next line) and close a fence left open at end of input, so the assembled
    description always has balanced fences.
    """
    lines = text.split("\n")
    out: list[str] = []
    open_fence: str | None = None
    for line in lines:
        stripped = line.lstrip()
        if not stripped.startswith("```"):
            out.append(line)
            continue
        backticks = len(stripped) - len(stripped.lstrip("`"))
        marker = "`" * backticks
        rest = stripped[backticks:].strip()
        if open_fence is None:
            # Opening fence: an info string (e.g. ```python) is valid, keep it.
            open_fence = marker
            out.append(line)
        else:
            # Inside a block: this closes it. A closing fence cannot carry an
            # info string, so emit the fence alone and push any trailing text
            # (typically the commit link) onto its own line.
            out.append(marker)
            if rest:
                out.append(rest)
            open_fence = None
    if open_fence is not None:
        out.append(open_fence)
    return "\n".join(out)


class CustomMetadataHook(MetadataHookInterface):
    """Assemble the long description from README.md + CHANGELOG.md."""

    def update(self, metadata):
        with open(os.path.join(self.root, "README.md"), encoding="utf-8") as readme_file:
            readme = readme_file.read()
        with open(os.path.join(self.root, "CHANGELOG.md"), encoding="utf-8") as changelog_file:
            changelog = changelog_file.read()

        metadata["readme"] = {
            "content-type": "text/markdown",
            "text": readme + "\n\n" + _balance_code_fences(changelog),
        }
