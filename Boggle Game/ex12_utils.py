import copy
import os
TEST_DICT_ROOT = "test-dicts"

def is_valid_path(board, path, words):
    dup_set = set(path)
    word = ""
    if len(dup_set) != len(path):
        return None
    for i in range(len(path)):
        row = path[i][0]
        col = path[i][1]
        if _out_of_bounderies(row, col, board):
            return None
        word += board[row][col]
        if i == len(path)-1:
            continue
        else:
            next_row = path[i+1][0]
            next_col = path[i+1][1]
            if _out_of_bounderies(next_row, next_col, board):
                return None
            if not _valid_move(next_row, next_col, row, col):
                return None
    if word in words:
        return word
    return None


def _valid_move(next_row, next_col, current_row, current_col):
    valid_moves = [(current_row, current_col-1), (current_row, current_col+1),
                   (current_row-1, current_col-1), (current_row+1, current_col+1),
                   (current_row+1, current_col-1), (current_row-1, current_col+1),
                   (current_row-1, current_col), (current_row+1, current_col)]
    if (next_row, next_col) in valid_moves:
        return True
    else:
        return False


def _out_of_bounderies(row, col, board):
    height = len(board)
    width = len(board[0])
    if row > height-1 or row < 0 or col > width-1 or col < 0:
        return True
    return False


def possible_moves(current_row, current_col, board):
    if current_row == 0: #upper row
        if current_col == 0:  # left upper corner
            return [(current_row, current_col+1), (current_row+1, current_col),
                    (current_row+1, current_col+1)]
        if current_col == len(board[0]) -1:  # right upper corner
            return [(current_row, current_col-1), (current_row+1, current_col-1),
                    (current_row+1, current_col)]
        else:
            return [(current_row, current_col+1), (current_row, current_col-1),
                    (current_row+1, current_col), (current_row+1, current_col+1),
                    (current_row+1, current_col-1)]
    if current_row == len(board) -1:  # bottom row
        if current_col == 0:  # bottom left corner
            return [(current_row-1, current_col), (current_row-1, current_col+1),
                    (current_row, current_col+1)]
        if current_col == len(board[0]) -1:  # bottom right corner
            return [(current_row, current_col -1), (current_row-1, current_col),
                    (current_row-1, current_col-1)]
        else:
            return [(current_row, current_col+1), (current_row, current_col-1),
                    (current_row-1, current_col+1), (current_row-1, current_col),
                    (current_row-1, current_col-1)]
    if current_col == 0:  # left column
        return [(current_row-1, current_col), (current_row+1, current_col),
                (current_row-1, current_col+1), (current_row, current_col+1),
                (current_row+1, current_col+1)]
    if current_col == len(board[0]) -1:  # right column
        return [(current_row-1, current_col-1), (current_row-1, current_col),
                (current_row, current_col-1), (current_row+1, current_col),
                (current_row+1, current_col-1)]
    else:
        return [(current_row, current_col+1), (current_row, current_col-1),
                (current_row-1, current_col), (current_row-1, current_col-1),
                (current_row-1, current_col+1), (current_row+1, current_col-1),
                (current_row+1, current_col), (current_row+1, current_col+1)]


def _find_paths_helper(temp_word, row, col, button_num, n, words, temp_path, final_path, method, board):
    if n == 0:
        return []
    if (button_num == n and method == 1) or (method == 2 and len(temp_word) == n):
            if temp_word in words:
                final_path.append(copy.deepcopy(temp_path))
            return
    temp_possible_moves = possible_moves(row, col, board)
    for path in temp_path:
        if path in temp_possible_moves:
            temp_possible_moves.remove(path)

    for move in temp_possible_moves:
        temp_word += board[move[0]][move[1]]
        button_num += 1
        temp_path.append(move)
        _find_paths_helper(temp_word, move[0], move[1], button_num, n, words, temp_path, final_path, method, board)
        temp_word = temp_word[:-len(board[move[0]][move[1]])]
        button_num -= 1
        temp_path.remove(move)


def find_length_n_paths(n, board, words):
    final_path = []
    if n == 0:
        return []
    for row in range(len(board)):
        for col in range(len(board[0])):
            button_num = 1
            temp = _find_paths_helper(board[row][col], row, col, button_num, n, words, [(row, col)], final_path, 1, board)
            if temp:
                final_path.append(temp)
    return final_path


def find_length_n_words(n, board, words):
    final_path = []
    if n == 0 :
        return []
    for row in range(len(board)):
        for col in range(len(board[0])):
            button_num = 1
            temp = _find_paths_helper(board[row][col], row, col, button_num, n, words, [(row, col)], final_path, 2, board)
            if temp:
                final_path.append(temp)
    return final_path

def max_score_helper(path_lst, final_rank_dict, board):
    for path in path_lst:
        word = ""
        for item in path:
            word += board[item[0]][item[1]]
        if word in final_rank_dict:
            final_rank_dict[word] = path
        else:
            final_rank_dict[word] = path


def max_score_paths(board, words):
    height = len(board)
    width = len(board[0])
    final_rank_dict = {}
    for n in range(1, height*width+1):
        len_paths_lst = find_length_n_paths(n, board, words)
        max_score_helper(len_paths_lst, final_rank_dict, board)
    return final_rank_dict

def load_words_dict(file):
    milon = open(file)
    lines = set(line.strip() for line in milon.readlines())
    milon.close()
    return lines

def file_path(name):
    return os.path.join(TEST_DICT_ROOT, name)