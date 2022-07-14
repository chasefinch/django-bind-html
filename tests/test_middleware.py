"""Test the Django Bind HTML package."""

# Third Party
from mock import MagicMock, Mock, patch

# Django Bind HTML
from django_bind_html.middleware import HTMLBindingMiddleware

TRIGGERING = "<!doctype html><html><head></head><body></body></html>".encode("utf-8")


class TestMiddleware:
    """Test the Django HTML Binding middleware."""

    def setup_method(self, method):
        """Set up a middleware with mock request values."""
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        self.request = request

        response = MagicMock()
        response.has_header = MagicMock(return_value=True)
        headers = {"Content-Type": "text/html", "Processing-Needed": "bind"}
        response.__getitem__.side_effect = headers.__getitem__
        self.response = response

        self.middleware = HTMLBindingMiddleware(self._get_response)

    def teardown_method(self, method):
        """Clean up."""
        del self.request
        del self.response
        del self.middleware

    @patch("django_bind_html.middleware.HTMLAttributeBinder")
    def test_triggering(self, mock_html_attribute_binder):
        """Test #1."""
        self._setup_binder(mock_html_attribute_binder)

        self.response.content = TRIGGERING

        self.middleware.process_response(self.request, self.response)

        assert mock_html_attribute_binder.called
        self.binder.apply.assert_called_once()

    def _setup_binder(self, mock_html_attribute_binder):
        self.binder = MagicMock()
        self.binder.apply = MagicMock(return_value="Yay! HTML!")
        mock_html_attribute_binder.return_value = self.binder

    def _get_response(self):
        pass
