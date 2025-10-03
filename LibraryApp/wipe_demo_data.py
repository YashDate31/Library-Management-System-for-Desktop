from database import Database

if __name__ == '__main__':
    db = Database()
    ok, msg = db.clear_all_data()
    print(msg if ok else f"Failed: {msg}")
