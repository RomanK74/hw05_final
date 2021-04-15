from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User, Follow

GROUP_SLUG = 'test_group'
AUTHOR_USERNAME = 'test_user'

FOLLOW_URL = reverse('follow_index')


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='test_user',
            password='testpas'
        )
        cls.author_2 = User.objects.create_user(
            username='test_user_2',
            password='testpas'
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.authorized_client_2 = Client()
        cls.authorized_client_2.force_login(cls.author_2)
        cls.group = Group.objects.create(
            title='test_group',
            description='test_description',
            slug=GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
            image='smal.gif'
        )

    def test_user_can_follow_author(self):
        """Тест follow"""
        Follow.objects.create(
            user=self.author,
            author=self.author_2)
        follow_user = self.author.follower.get(author=self.author_2)
        self.assertEqual(follow_user.user.username, self.author.username)

    def test_user_can_unfollow_author(self):
        """ Тест unfollow """
        Follow.objects.create(
            user=self.author,
            author=self.author_2)
        Follow.objects.get(
            user=self.author,
            author=self.author_2
        ).delete()
        self.assertFalse(
            Follow.objects.filter(user=self.author,
                                  author=self.author_2).exists())

    def test_new_post_on_follow_page(self):
        """ Новый пост попадает на страницу Follow подписавшегося пользователя
         и не попадает в Follow других пользователей """
        Follow.objects.create(
            user=self.author,
            author=self.author_2)
        Post.objects.create(
            text='follow_test',
            author=self.author_2,
        )
        response = self.authorized_client.get(FOLLOW_URL)
        post = response.context['page'][0]
        self.assertIn(post, response.context['page'])
        response_2 = self.authorized_client_2.get(FOLLOW_URL)
        self.assertNotIn(post, response_2.context['page'])
