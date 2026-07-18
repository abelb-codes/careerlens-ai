import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)
AI_SERVICE_TIMEOUT = getattr(settings, "AI_SERVICE_TIMEOUT", 120)


class AIServiceError(Exception):
    """Raised when the AI Engine returns an error or is unreachable."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AIServiceClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.AI_SERVICE_BASE_URL
        self.service_token = settings.AI_SERVICE_TOKEN

    def analyze_document(self, document_path: str, filename: str) -> dict:
        """Send document bytes, never Django's local filesystem path, to the AI service."""
        try:
            with open(document_path, "rb") as document:
                headers = {
                    "Content-Type": "application/octet-stream",
                    "X-Filename": filename,
                }
                if self.service_token:
                    headers["Authorization"] = f"Bearer {self.service_token}"
                request = Request(
                    f"{self.base_url}/analyze",
                    data=document.read(),
                    headers=headers,
                    method="POST",
                )
            with urlopen(request, timeout=AI_SERVICE_TIMEOUT) as response:  # nosec B310: configured internal service URL
                result = json.loads(response.read().decode("utf-8"))
            if not isinstance(result, dict):
                raise AIServiceError("AI Engine returned an invalid JSON response")
            return result
        except OSError as exc:
            msg = f"Unable to read resume {filename}: {exc}"
            logger.error(msg)
            raise AIServiceError(msg)
        except json.JSONDecodeError as exc:
            msg = f"AI Engine returned invalid JSON for {filename}: {exc}"
            logger.error(msg)
            raise AIServiceError(msg)
        except TimeoutError:
            msg = f"AI Engine timed out after {AI_SERVICE_TIMEOUT}s for {filename}"
            logger.error(msg)
            raise AIServiceError(msg)
        except HTTPError as exc:
            msg = f"AI Engine returned HTTP {exc.code} for {filename}"
            logger.error(msg)
            raise AIServiceError(msg, status_code=exc.code)
        except URLError as exc:
            msg = f"AI Engine is unreachable at {self.base_url}: {exc}"
            logger.error(msg)
            raise AIServiceError(msg)

    def health_check(self) -> bool:
        """Return True if the AI Engine is reachable and healthy."""
        try:
            request = Request(f"{self.base_url}/health")
            if self.service_token:
                request.add_header("Authorization", f"Bearer {self.service_token}")
            with urlopen(request, timeout=5) as response:  # nosec B310: configured internal service URL
                return response.status == 200
        except (HTTPError, URLError, TimeoutError):
            return False
