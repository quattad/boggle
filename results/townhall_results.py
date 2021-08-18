import pandas as pd
import enchant
from datetime import datetime
import re

class Results:
    def __init__(self, csv_path, board):
        """
        Board: list of lists with each element a single char string representing the alphabet located
        at that point in the board
        """
        self.csv_path = csv_path
        self.board = board

        self.df = None
        self.cache = {}
        self.answers = []
        self.results = {}
        self.d_to_csv = {}
        self.directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
    
    def import_csv_to_df(self):
        """
        Imports csv file exported from Microsoft Forms to pandas dataframe.
        """
        self.df = pd.read_excel(self.csv_path, sheet_name='Sheet1', engine='openpyxl')

    def extract(self):
        """
        Extracts name and words columns and returns a list of tuples as (name, words).
        """
        name_col = self.df['Email']
        answers_col = self.df['Answers']

        if len(name_col) == len(answers_col):
            self.answers = list(zip(name_col, answers_col))
    
    def parse_words(self, words):
        """
        Takes in a comma-separated string, converts all to lowercase and split by comma into array.
        """
        if not words:
            return []
        
        # lowercase_words = words.casefold().replace(" ", "")
        lowercase_words = re.sub(r'[^a-zA-Z,]', '', words.casefold())
        return lowercase_words.split(',')
    
    def bfs(self, i, j, s, visited, path):
        """
        Returns true if s is an empty string.
        Else check if i, j is equal to first char of s[0].
        If yes, call bfs on vertical, horizontal and diagonal neighbors and return result.
        If none of the directions match first char, return false.
        """
        if s == "":
            return True

        visited.add((i, j))

        if self.board[i][j] == s[0]:
            path.append((i, j))
            remaining = s[1:]

            for direction in self.directions:
                new_i, new_j = i + direction[0], j + direction[1]

                if 0 <= new_i < len(self.board) and 0 <= new_j < len(self.board[0]) and (new_i, new_j) not in visited:
                    # Check potential new candidate position to add to current path
                    if self.bfs(new_i, new_j, remaining, visited, path):
                        return True
                    
                    # Since candidate did not match whole word, remove position from
                    # visited to allow other paths to use the position
                    visited.remove((new_i, new_j))
        
        return False

    def get_path(self, word):
        """
        Get word path in board provided by using BFS traversal.
        Returns word path if word exists in the board, else return empty list.
        """
        m, n = len(self.board), len(self.board[0])

        for i in range(m):
            for j in range(n):
                visited = set()
                path = []

                if self.bfs(i, j, word, visited, path):
                    return path
        
        return []
    
    def check_if_real_word(self, word):
        """
        Checks whether word is a real English word using pyenchant
        """
        d_us = enchant.Dict("en_US")
        d_uk = enchant.Dict("en_UK")
        return d_us.check(word) or d_uk.check(word)
    
    def check_if_valid_word(self, word):
        """
        Checks whether word both exists in board and is a valid english word
        """
        if word not in self.cache:
            self.cache[word] = self.get_path(word)
        
        word_path = self.cache[word]

        return self.check_if_real_word(word) and len(word_path) != 0

    def tabulate_results(self):
        """
        Populate results using list of tuples.
        """
        for one_bank_id, words in self.answers:
            default = {
                'words': set(),
                'score': 0
            }
            # default = set()

            self.results[one_bank_id] = self.results.get(one_bank_id, default)
            word_arr = self.parse_words(words)

            for w in word_arr:
                if len(w) > 1 and self.check_if_valid_word(w):
                    # self.results[one_bank_id].add(w)
                    self.results[one_bank_id]['words'].add(w)
                    self.results[one_bank_id]['score'] += len(w)
    
    def export_results(self):
        """
        Export results as a CSV file.
        """
        self.d_to_csv = {
            'name': [],
            'words': [],
            'count': []
        }

        for one_bank_id, result in self.results.items():
            self.d_to_csv['name'].append(one_bank_id)
            self.d_to_csv['words'].append(",".join(result['words']))
            self.d_to_csv['count'].append(result['score'])
        
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M")
        
        df = pd.DataFrame.from_dict(self.d_to_csv)
        df.to_csv('results_{}.csv'.format(dt_string), index=False)

    def run(self):
        """
        Main function.
        """
        self.import_csv_to_df()
        self.extract()
        self.tabulate_results()
        self.export_results()