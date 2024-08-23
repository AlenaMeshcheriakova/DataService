import uuid

import grpc
from google.protobuf import empty_pb2

from src.grpc.error_handler import grpc_error_handler
from src.grpc.word_type_service import word_type_service_pb2
from src.grpc.word_type_service.word_type_service_pb2_grpc import WordTypeServiceServicer
from src.log.logger import log_decorator, CustomLogger
from src.service.word_type_service import WordTypeService


class WordTypeServiceServicer(WordTypeServiceServicer):

    @log_decorator(my_logger=CustomLogger())
    @grpc_error_handler
    def get_word_type_id(self, request, context):
        try:
            word_type = request.word_type
            res_uuid = WordTypeService.get_word_type_id(word_type)
            return word_type_service_pb2.GetWordTypeIdResponse(word_type_id=str(res_uuid))
        except ValueError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("WordType was not found")
            return word_type_service_pb2.GetWordTypeIdResponse()


    @log_decorator(my_logger=CustomLogger())
    @grpc_error_handler
    def create_word_type(self, request, context):
        word_type = request.word_type
        new_word_type_id = WordTypeService.create_word_type(word_type)
        return word_type_service_pb2.CreateWordTypeResponse(word_type_id=str(new_word_type_id))

    @log_decorator(my_logger=CustomLogger())
    @grpc_error_handler
    def update_word_type(self, request, context):
        word_type_id = uuid.UUID(request.word_type_id)
        new_word_type = request.new_word_type
        WordTypeService.update_word_type(word_type_id, new_word_type)
        return empty_pb2.Empty()

    @log_decorator(my_logger=CustomLogger())
    @grpc_error_handler
    def delete_word_type(self, request, context):
        word_type_id = uuid.UUID(request.word_type_id)
        WordTypeService.delete_word_type(word_type_id)
        return empty_pb2.Empty()