import json
import os

def load_recipe(file_name='recipes.json'):
    """Функция выгрузки информации о блюдах и рецептах пользователя
    Возвращает:
    - Список блюд и рецептов в случае, если у пользователя они присутствуют
    - Создается пустой список с ключем recipes в случае, если пользователь новый"""

    if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as r:
                data = json.load(r)
                return data
    else:
        return {}


def save_recipe(data: dict, file_name='recipes.json'):
    """Функция сохраняет блюда и рецепты пользователя
    
    - Принимает данные добавленных рецептов и блюд и добавляет их в основной список рецептов"""
    
    with open(file_name, "w", encoding="utf-8") as s:
        json.dump(data, s, ensure_ascii=False, indent=4)
