# Задание 3: View-функции и запросы к БД

## Код целиком (`django_control_point_1\project_blog_02\blog\views.py`)

```python
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
    ).order_by('-pub_date')
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
```

## Что сделано и почему

### 1. Удалён словарь `posts`
Старый захардкоженный список из `django_control_point_1\project_blog_02\blog\views.py` удалён — теперь данные приходят из БД.

### 2. Главная страница (`index`)
```python
Post.objects.filter(
    is_published=True,                    # пост опубликован
    category__is_published=True,           # категория опубликована
    pub_date__lte=timezone.now(),          # дата публикации не в будущем
).order_by('-pub_date')[:5]                # 5 послубщих постов
```
- `category__is_published` — фильтрация по полю связанной модели (двойное подчёркивание `__` — это «переход по связи»).
- `[:5]` — срез: ровно 5 последних постов.
- `order_by('-pub_date')` — сортировка от новых к старым.

### 3. Страница публикации (`post_detail`)
Используем `get_object_or_404` — если пост не найден ИЛИ не подходит по условиям, Django автоматически вернёт 404. Это компактнее и надёжнее, чем вручную проверять и бросать `Http404`.

### 4. Страница категории (`category_posts`)
Сначала `get_object_or_404` для категории — если категория не опубликована, сразу 404. Затем фильтруем посты по этой категории.

## Проверка

```bash
venv\Scripts\python.exe -m pytest tests/test_posts_page_views.py tests/test_post_detail_views.py tests/test_category_page_views.py -v
```
