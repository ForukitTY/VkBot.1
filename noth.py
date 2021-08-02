import vk_api
import requests
import subprocess
from bs4 import BeautifulSoup
from vk_api.longpoll import VkLongPoll, VkEventType
token2 = "cda923ac6d6cdbf05a2ba3b791f97869fc7f237f623c07bf93935e774ae23581fb35e7a8bba37dbf7e145"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token2)
# Работа с сообщениями
longpoll = VkLongPoll(vk)

class VkBot:
    def _clean_all_tag_from_str(self, string_line): #приходит в формате Tag

        result = ""
        for i in string_line.text: #now is string
            not_skip = True
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

#firstly we need to know what the command said user
    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Уи махуэ фlыуэ, {self._USERNAME}!"
        if message.upper() == self._COMMANDS[3]:            
            vk.method('messages.send', {'user_id': event.user_id, 'attachment': 'photo-174309237_457256559', 'random_id': 0})
            return " "

        # Погода
        if message.upper().split()[0]==self._COMMANDS[1]:
            if message.upper()==self._COMMANDS[1]:
                if self._USER_CITY:
                    return self._get_weather(self._USER_CITY)
                else:
                    return 'Я не нашел твой город. Потому что ты, идиот, не указал его в профиле.. \n Я по твоему Савос Арен из Винтерхолда??? \n Ладно ладно. Напиши "Погода " и город в котором хочешь узнать погоду дальше я сам разберусь.'
            else:
                return self._get_weather(message.upper().split()[1])
    
        # Пока
        elif message.upper() == self._COMMANDS[2]:
            return f'Гъуэгу махуэ, {self._USERNAME}'
        
        #Parser
        elif message.upper() == self._COMMANDS[4]:
             return self.pars()

        else: 
            return "могу только погоду сказать или попрощаться. \nЧтобы узнать погоду напиши 'погода'"
#Time
    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        if request.status_code == 200:
            print('Success! time req')
        else:
            print("casino time req")
        b = BeautifulSoup(request.text, "html.parser")
        res2=self._clean_all_tag_from_str(b.find_all("h2"))
        
        res2=res2.replace('В', '\nB')
        return res2
#Weather
    def _get_weather(self, city):
        request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
        if request.status_code!=200:
            return "А может ты нормально название напишешь?? A то такого Залупосранска я не нахожу."
        b = BeautifulSoup(request.text, "html.parser")
        
        min_and_maxWeath = self._clean_all_tag_from_str(b.select_one('.weather__content_tab-temperature'))
        min_and_maxWeath = min_and_maxWeath.replace('макс.', 'Максимум днем')
        min_and_maxWeath = min_and_maxWeath.replace('мин.', 'Минимум днем')
        currentWeather = self._clean_all_tag_from_str(b.select('.table__col.current .table__felt')[0])
        return f'Сегодня в {city.title()}: {min_and_maxWeath} \nВ данный момент {currentWeather}'

    def pars(self):
        outputSum=""
        
        cost=[]
        f=open('HtmlCodeFileEldorado.txt', 'r+',  encoding='utf-8')
        for iter in range(1,7):
            
            print(f"\n\n______________________________Страница {iter}:______________________________")

            txt="curl https://www.eldorado.ru/c/smartfony/?page=%i"%iter
            if iter==1:
                txt="curl https://www.eldorado.ru/c/smartfony/"

            x = subprocess.check_output(txt, shell=True)
            strHTMLCode=str(x, encoding='utf-8')
        

            b = BeautifulSoup(f'{strHTMLCode}','html.parser')

            costAndTags = b.find_all(attrs={"data-pc": "offer_price"})
            ItemNameTags = b.find_all(attrs={"data-dy": "title"})
            
            for i in range(len(costAndTags)):
                cost.append(self._clean_all_tag_from_str(costAndTags[i])  + " " + self._clean_all_tag_from_str(ItemNameTags[i]) )
                print(f'{(iter-1)*36+1+i}) '+cost[-1], end="\n\n")
   
                
        #f.write(strHTMLCode)
        #f.close()
        print(cost)
        return "че то да произошло"

    def __init__(self, user_id):
    
        print("Создан объект бота!")
        self._USER_ID = user_id
        try:
            self._USER_CITY=vk.method('users.get',{'user_ids':user_id, 'fields': 'city'})[0]['city']['title']
        except:
            self._USER_CITY=False

        self._USERNAME = vk.method('users.get',{'user_ids':user_id})[0]['first_name']
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ПОКА", "ЗАПРЕЩЁНКА", "СТАРТ"]
        print(f'Указанный город для id {user_id}: ', self._USER_CITY)

print("Server started")

ids=[]

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            UserName=vk.method('users.get',{'user_ids':event.user_id})[0]['first_name']+' '+vk.method('users.get',{'user_ids':event.user_id})[0]['last_name']
            if ids.count(event.user_id)==1:
                print(f'For me by:{UserName} id:{event.user_id}', end= ' ')
                print('| New message:', event.text)
                vk.method('messages.send', {'user_id': event.user_id, 'message': bot.new_message(event.text), 'random_id': 0})
            else:       
                ids.append(event.user_id)
                bot = VkBot(event.user_id)
                print(f'For me by:{UserName} id:{event.user_id}', end=' ')
                print('| New message:', event.text)
                vk.method('messages.send', {'user_id': event.user_id, 'message': bot.new_message(event.text), 'random_id': 0})
