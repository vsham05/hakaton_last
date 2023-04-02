from main import *
from button import Button
from random import choice, randrange
from config_examples import examples
from card import Photo, BigImage
from EGE_counter import counter
from teoria import videos

skill.add_variables(task_number=0)
skill.add_variables(task_answer=0, task_link='')
skill.add_variables(cur_scene='', cur_text='', test=[])
skill.add_variables(wrong_count=0)
AUTH_TOKEN = 'OAuth AQAAAABFR7qRAAT7o-z5WS14-E3NgJ6iI4IoUeI'
SKILL_ID = 'be55abd0-b4c2-4bf8-b57c-765f1151c91a'



def what_are_you_can(text, entity):
    response = build_default_response()
    response['next_scene'] = 'what_can'
    if text.lower() == 'назад':
        print('77777:', skill.dialogs[skill.current_id].variables['cur_text'].value)
        print(skill.dialogs[skill.current_id].variables['cur_scene'].value)
        
        response['response']['buttons'] = []
        response = skill.dialogs[skill.current_id].variables['cur_scene'].value(skill.dialogs[skill.current_id].variables['cur_text'].value, entity)
    
    elif text.lower() == 'совет':
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
        response['response']['text'] = choice(['Важным этапом при подготовке к ЕГЭ является планирование. Гораздо проще достичь большой цели, разбив ее на маленькие шаги.',
                                               'Для начала нужно разобраться, сколько же времени осталось до экзамена. После чего составить понедельный план того, что вы будете изучать.',
                                               'Каждую неделю, в разные дни, уделяйте внимание изучению новых материалов, закреплению того, что вы уже знаете. А так же решайте каждую неделю разные варианты из ЕГЭ',
                                               'Мы все знаем, что нужны силы для того чтобы учиться. Но часто мы отдыхаем не правильно. Точнее нам кажется, что мы отдыхаем, например, смотря любимый сериал или читая любимого блогера. Но на самом деле мозг наш в это время занят и работает. Лучше сходите в магазин, прогуляйтесь с друзьями, уберитесь в комнате и подготовьте свое рабочее место.',
                                               'Очень важно высыпаться. Нужно спать минимум 7 часов в сутки'])
    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice(['Я не очень вас поняла. Скажите, пожалуйста, еще раз.', 'Я вас не расслышала. Повторите еще раз'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = 'Напишите "Совет" или "Назад", чтобы продолжить.'
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        
    return response


class Test():
    def __init__(self):
        self.num = 0
        self.tasks = [f'{randrange(1, 27)}_{randrange(1, 7)}.png' for _ in range(15)]
        self.first_p, self.first_n = self.tasks[0].split('_')
        self.result = {'1': 0,
                       '2': 0,
                       '3': 0,
                       '4': 0,
                       '5': 0,
                       '6': 0,
                       '7': 0,
                       '8': 0,
                       '9': 0,
                       '10': 0,
                       '11': 0,
                       '12': 0,
                       '13': 0,
                       '14': 0,
                       '15': 0,
                       '16': 0,
                       '17': 0,
                       '18': 0,
                       '19': 0,
                       '20': 0,
                       '21': 0,
                       '22': 0,
                       '23': 0,
                       '24': 0,
                       '25': 0,
                       '26': 0,
                       '27': 0,
                       }
        self.wrong = []
        self.total = 0

    def get_task_data(self):
        res = {'answer': examples[self.tasks[self.num]][0], 'link': examples[self.tasks[self.num]][1],
               'prototype_num': self.tasks[self.num].split('_')[0]}
        if len(examples[self.tasks[self.num]]) == 3:
            res['file_link'] = examples[self.tasks[self.num]][2]

        return res

    def next_task(self):
        self.num = self.num + 1


def start(text, entity):
    response = build_default_response()
    counter('count.png')
    task_var = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN, file='count.png', title=choice(
        ['Привет, готов готовиться к ЕГЭ? Давай начнем!', 'Привет, давай начнём готовиться к ЕГЭ!',
         'Ну что ж, пришло время прокачать свой скилл по информатике, ты готов?']))
    task_var.upload_image()
    
    photo = BigImage(task_var)

    response['response']['text'] = choice(
        ['Привет, готов готовиться к ЕГЭ? Давай начнем!', 'Привет, давай начнём готовиться к ЕГЭ!',
         'Ну что ж, пришло время прокачать свой скилл по информатике, ты готов?'])
    response['response']['card'] = photo.get_card_object()
    skill.dialogs[skill.current_id].variables['cur_text'].value = text
    skill.dialogs[skill.current_id].variables['cur_scene'].value = start
    response['next_scene'] = 'handler1'
    return response


def first_help_handler(text, entity):
    if text.lower() not in ['помощь', 'что ты умеешь?']:
        response = first_choice(text, entity)
    elif text.lower() =='помощь' :
        response = build_default_response()
        response['response'][
            'text'] = 'Добро пожаловать в навые для подготовки к ЕГЭ. Чтобы начать получать полезную информацию для ЕГЭ по информатике, напиши "Да". Если, работая в навыке, ты будешь что-то не понимать, всегда пиши "Помощь". А теперь стоит сказать лишь "Да"!'
        response['next_scene'] = 'handler1'
    else:
        response = build_default_response()
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть список тем и советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
        
    return response


def first_choice(text, entity):
    response = build_default_response()
    if text.lower() in ['да', 'давай']:
        random_word = choice(['Отлично!', 'Круто!', ''])
        response['response']['text'] = random_word + choice(['Ты хочешь пройти тестирование или начать прорешивание отдельных заданий?', "Ты готов начать тестирование или приступим к прорешиванию отдельных заданий?"])
        response['response']['buttons'] = [Button('Тестирование', hide=True).get_button_object(),
                                           Button('Задания', hide=True).get_button_object()]
        response['next_scene'] = 'choice'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = first_choice
    elif text.lower() == 'нет':
        response['response']['text'] = choice(['Когда захотите прокочать свой скил по ЕГЭ - обращайтесь! До встречи!',
                                               'Когда захотите улучшить свои навыки по ЕГЭ - обращайтесь! До встречи! "Навык выключается"']
                                              )
        response['next_scene'] = 'END'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice(['Я не очень вас поняла. Повторите пожалуйста, что вы сказали.',
                                               'Я вас не расслышала, повторите пожалуйста'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = choice(['Скажите "да", чтобы начать свою подготовку.',
                                               'На это сложно что-то сказать, но я знаю, что если сказать "да", начнется подготовка к ЕГЭ.'])
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        response['next_scene'] = 'first'

    if text.lower() == 'помощь':
        response = build_default_response()
        response['response']['buttons'] = []
        response['response'][
            'text'] = choice(['Напиши "Тестирование" и тогда тебе придется решить 15 случайных номеров из ЕГЭ. Советуем проходить его хотя бы раз в неделю, тогда на экзамене ты будешь готов ко всем заданиям.\nНапиши "Задания" и тогда найдешь задания и теорию для каждого номера ЕГЭ.','Напиши "Тестирование" и тогда ты сможешь решить 15 случайных номеров из ЕГЭ. Говорят ,если его  решать хотя бы раз в неделю, тогда на экзамене ты будешь готов ко всем заданиям.\nНапиши "Задания" и тогда увидишь задания и теорию для каждого номера ЕГЭ.'])
        response['next_scene'] = 'fisrt'
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]

    return response


def second_scenary(text, entity):
    response = build_default_response()
    if text.lower() in ['прорешивать', 'задания']:
        response['response']['text'] = choice(['Отлично! напиши номер задания, которое хочешь отработать',
                                               'Тогда отправь мне номер задания для отработки'])
        response['next_scene'] = 'task'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = second_scenary
    elif text.lower() == 'тестирование':
        response['response']['text'] = choice([ 'Сейчас тебе придется решить 15 номеров из ЕГЭ. Задания подобраны случайным образом. Таким образом, периодически решая тестирование, ты всегда будешь знать свои слабые и сильные стороны.\nНапиши "начать" и тогда тестирование начнется.', 'Вот и настал этот момент,сейчас тебе придется решить 15 номеров из ЕГЭ. Задания подобраны случайным образом. Таким образом, периодически решая тестирование, ты всегда будешь знать свои слабые и сильные стороны.\nНапиши "начать" и тогда тестирование начнется.'])
        response['response']['buttons'] = [Button('Начать').get_button_object()]
        response['next_scene'] = 'start_test'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = second_scenary
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0

    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice(['Я не очень вас поняла. Скажите, пожалуйста, еще раз.', 'Я вас не расслышала. Повторите еще раз'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = 'Напишите "Тестирование" или "Задания", чтобы продолжить.'
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        response['next_scene'] = 'choice'
        response['response']['buttons'] = []

    if text == 'Помощь':
        response = build_default_response()
        response['response']['buttons'] = []
        response['response'][
            'text'] = choice([ 'Напиши "Задания", если хочешь сейчас прорешать отдельные задания. Напиши "Тестирование", если хочешь проверить уровень своих знаний', 'Напиши "Задания", и мы начнём прорешивать отдельные задания. Напиши "Тестирование", если хочешь узнать уровень своих знаний'])
        response['next_scene'] = 'choice'
    
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]

    return response


def number_task_choice(text, entity):
    response = build_default_response()
    if text.lower().split()[-1].isdigit() and 1 <= int(text.lower().split()[-1]) <= 27:
        skill.dialogs[skill.current_id].variables['task_number'].value = int(text.lower().split()[-1])
        response['response']['text'] = choice(['Вы хотите начать прорешивать задания или ознакомиться с теорией?', 'С чего начнём?'])
        response['next_scene'] = 'task_complaining'
        response['response']['buttons'] = [Button('Практика', hide=True).get_button_object(),
                                           Button('Теория', hide=True).get_button_object()
                                           ]
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = number_task_choice
    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice(['Я не очень вас поняла. Скажите, пожалуйста, еще раз.',
                                               'Мне кажется, что я не совсем поняла вас, попробуйте перефразировать или повторить запрос',
                                               'Ой, кажется такого номера не существует',
                                               'Мне очень жаль, но такого задания нет в моем каталоге, попробуйте выбрать другой номер'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = choice(['Воможно, вы хотите написать номер задания. Напишите число от 1 до 27, чтобы продолжить', 'Напишите номер задания от 1 до 27, если вы хотите прорешать задания'])
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'

        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        response['next_scene'] = 'task'

    if text == 'Помощь':
        response = build_default_response()
        response['response'][
            'text'] = choice(['Просто напишите номер задания, которое вы хотите подготовить. В ЕГЭ их 27.\nНапишите или выберите 1 из списка сверху.', 'Напишите номер задания,с которым вы работать. В ЕГЭ их 27.\nНапишите или выберите 1 из списка сверху.'])
        response['next_scene'] = 'task'
    
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
    return response


def post_teoria(text, entity):
    response = build_default_response()
    
    if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
        response['response']['text'] = choice([ 'Я не очень поняла вас. Напишите "Практика", чтобы проработать задание.\n Напишите "Задания", чтобы сменить задание.', 
                                                'Ой, кажется я не очень поняла вас.Напишите "Практика", чтобы начать работать над заданием.\n Напишите "Задания", чтобы сменить задание.' ])
    
    elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
        response['response']['text'] = choice(['Напишите "Практика", чтобы проработать задание.\n Напишите "Задания", чтобы сменить задание.',
                                               'Вы хотите прорешать задания?. Тогда напишите "Задания". Возможно, вы хотите проерить свои знания - напишите "Задания"'])
    else:
        response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
    skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
    response['response']['buttons'] = [Button('Практика', hide=True).get_button_object(),
                                       Button('Задания', hide=True).get_button_object()]
    response['next_scene'] = 'pteoria'

    if text.lower() == 'Помощь':
        response['response'][
            'text'] = 'Напишите "Практика", чтобы проработать задание.\n Напишите "Задания", чтобы сменить задание.'
        response['response']['buttons'] = [Button('Практика', hide=True).get_button_object(),
                                           Button('Задания', hide=True).get_button_object()]
        response['next_scene'] = 'pteoria'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
    
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]

    if text.lower() == 'практика':
        response = task_complaining(text, entity)
    if text.lower() == 'задания':
        response = second_scenary(text, entity)
    return response


def task_complaining(text, entity):
    response = build_default_response()
    if text.lower() == 'практика':

        task_num = skill.dialogs[skill.current_id].variables['task_number'].value
        path = f'examples\\{task_num}\\'
        filename = str(task_num) + '_' + str(randrange(1, 7)) + '.png'
        skill.dialogs[skill.current_id].variables['task_answer'].value = examples[filename][0]
        skill.dialogs[skill.current_id].variables['task_link'].value = examples[filename][1]
        task_var = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN, file=path + filename,
                         title='Попробуйте решить это задание.\nНажмите на изображение, если вам не видно текст задания')
        task_var.upload_image()
        complete_photo = BigImage(task_var)
        complete_photo.button = Button('', url=skill.dialogs[skill.current_id].variables['task_link'].value)
        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'check_answer'
        response['response']['text'] = 'Ой'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = task_complaining
        if len(examples[filename]) == 3:
            response['response']['buttons'] = [Button('Скачать файл', url=examples[filename][2]).get_button_object()]
            if task_num in ['20', '21']:
                response['response']['buttons'] = [
                    Button('Посмотреть исходное условие', url=examples[filename][2]).get_button_object()]

        if len(examples[filename]) == 4:
            response['response']['buttons'] = [Button('Скачать файл A', url=examples[filename][2]).get_button_object(),
                                               Button('Скачать файл B', url=examples[filename][3]).get_button_object()]
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
    elif text.lower() == 'теория':
        task_num = str(skill.dialogs[skill.current_id].variables['task_number'].value)
        if task_num in ['19', '20', '21']:
            task_num = '19-21'
        print(task_num)
        data = videos[task_num]
        print(data)
        buttons = []
        response['response'][
            'text'] =choice([ f'Посмотри эту теорию: {data[0]}. После просмотра напишите "Практика", чтобы прорешать задания по этому уроку.\nТакже вы можете написать "Задания", чтобы сменить задание', f'Узнать как решать задание можно сдесь: {data[0]}. После просмотра напишите "Практика", чтобы прорешать задания по этому уроку.\nТакже вы можете написать "Задания", чтобы сменить задание'])
        response['response']['buttons'] = [Button('Практика', hide=True).get_button_object(),
                                           Button('Задания', hide=True).get_button_object()]
        response['next_scene'] = 'pteoria'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0


    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice([' Я не очень вас поняла. Пожалуйста, повторите, что вы сказали.', 'Ой, кажется я не очень поняла вас. Повторите еще раз.'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = choice(['Напишите "теория" или "практика", чтобы продолжить.', 'Ой, кажется я снова не очень поняла вас. Напишите "теория" или "практика".'])
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        response['next_scene'] = 'task_complaining'
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1

    if text == 'Помощь':
        response = build_default_response()
        response['response']['text'] = choice(['Если вы хотите изучить теорию, напишите "теория", тогда вы получите видео ролик.\nЕсли вы хотите порешать задачи сами, то пишите "Практика".', 'Если вы хотите посмотреть теорию, напишите "теория", тогда вы получите некоторые примеры решения задач.\nЕсли вы увернны в своих знаниях, то пишите "Практика".'])
        response['next_scene'] = 'task_complaining'
    
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть список тем и советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]

    return response


def task_check_answer(text, entity):
    response = build_default_response()
    if skill.dialogs[skill.current_id].variables['task_answer'].value == text:
        response['response']['text'] = choice(['Всё правильно! Ты молодец. Хочешь еще решить что-нибудь?', 'фантастика!Всё правильно. Хочешь еще решить что-нибудь?'])
        response['response']['buttons'] = [Button('да', hide=True).get_button_object(),
                                           Button('нет', hide=True).get_button_object(),
                                           Button('Поменять задание', hide=True).get_button_object()]
        response['next_scene'] = 'continue'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = task_check_answer
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = task_check_answer

    else:
        answer = skill.dialogs[skill.current_id].variables['task_answer'].value
        response['response']['text'] = f'Похоже вы ошиблись. Правильный ответ: {answer}. Еще немного практики и всё получится. Хотите еще порешать заданий?'
        response['response']['buttons'] = [Button('да', hide=True).get_button_object(),
                                           Button('нет', hide=True).get_button_object(),
                                           Button('Поменять задание', hide=True).get_button_object()]
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = task_check_answer
        response['next_scene'] = 'continue'

    if text == 'Помощь':
        response = build_default_response()
        response['next_scene'] = 'check_answer'
        response['response']['text'] = choice(['Когда вы решите задачу, просто вбейте ответ, тогда система скажет, правильно ли вы ее решили.\nЕсли вам не видно содержание задания, то кликните по фотке. Если в задании требуется файл, кликните по соответствующей кнопке.\nЕсли в ответ нужно записать больше 1 числа, пишите их через пробел.',
                                         'Когда вы решите задачу, просто отправте ответ мне , тогда я вам скажу, правильно ли вы ее решили.\nЕсли вам не видно содержание задания, то кликните по фотке. Если в задании требуется файл, кликните по соответствующей кнопке.\nЕсли в ответ нужно записать больше 1 числа, пишите их через пробел.'])
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть список тем и советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
    
    return response


def continue_scene(text, entity):
    response = build_default_response()
    response['response']['text'] = choice(['Я не очень вас поняла, повторите пожалуйста еще раз', 'Ой, кажется я вас не очень поняла, повторите пожалуйста еще раз'])
    response['next_scene'] = 'continue'
    if text.lower() in ['да', 'конечно', 'го', 'давай']:
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = continue_scene
        task_num = skill.dialogs[skill.current_id].variables['task_number'].value
        path = f'examples\\{task_num}\\'
        filename = str(task_num) + '_' + str(randrange(1, 7)) + '.png'
        skill.dialogs[skill.current_id].variables['task_answer'].value = examples[filename][0]
        skill.dialogs[skill.current_id].variables['task_link'].value = examples[filename][1]
        task_var = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN, file=path + filename,
                         title='Вот еще одно задание для вас.\n Нажмите на изображение, если вам не видно текст задания')
        task_var.upload_image()
        complete_photo = BigImage(task_var)
        complete_photo.button = Button('', url=skill.dialogs[skill.current_id].variables['task_link'].value)
        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'check_answer'
        response['response']['text'] = 'Ой'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = continue_scene
        if len(examples[filename]) == 3:
            response['response']['buttons'] = [Button('Скачать файл', url=examples[filename][2]).get_button_object()]
        if len(examples[filename]) == 4:
            response['response']['buttons'] = [Button('Скачать файл A', url=examples[filename][2]).get_button_object(),
                                               Button('Скачать файл B', url=examples[filename][3]).get_button_object()]
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
    elif text.lower() in ['нет', 'неа', 'не хочу', 'хватит']:
        response['response']['text'] = 'Вы сегодня хорошо постарались. Приходите, когда захотите прорешать еще заданий.'
        response['next_scene'] = 'END'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
    elif text.lower() == 'поменять задание':
        response['response']['text'] = 'Какое задание с 1 по 27 хотите прорешать?'
        response['next_scene'] = 'task'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        skill.dialogs[skill.current_id].variables['cur_scene'].value = continue_scene
    
    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice([' Я не очень вас поняла. Пожалуйста, повторите, что вы сказали.', 'Ой, кажется я не очень поняла вас. Повторите еще раз.'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = choice(['Напишите одну из перечисленных выше команд, чтобы продолжить.', 'Выше мы написали варианты, которые вы можете выбрать.'])
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        response['next_scene'] = 'continue'

    if text == 'Помощь':
        response = build_default_response()
        response['response']['text'] = choice([ 'Напишите "да", если хотите решить еще одно подобное задание. Если вы хотите поменять номер, то напишите "Поменять задание".', 'Напишите "да",  и тогда вы сможете решить ещё одно подобное задание. Если вы хотите поменять номер, то напишите "Поменять задание".'])
        response['next_scene'] = 'continue'
    if text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть список тем и советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]
    return response


def start_test(text, entity):
    response = build_default_response()
    if text.lower() == 'начать':
        test = Test()
        for e in test.tasks:
            q = e.split('_')[0]
            break
        skill.dialogs[skill.current_id].variables['test'].value = test
        photo = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN,
                      file=f'examples\\{(test.first_p if not (19 <= int(test.first_p) <= 21) else "19-21")}\\' +
                           test.tasks[test.num],
                      title=f'Задание номер 1.\nНажмите на изображение, если вам не видно текст задания')
        photo.upload_image()
        complete_photo = BigImage(photo)
        complete_photo.button = Button('', url=test.get_task_data()['link'])
        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'testing'
        response['response']['text'] = 'Ой'
        skill.dialogs[skill.current_id].variables['wrong_count'].value = 0

    elif text.lower() == 'что ты умеешь?':
        response['response']['text'] = choice(['Вот что я умею', 'Вот что я могу' , 'Вот такие у меня возможности'])
        response['response']['text'] += ':\nПроверить ваши знания информатики во вкладке "Тестирование".\nПрорешать любые задания во вкладке "Задания".\nТакже вы можете посмотреть список тем и советы для подготовки.'
        response['next_scene'] = 'what_can'
        response['response']['buttons'] = [Button('Назад', hide=False).get_button_object(), Button('Совет', hide=False).get_button_object()]

    elif text.lower() == 'помощь':
        response['response']['text'] = choice([ 'Напиши "Начать", чтобы продолжить.', 'Если вы хотите начать тестирование - напишите "Начать"'])
        response['next_scene'] = 'continue'
    else:
        if skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 0:
            response['response']['text'] = choice([' Я не очень вас поняла. Пожалуйста, повторите, что вы сказали.', 'Ой, кажется я не очень поняла вас. Повторите еще раз.'])
        elif skill.dialogs[skill.current_id].variables['wrong_count'].value % 3 == 1:
            response['response']['text'] = choice(['Напиши "начать", чтобы начать тестирование!', 'Напиши  мне "начать", чтобы начать проверку знаний!'])
        else:
            response['response']['text'] = 'Чтобы узнать, что я умею, вы можете сказать «Что ты умеешь», а если у вас есть какие-то вопросы, то скажите: «Помощь»'
        skill.dialogs[skill.current_id].variables['wrong_count'].value += 1
        response['next_scene'] = 'start_test'

    return response


def testing_check(text, entity):
    response = build_default_response()
    test = skill.dialogs[skill.current_id].variables['test'].value
    test.next_task()
    print(skill.dialogs[skill.current_id].variables['test'].value.num)
    if test.num != 15:
        data = test.get_task_data()
        print(data)
        answer = data['answer']
        link = data['link']
        task_num = data['prototype_num']
        if 'file_link' in data:
            file_link = data['file_link']
            response['response']['buttons'] = [Button('Скачать файл', url=file_link).get_button_object()]
        if test != answer:
            test.result[task_num] += 1
            test.total += 1
            test.wrong.append(test.num + 1)

        photo = Photo(skill_id=SKILL_ID, auth_token=AUTH_TOKEN,
                      file=f'examples\\{(task_num if not (19 <= int(task_num) <= 21) else "19-21")}\\' + test.tasks[
                          test.num],
                      title=f'Задание номер {test.num + 1}.\nНажмите на изображение, если вам не видно текст задания')
        photo.upload_image()
        complete_photo = BigImage(photo)
        complete_photo.button = Button('', url=link)

        response['response']['card'] = complete_photo.get_card_object()
        response['next_scene'] = 'testing'
        response['response']['text'] = 'Ой'

    else:
        wrong = list({r for r in test.result if test.result[r] != 0})
        response['response']['text'] = choice([f'Ваш результат: {15 - test.total}/15.\n', f'Вот,что получилось у вас: {15 - test.total}/15.\n'])
        if len(wrong) == 0:
            response['response']['text'] += choice(['Ни одной ошибки! Так держать.', 'А вы умён!,Ни одной ошибки!'])
        else:
            w = ' '.join([str(i) for i in test.wrong])
            response['response'][
                'text'] += choice([f'Вы ошиблись в заданиях: {w}. Советуем обратить внимание на прототипы заданий: {" ".join(list({str(i) for i in wrong}))}.', f'Вы допустили ошибки в заданиях: {w}. Советуем прорешать этот тип заданий: {" ".join(list({str(i) for i in wrong}))}.' ])
        response['response']['text'] += choice(['\nВы хотите перейти к заданиям или решить ещё одно тестирование?', '\nВы желаете перейти к заданиям или решить ещё одно тестирование?'])
        response['response']['buttons'] = [Button('Тестирование', hide=True).get_button_object(),
                                           Button('Задания', hide=True).get_button_object()]
        response['next_scene'] = 'choice'
        skill.dialogs[skill.current_id].variables['cur_text'].value = text
        test.num = 14
        skill.dialogs[skill.current_id].variables['cur_scene'].value = testing_check

    return response


start_scene = Scene('start', skill, scenary=start, buttons=[Button('Давай', hide=True), Button('Помощь', hide=True), Button('Что ты умеешь?', hide=True)])
second_scene = Scene('choice', skill, second_scenary, buttons=[Button(str(x + 1), hide=False) for x in range(27)])
task_scene = Scene('task', skill, number_task_choice)
complete_scene = Scene('task_complaining', skill, task_complaining)
check_answer = Scene('check_answer', skill, task_check_answer)
continue_scene = Scene('continue', skill, continue_scene)
fisrt = Scene('first', skill, first_choice)
testing = Scene('testing', skill, testing_check)
start_test_scene = Scene('start_test', skill, start_test)
post_teoria_scene = Scene('pteoria', skill, post_teoria)
handler1 = Scene('handler1', skill, first_help_handler)
what_are_you_can = Scene('what_can', skill, what_are_you_can)

skill.add_scene(fisrt)
skill.add_scene(testing)
skill.add_scene(start_test_scene)
skill.add_scene(start_scene)
skill.add_scene(second_scene)
skill.add_scene(task_scene)
skill.add_scene(complete_scene)
skill.add_scene(check_answer)
skill.add_scene(continue_scene)
skill.add_scene(post_teoria)
start_skill(skill.host, skill.port)