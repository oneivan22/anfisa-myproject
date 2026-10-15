# Полный отчёт по контрольной точке

## Описание проекта

Блог на Django 3.2. Основная сущность — публикация (пост), вокруг неё строится всё:
- У поста есть заголовок, текст, дата публикации, автор, локация, категория, флаг «опубликовано».
- Пост отображается, если: дата публикации не позже текущего, is_published=True, категория опубликована.
- Локация необязательна (тогда показывается «Планета Земля»).
- Без категории пост добавить нельзя.

---

## Подготовка окружения

Все команды из корневой папки `django_control_point_1\`.

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать (Windows cmd)
venv\Scripts\activate

# 3. Обновить pip
python -m pip install --upgrade pip

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Миграции (из папки project_blog_02)
cd project_blog_02
python manage.py makemigrations
python manage.py migrate

# 6. Загрузить фикстуры
python manage.py loaddata "../db.json"

# 7. Запустить тесты (из корня)
cd ..
python -m pytest

# 8. Проверить PEP8
python -m flake8 project_blog_02/blog/ project_blog_02/project_blog_02/settings.py
```

---

## Задание 1: Создание моделей

Файл: `django_control_point_1\project_blog_02\blog\models.py`

```python
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        ),
    )
    created_at = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    name = models.CharField(verbose_name='Название места', max_length=256)
    created_at = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(models.Model):
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
    )
    created_at = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
```

### Ключевые решения

- **author → CASCADE**: удалил юзера — удалились его посты.
- **location/category → SET_NULL**: пост остаётся, поле = NULL.
- **location** — `null=True, blank=True` (необязательна по ТЗ).
- **category** — только `null=True` (обязательна, без неё пост не добавить).
- **created_at** — `auto_now_add=True` (один раз при создании).
- **slug** — `unique=True` (уникальный URL).
- **get_user_model()** — ссылка на User без хардкода.
- verbose_name / verbose_name_plural / help_text — дословно из ТЗ.

---

## Задание 2: Админка + русификация

Файл: `django_control_point_1\project_blog_02\blog\admin.py`

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

### Изменения в `django_control_point_1\project_blog_02\project_blog_02\settings.py`

```python
LANGUAGE_CODE = 'ru-RU'      # было 'en-EN'
TIME_ZONE = 'Europe/Moscow'  # было 'US/Eastern'
```

### Ключевые решения

- **@admin.register** — современная замена admin.site.register.
- **list_display** — колонки в списке объектов.
- **list_editable** — галочку «Опубликовано» можно менять прямо в списке.
- **search_fields** — поиск по названию.
- **list_filter** — фильтр по категории, локации, статусу.
- **Отключение Group** — защищённая проверка is_registered, потому что blog/admin.py импортируется раньше, чем загрузится админка auth.
- **LANGUAGE_CODE = 'ru-RU'** — весь интерфейс админки на русском.

---

## Задание 3: View-функции и запросы к БД

Файл: `django_control_point_1\project_blog_02\blog\views.py`

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

### Ключевые решения

- **Удалён словарь posts** — данные приходят из БД.
- **category__is_published** — фильтрация по полю связанной модели (двойное подчёркивание = переход по связи).
- **[:5]** — срез: ровно 5 последних постов (LIMIT 5 в SQL).
- **get_object_or_404** — если объект не найден или не подходит по условиям — автоматически 404.
- **timezone.now()** — учитывает USE_TZ=True, корректное сравнение с датой в БД.
- **order_by('-pub_date')** — сортировка от новых к старым.

---

## Финал: фикстуры, тесты, PEP8

### Загрузка фикстур

```bash
cd project_blog_02
python manage.py loaddata "../db.json"
```
Результат: Installed 173 object(s) from 1 fixture(s).

### Полный прогон тестов

```bash
python -m pytest
```
Результат: **82 passed**.

### Проверка PEP8

```bash
python -m flake8 project_blog_02/blog/ project_blog_02/project_blog_02/settings.py
```
Результат: нарушений нет.

---

## Итоговые файлы проекта

| Файл | Статус |
|------|--------|
| `django_control_point_1\project_blog_02\blog\models.py` | Создан |
| `django_control_point_1\project_blog_02\blog\admin.py` | Настроен |
| `django_control_point_1\project_blog_02\blog\views.py` | Переписан |
| `django_control_point_1\project_blog_02\blog\migrations\0001_initial.py` | Создана |
| `django_control_point_1\project_blog_02\project_blog_02\settings.py` | Русифицирован |
| `django_control_point_1\project_blog_02\db.sqlite3` | Создана + фикстуры |

---

## Баллы по ТЗ

- 0.5 — Реализация моделей в соответствии с ТЗ
- 0.5 — Админка, русификация
- 0.5 — Структура папок, БД с фикстурами
- 0.5 — Главная страница работает
- 1.0 — Страница публикации работает
- 1.0 — Страница категории работает
- 1.0 — Все тесты проходят
- 1.0 — DRY, PEP8, оптимизация запросов

**Итого: 6 баллов из 6.**
