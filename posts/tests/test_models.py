from django.test import TestCase


from posts.models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create_user(username='test_author')
        cls.group = Group.objects.create(title='test_group')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=test_author,
            group=cls.group
        )

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст',
            'author': 'Автор',
            'group': 'Группа',
            'pub_date': 'Дата публикации'

        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        field_help_texts = {
            'text': 'Заполните поле.'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).help_text, expected)

    def test_post_object_name_is_text_field(self):
        """В поле __str__  объекта post записано значение поля task.title."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_group_object_name_is_title_field(self):
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))
