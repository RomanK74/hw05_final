from django.test import Client, TestCase
from django.urls import reverse

from posts.constans import POSTS_ON_PAGE
from posts.models import Post, User, Group

# Persistent url
INDEX_URL = reverse('index')

GROUP_SLUG = 'test_group'
AUTHOR_USERNAME = 'test_user'
# url dependent on constant test data
GROUP_URL = reverse(
    'group_posts', args=[GROUP_SLUG])
PROFILE_URL = reverse(
    'profile', args=[AUTHOR_USERNAME])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR_USERNAME)
        cls.group = Group.objects.create(
            title='test_group',
            description='test_description',
            slug=GROUP_SLUG,
        )
        for _ in range(POSTS_ON_PAGE + 3):
            Post.objects.create(
                text='Тестовый текст',
                author=cls.author,
                group=cls.group
            )
        cls.guest_client = Client()

    def test_first_page(self):
        """Тест отображения первой страницы"""
        urls = [INDEX_URL, GROUP_URL, PROFILE_URL]
        for url in urls:
            response = self.guest_client.get(url)
        self.assertEqual(len(
            response.context['page']),
            POSTS_ON_PAGE
        )

    def test_second_page(self):
        """Тест отображения второй страницы"""
        urls = [INDEX_URL, GROUP_URL, PROFILE_URL]
        for url in urls:
            response = self.guest_client.get(url)
            response = self.client.get(url + '?page=2')
            self.assertEqual(len(response.context['page']), 3)
