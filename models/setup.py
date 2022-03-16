from models import (
    delete_db_file,
    prepare_session,
    fill_db
)

if __name__ == '__main__':
    delete_db_file()
    session = prepare_session()
    fill_db(session())
