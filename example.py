from orm_sqlite import OrmModel, OrmText, OrmInteger, OrmFloat
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SomeTable(OrmModel):
    some_field_1 = OrmText()
    some_field_2 = OrmInteger()
    some_field_3 = OrmFloat()


try:
    SomeTable.create_table()

    row1 = SomeTable(some_field_1='test', some_field_2=25, some_field_3=123.123)
    row1.save()

    row2 = SomeTable(some_field_1='test2', some_field_2=100, some_field_3=321.321)
    row2.save()

    all_rows = SomeTable.execute_query('SELECT * FROM SomeTable;')
    logging.info("All rows:")
    logging.info(all_rows)

    filtered_rows = SomeTable.filter(some_field_1='test')
    logging.info("Filtered rows:")
    logging.info(filtered_rows)

except Exception as e:
    logging.error(f"An error occurred: {e}")
