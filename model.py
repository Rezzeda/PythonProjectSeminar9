import sqlite3


def connect():
    global conn, cursor
    conn = sqlite3.connect('phones.db')
    cursor = conn.cursor()


def disconnect():
    conn.commit()
    conn.close()


def all(update, context):
    cursor.execute("select * from phones")
    results = cursor.fetchall()
    update.message.reply_text(''.join([str(element) for element in results]))


def find_abonent(update, context):
    fl = 0
    name = update.message.text
    if name != name.title():
        update.message.reply_text('Введите фамилию с заглавной буквы!')
        name = update.message.text
    elif name == name.title():
        cursor.execute(f"select surname from phones")
        results = cursor.fetchall()
        for elements in results:
            if name in elements:
                cursor.execute(f"select * from phones where surname like '%{name}%'")
                result = cursor.fetchall()
                fl = 1
                update.message.reply_text(''.join([str(element) for element in result]))
    if fl == 0:
        update.message.reply_text("Контакт не найден")


def add_abonent(update, context):
    flag = 0
    surname, name, phone = update.message.text.split()
    cursor.execute("select * from phones")
    results = cursor.fetchall()
    for el in results:
        if int(phone) in el:
            update.message.reply_text("Такой номер уже существует!")
            flag = 1
            break
    if flag != 1:
        cursor.execute(
            f"insert into phones (surname, name, phone) "
            f"values ('{surname}', '{name}', {phone})")
        update.message.reply_text("Контакт добавлен")


def update_info(update, context):
    surname, phone = update.message.text.split()
    cursor.execute(
        f"update phones set phone={phone} where surname='{surname}'"
    )
    update.message.reply_text("Изменения внесены")


def delete_abonent(update, context):
    surname = update.message.text
    cursor.execute(
        f"delete from phones where surname='{surname}'"
    )
    update.message.reply_text("Контакт удален")