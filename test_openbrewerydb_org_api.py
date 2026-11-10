import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1"

"""Тест 1: Получаем список пивоварен"""
def test_get_breweries():
    response = requests.get(f"{BASE_URL}/breweries")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что это список и он не пустой
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Проверяем структуру первой пивоварни
    first_brewery = data[0]
    assert "id" in first_brewery
    assert "name" in first_brewery
    assert "brewery_type" in first_brewery
    assert "city" in first_brewery
    assert "state" in first_brewery
    assert "country" in first_brewery

"""Тест 2: Фильтруем по разным типам пивоварен"""
@pytest.mark.parametrize("brewery_type, expected_count_at_least", [
    ("micro", 50),    # Микропивоварен должно быть много
    ("nano", 5),      # Нанопивоварен меньше
    ("regional", 5),  # Региональных тоже несколько
])
def test_filter_by_type(brewery_type, expected_count_at_least):
    response = requests.get(f"{BASE_URL}/breweries?by_type={brewery_type}")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что все результаты имеют правильный тип
    for brewery in data:
        assert brewery["brewery_type"] == brewery_type
    
    # Проверяем, что результатов достаточно много
    assert len(data) >= expected_count_at_least

"""Тест 3: Ищем пивоварни в разных городах"""
@pytest.mark.parametrize("city", [
    "Portland", 
    "Denver", 
    "Austin"
])
def test_filter_by_city(city):
    response = requests.get(f"{BASE_URL}/breweries?by_city={city}")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что все результаты находятся в указанном городе
    for brewery in data:
        assert city.lower() in brewery["city"].lower(), f"Город {brewery['city']} не содержит {city}"
    
    # В этих городах должны быть пивоварни
    assert len(data) > 0

"""Тест 4: Получаем конкретную пивоварню по ID"""
def test_get_single_brewery():
    response = requests.get(f"{BASE_URL}/breweries?per_page=1")
    data = response.json()
    if len(data) > 0:
        first_id = data[0]["id"]
        response2 = requests.get(f"{BASE_URL}/breweries/{first_id}")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["id"] == first_id

"""Тест 5: Получаем случайную пивоварню"""
def test_get_random_brewery():
    response = requests.get(f"{BASE_URL}/breweries/random")
    assert response.status_code == 200
    data = response.json()
    
    # Должен вернуться список с одной пивоварней
    assert isinstance(data, list)
    assert len(data) == 1
    
    # Проверяем структуру
    brewery = data[0]
    assert "id" in brewery
    assert "name" in brewery
    assert "brewery_type" in brewery

"""Тест 6: Ищем пивоварни по названию"""
def test_search_breweries():
    search_term = "dog"
    response = requests.get(f"{BASE_URL}/breweries/search?query={search_term}")
    assert response.status_code == 200
    data = response.json()
    
    # Должны найтись пивоварни с "dog" в названии
    assert len(data) > 0
    
    # Проверяем, что хотя бы одна пивоварня содержит "dog" в названии
    found_dog = False
    for brewery in data:
        if "dog" in brewery["name"].lower():
            found_dog = True
            break
    assert found_dog, f"Не найдено пивоварен с '{search_term}' в названии"


"""Тест 8: Ищем пивоварни в разных штатах"""
@pytest.mark.parametrize("state, min_breweries", [
    ("Oregon", 5),
    ("Colorado", 5),
    ("Texas", 5),
])
def test_filter_by_state(state, min_breweries):
    response = requests.get(f"{BASE_URL}/breweries?by_state={state}")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что все результаты в правильном штате
    for brewery in data:
        assert brewery["state"] == state
    
    # Проверяем минимальное количество
    assert len(data) >= min_breweries, \
        f"В штате {state} найдено {len(data)} пивоварен, ожидалось минимум {min_breweries}"

"""Тест 9: Пытаемся получить несуществующую пивоварню"""
def test_get_nonexistent_brewery():
    response = requests.get(f"{BASE_URL}/breweries/999999")
    
    # API может вернуть 404 или пустой список
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        # Если вернулся 200, то должен быть пустой объект
        assert data == {} or data == []
