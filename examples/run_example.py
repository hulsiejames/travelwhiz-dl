"""
Running an example
==================

This script runs when the Sphinx example gallery is built.
Its output appears alongside the source code in the documentation.
"""

import logging

LOG = logging.getLogger(__name__)

# %%
# Use comments between cells to explain each step.
LOG.info("This example executes during the documentation build.")
