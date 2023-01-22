from random import choice

#функция ввода и его проверки, работает в двух режимах
# - перед стартом сессии проверяет желание играть (режим start)
# - внутри сессии проверяет вводимые буквы (режим letter)
def check_input(word='', tried_letters=[], mode='start'):
    if mode == 'start':
        while True:
            user_input = input('''Введите (1 - начать новую игру, 2 - завершить игру): ''')
            if user_input == '1':
                return True
            elif user_input == '2':
                return False
            else: print('\nЯ вас не понял')

    elif mode == 'letter':
        while True:
            user_input = input('Введите любую букву на кириллице:').lower()
            if user_input in [chr(_) for _ in range(1072, 1104)]:
                if user_input in tried_letters: print(f"Вы уже пробовали эту букву, введите другую")
                elif user_input in word:
                    print(f"Отлично, вы угадали букву\n")
                    return True, user_input
                else:
                    return False, user_input
            else:
                print('Некорректный ввод.', end=' ')


# функция загрузки ассетов, принимает словарь,"картинки" виселицы и кодировку
def load_assets(words='resdictionary2.txt', pics='hangman.txt', enc='UTF-8'):
    with open(words, encoding=enc) as dictionary, open(pics, encoding=enc) as hangman:
        content = dictionary.readlines()
        word = choice(content).rstrip()
        hangman_pics = hangman.read().split(',')
        assets = (word, hangman_pics)
        return assets


# функция показа игровой доски со словом и сокрытием неотгаданных символов
def show_board(word, guessedletters, top='_', delimiter='|'):
    wordlist = list(word)
    for i, v in enumerate(wordlist):
        if v in guessedletters:
            wordlist[i] = v
        else:
            wordlist[i] = '*'
    print(top * len(wordlist) * 2)
    print('\033[1m' + delimiter + delimiter.join(wordlist) + delimiter + '\033[0m')
    print(top * len(wordlist) * 2)


# функция основной игры, принимает загаданное слово и "картинки" виселицы
def run_main_game(word, hangman_pics):
    tried_letters = []
    guessed_letters = []
    livesleft = len(hangman_pics) - 1
    session_running = 1

    # основной цикл сессии выводит виселицу, текущий статус, слово и модифицирует статус в зависимости от угадывания
    while game_running and session_running:
        print('\033[0;34m' + hangman_pics[len(hangman_pics) - livesleft - 1] + '\n\033[0;30m')
        print(f"Загадано слово из {len(word)} букв. Вы угадали {len(guessed_letters)} букв. Осталось {livesleft} жизней\n")

        show_board(word, guessed_letters)

        res = check_input(word, tried_letters, mode='letter')
        if res[0]:
            guessed_letters.append(res[1])
            tried_letters.append(res[1])
        else:
            tried_letters.append(res[1])
            livesleft -= 1

        if len(set(guessed_letters)) == len(set(word)):
            print(f'\033[1mПоздравляем вы выиграли!\n\033[0m')
            session_running = 0

        if livesleft == 0:
            print(f'\033[1mК сожалению, вы проиграли\n\033[0m')
            session_running = 0


if __name__ == '__main__':
    print('\033[1mДобро пожаловать в Hangman!\nХотите сыграть?\n\033[0m')
    game_running = True

    # основной цикл игры
    while game_running:
        if check_input(mode='start'):
            run_main_game(*load_assets())
            print('Cыграем еще раз?', end=' ')
        else:
            game_running = False
    else:
        print('\n\033[1mCпасибо за интерес к Hangman\033[0m')