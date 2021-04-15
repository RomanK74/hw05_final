from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

GROUP_SLUG = 'test_group'
AUTHOR_USERNAME = 'test_user'
GROUP_2_SLUG = 'test_group_2'
# Persistent url
INDEX_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
# url dependent on constant test data
GROUP_2_URL = reverse(
    'group_posts', args=[GROUP_2_SLUG])
GROUP_URL = reverse(
    'group_posts', args=[GROUP_SLUG])
PROFILE_URL = reverse(
    'profile', args=[AUTHOR_USERNAME])


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='test_user',
            password='testpas'
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)

        cls.group = Group.objects.create(
            title='test_group',
            description='test_description',
            slug=GROUP_SLUG,
        )
        cls.group_2 = Group.objects.create(
            title='test_group_2',
            description='test_description_2',
            slug=GROUP_2_SLUG,
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
            image='smal.gif'
        )
        # url dependent on variables test data
        cls.POST_URL = reverse('post', args=[cls.author.username,
                                             cls.post.id])

    def test_pages_shows_correct_page_post_context_parts(self):
        """Проверка контекста "page", "post"."""
        items = [
            [INDEX_URL, 'page'],
            [GROUP_URL, 'page'],
            [PROFILE_URL, 'page'],
            [self.POST_URL, 'post']
        ]
        for url, item in items:

            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if item == 'page':
                    first_post = response.context['page'][0]
                    self.assertEqual(len(response.context['page']), 1)
                else:
                    first_post = response.context['post']
                self.assertEqual(first_post.text, self.post.text)
                self.assertEqual(first_post.author, self.post.author)
                self.assertEqual(first_post.group, self.post.group)
                self.assertEqual(first_post.image, self.post.image)

    def test_the_post_did_not_get_on_the_page_of_the_wrong_group(self):
        """Пост не попал на страницу не своей группы"""
        response = self.authorized_client.get(GROUP_2_URL)
        self.assertNotIn(self.post, response.context['page'])

    def test_pages_shows_correct_author_context_parts(self):
        """ Проверка контекста "author" """
        urls = [PROFILE_URL, self.POST_URL]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                context_part = response.context['author']
                self.assertEqual(context_part.username,
                                 self.post.author.username)
                self.assertEqual(str(context_part.get_full_name),
                                 str(self.post.author.get_full_name))

    def test_pages_shows_correct_group_context_parts(self):
        """ Проверка контекста "group" """
        response = self.guest_client.get(GROUP_URL)
        group = response.context['group']
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)

    def test_cache_index_page(self):
        first_response = self.authorized_client.get(INDEX_URL)
        Post.objects.create(
            text='text_Test_cache',
            author=self.author,
            group=self.group
        )
        second_response = self.authorized_client.get(INDEX_URL)
        cache.clear()
        third_response = self.authorized_client.get(INDEX_URL)
        self.assertEqual(first_response.content, second_response.content)
        self.assertNotEqual(second_response, third_response)
