from converter import *
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# app = ApplicationBuilder().token("YOUR TOKEN HERE").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()


# Добавляем новый рецепт
def add_recipe(recipe):
    """Добавить новый рецепт

    - принимает название блюда и рецепт блюда, разделение проиходит через ":" 
    - - 1. В случае если блюдо уже в книге рецептов - можно добавить к нему ингредиенты
    - - 1.1. Программа не добавляет уже существующие ингредиенты, а только новые и приводит все к правильному виду
    - - 2. В случае, если рецепт новый - он добавляется полностью. """

    recipe = recipe.split(": ")
    name = recipe[0].title()
    ingredients = [x.capitalize() for x in recipe[1].split(", ")]
    data = load_recipe()
    if name in data.keys():
        for i in ingredients:
            if i.casefold() not in [x.casefold() for x in data[name]]:
                answer = input("Данного ингредиента(ов) нет в рецепте этого блюда. Добавить его(их)? 1 или 2: ").lower()
                if answer == "1":
                    data[name].append(i)
                    print("Ингредиент успешно добавлен в рецепт!")
                else:
                    break
    else:
        data[name] = ingredients
        print("Блюдо успешно добавлено!")
    save_recipe(data)


def print_all_recipes():
    """Вывод всех рецептов
    
    - Программа выводит все названия блюд, записанных в JSON файл"""

    data = load_recipe()
    if data and data.keys():
        for key in data.keys():
            print(key)
    else:
        print("Нет сохраненных рецептов.")


def print_recipe(recipe):
    """Вывод ингредиентов для приготовления блюда
    
    - Принимает название блюда
    - Выводит рецепт блюда через ',' 
    - В случае, если введенного рецепта не существует в книге рецептов - выведется информация об этом"""

    data = load_recipe()
    if data and data.keys():
        if recipe in data.keys():
            for k, v in data.items():
                if k == recipe:
                    print(", ".join(v))
        else:
            print("Такого рецепта еще не существует.")
    else:
        print("Нет сохраненных рецептов.")


def find_ingredient_in_all_recipes(ingredient):
    """Вывод названий блюд, в которых имеется определенный ингредиент. 
    
    - Принимает название ингредиента и проверяет его наличие во всех рецептах
    - В случае, если ингредиент присутствует в рецептах - выводитя список всех блюд, в которых есть данный ингредиент
    - В случае отсутствия ингредиента во всех рецептах - выводится информация об отсутствии."""

    data = load_recipe()
    recipes_with_ingredient = []
    for k, v in data.items():
        for i in v:
            if correct_split(ingredient, i) == ingredient.casefold():
                recipes_with_ingredient.append(k)
                break
    if len(recipes_with_ingredient) > 0:
        print(f'{ingredient.title()} есть в таких рецептах: {", ".join(sorted(recipes_with_ingredient))}')
    else:
        print("Блюда с таким ингредиентом нет")


def correct_split(ingredient, i):
    """Определение способа разбития ингредиентов
    
    - В случае, если ингредиенты записаны в формате <Ингредиент> - <информация о граммовке> вернется определенный split
    - В случае, если ингредиенты записаны в формате <Ингредиент> <информация о граммовке> или просто <Ингредиент>
    вернется другой вариант split"""

    if ingredient.find(" - ") != -1:
        return i.split(" - ")[0].casefold()
    else:
        return i.split()[0].casefold()


def find_ingredient_in_recipe(recipe, ingredient):
    """Определяет наличие ингредиента в определенном рецепте
    
    - Принимает название блюда и определенный ингредиент
    - - 1. В случае нахождения - возвращается сам ингредиент и значение True в виде кортежа
    - - 2. В случае отсутствия - возвращается информация об отсутствии и False в виде кортежа. """

    data = load_recipe()
    for k, v in data.items():
        if k.casefold() == recipe.casefold():
            for i in v:
                if correct_split(ingredient, i) == ingredient.casefold():
                    return i, True
            return "Такого ингредиента нет в данном блюде", False


def find_recipe(recipe):
    """Определяет наличие определенного блюда в книге рецептов. 
    
    - - 1. В случае обнаружения - возвращает его и True в виде кортежа
    - - 2. В случае отсутствия - возвращает информацию об этом и False в виде кортежа. """

    data = load_recipe()
    if recipe.casefold() in [x.casefold() for x in data.keys()]:
        return recipe.casefold(), True
    else:
        return "Такого рецепта еще не существует.", False


def delete_ingredient(recipe, ingredient):
    """Удаление определенного ингредиента из определенного рецепта
    
    - Принимает название блюда и определенный ингредиент
    
    - Проверяет наличие ингредиента в рецепте блюда
    - - 1. В случае, если ингредиент существует в рецепте - он удаляется и пользователь получает об этом информацию
    - - 2. В случае отсутствия - выдает об этом информацию. """

    data = load_recipe()
    availability, is_true = find_ingredient_in_recipe(recipe, ingredient)
    if is_true:
        data[recipe].remove(availability)
        print(f"{ingredient} успешно удален из рецепта!")
    else:
        print(availability)
    save_recipe(data)


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
            print("Некорректный ввод, проверьте регистр!")
    else:
        print(availability)


#add_recipe(input())
#print_all_recipes()
#print_recipe("Чай")
#find_ingredient_in_all_recipes("вода")
#print(find_ingredient_in_recipe("моХИто", "вОДа"))
#delete_ingredient("Мохито", "вода")
#delete_recipe("кофе")
#print(find_recipe("кофе"))


