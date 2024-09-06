from google.protobuf import empty_pb2

from src.dto.learning_set import LearningSet
from src.grpc.mapping_helper import pydantic_to_protobuf, learning_set_to_protobuf, learning_set_from_protobuf
from src.grpc.process_service import process_service_pb2
from src.grpc.process_service.process_service_pb2_grpc import ProcessServiceServicer
from src.grpc.user_service import user_service_pb2
from src.grpc.word_service import word_service_pb2
from src.log.logger import logger, log_decorator
from src.service.process_service import ProcessService
from user_action_enum import UserActionEnum
from word_type_enum import WordTypeEnum


class ProcessServiceServicer(ProcessServiceServicer):

    @log_decorator(my_logger=logger)
    def start_learning_process(self, request, context):
        # Get data from request
        user_name = request.user_name
        word_type = WordTypeEnum(process_service_pb2.WordTypeEnum.Name(request.word_type))

        # Call method in Service
        learning_set: LearningSet = ProcessService.start_learning_process(user_name, word_type)

        # Convert result to protobuf type
        resulted_learning_set = learning_set_to_protobuf(learning_set)
        return resulted_learning_set


    @log_decorator(my_logger=logger)
    def get_learning_set(self, request, context):
        # Get data from request
        user_name = request.user_name
        word_type = WordTypeEnum(process_service_pb2.WordTypeEnum.Name(request.word_type))

        # Call method in Service
        learning_set: LearningSet = ProcessService.get_learning_set(user_name, word_type)

        # Convert result to protobuf type
        resulted_learning_set = learning_set_to_protobuf(learning_set)
        return resulted_learning_set

    @log_decorator(my_logger=logger)
    def update_learning_progress(self, request, context):
        # Get data from request
        user_id = request.user_id
        word_id = request.word_id
        german_word = request.german_word
        user_action = UserActionEnum(process_service_pb2.UserActionEnum.Name(request.user_action))
        word_type = WordTypeEnum(process_service_pb2.WordTypeEnum.Name(request.word_type))

        # Call method in Service
        ProcessService.update_learning_progress(user_id, word_id, german_word, user_action, word_type)

        # Return Empty
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def add_learning_set_to_cash(self, request, context):
        # Get learning_set from request
        learning_set = learning_set_from_protobuf(request)

        # Call method in Service
        ProcessService.add_learning_set_to_cash(learning_set)

        # Return Empty
        return empty_pb2.Empty()