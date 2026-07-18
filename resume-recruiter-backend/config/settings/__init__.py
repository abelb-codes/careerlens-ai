"""Select Django settings from the deployment environment.

Development remains the safe default for local commands.  Production process
managers must set ``DJANGO_ENV=production``; this lets WSGI, ASGI, Django and
Celery use the same unambiguous settings selection.
"""

import os


if os.getenv("DJANGO_ENV", "development").lower() == "production":
    from .production import *  # noqa: F403
else:
    from .development import *  # noqa: F403
