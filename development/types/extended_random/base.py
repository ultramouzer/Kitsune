import string
from random import Random
from .lorem import lorem_sentences

from typing import List

class Extended_Random(Random):
    """
    `Random` with additional helper methods.
    """
    varchar_vocab = string.ascii_letters + string.digits
    text_vocab = string.printable
    sentence_list = lorem_sentences

    def string(self, min_length: int, max_length: int, vocabulary: str = varchar_vocab):
        "Creates a continious string with random letters."
        string_length = self.randint(min_length, max_length)
        result_string = ''.join(self.choice(vocabulary) for char in range(string_length))

        return result_string

    def varchar(self, min_length: int = 5, max_length: int = 20):
        """Generates `varchar` type of string."""
        result_string = self.string(min_length, max_length, vocabulary= self.varchar_vocab)

        return result_string

    def text(self, min_length: int = 20, max_length: int = 256):
        """Generates `text` type of string."""
        result_string = self.string(min_length, max_length, vocabulary= self.text_vocab)

        return result_string

    def boolean(self):
        result = bool(self.randint(0, 1))
        return result

    def lorem_ipsum(self, min_paragraphs: int = 1,
    max_paragraphs: int = 5, max_sentences: int = 7, sentence_list: List[str] = sentence_list):
        """Creates a semi-readable string."""
        paragraphs_amount = self.randint(min_paragraphs, max_paragraphs)

        paragraphs = [*range(paragraphs_amount)]
        for paragraph in paragraphs:
            sentences = [*range(self.randint(1, max_sentences))]

            for sentence in sentences:
                if paragraphs.index(paragraph) == 0 and sentences.index(sentence) == 0:
                    sentences[sentence] = sentence_list[0]
                else:
                    sentences[sentence] = self.choice(sentence_list)

            paragraphs[paragraph] = " ".join(sentences)

        result = "\n".join(paragraphs)

        return result

    # def date(self):
    #     pass
