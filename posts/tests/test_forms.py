import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User

INDEX_URL = reverse('index')
NEW_POST_URL = reverse('new_post')


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.author = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='test_group', slug='test_group')
        cls.post = Post.objects.create(
            group=cls.group,
            text='Test_text',
            author=cls.author
        )
        cls.group_2 = Group.objects.create(
            title='test_group_2',
            description='test_description_2',
            slug='test_group_2',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.form = PostForm()
        cls.POST_URL = reverse('post', args=[cls.author.username,
                                             cls.post.id])
        cls.POST_EDIT_URL = reverse('post_edit',
                                    args=[cls.author.username,
                                          cls.post.id])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """ Создание поста """
        ids_before_post_creation = set(Post.objects.all().values_list(
            'pk', flat=True))
        posts_count = Post.objects.count()

        smal_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=smal_gif,
            content_type='image/gif'
        )
        form_data = {
            'group': self.group.id,
            'text': 'Test_fore_test',
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        ids_after_post_creation = set(
            Post.objects.all().values_list('pk', flat=True)
        )
        new_post_keys = ids_after_post_creation.difference(
            ids_before_post_creation)
        self.assertEqual(len(new_post_keys), 1)
        post = Post.objects.get(id=new_post_keys.pop())
        self.assertRedirects(response, INDEX_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.image.name, 'posts/' + form_data['image'].name)

    def test_edit_post(self):
        """ Редактирование  поста """
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group_2.id,
            'text': 'Modified_text',
        }
        response = self.authorized_client.post(self.POST_EDIT_URL,
                                               data=form_data,
                                               follow=True
                                               )
        post = response.context['post']
        self.assertRedirects(response, self.POST_URL)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.author)

    def test_new_post_page_shows_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(NEW_POST_URL)
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
