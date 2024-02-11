import database
import random
db = database.Database()

list_nub = [1,2,3,4,5,6,7,8,9,10]

for idnumber in range(10):
    chat_id = 0
    random_number = random.choice(list_nub)
    data = db.programming(chat_id, random_number)
    print(random_number)
    if random_number in list_nub:
        print("Это число есть, значит я могу задать вопрос")
        list_nub.remove(random_number)
        print(list_nub)
    elif len(list_nub) == 0:
        print("Список полностью пуст")

        




