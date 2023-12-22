# Django-подобную ORM модель

## Описание

Данная ORM модель позволяет работать с базой данных, используя объектно-ориентированный подход.
Она позволяет создавать таблицы, добавлять в них данные, удалять их, а также выполнять запросы к ним.

## Использование

Для работы с ORM моделью необходимо создать класс, наследующийся от класса `OrmModel` и определить в нем поля таблицы.
Для каждого поля необходимо указать его тип, а также, при необходимости, дополнительные параметры.
После этого вызвать у класса метод `create_table()`, который создаст таблицу в базе данных.
Для добавления записей необходимо создать объект класса, передав в конструктор значения полей, и вызвать у него метод `save()`.
Также можно выполнить запрос на чистом sql, вызвав у класса метод `execute_sql()`.
Для получения значений по условию, необходимо вызвать у класса метод filter(), передав в него условие.

Пример находится в файле `example.py`.