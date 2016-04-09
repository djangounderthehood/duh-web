from collections import OrderedDict
from unittest.mock import patch
from django.shortcuts import resolve_url

from django.test import TestCase

from .models import Post


@patch('tinyblog.models.read_all_posts')
class PostManagerTest(TestCase):
    def setUp(self):
        from .models import _local
        if hasattr(_local, 'posts'):
            del _local.posts

    def test_get_returns_post_by_slug(self, read_all_posts_mock):
        post = Post('hello', '# Hello world!')
        read_all_posts_mock.return_value = OrderedDict([('hello', post)])

        self.assertEquals(Post.objects.get('hello'), post)

    def test_get_returns_none_on_wrong_slug(self, read_all_posts_mock):
        read_all_posts_mock.return_value = OrderedDict()
        self.assertIsNone(Post.objects.get('nope'))

    def test_all_returns_all_posts(self, read_all_posts_mock):
        read_all_posts_mock.return_value = OrderedDict([
            ('3hello', Post('3hello', '# Three')),
            ('2hello', Post('2hello', '# Two')),
            ('1hello', Post('1hello', '# One')),
        ])

        all_posts = Post.objects.all()
        self.assertEqual(3, len(all_posts))
        self.assertEqual('3hello', all_posts[0].slug)
        self.assertEqual('2hello', all_posts[1].slug)
        self.assertEqual('1hello', all_posts[2].slug)


class PostTest(TestCase):
    def test_renders_html(self):
        post = Post('hello', '# Hello world!')
        self.assertEquals(post.html, '<h1>Hello world!</h1>')

    def test_renders_intro_html(self):
        post = Post('hello', '# Hello world!\n---\nThis is not welcome.')
        self.assertEquals(post.intro_html, '<h1>Hello world!</h1>')


class PostListViewTest(TestCase):
    def test_get_renders_template(self):
        resp = self.client.get(resolve_url('blog:index'))

        self.assertTemplateUsed(resp, 'tinyblog/index.html')
        self.assertIn('posts', resp.context)


class PostDetailViewTest(TestCase):
    def test_get_renders_template(self):
        post = Post.objects.all()[0]
        resp = self.client.get(resolve_url('blog:article', slug=post.slug))

        self.assertTemplateUsed(resp, 'tinyblog/article.html')
        self.assertIn('post', resp.context)
        self.assertEqual(post, resp.context['post'])
