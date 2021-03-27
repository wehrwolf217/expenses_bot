#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = connection.cursor()


def insert(table: str, column_values: tuple):
    values = tuple(column_values)
    placeholder = ', '.join('?' * len(column_values))
    try:
        cursor.execute(f"""INSERT INTO {table} VALUES({placeholder});""", values)
        connection.commit()
        # print("Запись успешно вставлена в таблицу expenses ", cursor.rowcount)
        # cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    # finally:
    #     if connection:
    #         connection.close()
    #         print("Соединение с SQLite закрыто")


def output_data(date: str):
    try:
        cursor.execute(f'''SELECT * FROM expenses WHERE date LIKE "{date}"''')
        result = cursor.fetchall()
        all_expenses = 0
        food_expenses = 0
        transport_expenses = 0
        sigaret_expenses = 0
        etc_expenses = 0
        stable_expenses = 0
        for row in result:
            all_expenses += row[1]
            if row[2] == "еда":
                food_expenses += row[1]
            elif row[2] == 'проезд':
                transport_expenses += row[1]
            elif row[2] == 'сигареты':
                sigaret_expenses += row[1]
            elif row[2] == 'прочее':
                etc_expenses += row[1]
            elif row[2] == 'комуналка':
                stable_expenses += row[1]
        cursor.execute(f'''SELECT * FROM receipts WHERE date LIKE "{date}"''')
        result = cursor.fetchall()
        salary = 0
        hackwork = 0
        parents = 0
        total_money = 0
        for row in result:
            total_money += row[1]
            if row[2] == "зарплата":
                salary += row[1]
            elif row[2] == 'левак':
                hackwork += row[1]
            elif row[2] == 'родители':
                parents += row[1]
        if len(date) <= 8:
            month_day = 'месяц'
        else:
            month_day = 'день'
        return f'затраты за текущий {month_day}:\nеда: {food_expenses}\nпроезд: {transport_expenses}\nсигареты: {sigaret_expenses}\n' \
               f'прочее: {etc_expenses}\nкомуналка: {stable_expenses}\n' \
               f'итого потрачено за текущий {month_day}: {all_expenses}\n\nдоходы за текущий {month_day}:\nзарплата: {salary}\n' \
               f'левак: {hackwork}\nродители: {parents}\nитого доход:{total_money}\nкуда мы летим: {total_money - all_expenses}'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


if __name__ == '__main__':
    insert()
    output_data()
