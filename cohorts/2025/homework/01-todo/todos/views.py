from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoForm


def todo_list(request):
    """Display all TODOs."""
    todos = Todo.objects.all()
    return render(request, "home.html", {"todos": todos})


def todo_create(request):
    """Create a new TODO."""
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "TODO created successfully!")
            return redirect("todos:list")
    else:
        form = TodoForm()
    return render(request, "todo_form.html", {"form": form, "title": "Create TODO"})


def todo_edit(request, pk):
    """Edit an existing TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "TODO updated successfully!")
            return redirect("todos:list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todo_form.html", {"form": form, "title": "Edit TODO"})


def todo_delete(request, pk):
    """Delete a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        messages.success(request, "TODO deleted successfully!")
        return redirect("todos:list")
    return render(request, "todo_confirm_delete.html", {"todo": todo})


def todo_toggle(request, pk):
    """Toggle the resolved status of a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save()
    status = "resolved" if todo.resolved else "reopened"
    messages.success(request, f"TODO {status}!")
    return redirect("todos:list")