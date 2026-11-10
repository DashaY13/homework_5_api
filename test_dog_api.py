import pytest
import requests

BASE_URL = "https://dog.ceo/api"

"""Тест 1: Получаем список всех пород собак"""
def test_get_all_breeds():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["message"]) > 0  # Есть хотя бы одна порода собак

"""Тест 2: Параметризованный тест для разных пород собак"""
@pytest.mark.parametrize("breed", ["hound", "husky", "poodle"])
def test_get_breed_image(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images/random")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Проверяем, что это картинка
    assert data["message"].endswith((".jpg", ".png"))

"""Тест 3: Параметризованный тест разного количества фото"""
@pytest.mark.parametrize("count", [1, 3, 5])
def test_get_multiple_images(count):
    response = requests.get(f"{BASE_URL}/breeds/image/random/{count}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["message"]) == count  # Проверяем количество фото

"""Тест 4: Негативный тест - несуществующая порода собак"""
def test_invalid_breed():
    response = requests.get(f"{BASE_URL}/breed/unicorn/images/random")
    assert response.status_code == 404

"""Тест 5: Проверяем структуру ответа"""
def test_response_structure():
    response = requests.get(f"{BASE_URL}/breeds/image/random")
    data = response.json()
    # Проверяем, что есть нужные ключи
    assert "status" in data
    assert "message" in data
    # Проверяем типы данных
    assert isinstance(data["status"], str)
    assert isinstance(data["message"], str)