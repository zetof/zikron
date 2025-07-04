import curses


class Digits():
    def print_number(stdscr, line, col, color, number, digits):
        DIGITS = [
            [[0, 1, 3],
             [1, 0, 1], [1, 4, 1],
             [2, 0, 1], [2, 4, 1],
             [3, 0, 1], [3, 4, 1],
             [4, 1, 3]],
            [[0, 1, 2],
             [1, 0, 1], [1, 2, 1],
             [2, 2, 1],
             [3, 2, 1],
             [4, 0, 5]],
            [[0, 1, 3],
             [1, 0, 1], [1, 4, 1],
             [2, 3, 1],
             [3, 1, 2],
             [4, 0, 5]],
            [[0, 1, 3],
             [1, 0, 1], [1, 4, 1],
             [2, 2, 2],
             [3, 0, 1], [3, 4, 1],
             [4, 1, 3]],
            [[0, 0, 1], [0, 4, 1],
             [1, 0, 1], [1, 4, 1],
             [2, 0, 5],
             [3, 4, 1],
             [4, 4, 1]],
            [[0, 0, 5],
             [1, 0, 1],
             [2, 0, 4],
             [3, 4, 1],
             [4, 0, 4]],
            [[0, 1, 3],
             [1, 0, 1],
             [2, 0, 4],
             [3, 0, 1], [3, 4, 1],
             [4, 1, 3]],
            [[0, 0, 5],
             [1, 4, 1],
             [2, 3, 1],
             [3, 2, 1],
             [4, 1, 1]],
            [[0, 1, 3],
             [1, 0, 1], [1, 4, 1],
             [2, 1, 3],
             [3, 0, 1], [3, 4, 1],
             [4, 1, 3]],
            [[0, 1, 3],
             [1, 0, 1], [1, 4, 1],
             [2, 1, 4],
             [3, 4, 1],
             [4, 1, 3]]
        ]

        for i in range(0, 5):
            stdscr.addstr(line + i,
                          col,
                          " " * (5 + 6 * (digits - 1)),
                          curses.color_pair(color))
        string = str(number)
        string = "0" * (digits - len(string)) + string

        i = 0
        for char in string:
            index = int(char)
            for digit in DIGITS[index]:
                stdscr.addstr(line + digit[0],
                              col + i + digit[1],
                              "O" * digit[2],
                              curses.color_pair(color))
            i += 6
