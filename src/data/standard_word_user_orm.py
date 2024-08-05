from typing import List
from uuid import UUID

from sqlalchemy import select, insert, update

from src.data.base_orm import BaseOrm
from src.db.database import session_factory
from src.dto.schema import StandardWordAddDTO, StandardWordDTO
from src.log.logger import CustomLogger, log_decorator
from src.model.standard_word_user import StandardWordUser


class StandardWordUserOrm(BaseOrm):

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def find_word_by_id(standard_word_id: UUID) -> StandardWordAddDTO:
        """
        Get standard word word_id
        @param word_id: id for table word
        @return: model for word
        """
        if (standard_word_id is None):
            raise ValueError(f"Word ID is None: {standard_word_id}, expected UUID")
        with session_factory() as session:
            query = (select(StandardWordUser)
                     .filter_by(id=standard_word_id))
            result = session.execute(query)
            res = result.first()
            word = StandardWordAddDTO.model_validate(res)
            return word

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def create_list_new_words(new_words_list: List[StandardWordDTO]) -> None:
        """
        Create standard words on StandardWordUser
        Which mean that User started to practice them
        @param new_words_list: List of standard words which need to link with user
        @return:
        """
        if (new_words_list is None):
            raise ValueError(f"List of neue words is None: {new_words_list}, expected List[StandardWordDTO]")
        with session_factory() as session:
            for new_word in new_words_list:
                # query = select(StandardWordUser).filter_by(
                #     word_id=new_word.word_id,
                #     user_id=new_word.user_id
                # )
                # res_first = session.execute(query).first()
                #
                # if not res_first:
                stmt = insert(StandardWordUser).values(**new_word.dict())
                session.execute(stmt)
            session.commit()

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def update_counter_for_word(word_id: UUID, user_id: UUID, inc_amount_already_know, inc_amount_back_to_learning) -> None:
        if (inc_amount_already_know < 0) or (inc_amount_back_to_learning < 0):
            raise ValueError(
                f"Updated word parameters have to be > 0: {inc_amount_already_know} or {inc_amount_back_to_learning}")
        with session_factory() as session:
            stmt = (update(StandardWordUser)
            .where(
                StandardWordUser.word_id == word_id,
                StandardWordUser.user_id == user_id
            ).values(
                amount_already_know=StandardWordUser.amount_already_know + inc_amount_already_know,
                amount_back_to_learning=StandardWordUser.amount_back_to_learning + inc_amount_back_to_learning
            ))
            result = session.execute(stmt)
            session.commit()
        return None


