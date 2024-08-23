from typing import List, Optional
from uuid import UUID

from sqlalchemy import insert, select, update, desc
from sqlalchemy.sql.functions import count

from src.db.database import session_factory
from src.dto.schema import WordAddDTO, WordDTO, WordGetDTO
from src.log.logger import log_decorator, CustomLogger
from src.model.word import Word
from src.data.base_orm import BaseOrm
from src.model.word_type import WordType
from src.model.word_type_enum import WordTypeEnum
from src.model.standard_word_user import StandardWordUser


class WordOrm(BaseOrm):

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_words_by_user_id(user_id: UUID, training_length: int = 10,
                              word_type: WordTypeEnum = WordTypeEnum.custom) -> List[WordDTO]:
        """
        Find set of words for next training for user with user_id and limited by total_length
        @param training_length: length of selected set
        @param user_id: user id
        @return: list of words for training (list of WordAddDTO)
        """
        if (training_length <= 0):
            raise ValueError(f"Inappropriate Length for learning set: {training_length}")
        with session_factory() as session:
            query = (select(Word.id,
                            Word.user_id,
                            Word.russian_word,
                            Word.english_word,
                            Word.german_word,
                            Word.word_type_id,
                            Word.lang_level_id,
                            Word.group_id,
                            Word.amount_already_know,
                            Word.amount_back_to_learning)
                     .join(WordType, WordType.id == Word.word_type_id)
                     .where(Word.user_id==user_id, WordType.word_type==word_type)
                     .order_by((Word.amount_back_to_learning/(1 + Word.amount_already_know+Word.amount_back_to_learning)))
                     .slice(0, training_length)) #desc
            result = session.execute(query)
            all_results = result.mappings().all()
            lines = [WordDTO(**element) for element in all_results]
            return lines

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def words_amount_in_standard_word_user(user_id: UUID) -> int:
        """
        Get amount of standard word which was trained at least once for user with user_id
        @param user_id: user id
        @return:Amount of trained standard words in User
        """
        with session_factory() as session:
            query = (select(count(StandardWordUser.user_id))
                     .where(StandardWordUser.user_id == user_id))
            result = session.execute(query)
            res = result.scalar()
            return int(res)

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_words_for_standard_type(user_id: UUID, training_length: int = 10,
                              word_type: WordTypeEnum = WordTypeEnum.standard) -> List[WordDTO]:
        """
        GET INFORMATION FROM TABLE STANDARD_WORD_USER
        Find set of words for next standard word training with user training count amounts
        @param training_length: length of selected set
        @param user_id: user id
        @return: list of words for training (list of WordAddDTO)
        """
        if (training_length <= 0):
            raise ValueError(f"Inappropriate Length for learning set: {training_length}")
        with session_factory() as session:
            # Calculate the ratio for ordering
            ratio = (StandardWordUser.amount_back_to_learning / (
                        1 + StandardWordUser.amount_already_know + StandardWordUser.amount_back_to_learning))

            # Main query with filter, order, and ratio calculation
            query = (select(
                Word.id,
                StandardWordUser.amount_already_know,
                StandardWordUser.amount_back_to_learning,
                Word.german_word,
                Word.english_word,
                Word.russian_word,
                Word.word_type_id,
                Word.lang_level_id,
                Word.group_id,
                Word.user_id
            )
             .join(Word, StandardWordUser.word_id == Word.id)
             .join(WordType, WordType.id == Word.word_type_id)
             .where(StandardWordUser.user_id == user_id, WordType.word_type == word_type)
             .order_by(desc(ratio))
             .limit(training_length))

            result = session.execute(query)
            all_results = result.mappings().all()
            lines = [WordDTO(**element) for element in all_results]
            return lines

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_new_words_for_standard_type(training_length: int = 10) -> List[WordDTO]:
        """
        GET INFORMATION FROM TABLE WORD
        Find set of new words for user (not for specific user) from table Words with Standard type
        (which should be added to table WordUser fir future training)
        Use words from Word table which was not used in User training before
        @param training_length: length of selected set
        @param word_type: length of selected set
        @return: list of words for training (list of WordAddDTO)
        """
        if (training_length <= 0):
            raise ValueError(f"Inappropriate Length for learning set: {training_length}")
        word_type = WordTypeEnum.standard
        with session_factory() as session:
            # Calculate the ratio for ordering
            ratio = Word.amount_back_to_learning / (1 + Word.amount_already_know + Word.amount_back_to_learning)

            subquery = select(StandardWordUser.word_id).filter(StandardWordUser.word_id == Word.id).exists()
            query = (select(
                Word.id,
                Word.user_id,
                Word.russian_word,
                Word.english_word,
                Word.german_word,
                Word.word_type_id,
                Word.lang_level_id,
                Word.group_id,
                Word.amount_already_know,
                Word.amount_back_to_learning
            )
            .join(WordType, WordType.id == Word.word_type_id)
            .where(~subquery, WordType.word_type == word_type)
            .order_by(desc(ratio))
            .limit(training_length))

            result = session.execute(query)
            all_results = result.mappings().all()
            lines = [WordDTO(**element) for element in all_results]
            return lines

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_word_by_id(word_id: UUID) -> WordAddDTO:
        """
        Get word model by word_id
        @param word_id: id for table word
        @return: model for word
        """
        if (word_id is None):
            raise ValueError(f"Word ID is None: {word_id}, expected UUID")
        with session_factory() as session:
            query = (select(Word)
                     .filter_by(id=word_id))
            result = session.execute(query)
            word: WordAddDTO = WordAddDTO.model_validate(result.scalars().first())
            return word

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def add_word(new_word: WordDTO) -> Optional[Word]:
        """
        Add new word to database
        @param new_word: new word
        @return: None
        """
        if (new_word is None):
            raise ValueError(f"Word is None: {new_word}, expected WordDTO")
        with session_factory() as session:
            stmt = insert(Word).values(**new_word.dict()).returning(Word)
            result = session.execute(stmt)
            session.commit()

            created_word = result.fetchone()
            if created_word:
                return created_word[0]
            else:
                raise RuntimeError("Failed to retrieve created word")
        return None


    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_counter_for_word(german_word: str, user_id: UUID, inc_amount_already_know, inc_amount_back_to_learning) -> None:
        """
        Update parameters in existed words
        - Added value inc_amount_already_know to already existed parameter amount_already_know
        - Added value inc_amount_back_to_learning to already existed parameter amount_back_to_learning
        amount_already_know or amount_back_to_learning have to be more than 0
        @param german_word: used for searching
        @param user_id: used for searching
        @param inc_amount_already_know: that value will be incremented to amount_already_know
        @param inc_amount_back_to_learning: that value will be incremented to amount_back_to_learning
        @return: None
        """
        if (inc_amount_already_know<0) or (inc_amount_back_to_learning<0):
            raise ValueError(f"Updated word parameters have to be > 0: {inc_amount_already_know} or {inc_amount_back_to_learning}")
        with session_factory() as session:
            stmt = update(Word).where(
                Word.german_word==german_word,
                Word.user_id==user_id
            ).values(
                amount_already_know =Word.amount_already_know + inc_amount_already_know,
                amount_back_to_learning =Word.amount_back_to_learning + inc_amount_back_to_learning
            )
            session.execute(stmt)
            session.commit()
        return None

