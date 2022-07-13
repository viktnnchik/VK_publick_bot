import vk_api, json
from vk_api.longpoll import VkEventType, VkLongPoll
from config import tok
vk_session = vk_api.VkApi(token = tok)
longpoll = VkLongPoll(vk_session)
class User():
    def __init__(self, id, mode, cash):
        self.id = id
        self.mode = mode
        self.cash = cash
def get_keyboard(buts):
    nb = []
    color = ''
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            color = {'зеленый': 'positive', 'красный': 'negative', 'синий': 'primary'}[buts[i][k][1]]
            nb[i][k] = {"action": {"type": "text", "payload": "{\"button\" : \"" + "1" + "\"}", "label": f"{text}"},"color":f"{color}"}
    first_keyboard = {'one_time': False, 'buttons': nb}
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard
start_key = get_keyboard([
    [('поддержка','синий'),('информация','зеленый')]
])
game_key = get_keyboard([
    [('назад','красный'),('получить контакты разработчика','зеленый')]
])
def sender(id,text,key):
    vk_session.method('messages.send',{'user_id' : id, 'message' : text,'random_id' : 0, 'keyboard' : key })
users = []
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            id = event.user_id
            msg = event.text.lower()
            if msg == 'начать':
                flag1 = 0
                for user in users:
                    if user.id == id:
                        sender(id,'Выберите действие',start_key)
                        user.mode = 'start'
                        flag1 = 1
                if flag1 == 0:
                    users.append(User(id,'start',0))
                    sender(id,'Выберите действие:',start_key)
            for user in users :
                if user.id == id:
                    if user.mode == 'start':
                        if msg == 'поддержка':
                            sender(id,'Опишите в следующем сообщении вашу проблему и скоро с Вами свяжутся.',start_key)
                        if msg == 'информация':
                            sender(id,'Здесь ответы на частозадаваемые вопросы - https://vk.com/topic-214490066_48737329',game_key)
                            user.mode = 'game'
                    if user.mode == 'game':
                        if msg == 'назад':
                            sender(id,'Выберите действие:',start_key)
                            user.mode = 'start'
                        if msg == 'клик':
                            user.cash +=1
                            if msg == 'играть':
                                sender(id,'Кликайте на кнопку слик',game_key)
                                user.mode = 'game'
                        if user.mode == 'game':
                            if msg == 'назад':
                                sender(id,'Выберите действие:',start_key)
                                user.mode = 'start'
                            if msg == 'получить контакты разработчика':
                                sender(id,'viktnnchik@mail.ru',start_key)
                                user.mode = 'start'
