import database
import random
db = database.Database()

list_nub = [1,2,3,4,5,6,7,8,9,10]

for i in range(10):
    random_number = random.choice(list_nub)
    data = db.programming(chat_id)
    print(random_number)
    if random_number in list_nub:
        print("Это число есть, значит я могу задать вопрос")
        list_nub.remove(random_number)
        print(list_nub)
    if len(list_nub) == 0:
        print("Список полностью пуст")
        break

        
