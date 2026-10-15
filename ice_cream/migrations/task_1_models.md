# Задание 1: Создание моделей

## С чего начать работу (подготовка окружения)

Все команды выполняются в терминале из корневой папки `django_control_point_1\`.
Рекомендуется **Python 3.9** (по ТЗ). Если у тебя другая версия — команды те же,
но путь к python может отличаться.

### Шаг 1. Создать виртуальное окружение
```bash
python -m venv venv
```

### Шаг 2. Активировать окружение
```bash
# Windows (cmd):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```
После активации в начале строки появится `(venv)`.

### Шаг 3. Обновить pip
```bash
python -m pip install --upgrade pip
```

### Шаг 4. Установить зависимости
```bash
pip install -r requirements.txt
```
Этот файл лежит в `django_control_point_1\requirements.txt` — там Django 3.2.16, pytest, mixer, flake8 и другие пакеты.

### Шаг 5. Создать и применить миграции
Команды выполняются из папки `django_control_point_1\project_blog_02\`:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Шаг 6. Загрузить фикстуры (данные в БД)
```bash
python manage.py loaddata "../db.json"
```
Файл `db.json` лежит в `django_control_point_1\db.json`. Кавычки и прямой слэш обязательны — bash на Windows не понимает `..\db.json`.

### Шаг 7. Запустить тесты
Из корневой папки `django_control_point_1\`:
```bash
python -m pytest
```
Если всё сделано правильно — увидишь `82 passed`.

### Шаг 8. Проверить PEP8
```bash
python -m flake8 project_blog_02/blog/ project_blog_02/project_blog_02/settings.py
```
Если команда ничего не вывела — нарушений нет, всё чисто.

---

## Код целиком (`django_control_point_1\project_blog_02\blog\models.py`)

```python
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, '
                  'дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField('Название места', max_length=256)
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
```

## Ключевые решения

- **verbose_name позиционно** — `models.CharField('Заголовок', max_length=256)` — стандартный Django-стиль.
- **author → CASCADE**: удалил юзера — удалились его посты.
- **location/category → SET_NULL**: пост остаётся, поле = NULL.
- **location** — `null=True, blank=True` (необязательна по ТЗ).
- **category** — только `null=True` (обязательна, без неё пост не добавить).
- **help_text для is_published** — во всех трёх моделях («Снимите галочку, чтобы скрыть публикацию.»).
- **created_at** — `auto_now_add=True` (один раз при создании).
- **slug** — `unique=True` (уникальный URL).
- **get_user_model()** — ссылка на User без хардкода.
- Порядок полей: title → description → slug → is_published → created_at (как в конспектах преподавателя).

## Проверка

```bash
venv\Scripts\python.exe -m pytest tests/test_post_model.py tests/test_category_model.py tests/test_location_model.py -v
```

**18 passed** — модели соответствуют ТЗ.
