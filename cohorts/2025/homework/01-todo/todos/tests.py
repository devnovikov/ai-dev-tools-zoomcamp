from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from .models import Todo


class TodoModelTests(TestCase):
    """Tests for the Todo model."""

    def test_create_todo(self):
        """Test creating a TODO item."""
        todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date.today(),
        )
        self.assertEqual(todo.title, "Test TODO")
        self.assertEqual(todo.description, "Test description")
        self.assertFalse(todo.resolved)

    def test_todo_str_representation(self):
        """Test the string representation of TODO."""
        todo = Todo.objects.create(title="My Task")
        self.assertEqual(str(todo), "My Task")

    def test_todo_default_resolved_is_false(self):
        """Test that resolved defaults to False."""
        todo = Todo.objects.create(title="New Task")
        self.assertFalse(todo.resolved)

    def test_todo_ordering(self):
        """Test that TODOs are ordered by created_at descending."""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = list(Todo.objects.all())
        self.assertEqual(todos[0], todo2)
        self.assertEqual(todos[1], todo1)


class TodoViewTests(TestCase):
    """Tests for TODO views."""

    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test description",
            due_date=date.today() + timedelta(days=7),
        )

    def test_todo_list_view(self):
        """Test the TODO list view."""
        response = self.client.get(reverse("todos:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test TODO")
        self.assertTemplateUsed(response, "home.html")

    def test_todo_create_view_get(self):
        """Test GET request to create view."""
        response = self.client.get(reverse("todos:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_form.html")

    def test_todo_create_view_post(self):
        """Test creating a TODO via POST."""
        response = self.client.post(
            reverse("todos:create"),
            {
                "title": "New TODO",
                "description": "New description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title="New TODO").exists())

    def test_todo_edit_view_get(self):
        """Test GET request to edit view."""
        response = self.client.get(reverse("todos:edit", args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test TODO")

    def test_todo_edit_view_post(self):
        """Test editing a TODO via POST."""
        response = self.client.post(
            reverse("todos:edit", args=[self.todo.pk]),
            {"title": "Updated TODO", "description": "Updated desc"},
        )
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Updated TODO")

    def test_todo_delete_view_get(self):
        """Test GET request to delete view shows confirmation."""
        response = self.client.get(reverse("todos:delete", args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_confirm_delete.html")

    def test_todo_delete_view_post(self):
        """Test deleting a TODO via POST."""
        todo_pk = self.todo.pk
        response = self.client.post(reverse("todos:delete", args=[todo_pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=todo_pk).exists())

    def test_todo_toggle_resolves_todo(self):
        """Test toggling TODO to resolved."""
        self.assertFalse(self.todo.resolved)
        response = self.client.get(reverse("todos:toggle", args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.resolved)

    def test_todo_toggle_reopens_todo(self):
        """Test toggling a resolved TODO back to unresolved."""
        self.todo.resolved = True
        self.todo.save()
        response = self.client.get(reverse("todos:toggle", args=[self.todo.pk]))
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.resolved)

    def test_todo_404_for_nonexistent(self):
        """Test 404 for non-existent TODO."""
        response = self.client.get(reverse("todos:edit", args=[9999]))
        self.assertEqual(response.status_code, 404)


class TodoFormValidationTests(TestCase):
    """Tests for form validation."""

    def test_create_todo_without_title_fails(self):
        """Test that title is required."""
        response = self.client.post(
            reverse("todos:create"), {"description": "Description only"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Todo.objects.filter(description="Description only").exists())

    def test_create_todo_with_past_due_date(self):
        """Test creating TODO with past due date (should be allowed)."""
        past_date = date.today() - timedelta(days=7)
        response = self.client.post(
            reverse("todos:create"),
            {"title": "Past TODO", "due_date": past_date.isoformat()},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title="Past TODO").exists())