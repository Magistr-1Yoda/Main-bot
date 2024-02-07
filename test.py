import database
db = database.Database()


list_nub = [1,2,3,4,5,6,7,8,9,10]


for idnumber in list_nub:
    chat_id = 0
    data = db.programming(chat_id)
    number = data[1]
    idnumber = number[0]
    print(idnumber)
    if idnumber in list_nub:
        print("Это число есть, значит я могу задать вопрос")
        list_nub.remove(idnumber)
        print(list_nub)
    elif idnumber not in list_nub:
        print("Этого числа нет")
    elif len(list_nub) == 0:
        print("Список полностью пуст")
        break




