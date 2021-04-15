from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

GROUP_SLUG = 'test_group'
AUTHOR_USERNAME = 'test_user'
# Persistent url
INDEX_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
ABOUT_URL = reverse('about:author')
TECH_URL = reverse('about:tech')
FOLLOW_URL = reverse('follow_index')
# url dependent on constant test data
GROUP_URL = reverse(
    'group_posts', args=[GROUP_SLUG])
PROFILE_URL = reverse(
    'profile', args=[AUTHOR_USERNAME])


class PostURLTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username=AUTHOR_USERNAME, password='testpas'
        )
        cls.group = Group.objects.create(
            title='test_group',
            description='test_description',
            slug=GROUP_SLUG,
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.guest_client = Client()
        cls.author_2 = User.objects.create_user(
            username='test_user_2', password='testpas')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group)
        cls.post_2 = Post.objects.create(
            text='Тестовый текст',
            author=cls.author_2,
            group=cls.group)

        # url dependent on variables
        cls.POST_URL = reverse('post', args=[cls.author.username,
                                             cls.post.id])
        cls.POST_EDIT_URL = reverse('post_edit',
                                    args=[cls.author.username,
                                          cls.post.id])
        # URL for redirection tests
        cls.POST_2_URL = reverse('post', args=[cls.author_2.username,
                                               cls.post_2.id])
        cls.POST_2_EDIT = reverse('post_edit',
                                  args=[cls.author_2.username,
                                        cls.post_2.id])
        cls.COMMENT_URL = reverse('add_comment',
                                  args=[cls.author.username,
                                        cls.post.id])
        # url redirects
        cls.REDIRECT_URL = reverse('login') + '?next='

    def test_urls_status(self):
        """Тест кодов возврата."""
        items = [
            [INDEX_URL, self.guest_client, 200],
            [TECH_URL, self.guest_client, 200],
            [NEW_POST_URL, self.authorized_client, 200],
            [PROFILE_URL, self.guest_client, 200],
            [self.POST_URL, self.guest_client, 200],
            [self.POST_EDIT_URL, self.authorized_client, 200],
            [self.POST_EDIT_URL, self.guest_client, 302],
            [NEW_POST_URL, self.guest_client, 302],
            [self.POST_2_EDIT, self.authorized_client, 302],
            [self.COMMENT_URL, self.guest_client, 302],
            [FOLLOW_URL, self.guest_client, 302]
        ]
        for url, client, status in items:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, status)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            INDEX_URL: 'index.html',
            NEW_POST_URL: 'new.html',
            GROUP_URL: 'group.html',
            self.POST_URL: 'post.html',
            PROFILE_URL: 'profile.html',
            self.POST_EDIT_URL: 'new.html',
            FOLLOW_URL: 'follow/follow.html'
        }
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                self.assertTemplateUsed(self.authorized_client.get(url),
                                        template)

    def test_post_edit_redirect(self):
        """Тест перенаправления."""
        items = [
            [self.POST_EDIT_URL, self.guest_client,
             self.REDIRECT_URL + self.POST_EDIT_URL],
            [NEW_POST_URL, self.guest_client,
             self.REDIRECT_URL + NEW_POST_URL],
            [self.POST_2_EDIT, self.authorized_client,
             self.POST_2_URL],
            [self.COMMENT_URL, self.guest_client,
             self.REDIRECT_URL + self.COMMENT_URL]
        ]
        for url, client, redirect_url in items:
            with self.subTest(url=redirect_url):
                self.assertRedirects(client.get(url, follow=True),
                                     redirect_url)

    def test_page_not_found(self):
        """Тест возврата ошибки"""
        response = self.guest_client.get('/404/')
        self.assertEqual(response.status_code, 404)
