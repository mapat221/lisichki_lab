# Лабораторная работа №4: Регистрация пользователя и модели разграничения доступа (Вариант 3: Ролевая модель доступа)

## Состав команды Lisichki
- **Марат Назмиев** (Backend): архитектура, реализация юзкейсов, сессий и ролевой модели;
- **Артем Гриняев** (DB): схемы PostgreSQL, миграции, Dockerfile, docker-compose для сервисов;
- **Эрик Мавлявиев** (Frontend): UI, автотесты pytest, документация, тестирование.


## Как поднять окружение

В корне проекта прописать:

```bash
docker compose up --build -d
```

В результате поднимется 3 сервиса:

- frontend;
- backend;
- bd;

Сервисы доступны по адресам:

- Frontend: http://localhost:5173 локально (или http://45.86.68.5:5173);
- Swagger API: http://localhost:8000/docs локально (или http://45.86.68.5:8000/docs);
- PostgreSQL: localhost:5432 (на hosted by me on vps недоступна извне).

## Ролевая модель доступа

В системе реализовано разграничение прав на основе трех ролей:

### Роль `user`
Назначается всем новым пользователям по умолчанию при регистрации.

**Права:**
- Чтение общего чата;
- Отправка сообщений в чат.

**Ограничения:** не имеет доступа к удалению сообщений и просмотру панели администратора.

### Роль `moderator`
Назначается администратором. Предназначена для контроля за чистотой чата.

**Права:**
- Все права роли `user`;
- **Удаление любых сообщений** из чата.

**Ограничения:** не имеет доступа к панели администратора.

### Роль `admin` (Администратор)
Создается автоматически при старте сервиса

**Права:**
- Все права ролей `moderator` и `user`;
- Выдача и снятие роли `moderator` с других пользователей;
- Доступ к панели администратора со списком пользователей.

**Ограничения:** не может выдавать или снимать роль `admin` для защиты от эскалации привилегий.

## Примеры API запросов (cURL)

### Регистрация

Запрос:

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login": "user1", "password": "UserPassword1!"}'
```

Ответ:

```json
{"success":true,"message":"User registrated","access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.xDdvsOYOwEekHIzzJpwenMki5Wm_f_ucIZ8N9ODlguc","login":"user1","roles":["user"]}
```

### Вход

Запрос:

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"login": "user1", "password": "UserPassword1!"}'
```

Ответ:

```json
{"message":"User logged in","access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.xDdvsOYOwEekHIzzJpwenMki5Wm_f_ucIZ8N9ODlguc","login":"user1","roles":["user"]}
```

### Отправка сообщения

Запрос:

```bash
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.xDdvsOYOwEekHIzzJpwenMki5Wm_f_ucIZ8N9ODlguc"\
  -d '{"text": "Hello world"}'
```

Ответ:

```json
{"message":{"id_":"48","author_login":"user1","text":"Hello world","created_at":"2026-11-05T04:32:16.727299Z"}}
```

### Попытка удаления сообщения

Запрос:

```bash
curl -X DELETE http://localhost:8000/api/messages/1 \
  -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSJ9.xDdvsOYOwEekHIzzJpwenMki5Wm_f_ucIZ8N9ODlguc"
```

Ответ:

```json
{"detail":"Access denied for caller"}
```

### Назначение роли модератора

Запрос:

```bash
curl -X POST http://localhost:8000/api/roles \
  -H "Content-Type: application/json" \
  -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.VslRrz8vCKya9Nte32L_p8Lk9IBTYWpythvpJBsHaoI" \
  -d '{"target_login": "user1", "roles": ["user", "moderator"]}'
```

Ответ:

```json
{"message":"Roles updated","login":"user1","roles":["user","moderator"]}
```

## Демонстрация работы

### Форма регистрации

![registration](resources/registration.png)

### Проверка ролевой модели
![Image](resources/forbidden.png)

### Панель управления ролями
![Image](resources/panel.png)

### Ветка Git
![Image](resources/git.png)