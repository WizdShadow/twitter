from sqlalchemy import create_engine
from database import Base


def dt_1(base):
    engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5400/twitter_test")
    if base == 1:
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        
        
def dt_2(base):
    engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5400/twitter")
    if base == 1:
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        
        
        
num = int(input("Введите номер базы 1 \ 2 тестовая\основная: "))
action = int(input("Введите номер действия 1 \ 2 создать\удалить: "))
if num == 1:
    dt_1(action)
else:
    dt_2(action)