# ElectoLibrary

## 1. Титульная часть

- Автор: указать ФИО
- Группа: указать группу
- Дата: 24.06.2026
- Название работы: SPA-приложение "Электронная библиотека" на Vue 3 с сервером FastAPI

## 2. Цель работы

Разработать SPA-приложение на Vue 3, закрепить работу с компонентами, формами, слотами, маршрутизацией, REST API, сервером на Python, SQLite и запуском проекта в Docker.

## 3. Реализованный функционал

### Клиентская часть

- Главная страница `/` с dashboard и переходом в электронный каталог.
- Каталог `/books` со списком книг, фильтрацией по статусу, поиском и сортировкой по дате добавления или названию.
- Страница избранного `/favorites`.
- Админка `/admin` с простым входом по паролю.
- Создание книги `/admin/books/new` через форму с `v-model.trim`, `v-model.number`, textarea, JPG-файлом, ручным вводом издательства и radio.
- Редактирование книги `/admin/books/:id/edit` с предварительной загрузкой данных.
- Подборки `/books/collections`, которые группируют книги по тематике.
- Страница 404 для неизвестных маршрутов.
- Пользователь может добавлять книги в избранное и бронировать книги.
- Администратор может добавлять, редактировать, удалять книги и менять статус наличия.

### Компоненты

- `AppHeader.vue` — верхнее меню.
- `AppFooter.vue` — нижняя панель.
- `BookList.vue` — вывод массива книг через `v-for` и пустое состояние через `v-if`.
- `BookItem.vue` — карточка одной книги, принимает `props` и отправляет события родителю.
- `BookForm.vue` — форма создания и редактирования книги.
- `LayoutCard.vue` — компонент со слотами.

### Vue 3

- `computed`: сортировка, фильтрация, статистика, группировка подборок.
- `watch`: реакция на изменение фильтров и автоподстановка темы для книг про Vue.
- `refs` и lifecycle: фокус на поле заголовка после `onMounted`.
- События: `BookItem` передает `edit`, `delete`, `toggle-status`, `toggle-favorite`, `toggle-reserve`.
- Слоты: обычный слот, именованные слоты `header`, `actions`, `footer`, scoped slot в `LayoutCard`.

### Серверная часть

- FastAPI-приложение в `backend/main.py`.
- SQLite-файл `data/tasks.db`.
- CRUD API:
  - `GET /api/books`
  - `GET /api/books/{id}`
  - `GET /api/boooks/{id}` — совместимость с опечаткой из задания
  - `POST /api/books`
  - `PUT /api/books/{id}`
  - `DELETE /api/books/{id}`
  - `PATCH /api/books/{id}/favorite`
  - `PATCH /api/books/{id}/reserve`
- Админские `POST`, `PUT`, `DELETE` требуют токен после `POST /api/auth/login`.
- При каждом запросе к `/api` обновляется таблица `api_meta`, поэтому файл БД меняется и доступен для ручной проверки.

## 4. Скриншоты интерфейса

После запуска проекта добавить скриншоты:

- Главная страница: `http://localhost:8080/`
- Список книг: `http://localhost:8080/books`
- Избранное: `http://localhost:8080/favorites`
- Фильтрация и сортировка: `http://localhost:8080/books`
- Админка: `http://localhost:8080/admin`
- Форма создания: `http://localhost:8080/admin/books/new`
- Форма редактирования: `http://localhost:8080/admin/books/1/edit`
- Страница 404: `http://localhost:8080/unknown-route`

## 5. Пример кода

```vue
<BookItem
  v-for="book in books"
  :key="book.id"
  :book="book"
  @edit="$emit('edit', $event)"
  @delete="$emit('delete', $event)"
  @toggle-status="$emit('toggle-status', $event)"
/>
```

```js
const sortedBooks = computed(() => {
  return [...filteredBooks.value].sort((first, second) => {
    if (sortMode.value === 'title') {
      return first.title.localeCompare(second.title, 'ru')
    }

    return new Date(second.created_at) - new Date(first.created_at)
  })
})
```

## 6. JSON или SQLite данные

Пример записи в SQLite:

```json
{
  "id": 1,
  "title": "Чапаев и Пустота",
  "author": "В. О. Пелевин",
  "publisher": "Эксмо",
  "category": "16+",
  "year": 1996,
  "theme": "Современная проза",
  "status": "available",
  "is_favorite": true,
  "is_reserved": false
}
```

## 7. Инструкция по запуску

### Docker

```bash
docker compose up --build
```

После запуска:

- Frontend: `http://localhost:8080` или `http://127.0.0.1:8080`
- Backend: `http://localhost:8000/api/books`
- SQLite: `data/tasks.db`
- Админка: `http://localhost:8080/admin`
- Пароль администратора по умолчанию: `admin123`

### Локальная разработка

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## 8. Выводы

В ходе работы были изучены структура Vue 3 SPA, компонентный подход, формы и модификаторы ввода, фильтрация и сортировка данных, маршрутизация Vue Router, REST API, FastAPI, SQLite и контейнеризация через Docker Compose.
