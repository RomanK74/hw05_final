from django.test import TestCase
from django.urls import reverse

# Persistent url
ABOUT_URL = reverse('about:author')
TECH_URL = reverse('about:tech')


class PostURLTest(TestCase):

    def test_routes(self):
        """ Тест расчёта URL """
        url_routes = {
            '/about/author/': ABOUT_URL,
            '/about/tech/': TECH_URL,
        }
        for url, reverse_name in url_routes.items():
            self.assertEqual(url, reverse_name)
