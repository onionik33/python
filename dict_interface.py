import tkinter as tk
import dict_game as dgame


def main():
    d = DictInterface()


class DictInterface():

    COUNTWORDSDICT = 'Кол-во слов в словаре:'

    def __init__(self):
        '''
        main_window - главное окно
        rusword - русское слово для перевода
        engword - английское слово, вводимое игроком
        name_dict - имя выбранного словаря
        count_str_log_text - в какую строку лог-файла записывать текст
        countwords - количество слов в словаре
        correct - количество правильных ответов
        incorrect - количество неправильных ответов
        '''
        self.main_window = tk.Tk()
        self.main_window.title('Dictionary')
        self.main_window.config(bg='blue')
        self.main_window.protocol('WM_DELETE_WINDOW', self.window_delete)
        # переменные
        self.game = dgame.DictGame()
        self.rusword = tk.StringVar()
        self.engword = tk.StringVar()
        self.correct_answer = tk.StringVar()
        self.name_dict = tk.StringVar()
        self.notification = tk.StringVar(value='Кирилл! Я в тебя верю')
        self.countwords = tk.IntVar(value=0)
        self.correct = tk.IntVar(value=0)
        self.incorrect = tk.IntVar(value=0)
        self.count_str_log_text = 0.0
        # вызов функций
        self.create_title_frame()
        self.create_dict_frame()
        self.create_result_frame()
        self.create_choice_dict_frame()
        self.create_log_frame()
        self.main_window.mainloop()

    def window_delete(self):
        if not self.game.gameover:
            self.log_text.insert(
                self.count_str_log_text,
                dgame.time_now().center(self.game.CENTERLOGFILE) + '\n')
            self.game.create_crash_file(self.log_text.get(0.0, tk.END))
        self.main_window.destroy()

    def create_title_frame(self):
        # Frame
        title_frame = tk.LabelFrame(
            self.main_window, bg='orange', bd=5, text='title')
        title_frame.pack(expand=0)
        # кнопка старт
        self.btn_start = tk.Button(
            title_frame, text='START', font='14')
        self.btn_start.config(command=self.press_btn_start)
        self.btn_start.pack(side='left', padx=5, pady=10)
        # метка с названием словаря
        lbl_title_dict = tk.Label(
            title_frame, textvariable=self.name_dict, width=34)
        lbl_title_dict.config(font='bold 14', bg='orange')
        lbl_title_dict.pack(side='left', padx=5, pady=10)
        lbl_countwords_dict = tk.Label(
            title_frame, text=self.COUNTWORDSDICT, width=18)
        lbl_countwords_dict.config(font='bold 14', bg='orange')
        lbl_countwords_dict.pack(side='left', padx=5, pady=10)
        # метка со счетчиком слов в словаре
        lbl_countwords = tk.Label(title_frame, textvariable=self.countwords,
                                  font=('bold', 14), bg='gray', width=3)
        lbl_countwords.config(font=('bold', 14), bg='gray', width=3)
        lbl_countwords.pack(side='left', padx=5, pady=5)

    def create_dict_frame(self):
        # Frame
        dict_frame = tk.LabelFrame(
            self.main_window, bg='green', bd=5, text='dict')
        dict_frame.pack(expand=0)
        # метка с 'Переведите слово'
        lbl_title_dict = tk.Label(dict_frame, text='Переведите слово:')
        lbl_title_dict.config(font='bold 14', bg='green')
        lbl_title_dict.pack(side='left', padx=10, pady=10)
        # метка с русским словом
        lbl_rusword = tk.Label(
            dict_frame, textvariable=self.rusword, width=40)
        lbl_rusword.config(font='bold 14', bg='green', fg='orange')
        lbl_rusword.pack(side='top', padx=10, pady=10)
        # поле для ввода английского слова
        self.entry_engword = tk.Entry(
            dict_frame, textvariable=self.engword, font='bold 14')
        self.entry_engword.config(bd=5, width=45)
        self.entry_engword.bind('<Return>', self.game_dict)
        self.entry_engword.pack(side='top', padx=10, pady=10)
        # метка с правильным ответом
        lbl_correct_answer = tk.Label(
            dict_frame, textvariable=self.correct_answer, width=40)
        lbl_correct_answer.config(
            font='bold 14', bg='green', fg='purple')
        lbl_correct_answer.pack(side='bottom', padx=10, pady=10)

    def create_result_frame(self):
        # Frame
        result_frame = tk.LabelFrame(
            self.main_window, bg='gray', bd=5, text='result')
        result_frame.pack()
        # метка правильно или нет
        lbl_notification = tk.Label(
            result_frame, textvariable=self.notification)
        lbl_notification.config(bg='gray', width=52, font='bold 14')
        lbl_notification.pack(side='left')
        # метка ответы
        lbl_title_result = tk.Label(result_frame, text='Ответы:')
        lbl_title_result.config(
            font=('bold', 14), bg='gray', fg='purple')
        lbl_title_result.pack(side='left', padx=10, pady=10)
        # метка с числом правильных ответов
        lbl_correct = tk.Label(result_frame, textvariable=self.correct)
        lbl_correct.config(font=('bold', 14), bg='green', width=3)
        lbl_correct.pack(side='top', padx=5, pady=5)
        # метка с числом неправильных ответов
        lbl_incorrect = tk.Label(result_frame, textvariable=self.incorrect)
        lbl_incorrect.config(font=('bold', 14), bg='red', width=3)
        lbl_incorrect.pack(side='left', padx=5, pady=5)

    def create_choice_dict_frame(self):
        '''окно выбора словаря'''
        # Frame
        self.change_dict_frame = tk.LabelFrame(
            self.main_window, bg='red', bd=5, text='change_dict')
        self.change_dict_frame.pack()
        # флажки выбора словаря
        # self.flag = tk.StringVar()
        namesdict = self.game.get_tuple_namesdict()
        self.name_dict.set(namesdict[0])
        # создаем группу флажков по количеству словарей
        for name in namesdict:
            self.create_radiobut(self.change_dict_frame,
                                 name, self.name_dict, name)

    def create_radiobut(self, master, text, variable, value):
        radiobut = tk.Radiobutton(
            master, text=text, variable=variable, value=value, bg='red')
        radiobut.config(font=('bold', 8))
        radiobut.pack(side='left', padx=2, pady=5)
        return radiobut

    def create_log_frame(self):
        # Frame
        self.log_frame = tk.LabelFrame(
            self.main_window, bd=5, text='log_text')
        self.log_frame.pack()
        # поле для текста
        self.log_text = tk.Text(self.log_frame, width='100')
        self.log_text.pack(side='left')
        # прокрутка текста
        scroll = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        scroll.pack(side='left', fill='y')
        self.log_text.config(yscrollcommand=scroll.set)

    def press_btn_start(self):
        '''запускаем игру'''
        self.btn_start.config(state='disable')
        self.entry_engword.focus_set()
        self.game.initgame(self.name_dict.get())
        self.count_str_log_text = float(self.game.numstr_headlogfile + 1)
        self.countwords.set(self.game.count_wordsdict)
        # выбираем случайное слово
        self.game.random_word()
        self.log_text.insert(1.0, self.game.game_result + '\n')
        # в метку вписываем русское слово для перевода
        self.rusword.set(self.game.rus)

    def game_dict(self, event):
        '''срабатывает при вводе слова и нажатии на Enter'''
        self.game.my_eng = event.get()
        self.game.game()
        self.countwords.set(self.game.count_wordsdict)
        self.log_text.insert(self.count_str_log_text,
                             self.game.game_result + '\n')
        self.count_str_log_text += 1
        self.correct_answer.set(self.game.correct_answer)
        self.notification.set(self.game.notification)
        self.correct.set(self.game.correct)
        self.incorrect.set(self.game.incorrect)
        self.rusword.set(self.game.rus)
        self.entry_engword.delete(0, tk.END)
        self.game_over()

    def game_over(self):
        if self.game.gameover:
            self.rusword.set('')
            self.entry_engword.config(state='disable')
            self.notification.set('Вы закончили')
            timenow = dgame.time_now().center(self.game.CENTERLOGFILE) + '\n'
            delta = self.game.timedelta_game().center(self.game.CENTERLOGFILE)
            self.log_text.insert(
                self.count_str_log_text, timenow + delta + '\n')
            self.game.create_log_file(self.log_text.get(0.0, tk.END))


if __name__ == '__main__':
    main()
