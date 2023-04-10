import sqlite3


def read_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sensor_data')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    read_data()
