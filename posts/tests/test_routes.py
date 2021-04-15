from django.test import TestCase
from django.urls import reverse

from posts.models import Post, User

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

    def test_routes(self):
        """ Тест расчёта URL """
        self.author = User.objects.create_user(
            username=AUTHOR_USERNAME, password='testpas'
        )
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.author)

        # variables for test routes
        self.POST_1_ID = self.post.id

        # url dependent on variables
        self.POST_URL = reverse('post', args=[self.author.username,
                                              self.post.id])
        self.POST_EDIT_URL = reverse('post_edit',
                                     args=[self.author.username,
                                           self.post.id])
        url_routes = {
            '/': INDEX_URL,
            '/new/': NEW_POST_URL,
            f'/group/{GROUP_SLUG}/': GROUP_URL,
            f'/{AUTHOR_USERNAME}/': PROFILE_URL,
            f'/{AUTHOR_USERNAME}/{self.POST_1_ID}/': self.POST_URL,
            f'/{AUTHOR_USERNAME}/{self.POST_1_ID}/edit/': self.POST_EDIT_URL,
            '/follow/': FOLLOW_URL
        }
        for url, calculated_route in url_routes.items():
            self.assertEqual(url, calculated_route)
