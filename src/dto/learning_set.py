from typing import List

from src.dto.schema import UserCreateFullDTO, WordDTO


class LearningSet:

    def __init__(self, user: UserCreateFullDTO, words: List[WordDTO], current_training_position: int = 1):
        """
        Information About learning set
        @param user: Info about User
        @param words: List of words (remember that list go by (current_training_position-1) )
        @param current_training_position: Current position in the list (Start from 1)
        """
        self.user: UserCreateFullDTO = user
        self.words: List[WordDTO] = words
        self.current_training_position = current_training_position

    def get_current_word(self) -> WordDTO:
        return self.words[self.current_training_position - 1]

    def get_next_word(self) -> WordDTO:
        self.inc_current_position()
        return self.get_current_word()

    def get_words(self) -> List[WordDTO]:
        return self.words

    def get_current_position(self) -> int:
        return self.current_training_position

    def inc_current_position(self) -> None:
        self.current_training_position += 1

    def get_total_length(self):
        return self.user.training_length

    def json(self):
        return {
            'user': self.user.json(),
            'words': [word.json() for word in self.words],
            'current_training_position': self.current_training_position
        }

    @classmethod
    def from_json(cls, data):
        user = UserCreateFullDTO.parse_raw(data['user'])
        words = [WordDTO.parse_raw(word_data) for word_data in data['words']]
        obj = cls(user, words)
        obj.current_training_position = data['current_training_position']
        return obj
