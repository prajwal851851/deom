from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow

class PostFunctionalityTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, content='Test Post')

    def test_like_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {'content': 'Test Comment'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(user=self.user, post=self.post, content='Test Comment').exists())

    def test_edit_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('edit_post', args=[self.post.id]), {'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated Content')

    def test_delete_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_follow_user(self):
        self.client.login(username='testuser', password='testpass')
        follow_user = User.objects.create_user(username='followuser', password='followpass')
        response = self.client.post(reverse('follow_user', args=[follow_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(follower=self.user, followed=follow_user).exists())

    def test_unfollow_user(self):
        self.client.login(username='testuser', password='testpass')
        follow_user = User.objects.create_user(username='followuser', password='followpass')
        Follow.objects.create(follower=self.user, followed=follow_user)
        response = self.client.post(reverse('unfollow_user', args=[follow_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follow.objects.filter(follower=self.user, followed=follow_user).exists())
