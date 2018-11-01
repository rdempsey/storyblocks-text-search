#!/usr/bin/env python

import re
from nltk.tokenize import word_tokenize
import itertools

class TextSearcher(object):
    def __init__(self, file):
        self.file = file
        # TODO: add an internal cache and check that for the results of previous queries

    def _read_file(self):
        """
        Read the file and return the content.

        :return: content: the file content
        """
        with open(self.file, 'r') as  the_file:
            content = the_file.read()
        return content

    def search(self, query_word, context_words):
        """
        Find a query word and context in a file.

        :param query_word: the word to find in the text
        :param context_words: words of context surrounding the query word
        :return: results: list of strings containing the query results
        """
        results = list()

        # Get the contents of the file
        file_content = self._read_file()

        # Clean up the file a bit - convert double spaces to single spaces
        file_content = file_content.replace("  ", " ")

        # Tokenize the entire text and ensure we have all spaces
        tokens = [[word_tokenize(w), ' '] for w in file_content.split()]
        token_list = list(itertools.chain(*list(itertools.chain(*tokens))))

        # Find the query_word in our tokens
        hit_indices = [idx for idx, hit in enumerate(token_list) if hit.lower() == query_word.lower()]

        if len(hit_indices) == 0:
            return results
        elif len(hit_indices) >= 1 and context_words == 0:
            for i in range(0, len(hit_indices)):
                results.append(query_word)
            return results

        # Create a regex to find a word
        pattern = re.compile("\W*([a-zA-Z0-9']+)")

        # Get the context around the query_word
        for hit_idx in hit_indices:
            left = ""
            right = ""

            # Get context to the left
            found_words = 0
            i = 1
            while found_words < context_words and hit_idx - i != -1:
                prev_token = token_list[hit_idx - i]
                left = prev_token + left
                if pattern.match(prev_token):
                    found_words += 1
                i += 1

            found_words = 0
            i = 1
            while found_words < context_words and hit_idx + i < len(token_list):
                next_token = token_list[hit_idx + i]
                right = right + next_token
                if pattern.match(next_token):
                    found_words += 1
                i += 1

            # Clean up the strings and return the result
            result = left.lstrip() + token_list[hit_idx] + right.rstrip()
            results.append(result)

        return results
