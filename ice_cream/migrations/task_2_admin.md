# Задание 2: Админка + русификация

## Код целиком (`django_control_point_1\project_blog_02\blog\admin.py`)

```python
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'pub_date',
        'is_published', 'created_at'
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'category', 'location')
    date_hierarchy = 'pub_date'
```

## Изменения в `django_control_point_1\project_blog_02\project_blog_02\settings.py`

```python
LANGUAGE_CODE = 'ru-RU'      # было 'en-EN'
TIME_ZONE = 'Europe/Moscow'  # было 'US/Eastern'
```

Приложение `blog` уже имело `verbose_name = 'Блог'` в `django_control_point_1\project_blog_02\blog\apps.py` — менять не пришлось.

## Что сделано и почему

- **Регистрация моделей** через декоратор `@admin.register` — современный способ, вместо `admin.site.register`.
- **try/except** для отключения `Group` — `blog/admin.py` импортируется раньше, чем загрузится админка `auth`.
- **list_display** — какие колонки видны в списке объектов (включая `created_at`).
- **list_editable** — галочку «Опубликовано» можно менять прямо в списке.
- **search_fields** — поиск по названию (и slug для категории, text для поста).
- **list_filter** — фильтр по статусу публикации, категории, локации.
- **prepopulated_fields** — slug автоматически заполняется из title при создании категории.
- **date_hierarchy** — навигация по датам в списке постов.
- **LANGUAGE_CODE = 'ru-RU'** — весь интерфейс админки на русском.

## Проверка

```bash
venv\Scripts\python.exe -m pytest tests/test_localization.py tests/test_admin_page.py -v
```

**24 passed** — русификация и админка соответствуют ТЗ.
