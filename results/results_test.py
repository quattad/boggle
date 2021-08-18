from results.results import Results
import timeit
import datetime

##########
# ACTUAL #
##########

# TRIAL RUN
# board = [
#     ['t', 't', 'e', 'a', 'g'],
#     ['l', 'n', 'p', 'i', 'n'],
#     ['o', 'c', 's', 'o', 'a'],
#     ['j', 'e', 'l', 'a', 'r'],
#     ['t', 'e', 'o', 'a', 'n']
#     ]

# BOARD 1
# board = [
#     ['o', 'p', 'o', 'n', 'i'],
#     ['z', 's', 'e', 'w', 'i'],
#     ['m', 't', 'o', 'r', 'o'],
#     ['t', 'o', 'e', 'u', 'e'],
#     ['i', 'c', 'a', 'a', 'd']
#     ]

# BOARD 2
board = [
    ['i', 'l', 'c', 's', 'w'],
    ['t', 's', 'i', 'l', 'y'],
    ['a', 'b', 'p', 't', 'r'],
    ['n', 'r', 't', 'w', 'g'],
    ['o', 'e', 's', 'n', 'i']
    ]

# csv_path = 'trial_board.xlsx'
# csv_path = 'board_1.xlsx'
csv_path = 'board_2.xlsx'

results = Results(board=board, csv_path=csv_path)
results.run()