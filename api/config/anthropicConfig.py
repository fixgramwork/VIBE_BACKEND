import os
from getpass import getpass

if "ANTHROPIC_API_KEY" not in os.environ:
  os.environ["ANTHROPIC_API_KEY"] = getpass()
