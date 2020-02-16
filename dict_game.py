import csv
import random
import time
import zipfile
import dict_game


def main():
    pass


def read_dict(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        arr = []
        for line in reader:
            if line:
                line_dict = dict(line)
                arr.append(line_dict)
        return arr


def write_dict(path, arrdict):
    headers = arrdict[0].keys()
    with open(path, 'w', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f, headers, delimiter=';')
            f_csv.writeheader()
            f_csv.writerows(arrdict)


def write_w_str(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def write_a_str(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)


def time_now():
    return time.strftime('%d:%m:%y  %H:%M:%S')


def timedelta(start, end):
    hour, minute, second = 0, 0, 0
    delta = int(end - start)
    if delta < 60:
        second = delta
    elif 60 <= delta < 3600:
        minute = delta // 60
        second = delta % 60
    else:
        hour = delta // 3600
        minute = (delta % 3600) // 60
        second = (delta % 3600) & 60
    arr_delta = ['Время в игре:', str(hour), 'ч.',
                 str(minute), 'м.', str(second), 'с.']
    text = ' '.join(arr_delta)
    return text


def arr_center_text(arr, num)-> list:
    for i in range(len(arr)):
        arr[i] = arr[i].center(num)
    return arr


class DictGame():

    # варианты ответов при ошибке
    NO1 = 'Неправильно! это '
    NO2 = 'Напишите еще раз '
    NO3 = 'Вы ошиблись, напишите правильно '
    # счетчик правильных ответов
    COUNTGAMEOVER = 2
    # пути к словарям
    CHANGEDICT = 'dict/change_dict.csv'
    NOTIFICATION = 'dict/notification.csv'
    FULLDICT = 'zipdict/full_dict.zip'
    LOGFILE = 'log.txt'
    CRASHFILE = 'crash.txt'
    # значение центра в лог-файле
    CENTERLOGFILE = 100

    def __init__(self):
        '''
        __correct - число правильных ответов
        __incorrect - число неправильных ответов
        __count_incorrect - сколько раз повторять правильный ответ при ошибке
        __rus - русское слово
        __eng - английское слово для проверки
        __my_eng - английское слово, введенное пользователем
        __notification - хвалит или ругает за ответ
        __correct_answer - хранит правильный ответ с пожеланиями
        __game_result - хранит всю информацию при каждом ответе игрока
        __remove_data - разрешает удалять данные из словаря
        __gameover - признак окончания игры
        __dict_random_data - словарь со случайным словами(русское и английское)
        __dict_data - заголовок словаря в файле и путь к файлу
        __notifications - словарь с похвалой или руганием за ответ
        __arr_pathdict - словарь с именами и путями к словарям
        __pathdict - путь к словарю
        __namedict - имя словаря
        __numstr_headlogfile - количество строк в заголовке лог-файла
        __count_wordsdict - количество слов в выбранном словаре
        '''
        self.__correct = 0
        self.__incorrect = 0
        self.count_incorrect = 0
        self.__rus = ''
        self.__eng = ''
        self.__my_eng = ''
        self.__notification = ''
        self.__correct_answer = ''
        self.__game_result = ''
        self.__remove_data = False
        self.__gameover = False
        self.__dict_random_data = {}
        self.__dict_data = []
        self.__time_startgame = 0
        self.__time_endgame = 0
        self.__notifications = read_dict(self.NOTIFICATION)
        self.__arr_pathdict = read_dict(self.CHANGEDICT)
        self.__pathdict = ''
        self.__namedict = ''
        self.__numstr_headlogfile = 0
        self.__count_wordsdict = 0

    def __set_nameandpathdict(self, namedict):
        '''записываем в переменные имя и путь к словарю'''
        self.__namedict = namedict
        for line in self.__arr_pathdict:
            if line['Name'] == self.__namedict:
                self.__pathdict = line["Path"]
                break

    def __create_dict_words(self):
        '''создаем словарь для игры'''
        self.__arr_dict = read_dict(self.__pathdict)
        if len(self.__arr_dict) <= self.COUNTGAMEOVER:
            with zipfile.ZipFile(self.FULLDICT, 'r') as z:
                z.extract(self.__pathdict)
            self.__arr_dict = read_dict(self.__pathdict)
        else:
            self.__remove_data = True
        self.__count_wordsdict = len(self.__arr_dict)

    def __create_heading_log_file(self):
        '''заголовок лог-файла'''
        parts = []
        text = ('Словарь - ' + self.__namedict).center(self.CENTERLOGFILE)
        parts.append(text)
        text = time_now().center(self.CENTERLOGFILE)
        parts.append(text)
        arr_text = ['rus', 'eng', 'my_eng', 'YES', 'NO']
        arr_text = arr_center_text(arr_text, 18)
        text = '|' + '|'.join(arr_text) + '|'
        parts.append(text)
        text = '=' * 100
        parts.append(text)
        text = '\n'.join(parts)
        self.__game_result = text
        self.__numstr_headlogfile = len(parts)

    def create_log_file(self, text):
        write_a_str(self.LOGFILE, text)

    def create_crash_file(self, text):
        write_a_str(self.CRASHFILE, text)

    def timedelta_game(self):
        return timedelta(self.__time_startgame, self.__time_endgame)

    def initgame(self, namedict):
        '''namedict - имя выбранного словаря'''
        self.__set_nameandpathdict(namedict)
        self.__create_heading_log_file()
        self.__create_dict_words()
        self.__time_startgame = time.monotonic()

    def random_word(self):
        '''выбираем случайное слово из словаря'''
        if len(self.__arr_dict) > 0:
            self.__dict_random_data = random.choice(self.__arr_dict)
            self.__rus = self.__dict_random_data['Russian']
            self.__eng = self.__dict_random_data['English']

    def game_over(self):
        self.__gameover = True
        self.__time_endgame = time.monotonic()
        write_dict(self.__pathdict, self.__arr_dict)

    def game(self):
        '''запускает игру: напиши правильно перевод'''
        game_level_win = False
        if self.count_incorrect == 0:
            notific = random.choice(self.__notifications)
            if self.__eng == self.my_eng:
                self.__correct += 1
                self.__notification = notific['correct']
                if self.__remove_data:
                    self.__arr_dict.remove(self.__dict_random_data)
                    self.__count_wordsdict -= 1
                game_level_win = True
            else:
                self.count_incorrect += 1
                self.__incorrect += 1
                self.__notification = notific['incorrect']
                self.__correct_answer = self.NO3 + self.__eng
        elif 0 < self.count_incorrect < 3:
            if self.__eng == self.my_eng:
                self.__correct_answer = self.NO2 + self.__eng
                self.count_incorrect += 1
            else:
                self.__correct_answer = self.NO3 + self.__eng
        else:
            if self.__eng == self.my_eng:
                self.count_incorrect = 0
                self.__correct_answer = 'Вы молодец '
                game_level_win = True
            else:
                self.__correct_answer = self.NO3 + self.__eng
        self.__game_result = '|' + '|'.join(self.get_text_result()) + '|'
        if game_level_win:
            if self.correct >= self.COUNTGAMEOVER:
                self.game_over()
            else:
                self.random_word()

    def get_text_result(self):
        '''возвращает кортеж данных игры в строчном виде'''
        text = [self.__rus, self.__eng, self.__my_eng,
                str(self.__correct), str(self.__incorrect)]
        text = arr_center_text(text, 18)
        return tuple(text)

    def get_tuple_namesdict(self):
        '''возвращает кортеж с именами словарей'''
        names = []
        for line in self.__arr_pathdict:
            names.append(line['Name'])
        return tuple(names)

    @property
    def my_eng(self):
        return self.__my_eng

    @my_eng.setter
    def my_eng(self, eng):
        self.__my_eng = eng

    @property
    def eng(self):
        return self.__eng

    @property
    def rus(self):
        return self.__rus

    @property
    def correct(self):
        return self.__correct

    @property
    def incorrect(self):
        return self.__incorrect

    @property
    def notification(self):
        return self.__notification

    @property
    def correct_answer(self):
        return self.__correct_answer

    @property
    def gameover(self):
        return self.__gameover

    @property
    def game_result(self):
        return self.__game_result

    @property
    def arr_dict(self):
        return self.__arr_dict

    @property
    def arr_pathdict(self):
        return self.__arr_pathdict

    @property
    def numstr_headlogfile(self):
        return self.__numstr_headlogfile

    @property
    def count_wordsdict(self):
        return self.__count_wordsdict


if __name__ == '__main__':
    main()
