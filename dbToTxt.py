import sqlite3

def toTxt(table):
    conn = sqlite3.connect("tweeter.db")
    curs = conn.cursor()
    curs.execute(f"SELECT {table}.content FROM {table}")
    res = curs.fetchall()
    with open(f"data/{table}.txt", "w") as file:
        for t in res:
            file.write(t[0] + "\n")

def main():
    print("Enter table to convert to txt")
    table = input().lower()
    toTxt(table)

if __name__ == "__main__":
    main()