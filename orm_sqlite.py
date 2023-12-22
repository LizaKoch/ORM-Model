import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    """Класс для работы с базой данных SQLite3."""
    @classmethod
    def create_database(cls):
        """Метод для создания базы данных SQLite3."""
        with sqlite3.connect('database.db') as connection:
            pass

class OrmField:
    """Класс для создания полей таблицы в базе данных SQLite3."""
    def __init__(self, field_type, primary_key=False):
        self.field_type = field_type
        self.primary_key = primary_key

class OrmModelMeta(type):
    """Метакласс для создания таблицы в базе данных SQLite3."""
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        Database.create_database()
        if not hasattr(cls, 'fields'):
            cls.fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, OrmField):
                cls.fields[attr_name] = attr_value

                if attr_value.primary_key:
                    attr_value.field_type += ' PRIMARY KEY AUTOINCREMENT'

class OrmModel(metaclass=OrmModelMeta):
    """Класс для работы с таблицей в базе данных SQLite3."""
    def __init__(self, **kwargs):
        self.values = kwargs

    @classmethod
    def create_table(cls):
        """Метод для создания таблицы в базе данных SQLite3."""
        fields = [f'{field_name} {field_obj.field_type}' for field_name, field_obj in cls.fields.items()]
        query = f'CREATE TABLE IF NOT EXISTS {cls.__name__} ({", ".join(fields)});'
        cls.execute_query(query)

    @classmethod
    def execute_query(cls, query, params=None):
        """Метод для выполнения SQL-запроса к базе данных SQLite3."""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()
                result = cursor.fetchall()
            except Exception as e:
                logging.error(f"An error occurred during query execution: {e}")
                raise
            return result

    def save(self):
        """Метод для сохранения записи в таблицу базы данных SQLite3."""
        fields = ', '.join(self.values.keys())
        placeholders = ', '.join(['?' for _ in range(len(self.values))])
        values = tuple(self.values.values())
        query = f'INSERT INTO {self.__class__.__name__} ({fields}) VALUES ({placeholders});'
        self.execute_query(query, values)

    @classmethod
    def filter(cls, **kwargs):
        """Метод для получения записей из таблицы базы данных SQLite3 по условию."""
        conditions = [f'{key} = ?' for key in kwargs]
        where_clause = ' AND '.join(conditions)
        query = f'SELECT * FROM {cls.__name__} WHERE {where_clause};'
        return cls.execute_query(query, tuple(kwargs.values()))

class OrmText(OrmField):
    """Класс для создания поля типа TEXT в таблице в базе данных SQLite3."""
    def __init__(self, primary_key=False):
        super().__init__(field_type='TEXT', primary_key=primary_key)

class OrmInteger(OrmField):
    """Класс для создания поля типа INTEGER в таблице в базе данных SQLite3."""
    def __init__(self, primary_key=False):
        super().__init__(field_type='INTEGER', primary_key=primary_key)

class OrmFloat(OrmField):
    """Класс для создания поля типа REAL в таблице в базе данных SQLite3."""
    def __init__(self, primary_key=False):
        super().__init__(field_type='REAL', primary_key=primary_key)