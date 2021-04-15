from django.test import Client, TestCase
from django.urls import reverse

ABOUT_URL = reverse('about:author')
TECH_URL = reverse('about:tech')


class PostURLTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls_status(self):
        """Тест кодов возврата."""
        items = [
            [ABOUT_URL, self.guest_client, 200],
            [TECH_URL, self.guest_client, 200],
        ]
        for url, client, status in items:
            with self.subTest():
                self.assertEqual(client.get(url).status_code, status)
