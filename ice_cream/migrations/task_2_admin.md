# Задание 2: Админка + русификация

## Код целиком (`django_control_point_1\project_blog_02\blog\admin.py`)

```python
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'location', 'pub_date', 'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('category', 'location', 'is_published')


if admin.site.is_registered(Group):
    admin.site.unregister(Group)
```

## Изменения в `django_control_point_1\project_blog_02\project_blog_02\settings.py`

```python
LANGUAGE_CODE = 'ru-RU'   # было 'en-EN'
TIME_ZONE = 'Europe/Moscow'  # было 'US/Eastern'
```

Приложение `blog` уже имело `verbose_name = 'Блог'` в `django_control_point_1\project_blog_02\blog\apps.py` — менять не пришлось.

## Что сделано и почему

- **Регистрация моделей** через декоратор `@admin.register` — современный способ, вместо `admin.site.register`.
- **`list_display`** — какие колонки видны в списке объектов.
- **`list_editable`** — галочку «Опубликовано» можно менять прямо в списке, не заходя в объект.
- **`search_fields`** — поиск по названию категории/локации/поста.
- **`list_filter`** — фильтр постов по категории, локации и статусу публикации.
- **Отключение `Group`** — по ТЗ «лишние модели отключите (кроме USER)». Защищённая проверка `is_registered` нужна, потому что `django_control_point_1\project_blog_02\blog\admin.py` импортируется раньше, чем загрузится админка `auth` (иначе `NotRegistered`).
- **`LANGUAGE_CODE = 'ru-RU'`** — весь интерфейс админки переключается на русский.

## Проверка

```bash
venv\Scripts\python.exe -m pytest tests/test_localization.py tests/test_admin_page.py -v
```

**24 passed** — русификация и админка соответствуют ТЗ.
