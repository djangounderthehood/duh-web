import os
import threading
import markdown as md
from collections import OrderedDict
from glob import glob

from django.conf import settings
from django.utils.functional import cached_property

_local = threading.local()


def read_all_posts():
    """
    Reads all posts from disk into OrderedDict in reverse alphabetical order.
    """
    posts = OrderedDict()
    filenames = glob('%s/*.md' % settings.TINYBLOG_ROOT_DIR)
    for filename in sorted(filenames, reverse=True):
        # [:-3] chops off the '.md' suffix
        slug = os.path.relpath(filename, settings.TINYBLOG_ROOT_DIR)[:-3]
        with open(filename) as f:
            markdown_content = f.read()
        posts[slug] = Post(slug, markdown_content)

    return posts


class PostManager(object):
    """
    Simple proxy object working on thread-local OrderedDict of posts.
    """

    def get(self, slug):
        """
        Return a Post instance from the given slug.
        """
        return self._posts.get(slug)

    def all(self):
        """
        Return a list of all existing Post instances, in reverse alphabetical order.
        """
        return list(self._posts.values())

    @property
    def _posts(self):
        if not hasattr(_local, 'posts'):
            _local.posts = read_all_posts()

        return _local.posts


class Post(object):
    objects = PostManager()

    def __init__(self, slug, markdown=None):
        self.slug = slug
        self.markdown = markdown

    @cached_property
    def html(self):
        return md.markdown(self.markdown)

    @cached_property
    def intro_html(self):
        return md.markdown(self.markdown.split('---')[0])
