import database 
def create_db():
    return database.Base.metadata.create_all(bind=database.engine)
create_db()