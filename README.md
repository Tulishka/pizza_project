# Конструктор пиццы

Учебный проект яндекс лицей PyQt

### Общее описание

Приложение для терминала самообслуживания в пиццерии. Позволяет сделать заказ пиццы по индивидуальному заказу.

### ТЗ

* [Интерфейс пользователя (figma)](https://www.figma.com/design/GnL1HHSoZgVWraLhC70lMX/pizza_designer?node-id=0-1&t=3cG2pVHnpJpBUBtz-1)
* [Техническое задание (docs/tz_terminal.md)](docs/tz_terminal.md)
* [Скрины ТЗ](docs/screens.png)

### Процесс создания пиццы

Пользователю предлагается создать пиццу, для этого он сначала выбирает размер, основу и соус. Потом открывается редактор
пиццы. Есть возможность добавлять ингредиенты. У каждого ингредиента можно выбрать размер порции и по желанию разместить
его на пицце самостоятельно. После завершения создания пиццы нужно будет оплатить заказ. После чего статус заказа
изменится и его смогут увидеть повара на кухне.

### БД
* Ингредиенты, виды теста, виды соусов хранятся в БД (создаются при отсутствии автоматически).
  * таблицы: 
    * categories
    * ingredients
    * dough_types
    * souses
* Созданная пицца и заказ сохраняется в БД.
  * таблицы: 
    * pizzas
    * pizzas_ingredients
    * orders
* Базовые цены на основу + соус в зависимости от выбранного размера
  * таблица
    * base_price

Изображение пиццы экспортируется в папку `pizzas_pictures` при завершении заказа

### Структура

#### Файлы

* [pizza_project.py](pizza_project.py) - главный (запускаемый) файл проекта
* [model.py](database/model.py) - классы модели данных
* [db.py](database/db.py) - функции работы с БД
* [payment_api.py](utils/payment_api.py) - платежный шлюз (эмуляция)
* [pizza_project.spec](pizza_project.spec) - настройки PyInstaller для экспорта проекта
  в [исполняемый файл](dist/pizza_project.zip)
* [requirements.txt](requirements.txt) - файл зависимостей

#### Папки

* [db_init](db_init) - SQL скрипты для создания БД и начального заполнения
* [docs](docs) - документация
* [images](images) - картинки проекта
* [pizzas_pictures](pizzas_pictures) - картинки пицц из заказов (будет создана при запуске)
* [utils](utils) - функции помощники
* [widget](widget) - классы виджетов
* [screens](screens) - классы экранов
* [dist](dist) - папка с архивом и исполняемый файлом

### Запуск проекта

#### Вариант 1:

[Скачать исполняемый файл](dist/pizza_project.zip)

#### Вариант 2

1. Клонировать проект:

```bash
git clone https://github.com/Tulishka/pizza_project.git
```

3. создать и активировать виртуальное окружение

```bash
cd pizza_project
```

```bash
python -m venv venv
```

```bash
venv/Scripts/activate
```

4. установить зависимости

```bash
pip install -r requirements.txt
```

5. запустить проект

```bash
python pizza_project.py
```

### Сборка исполняемого файла

```bash
pyinstaller pizza_project.spec
```

### Технологии и библиотеки

* Python 3.11
* PyQt6 6.7
* SQL, SQLite
* PyInstaller

### Скрины готовых пиц

<img src="images/welcome_image.png" width="200">
<img src="images/welcome_image2.png" width="200">
<img src="images/welcome_image3.png" width="200">
<img src="images/welcome_image4.png" width="200">
<img src="images/welcome_image5.png" width="200">
<img src="images/welcome_image6.png" width="200">

[экраны](docs/screens.png)



