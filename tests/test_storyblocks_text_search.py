#!/usr/bin/env python

"""
Storyblocks Text Search

To run the tests and coverage and print all the output to the console, run:
    python -m pytest -v --cov=. tests/

To produce a coverage report in HTML format, run:
    python -m pytest -v --cov=. --cov-report html tests/
"""


import pytest
import text_searcher as ts


class TestStoryblocksTextSearch(object):

    SHORT_FILE = 'tests/data/short_excerpt.txt'
    LONG_FILE = 'tests/data/long_excerpt.txt'

    def test_one_hit_no_context(self):
        """Simplest possible case, no context and the word occurs exactly once."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        result = searcher.search("sketch", 0)
        expected = ["sketch"]
        assert result == expected

    def test_multiple_hits_no_context(self):
        """Next simplest case, no context and multiple hits."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        result = searcher.search("naturalists", 0)
        expected = ["naturalists", "naturalists"]
        assert result == expected

    def test_basic_search(self):
        """This is the example from the document."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        result = searcher.search("naturalists", 3)
        expected = ["great majority of naturalists believed that species",
				    "authors. Some few naturalists, on the other"]
        assert result == expected

    def test_basic_more_context(self):
        """Same as basic search but a little more context."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        result = searcher.search("naturalists", 6)
        expected = ["Until recently the great majority of naturalists believed that species were immutable productions",
                    "maintained by many authors. Some few naturalists, on the other hand, have believed"]
        assert result == expected

    def test_apostrophe_query(self):
        """Tests query word with apostrophe."""
        searcher = ts.TextSearcher(file=self.LONG_FILE)
        result = searcher.search("animal's", 4)
        expected = ["not indeed to the animal's or plant's own good",
				    "habitually speak of an animal's organisation as\r\nsomething plastic"]
        assert result == expected

    def test_numeric_query(self):
        """Tests numeric query word."""
        searcher = ts.TextSearcher(file=self.LONG_FILE)
        result = searcher.search("1844", 2)
        expected = ["enlarged in 1844 into a",
				    "sketch of 1844--honoured me"]
        assert result == expected

    def test_mixed_query(self):
        """Tests mixed alphanumeric query word."""
        searcher = ts.TextSearcher(file=self.LONG_FILE)
        result = searcher.search("xxxxx10x", 3)
        expected = ["date first edition [xxxxx10x.xxx] please check"]
        assert result == expected

    def test_case_insensitive_search(self):
        """Should get same results regardless of case."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        expected = ["on the Origin of Species. Until recently the great",
                    "of naturalists believed that species were immutable productions, and",
                    "hand, have believed that species undergo modification, and that"]

        result = searcher.search("species", 4)
        assert len(result) == len(expected)
        assert result == expected

        result = searcher.search("SPECIES", 4)
        assert len(result) == len(expected)
        assert result == expected

        result = searcher.search("SpEcIeS", 4)
        assert len(result) == len(expected)
        assert result == expected

    def test_near_beginning(self):
        """Hit that overlaps file start should still work."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        expected = ["I will here give a brief sketch"]
        result = searcher.search("here", 4)
        assert result == expected

    def test_near_end(self):
        """Hit that overlaps file end should still work."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        expected = ["and that the existing forms of life",
				    "generation of pre existing forms."]
        result = searcher.search("existing", 3)
        assert result == expected

    def test_multiple_searches(self):
        """Searcher can execute multiple searches after initialization."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)

        expected = ["on the Origin of Species. Until recently the great",
                    "of naturalists believed that species were immutable productions, and",
                    "hand, have believed that species undergo modification, and that"]
        results = searcher.search("species", 4)
        assert results == expected

        expected = ["I will here give a brief sketch"]
        results = searcher.search("here", 4)
        assert results == expected

        expected = ["and that the existing forms of life",
					"generation of pre existing forms."]
        results = searcher.search("existing", 3)
        assert results == expected

    def test_overlapping_hits(self):
        """Overlapping hits should just come back as separate hits."""
        searcher = ts.TextSearcher(file=self.SHORT_FILE)
        expected = ["of naturalists believed that species were immutable",
				    "hand, have believed that species undergo modification",
				    "undergo modification, and that the existing forms"]
        results = searcher.search("that", 3)
        assert results == expected

    def test_no_hits(self):
        """If no hits, get back an empty array."""
        searcher = ts.TextSearcher(file=self.LONG_FILE)
        expected = []
        results = searcher.search("slejrlskejrlkajlsklejrlksjekl", 3)
        assert results == expected
