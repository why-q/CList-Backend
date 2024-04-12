from app.utils.url_loader import URLLoader


class TestURLLoader:
    def test_get_title(self):
        url = "https://example.com"
        assert URLLoader(url).get_title() == "Example Domain"
