from converter import *
import re
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# app = ApplicationBuilder().token("YOUR TOKEN HERE").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()


def get_first_value(string):
    return string.split(" - " if string.find(" - ") != -1 else " ")[0].casefold()


def correct_input_recipe_and_ingredient(recipe, ingredient):

    try:
        if isinstance(recipe, str):
            if any(i.isdigit() for i in recipe):
                return False
        
        elif isinstance(recipe, (int, float)):
            return False
        
        if isinstance(ingredient, (int, float)):
            return False

        elif isinstance(ingredient, (tuple, list, set)):
            if any(re.search(r'\d', i) for i in get_values(ingredient)):
                return False
        
        elif isinstance(ingredient, str):
            if any(re.search(r'\d', i) for i in get_first_value(ingredient)):
                return False

        return True
    except IndexError:
        pass


def add_recipe(recipe):
    """Добавить новый рецепт

    - принимает название блюда и рецепт блюда, разделение проиходит через ":"
    - - 1. В случае если блюдо уже в книге рецептов - можно добавить к нему ингредиенты
    - - 1.1. Программа не добавляет уже существующие ингредиенты, а только новые и приводит все к правильному виду
    - - 2. В случае, если рецепт новый - он добавляется полностью. 
    - - 3. В случае, если ингредиент записан в ином формате или не полностью - 
    программа запросит подтверждение на изменение этого конкретного ингредиента. """

    try:
        recipe = recipe.split(": ")
        name = recipe[0].title()
        ingredients = [x.capitalize() for x in recipe[1].split(", ")]
        data = load_recipe()
        is_correct = correct_input_recipe_and_ingredient(name, ingredients)
        if is_correct:
            if name in data.keys():
                if set(ingredients).issubset(data[name]):
                        print("Все ингредиенты уже присутствуют в рецепте, добавлять нечего!")
                else:
                    for ingredient in ingredients:
                        ingredient_name = get_first_value(ingredient)
                        if ingredient_name in [get_first_value(x) for x in data[name]]:
                            answer = input(f"{ingredient_name.title()} уже есть в рецепте этого блюда, изменить ингредиент? 1 (да) / 2 (нет): ")
                            if answer == "1":
                                for i in data[name]:
                                    if get_first_value(i) == ingredient_name:
                                        data[name].remove(i)
                                        data[name].append(ingredient)
                                        save_recipe(data)
                                        print("Рецепт успешно изменен!")
                                        break
                            else:
                                print("Рецепт не будет изменен!")
                                break
                        elif ingredient_name not in [x.casefold() for x in data[name]]:
                            data[name].append(ingredient)
                            save_recipe(data)
                            print(f"{ingredient_name.title()} успешно добавлен в рецепт блюда!")
            else:
                data[name] = ingredients
                save_recipe(data)
                print("Блюдо успешно добавлено!")
        else:
            print("Похоже вы ввели цифру в записи рецепта или ингредиента, это недопустимо!")
    except IndexError:
        print("Вы ничего не ввели, попробуйте снова!")


def print_all_recipes():
    """Вывод всех рецептов
    
    - Программа выводит все названия блюд из книги рецептов c нумерацией по порядку"""

    data = load_recipe()
    result = []
    if data and data.keys():
        for index, key in enumerate(data.keys()):
            result.append(f'{index + 1}. {key}')
        print(f'В книге рецептов на текущий момент существуют такие блюда:\n' + ", ".join(result))
    else:
        print("Книга рецептов пуста!")


def print_recipe(recipe):
    """Вывод ингредиентов для приготовления блюда
    
    - Принимает название блюда
    - Выводит рецепт блюда через ', ' с нумерацией
    - В случае, если введенного рецепта не существует в книге рецептов - выведется информация об этом"""

    data = load_recipe()
    if data and data.keys():
        if recipe in data.keys():
            if data[recipe]:
                print(f'{recipe} можно приготовить, используя следующие ингредиенты:')
                for index, value in enumerate(data[recipe], start=1):
                    print(f"{index}. {value}")
            else:
                print(f"{recipe.title()} не содержит ингредиентов")
        else:
            print("Такого рецепта еще не существует.")
    else:
        print("Нет сохраненных рецептов.")
    

def find_ingredient_in_all_recipes(ingredient):
    """Вывод названий блюд, в которых имеется определенный ингредиент.
    
    - Принимает название ингредиента и проверяет его наличие во всех рецептах
    - В случае, если ингредиент присутствует в рецептах - выводитя список всех блюд, в которых есть данный ингредиент
    - В случае отсутствия ингредиента во всех рецептах - выводится информация об отсутствии. """

    data = load_recipe()
    recipes_with_ingredient = []
    if data and data.keys():
        for k, v in data.items():
            for i in v:
                if correct_split(ingredient, i) == ingredient.casefold():
                    recipes_with_ingredient.append(k)
                    break
        if len(recipes_with_ingredient) > 0:
            print(f'{ingredient.title()} есть в следующих рецептах:')
            for index, recipe in enumerate(sorted(recipes_with_ingredient), start=1):
                print(f'{index}. {recipe}')
        else:
            print("Блюда с таким ингредиентом нет")
    else:
        print("Книга рецептов пуста!")


def correct_split(ingredient, i):
    """Определение способа разбития ингредиентов
    
    - В случае, если ингредиент записан в формате <Ингредиент> - <информация о граммовке> вернется определенный split
    - В случае, если ингредиент записан в формате <Ингредиент> <информация о граммовке> или просто <Ингредиент>
    вернется другой вариант split"""
    
    # в случае, если в функцию передаем по одному ингредиенту 
    if ingredient.find(" - ") != -1:
        return i.split(" - ")[0].casefold()
    else:
        return i.split()[0].casefold()


def find_in(ingredient, value):
    """Функция поиска ингридентов в ингридентах блюда
    
    - Принимает ингредиенты и место, где искать
    - Возвращает список найденных ингредиентов в случае, если они есть
    - Иначе возвращает пустой список"""

    result = []
    for i in value:
        if ingredient.casefold() in i.casefold():
            result.append(ingredient)
    return result


def get_values(value):
    """Получение всех первых слов вне зависимости от разделителя 

    - Принимает список, кортеж, множество (например значения по ключу) (' - ' или ' ')

    - Возвращает список всех первых значений вне зависимости от разделителя

    Пример:
    - 1. Чайный пакетик = [Чайный]
    - 2. Чайный - пакетик = [Чайный]
    - 3. ['Чайный - пакетик', 'Картофель - 300г', 'Вода 2л'] = ['Чайный', 'Картофель', 'Вода'] """

    if isinstance(value, (list, tuple, set)):
        return [x.split()[0].casefold() if " - " not in x else x.split(" - ")[0].casefold() for x in value]


def find_ingredient_in_recipe(recipe, ingredient):
    """Поиск ингредиента(ов) в рецепте
    
    - Проверяет формат ввода ингредиентов и приводит все в нужный формат
    - Проверяет наличие ингредиентов в рецепте
    - Возвращает кортеж множеств (<Уже есть в рецепте блюда>, <Еще нет в рецепте блюда>)"""

    # Так же можно проверять имееются ли недопустимые знаки #!@$%&*()^;"№+=

    data = load_recipe()
    ingredients = correct_instance(ingredient)
    is_correct = correct_input_recipe_and_ingredient(recipe, ingredients)
    if is_correct:
        if recipe.title() in data.keys():
            for key, value in data.items():
                if key.casefold() == recipe.casefold():
                    if value:
                        not_in_the_recipe = set()
                        in_the_recipe = set()
                        if ingredient:
                            for i in ingredients:
                                if get_first_value(i) not in get_values(value):
                                    not_in_the_recipe.add(i)
                                else:
                                    in_the_recipe.add(i)
                            return in_the_recipe, not_in_the_recipe
                        else:
                            print("Похоже вы ввели пустую строку место ингредиентов!")
                    else:
                        print(f"{recipe.title()} не содержит ингредиентов")
        else:
            print(f'{recipe.title()} нет в книге рецептов! Проверьте написание!')
    else:
        print("Похоже вы ввели цифру в записи рецепта или ингредиента, это недопустимо!")


def correct_instance(ingredient):
    if isinstance(ingredient, str):
        return [x.capitalize() for x in ingredient.split(", ")]
    elif isinstance(ingredient, (tuple, list, set)):
        return [x.capitalize() for x in ingredient]
    else:
        return ingredient


def find_recipe(recipe):
    """Определяет наличие определенного блюда в книге рецептов. 
    
    - - 1. В случае обнаружения - возвращает его и True в виде кортежа
    - - 2. В случае отсутствия - возвращает информацию об этом и False в виде кортежа. """

    data = load_recipe()
    if data and data.keys():
        if recipe.lower() in [x.lower() for x in data.keys()]:
            return recipe.casefold(), True
        return "Такого рецепта еще не существует", False
    else:
        print("Книга рецептов пуста!")


def delete_ingredient(recipe, ingredient):
    """Удаление определенного ингредиента из определенного рецепта
    
    - Принимает название блюда и определенный ингредиент
    
    - Проверяет наличие ингредиента в рецепте блюда
    - - 1. В случае, если ингредиент существует в рецепте - он удаляется и пользователь получает об этом информацию
    - - 2. В случае отсутствия - выдает об этом информацию. """

    data = load_recipe()
    ingredient = correct_instance(ingredient)
    in_the_recipe = find_ingredient_in_recipe(recipe, ingredient)[0]
    if data and data.keys():
        if recipe and ingredient:
            if in_the_recipe:
                data[recipe.title()] = list(filter(lambda x: get_first_value(x) not in get_values(in_the_recipe), data[recipe.title()]))
                save_recipe(data)
                print("Ингредиент(ы) успешно удален(ы) из рецепта!")
            else:
                print(f"Ингредиент(ы) отсутствует(ют) в рецепте этого блюда!")
        else:
            print("Вы ввели пустую строку в названии рецепта или ингредиента!")
    else:
        print("Книга рецептов пуста!")


def delete_recipe(recipe):
    """Удаление рецепта целиком
    
    - Принимает название блюда
    - Проверяет наличие блюда в книге рецептов
    - - 1. В случае обнаружения - удаляет его из книги
    - - 2. В случае отсутствия - выдает об этом информацию. """

    data = load_recipe()
    availability, is_true = find_recipe(recipe)
    
    if is_true:
        try:
            del data[recipe.title()]
            print(f'{recipe.title()} успешно удален из книги рецептов!')
            save_recipe(data)
        except KeyError:
            print("Рецепт не найден в книге рецептов. Проверьте название рецепта.")
    else:
        print(availability)


def add_ingredient(recipe, ingredient):
    """Добавление ингредиента в блюдо
    
    - Принимает название блюда и ингредиент, который нужно добавить
    - Проверяет наличие блюда и наличие ингредиента в нем
    - - 1. В случае, если блюдо существует и ингредиента нет - ингредиент будет добавлен
    - - 2. В случае, если блюдо существует и ингридент в нем тоже - выйдет оповещение о том, что уже в наличии
    - - 3. В случае, если блюда не существует в книге рецептов - выйдет оповещение об этом. """

    data = load_recipe()
    ingredient = correct_instance(ingredient)
    is_correct = correct_input_recipe_and_ingredient(recipe, ingredient)
    is_find_recipe = find_recipe(recipe)[1]
    if is_correct:
        if is_find_recipe:
            try:
                not_in_the_recipe = find_ingredient_in_recipe(recipe, ingredient)[1]
                if not_in_the_recipe:
                    for i in not_in_the_recipe:
                        data[recipe.title()].append(i)
                    save_recipe(data)
                    print("Ингредиент(ы) успешно добавлен(ы) в рецепт!")
                else:
                    print("В рецепте уже присутствуют все ингредиенты!")
            except TypeError:
                pass
        else:
            print(f"{recipe.title()} еще нет в книге рецептов!")
    else:
        print("Проверьте корректность ввода, пустые строки или цифры недопустимы!")


def reset_ingredients(recipe):
    """Удаление всех ингредиентов блюда
    
    - Принимает название блюда
    - Проверяет, существует ли блюдо в книге рецептов
    - Удаляет все ингредиенты не удаляя само название блюда """

    data = load_recipe()
    if data:
        is_true = find_recipe(recipe)[1]
        if is_true:
            data[recipe.title()].clear()
            save_recipe(data)
            print("Все ингредиенты блюда успешно удалены!")
        else:
            print("Такого рецепта еще не существует! Проверьте написание!")
    else:
        print("Книга рецептов пуста!")


#add_recipe(input())
#print_all_recipes()
#print_recipe("Борщ Классический")
#find_ingredient_in_all_recipes("вода")
#print(find_ingredient_in_recipe("моХИто", "водка - 100мл, ром - 300гр, мята - 80гр, сахар - 20г, вода 500мл"))
#delete_ingredient("Мохито", "водка - 100мл, ром - 300гр, мята - 80гр, сахар - 20г, вода 500мл")
#delete_recipe("чай")
#print(find_recipe("таНЯ"))
#add_ingredient("Чай", "Лепесток")
#reset_ingredients("мохито")
#add_ingredient("мохито", "сахар")

