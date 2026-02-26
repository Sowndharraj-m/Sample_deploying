from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo


@login_required(login_url='/login/')
def todo_list(request):
    """Show all todos for the logged-in user."""
    todos = Todo.objects.filter(user=request.user)
    total = todos.count()
    completed = todos.filter(completed=True).count()
    pending = total - completed

    context = {
        'todos': todos,
        'total': total,
        'completed': completed,
        'pending': pending,
    }
    return render(request, 'todo/todo_list.html', context)


@login_required(login_url='/login/')
def todo_add(request):
    """Add a new todo."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            Todo.objects.create(
                user=request.user,
                title=title,
                description=description,
            )
            messages.success(request, f'Task "{title}" added!')
        else:
            messages.error(request, 'Task title cannot be empty.')

    return redirect('todo_list')


@login_required(login_url='/login/')
def todo_toggle(request, todo_id):
    """Toggle a todo's completed status."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()

    status = 'completed' if todo.completed else 'reopened'
    messages.success(request, f'Task "{todo.title}" {status}!')
    return redirect('todo_list')


@login_required(login_url='/login/')
def todo_delete(request, todo_id):
    """Delete a todo."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    title = todo.title
    todo.delete()
    messages.success(request, f'Task "{title}" deleted!')
    return redirect('todo_list')
