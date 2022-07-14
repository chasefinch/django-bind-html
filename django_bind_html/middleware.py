"""Define middleware for applying Bind HTML to the output of Django views."""

# Third Party
from bind_html import HTMLAttributeBinder

# Django
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import DjangoUnicodeDecodeError


class HTMLBindingMiddleware(MiddlewareMixin):
    """Apply Bind HTML to the output of Django views."""

    def process_response(self, request, response):
        """Process the response after the view has rendered it."""
        if not response.has_header("Content-Type") or "text/html" not in response["Content-Type"]:
            return response

        try:
            response_content = response.content.decode("utf-8").strip()
        except (DjangoUnicodeDecodeError, UnicodeDecodeError):
            return response

        # Sniff for whether this response is a bound HTML view
        if response.get("Processing-Needed") != "bind":
            return response

        del response["Processing-Needed"]

        parser = HTMLAttributeBinder()
        response_content = parser.apply(response_content)

        response.content = response_content
        response["Content-Length"] = len(response.content)

        return response
