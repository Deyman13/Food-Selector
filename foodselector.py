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
    recipe = recipe.split(": ")
    name = recipe[0]
    ingredients = recipe[1].split(", ")
    data = load_recipe()
    if name in data.keys():
        for i in ingredients:
            if i.casefold() not in [x.casefold() for x in data[name]]:
                answer = input("Данного ингридиента(ов) нет в рецепте этого блюда. Добавить его(их)? Yes/No: ").lower()
                if answer == "yes":
                    data[name].append(i)
                    print("Рецепт успешно изменен!")
                else:
                    break
    else:
        data[name] = ingredients
        print("Блюдо успешно добавлено!")
    save_recipe(data)


def print_all_recipes():
    data = load_recipe()
    for key in data.keys():
        print(key)


def print_recipe(recipe):
    data = load_recipe()
    for k, v in data.items():
        if k == recipe:
            print(", ".join(v))


def find_ingredient(ingredient):
    data = load_recipe()
    for k, v in data.items():
        if ingredient in v:
            print(f'{ingredient} есть в таких рецептах: {k}')
        else:
            print("Блюда с таким ингридиентом нет")


add_recipe(input())
print_all_recipes()
print_recipe("Чай")
find_ingredient("Вода")


