from typing import List

from google.protobuf import empty_pb2

from src.dto.schema import WordGetDTO, WordAddDTO
from src.grpc.mapping_helper import pydantic_to_protobuf, convert_proto_to_pydantic
from src.grpc.word_service import word_service_pb2
from src.grpc.word_service.word_service_pb2_grpc import WordServiceServicer
from src.log.logger import CustomLogger, log_decorator
from src.service.word_service import WordService


class WordServiceServicer(WordServiceServicer):

    # TODO CRIT: Check it for API
    @log_decorator(my_logger=CustomLogger())
    def get_words_by_user(self, request, context) -> word_service_pb2.GetListWordsByUserResponse:
        user_id = request.user_id
        training_length = request.training_length
        words: List[WordGetDTO] = WordService.get_words_by_user(user_id, training_length)

        response = word_service_pb2.GetListWordsByUserResponse()
        for word in words:
            # Create a mapping template
            word_field_mapping = {k: k for k, v in word.dict().items()}

            # Convert Pydantic model to Protobuf response
            response_line = pydantic_to_protobuf(word, word_service_pb2.GetWordsByUserResponse, word_field_mapping)
            print(response_line)
            setattr(response, words, str(response_line))

        context.set_details("Response details: " + str(response))
        return response

    @log_decorator(my_logger=CustomLogger())
    def add_new_word_from_dto(self, request, context):
        word_dto = convert_proto_to_pydantic(request, WordAddDTO)
        WordService.add_new_word_from_dto(word_dto)
        return empty_pb2.Empty()

    @log_decorator(my_logger=CustomLogger())
    def add_new_word(self, request, context):
        user_name = request.user_name
        german_word = request.german_word
        english_word = request.english_word
        russian_word = request.russian_word
        amount_already_know = request.amount_already_know
        amount_back_to_learning = request.amount_back_to_learning
        group_word_name = request.group_word_name
        level = request.level
        word_type = request.word_type

        WordService.add_new_word(user_name, german_word, english_word, russian_word, amount_already_know,
                                 amount_back_to_learning, group_word_name, level, word_type)
        return empty_pb2.Empty()