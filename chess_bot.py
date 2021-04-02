# пока что нет возможности отката ходов пешки, дошедшей до противоположной горизонтали, остальное работает


import re
import time
import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)


def round_game():
    game_on = True  # при каких условиях game_on = False (т.е. игра кончается)
    winner = ''
    winner_points = 0
    while game_on:
        global letters, dict_for_letters, dict_for_numbers
        dict_for_letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        dict_for_numbers = {str(i + 1): 7 - i for i in range(0, 8)}
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        def get_lines(string, reverse=0):  # reverse=1 возвращает твою фигуру, которой нападаешь
            if reverse == 0:
                line = dict_for_numbers[string[3]]
                column = dict_for_letters[string[2]]
                figure = obj.board[line][column]
            else:
                line = dict_for_numbers[string[1]]
                column = dict_for_letters[string[0]]
                figure = obj.board[line][column]
            return figure

        def make_figures():
            figures_white, figures_black = [], []
            for i in range(8):
                figures_white.append(Pawn('P', 'white'))
                figures_black.append(Pawn('p', 'black'))

            for i in range(2):
                figures_white.append(Rook('R', 'white'))
                figures_black.append(Rook('r', 'black'))

                figures_white.append(Knight('N', 'white'))
                figures_black.append(Knight('n', 'black'))

                figures_white.append(Bishop('B', 'white'))
                figures_black.append(Bishop('b', 'black'))

            figures_white.append(Queen('Q', 'white'))
            figures_black.append(Queen('q', 'black'))

            figures_white.append(King('K', 'white'))
            figures_black.append(King('k', 'black'))

            return figures_white, figures_black

        def is_free(string):
            line = dict_for_numbers[string[1]]
            column = dict_for_letters[string[0]]
            if obj.board[line][column] == '•':
                return True
            else:
                return obj.board[line][column]

        def check_horizontal(pawn):  # pawn can be 'A8'
            my_color = is_free(pawn).color
            print(f'\tВыберите фигуру, на которую хотите заменить пешку {pawn}')
            print('\tЧтобы выбрать ферзя, нажмите 1')
            print('\tЧтобы выбрать коня, нажмите 2')
            print('\tЧтобы выбрать слона, нажмите 3')
            print('\tЧтобы выбрать ладью, нажмите 4')
            flag = False
            while not flag:
                cho = input('\tВаш выбор: ')
                if cho == '1':
                    obj.board[dict_for_numbers[pawn[1]]][dict_for_letters[pawn[0]]] = Queen('Q' if my_color == 'white' else 'q', my_color)
                    flag = True
                if cho == '2':
                    obj.board[dict_for_numbers[pawn[1]]][dict_for_letters[pawn[0]]] = Knight('N' if my_color == 'white' else 'n', my_color)
                    flag = True
                if cho == '3':
                    obj.board[dict_for_numbers[pawn[1]]][dict_for_letters[pawn[0]]] = Bishop('B' if my_color == 'white' else 'b', my_color)
                    flag = True
                if cho == '4':
                    obj.board[dict_for_numbers[pawn[1]]][dict_for_letters[pawn[0]]] = Rook('R' if my_color == 'white' else 'r', my_color)
                    flag = True
                else:
                    print('Введены неправильные данные!')
                    continue
            return True

        class Board(object):
            def __init__(self):
                self.border = ['   ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                self.board = [['•'] * 8 for _ in range(8)]
                self.count = 0  # если чётное, то очередь белых
                self.logger = []  # сюда сбрасываем все выполненные ходы
                self.white_point = 0
                self.black_point = 0

            def create_fields(self, whites, blacks):
                for i in range(8):  # заполняем пешками
                    self.board[1][i] = blacks[i]
                    self.board[6][i] = whites[i]
                for i in range(3):  # заполняем три фигуры слева и справа
                    self.board[0][i] = blacks[8 + i]
                    self.board[7][i] = whites[8 + i]
                    self.board[0][7 - i] = blacks[11 + i]
                    self.board[7][7 - i] = whites[11 + i]
                for i in range(2):
                    self.board[0][i + 3] = blacks[14 + i]
                    self.board[7][i + 3] = whites[14 + i]

            def show(self):
                print()
                print(*self.border, '\n')
                for i in range(8):
                    print(8 - i, ' ', end=' ')
                    for j in range(8):
                        if self.board[i][j] != '•':
                            if (i+j) % 2 == 0:
                                if self.board[i][j].color == 'black':
                                    print(f'{Back.GREEN}{Fore.LIGHTWHITE_EX}{self.board[i][j].typing} ', end='')
                                elif self.board[i][j].color == 'white':
                                    print(f'{Back.GREEN}{Fore.LIGHTWHITE_EX}{self.board[i][j].typing} ', end='')
                            else:
                                if self.board[i][j].color == 'black':
                                    print(f'{Back.RED}{Fore.LIGHTWHITE_EX}{self.board[i][j].typing} ', end='')
                                elif self.board[i][j].color == 'white':
                                    print(f'{Back.RED}{Fore.LIGHTWHITE_EX}{self.board[i][j].typing} ', end='')
                        else:
                            if (i+j) % 2 == 0:
                                print(f'{Back.GREEN}{Fore.GREEN}• ', end='')
                            else:
                                print(f'{Back.RED}{Fore.RED}• ', end='')
                    print(' ', 8 - i)
                print()
                print(*self.border)
                print()
                print(f'\tPlayer: {self.counter()}')

            def counter(self):
                if self.count % 2 == 0:
                    return 'white'
                else:
                    return 'black'

            def replace_field(self, string):
                self.board[dict_for_numbers[string[3]]][dict_for_letters[string[2]]], \
                    self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]] = \
                    self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]], \
                    self.board[dict_for_numbers[string[3]]][dict_for_letters[string[2]]]

                self.logger.append(string)

            def remove_field(self, string):
                # начисляем очки за съедение
                him_figure = get_lines(string)
                if him_figure.color == 'white':
                    self.black_point += him_figure.price
                else:
                    self.white_point += him_figure.price
                # процесс съедения
                self.board[dict_for_numbers[string[3]]][dict_for_letters[string[2]]] = \
                    self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]]
                self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]] = '•'

                self.logger.append((string, him_figure))

            def attack(self, string):
                # переставляем нашу пешку
                self.board[dict_for_numbers[string[3]]][dict_for_letters[string[2]]], \
                    self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]] = \
                    self.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]], \
                    self.board[dict_for_numbers[string[3]]][dict_for_letters[string[2]]]
                # убираем пешку соперника и начисляем очки
                column = string[2]
                my_figure = get_lines(string)
                if my_figure.color == 'white':
                    line = str(int(string[3]) - 1)
                    self.white_point += my_figure.price
                else:
                    line = str(int(string[3]) + 1)
                    self.black_point += my_figure.price

                him_figure = self.board[dict_for_numbers[line]][dict_for_letters[column]]
                self.board[dict_for_numbers[line]][dict_for_letters[column]] = '•'
                self.logger.append((string, him_figure, 'prohod'))

            def castling(self, string):
                if abs(letters.index(string[0]) - letters.index(string[2])) == 3:
                    # перестановка короля
                    self.board[dict_for_numbers[string[1]]][dict_for_letters['E']], self.board[dict_for_numbers[string[1]]][dict_for_letters['G']] = \
                        self.board[dict_for_numbers[string[1]]][dict_for_letters['G']], self.board[dict_for_numbers[string[1]]][dict_for_letters['E']]
                    # перестановка ладьи
                    self.board[dict_for_numbers[string[1]]][dict_for_letters['H']], self.board[dict_for_numbers[string[1]]][dict_for_letters['F']] = \
                        self.board[dict_for_numbers[string[1]]][dict_for_letters['F']], self.board[dict_for_numbers[string[1]]][dict_for_letters['H']]
                    self.logger.append('O-O')

                else:
                    # перестановка короля
                    self.board[dict_for_numbers[string[1]]][dict_for_letters['E']], self.board[dict_for_numbers[string[1]]][dict_for_letters['C']] = \
                        self.board[dict_for_numbers[string[1]]][dict_for_letters['C']], self.board[dict_for_numbers[string[1]]][dict_for_letters['E']]
                    # перестановка ладьи
                    self.board[dict_for_numbers[string[1]]][dict_for_letters['A']], self.board[dict_for_numbers[string[1]]][dict_for_letters['D']] = \
                        self.board[dict_for_numbers[string[1]]][dict_for_letters['D']], self.board[dict_for_numbers[string[1]]][dict_for_letters['A']]
                    self.logger.append('O-O-O')

        class Pawn(object):
            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 1

            def can_move_to(self, string):  # string = [A-H][1-8][A-H][1-8]
                other_figure = get_lines(string)
                if self.color == 'white':
                    if string[0] == string[2]:
                        if int(string[3]) - int(string[1]) == 1:
                            if other_figure == '•':
                                obj.replace_field(string)
                                if string[-1] == '8':
                                    check_horizontal(string[2:4])
                                return True
                            else:
                                return False
                        if int(string[3]) - int(string[1]) == 2:
                            new_string = string[0:-1] + str(int(string[-1]) - 1)
                            if other_figure == '•' and get_lines(new_string) == '•' and string[1] == '2':
                                obj.replace_field(string)
                                return True
                            else:
                                return False
                        else:
                            return False
                    elif abs(letters.index(string[0]) - letters.index(string[2])) == 1:
                        if int(string[3]) - int(string[1]) == 1:
                            him_pawn = get_lines(f'{string[2]}7{string[2]}5')
                            if other_figure == '•' and (string[1] == '5') and (obj.logger[-1] == f'{string[2]}7{string[2]}5') and (him_pawn.typing == 'p'):
                                obj.attack(string)
                                return True
                            elif other_figure == '•':
                                return False
                            elif other_figure.color == 'white':
                                return False
                            else:
                                obj.remove_field(string)
                                if string[-1] == '8':
                                    check_horizontal(string[2:4])
                                return True
                        else:
                            return False
                    else:
                        return False
                else:
                    if string[0] == string[2]:
                        if int(string[1]) - int(string[3]) == 1:
                            if other_figure == '•':
                                obj.replace_field(string)
                                if string[-1] == '1':
                                    check_horizontal(string[2:4])
                                return True
                            else:
                                return False
                        if int(string[1]) - int(string[3]) == 2:
                            new_string = string[0:-1] + str(int(string[-1]) + 1)
                            if other_figure == '•' and get_lines(new_string) == '•' and string[1] == '7':
                                obj.replace_field(string)
                                return True
                            else:
                                return False
                        else:
                            return False
                    elif abs(letters.index(string[0]) - letters.index(string[2])) == 1:
                        if int(string[1]) - int(string[3]) == 1:
                            him_pawn = get_lines(f'{string[2]}2{string[2]}4')
                            if other_figure == '•' and (string[1] == '4') and (obj.logger[-1] == f'{string[2]}2{string[2]}4') and (him_pawn.typing == 'P'):
                                obj.attack(string)
                                return True
                            elif other_figure == '•':
                                return False
                            elif other_figure.color == 'black':
                                return False
                            else:
                                obj.remove_field(string)
                                if string[-1] == '1':
                                    check_horizontal(string[2:4])
                                return True
                        else:
                            return False
                    else:
                        return False

        class Rook(object):
            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 5
                self.move = 0

            def can_move_to(self, string):
                my_figure = get_lines(string, reverse=True)
                him_figure = get_lines(string)
                if string[0] == string[2]:  # работаем со столбцом
                    for i in range(1, abs(int(string[3]) - int(string[1]))):
                        if type(is_free(string[0] + f'{int(string[1]) + i if self.color == "white" else (int(string[1]) - i)}')) == bool:
                            continue
                        else:
                            return False
                    if him_figure == '•':
                        obj.replace_field(string)
                        self.move = 1
                        return True
                    elif him_figure.color == my_figure.color:
                        return False
                    else:
                        obj.remove_field(string)
                        self.move = 1
                        return True

                elif string[1] == string[3]:  # работаем со строкой
                    for i in range(1, abs(letters.index(string[0]) - letters.index(string[2]))):
                        if type(is_free(f'{letters[letters.index(string[0])+i] if letters.index(string[0])<letters.index(string[2]) else letters[letters.index(string[0])-i]}' + string[1])) == bool:
                            continue
                        else:
                            return False
                    if him_figure == '•':
                        obj.replace_field(string)
                        self.move = 1
                        return True
                    elif him_figure.color == my_figure.color:
                        return False
                    else:
                        obj.remove_field(string)
                        self.move = 1
                        return True
                else:
                    return False

        class Knight(object):
            new_letters = ['-1', '-1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '-1', '-1']

            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 3

            def can_move_to(self, string):  # либо соседние буквы и цифры отличаются на два, либо буквы через одну и цифры отличаются на одну
                other_figure = get_lines(string)
                if (abs(letters.index(string[0]) - letters.index(string[2])) == 1 and abs(
                        int(string[1]) - int(string[3])) == 2) or (
                        abs(letters.index(string[0]) - letters.index(string[2])) == 2 and abs(
                        int(string[1]) - int(string[3])) == 1):
                    if other_figure == '•':
                        obj.replace_field(string)
                        return True
                    elif other_figure.color == self.color:
                        return False
                    else:
                        obj.remove_field(string)
                        return True

        class Bishop(object):
            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 3

            def can_move_to(self, string):
                my_figure = get_lines(string, reverse=True)
                him_figure = get_lines(string)
                if abs(int(string[3]) - int(string[1])) == abs(letters.index(string[0]) - letters.index(string[2])):
                    # 1 ситуация, когда идем по буквам слева направо
                    if letters.index(string[0]) < letters.index(string[2]):
                        for i in range(1, abs(int(string[3]) - int(string[1]))):
                            if type(is_free(f'{letters[letters.index(string[0])+i]}' + (f'{int(string[1])+i}' if int(string[3]) > int(string[1]) else f'{int(string[1])-i}'))) == bool:
                                continue
                            else:
                                return False
                        if him_figure == '•':
                            obj.replace_field(string)
                            return True
                        elif type(him_figure) != str and him_figure.color == my_figure.color:
                            return False
                        else:
                            obj.remove_field(string)
                            return True
                    # 2 ситуация, когда идём справа налево по буквам
                    elif letters.index(string[0]) > letters.index(string[2]):
                        for i in range(1, abs(int(string[3]) - int(string[1]))):
                            if type(is_free(f'{letters[letters.index(string[0])-i]}' + (f'{int(string[1])+i}' if int(string[3]) > int(string[1]) else f'{int(string[1])-i}'))) == bool:
                                continue
                            else:
                                return False
                        if him_figure == '•':
                            obj.replace_field(string)
                            return True
                        elif him_figure.color == my_figure.color:
                            return False
                        else:
                            obj.remove_field(string)
                            return True
                else:
                    return False

        class King(object):
            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 100
                self.move = 0

            def can_move_to(self, string):  # модуль разности букв не больше 1 и модуль разности чисел не больше 1
                if (abs(letters.index(string[0]) - letters.index(string[2])) <= 1) and abs((int(string[3]) - int(string[1])) <= 1):
                    if get_lines(string) == '•':
                        obj.replace_field(string)
                        self.move = 1
                        return True
                    else:
                        if get_lines(string).color == self.color:
                            return False
                        else:
                            obj.remove_field(string)
                            self.move = 1
                            return True
                elif self.move == 0:
                    other_figure = get_lines(string)
                    if other_figure != '•':
                        if other_figure.color == self.color and type(other_figure) == Rook:
                            if other_figure.move == 0:
                                for i in range(abs(letters.index(string[0]) - letters.index(string[2]))):
                                    if is_free(f'{letters[letters.index(string[0]) + i] if letters.index(string[0]) < letters.index(string[2]) else letters[letters.index(string[0]) - i]}' + string[1]):
                                        continue
                                    else:
                                        return False
                                obj.castling(string)
                                self.move = 1
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False

        class Queen(object):
            def __init__(self, typing, color):
                self.typing = typing
                self.color = color
                self.price = 9
                self.move = 0

        class BackToThePast(object):
            def __init__(self):
                self.current_list = []

            def back_step(self):
                if len(obj.logger) > 0:
                    # реализация отката обычного перемещения
                    self.current_list.append(obj.logger.pop())      # забираем последний ход из obj.logger
                    last_hod = self.current_list[-1]
                    if type(last_hod) == str and last_hod != 'O-O-O' and last_hod != 'O-O':
                        obj.replace_field(last_hod[2:4]+last_hod[0:2])
                        # убираем запись из основного массива, которая автоматом создается при использовании функции
                        obj.logger.pop()
                        obj.show()
                    elif len(last_hod) == 2:
                        obj.replace_field(last_hod[0][2:4] + last_hod[0][0:2])
                        obj.logger.pop()
                        self.input_enemy(last_hod[1], last_hod[0][2:4])
                        obj.show()
                    elif last_hod == 'O-O-O':
                        if len(obj.logger) % 2 == 0:
                            self.uncastling_triple('1')
                        else:
                            self.uncastling_triple('8')
                        obj.show()
                    elif last_hod == 'O-O':
                        if len(obj.logger) % 2 == 0:
                            self.uncastling_double('1')
                        else:
                            self.uncastling_double('8')
                        obj.show()
                    elif 'prohod' in last_hod:
                        obj.replace_field(last_hod[0][2:4] + last_hod[0][0:2])
                        obj.logger.pop()
                        if len(obj.logger) % 2 == 0:
                            self.input_enemy(last_hod[1], last_hod[0][2]+str(int(last_hod[0][3])-1))
                        else:
                            self.input_enemy(last_hod[1], last_hod[0][2] + str(int(last_hod[0][3]) - 1))
                        obj.show()
                else:
                    print('Вы в начале партии!')

            def input_enemy(self, other, string):       # возвращаем врага на карту, начисляем очки
                obj.board[dict_for_numbers[string[1]]][dict_for_letters[string[0]]] = other
                if other.color == 'white':
                    obj.black_point -= other.price
                else:
                    obj.white_point -= other.price

            def uncastling_triple(self, line):
                obj.board[dict_for_numbers[line]][dict_for_letters['A']] = obj.board[dict_for_numbers[line]][dict_for_letters['D']]
                obj.board[dict_for_numbers[line]][dict_for_letters['E']] = obj.board[dict_for_numbers[line]][dict_for_letters['C']]

                obj.board[dict_for_numbers[line]][dict_for_letters['C']] = '•'
                obj.board[dict_for_numbers[line]][dict_for_letters['D']] = '•'

            def uncastling_double(self, line):
                obj.board[dict_for_numbers[line]][dict_for_letters['E']] = obj.board[dict_for_numbers[line]][dict_for_letters['G']]
                obj.board[dict_for_numbers[line]][dict_for_letters['H']] = obj.board[dict_for_numbers[line]][dict_for_letters['F']]

                obj.board[dict_for_numbers[line]][dict_for_letters['F']] = '•'
                obj.board[dict_for_numbers[line]][dict_for_letters['G']] = '•'

            def future_step(self):
                if len(self.current_list) > 0:
                    now_hod = self.current_list.pop()
                    if type(now_hod) == str and now_hod != 'O-O-O' and now_hod != 'O-O':
                        obj.replace_field(now_hod)
                        obj.show()
                    elif len(now_hod) == 2:
                        obj.remove_field(now_hod)
                        obj.show()
                    elif now_hod == 'O-O-O':
                        if len(obj.logger) % 2 == 0:
                            obj.castling('E1A1')
                        else:
                            obj.castling('E8A8')
                        obj.show()
                    elif now_hod == 'O-O':
                        if len(obj.logger) % 2 == 0:
                            obj.castling('E1H1')
                        else:
                            obj.castling('E8H8')
                        obj.show()
                    elif 'prohod' in now_hod:
                        figure = get_lines(now_hod[0], reverse=True)
                        figure.can_move_to(now_hod[0])
                        obj.show()
                else:
                    print('Вы в конце партии!')

            def delete_inf(self):
                pass

            # рокировки хранятся в виде o-o-o или o-o, определяем какой игрок это сделал по индексу элемента
            # съедение на проходе хранится в виде кортежа (ход, пешка соперника, пометка 'prohod')\
            # горизонталь хранится в виде кортежа (ход, кого съели, кем были, кем стали)
            # обычное съедение хранится в виде кортежа (ход, кого съели)
            # обычный ход в виде строки

        obj = Board()
        whites, blacks = make_figures()
        obj.create_fields(whites, blacks)
        while game_on:
            flag_for_gamer = 0
            obj.show()
            print(obj.logger)
            print('\tPoints:', 'w:', obj.white_point, '|', 'b:', obj.black_point)
            while not flag_for_gamer:
                hod = input('\tInput your move or "Пас" for stop game or "Откат" for view last/future move: ')
                hod = hod.upper()
                p = re.compile(r'[A-H][1-8][A-H][1-8]')
                if hod == 'ПАС':
                    obj.count += 1
                    winner = obj.counter()
                    winner_points = (obj.white_point, obj.black_point)
                    game_on = False
                    flag_for_gamer = 1

                elif hod == 'ОТКАТ':
                    machine_of_time = BackToThePast()
                    flag = True
                    while flag:
                        print('Введите "-", чтобы посмотреть прошлый ход: ')
                        print('Введите "+", чтобы посмотреть будущий ход: ')
                        print('Введите "=", чтобы начать с этого места (все ходы, сделанные вами после этого не сохранятся, вы начнете с этого момента!): ')
                        what = input('Что делаем?')
                        if what == '-':
                            machine_of_time.back_step()
                        elif what == '+':
                            machine_of_time.future_step()
                        elif what == '=':
                            flag = False
                        else:
                            print('Введено что-то не то!')
                            continue

                elif not p.match(hod) or hod[0:2] == hod[2:4] or len(hod) > 4:
                    print('\tВведены неправильные данные для хода, повторите попытку')
                    continue
                else:
                    your_figure = get_lines(hod, reverse=1)
                    if your_figure == '•':
                        print('\tВы выбрали в качестве фигуры пустую клетку!')
                        continue
                    elif your_figure.color != obj.counter():
                        print('\tВы выбрали фигуру другого игрока!')
                        continue
                    elif your_figure.typing == ('Q' or 'q'):
                        if not Bishop.can_move_to(self=your_figure, string=hod):
                            if not Rook.can_move_to(self=your_figure, string=hod):
                                print('\tХод запрещён!')
                                continue
                            else:
                                flag_for_gamer = 1
                                obj.count += 1
                        else:
                            flag_for_gamer = 1
                            obj.count += 1
                    elif not your_figure.can_move_to(hod):
                        print('\tХод запрещён!')
                        continue
                    else:
                        if obj.white_point >= 100 or obj.black_point >= 100:
                            obj.show()
                            winner = obj.counter()
                            winner_points = (obj.white_point % 100, obj.black_point % 100)
                            game_on = False
                            flag_for_gamer = 1
                        else:
                            flag_for_gamer = 1
                            obj.count += 1
    else:
        if obj.white_point + obj.black_point > 100:
            print(f'\tВыиграл игрок {winner} со счётом w={winner_points[0]}, b={winner_points[1]}, съев короля соперника')
        else:
            print(f'\tВыиграл игрок {winner} со счётом w={winner_points[0]}, b={winner_points[1]}, так как другой игрок сдался')


print('Чтобы поиграть в шахматы, нажмите "1"')
print('Чтобы поиграть в шашки, нажмите "2"')
choose = input('Ваш выбор: ')

round_game() if choose == '1' else print('Шашки пока недоступны:(')
