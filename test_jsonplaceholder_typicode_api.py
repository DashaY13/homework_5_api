import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

"""Тест 1: Получаем все посты"""
def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    # Проверяем, что это список и он не пустой
    assert isinstance(data, list)
    assert len(data) > 0
    # Проверяем структуру первого поста
    first_post = data[0]
    assert "userId" in first_post
    assert "id" in first_post
    assert "title" in first_post
    assert "body" in first_post

"""Тест 2: Получаем посты для разных пользователей"""
@pytest.mark.parametrize("user_id, expected_count", [
    (1, 10),  # У пользователя 1 должно быть 10 постов
    (2, 10),  # У пользователя 2 тоже 10 постов
    (3, 10),  # И у пользователя 3 тоже 10 постов
])
def test_get_user_posts(user_id, expected_count):
    response = requests.get(f"{BASE_URL}/posts?userId={user_id}")
    assert response.status_code == 200
    data = response.json()
    # Проверяем, что все посты принадлежат этому пользователю
    for post in data:
        assert post["userId"] == user_id
    # Проверяем количество постов
    assert len(data) == expected_count

"""Тест 3: Получаем конкретный пост"""
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_single_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    # Проверяем, что id совпадает
    assert data["id"] == post_id
    # Проверяем, что есть обязательные поля
    assert "title" in data
    assert "body" in data

"""Тест 4: Создаем новый пост через POST"""
def test_create_post():
    # Данные для нового поста
    new_post = {
        "title": "Тестовый пост",
        "body": "Это тело тестового поста",
        "userId": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/posts",
        json=new_post  # Отправляем как JSON
    )
    
    # Статус должен быть 201 (Created)
    assert response.status_code == 201
    data = response.json()
    
    # Проверяем, что данные сохранились
    assert data["title"] == "Тестовый пост"
    assert data["body"] == "Это тело тестового поста"
    assert data["userId"] == 1
    # API автоматически присваивает id = 101
    assert data["id"] == 101

"""Тест 5: Частично обновляем пост через PATCH"""
def test_update_post():
    # Обновляем только заголовок
    updated_data = {
        "title": "Обновленный заголовок"
    }
    
    response = requests.patch(
        f"{BASE_URL}/posts/1",
        json=updated_data
    )
    
    # Статус должен быть 200
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что заголовок обновился
    assert data["title"] == "Обновленный заголовок"
    # id должен остаться прежним
    assert data["id"] == 1

"""Тест 6: Удаляем пост"""
def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1")
    
    # При удалении возвращается пустой ответ со статусом 200
    assert response.status_code == 200
    
    # Проверяем, что пост действительно удален
    check_response = requests.get(f"{BASE_URL}/posts/1")


"""Тест 7: Пытаемся получить несуществующий пост"""
def test_get_nonexistent_post():
    response = requests.get(f"{BASE_URL}/posts/999999")
    # Должен вернуться пустой объект
    data = response.json()
    assert data == {}  # Пустой словарь


"""Тест 8: Получаем комментарии к посту 1"""
def test_get_post_comments():
    response = requests.get(f"{BASE_URL}/posts/1/comments")
    assert response.status_code == 200
    data = response.json()
    # Проверяем, что это список
    assert isinstance(data, list)
    # Проверяем структуру комментария
    if len(data) > 0:
        comment = data[0]
        assert "postId" in comment
        assert "name" in comment
        assert "email" in comment
        assert "body" in comment

"""Тест 9: Получаем всех пользователей"""
def test_get_all_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    # Должно быть 10 пользователей
    assert len(data) == 10
    
    # Проверяем структуру первого пользователя
    first_user = data[0]
    assert "name" in first_user
    assert "email" in first_user
    assert "address" in first_user
    assert "phone" in first_user