from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Post, Comment, PublishedManager
from .forms import CommentForm


class PostModelTests(TestCase):
    """Test cases for the Post model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a test post body.',
            status=0
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 0)
        self.assertIsNotNone(post.created)
        self.assertIsNotNone(post.updated)

    def test_post_str_representation(self):
        """Test Post string representation"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test body',
            status=0
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_default_status_is_draft(self):
        """Test that new posts default to draft status"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test body'
        )
        self.assertEqual(post.status, 0)  # Draft

    def test_post_ordering(self):
        """Test that posts are ordered by publish date descending"""
        post1 = Post.objects.create(
            title='First Post',
            slug='first-post',
            author=self.user,
            body='First body',
            publish=timezone.now() - timedelta(days=1)
        )
        post2 = Post.objects.create(
            title='Second Post',
            slug='second-post',
            author=self.user,
            body='Second body',
            publish=timezone.now()
        )
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], post2)  # Most recent first
        self.assertEqual(posts[1], post1)

    def test_published_manager_only_returns_published_posts(self):
        """Test that PublishedManager only returns published posts"""
        draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=self.user,
            body='Draft body',
            status=0
        )
        published_post = Post.objects.create(
            title='Published Post',
            slug='published-post',
            author=self.user,
            body='Published body',
            status=1
        )
        
        published_posts = Post.published.all()
        self.assertIn(published_post, published_posts)
        self.assertNotIn(draft_post, published_posts)
        self.assertEqual(published_posts.count(), 1)

    def test_post_unique_title(self):
        """Test that post titles must be unique"""
        Post.objects.create(
            title='Unique Post',
            slug='unique-post',
            author=self.user,
            body='Body'
        )
        with self.assertRaises(Exception):
            Post.objects.create(
                title='Unique Post',
                slug='unique-post-2',
                author=self.user,
                body='Body'
            )


class CommentModelTests(TestCase):
    """Test cases for the Comment model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test body',
            status=1
        )

    def test_comment_creation(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            body='This is a test comment.'
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.name, 'John Doe')
        self.assertEqual(comment.email, 'john@example.com')
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertFalse(comment.active)  # Default is False
        self.assertIsNotNone(comment.created)
        self.assertIsNotNone(comment.updated)

    def test_comment_str_representation(self):
        """Test Comment string representation"""
        comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            body='Test comment'
        )
        expected = f'Comment by John Doe on {self.post}'
        self.assertEqual(str(comment), expected)

    def test_comment_default_active_is_false(self):
        """Test that new comments default to inactive"""
        comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            body='Test comment'
        )
        self.assertFalse(comment.active)

    def test_comment_ordering(self):
        """Test that comments are ordered by created date descending"""
        comment1 = Comment.objects.create(
            post=self.post,
            name='First',
            email='first@example.com',
            body='First comment',
            created=timezone.now() - timedelta(hours=1)
        )
        comment2 = Comment.objects.create(
            post=self.post,
            name='Second',
            email='second@example.com',
            body='Second comment'
        )
        comments = list(Comment.objects.all())
        self.assertEqual(comments[0], comment2)  # Most recent first
        self.assertEqual(comments[1], comment1)

    def test_comment_relationship_to_post(self):
        """Test comment relationship to post"""
        comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            body='Test comment'
        )
        self.assertEqual(comment.post, self.post)
        self.assertIn(comment, self.post.comments.all())


class CommentFormTests(TestCase):
    """Test cases for the CommentForm"""

    def test_comment_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_email(self):
        """Test form with invalid email"""
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form_missing_required_fields(self):
        """Test form with missing required fields"""
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('body', form.errors)

    def test_comment_form_save(self):
        """Test saving a comment from form"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        self.assertEqual(comment.name, 'John Doe')
        self.assertEqual(comment.email, 'john@example.com')
        self.assertEqual(comment.body, 'This is a test comment.')


class PostListViewTests(TestCase):
    """Test cases for PostListView"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create published and draft posts
        self.published_post1 = Post.objects.create(
            title='Published Post 1',
            slug='published-post-1',
            author=self.user,
            body='Body 1',
            status=1,
            publish=timezone.now() - timedelta(days=1)
        )
        self.published_post2 = Post.objects.create(
            title='Published Post 2',
            slug='published-post-2',
            author=self.user,
            body='Body 2',
            status=1,
            publish=timezone.now()
        )
        self.draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=self.user,
            body='Draft body',
            status=0
        )

    def test_post_list_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/list.html')

    def test_post_list_view_only_shows_published_posts(self):
        """Test that only published posts are shown"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.published_post1, response.context['posts'])
        self.assertIn(self.published_post2, response.context['posts'])
        self.assertNotIn(self.draft_post, response.context['posts'])

    def test_post_list_view_pagination(self):
        """Test that pagination works correctly"""
        # Create more posts to trigger pagination
        for i in range(5):
            Post.objects.create(
                title=f'Post {i}',
                slug=f'post-{i}',
                author=self.user,
                body=f'Body {i}',
                status=1
            )
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])


class PostDetailViewTests(TestCase):
    """Test cases for post_detail view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='Test body',
            status=1
        )

    def test_post_detail_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_view_shows_post(self):
        """Test that the view displays the correct post"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

    def test_post_detail_view_404_for_invalid_slug(self):
        """Test that invalid slug returns 404"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_shows_active_comments_only(self):
        """Test that only active comments are shown"""
        active_comment = Comment.objects.create(
            post=self.post,
            name='Active',
            email='active@example.com',
            body='Active comment',
            active=True
        )
        inactive_comment = Comment.objects.create(
            post=self.post,
            name='Inactive',
            email='inactive@example.com',
            body='Inactive comment',
            active=False
        )
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        self.assertIn(active_comment, comments)
        self.assertNotIn(inactive_comment, comments)

    def test_post_detail_view_get_comment_form(self):
        """Test GET request shows comment form"""
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('comment_form', response.context)
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_post_detail_view_post_comment_authenticated(self):
        """Test POST request to create comment when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'body': 'Test comment body'
        }
        response = self.client.post(
            reverse('post_detail', kwargs={'slug': self.post.slug}),
            data=form_data
        )
        self.assertEqual(response.status_code, 200)
        # Check that comment was created
        comment = Comment.objects.get(post=self.post, name='John Doe')
        self.assertEqual(comment.body, 'Test comment body')
        self.assertEqual(comment.post, self.post)

    def test_post_detail_view_post_comment_unauthenticated(self):
        """Test POST request to create comment when not authenticated"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'body': 'Test comment body'
        }
        response = self.client.post(
            reverse('post_detail', kwargs={'slug': self.post.slug}),
            data=form_data
        )
        self.assertEqual(response.status_code, 200)
        # Check that comment was created
        comment = Comment.objects.get(post=self.post, name='John Doe')
        self.assertEqual(comment.body, 'Test comment body')

    def test_post_detail_view_invalid_comment_form(self):
        """Test POST request with invalid comment form"""
        form_data = {
            'name': '',  # Missing required field
            'email': 'invalid-email',
            'body': ''
        }
        response = self.client.post(
            reverse('post_detail', kwargs={'slug': self.post.slug}),
            data=form_data
        )
        self.assertEqual(response.status_code, 200)
        # Check that no comment was created
        self.assertEqual(Comment.objects.count(), 0)
