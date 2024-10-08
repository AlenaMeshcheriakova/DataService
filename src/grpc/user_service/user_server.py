import uuid

from src.dto.schema import UserAuthTelegramDTO
from src.grpc.mapping_helper import pydantic_to_protobuf
from src.grpc.user_service import user_service_pb2
from src.grpc.user_service.user_service_pb2_grpc import UserServiceGRPCServicer
from src.log.logger import log_decorator, logger
from src.service.user_service import UserService
from google.protobuf import empty_pb2

class UserServiceServicer(UserServiceGRPCServicer):

    @log_decorator(my_logger=logger)
    def get_user_by_id(self, request, context) -> user_service_pb2.UserCreateFullDTOResponse:
        user_id = request.request_id
        user_dto = UserService.get_user_by_id(user_id)

        # Create a mapping template
        user_mapping = {k: k for k, v in user_dto.dict().items()}

        # Convert Pydantic model to Protobuf response
        response = pydantic_to_protobuf(user_dto, user_service_pb2.UserCreateFullDTOResponse,
                                        user_mapping)
        context.set_details("Response details: " + str(response))
        return response

    @log_decorator(my_logger=logger)
    def get_user_by_name(self, request, context) -> user_service_pb2.UserCreateFullDTOResponse:
        user_name = request.user_name
        user_dto = UserService.get_user_by_name(user_name)

        # Create a mapping template
        user_create_full_dto_field_mapping = {k: k for k, v in user_dto.dict().items()}

        # Convert Pydantic model to Protobuf response
        response = pydantic_to_protobuf(user_dto, user_service_pb2.UserCreateFullDTOResponse, user_create_full_dto_field_mapping)
        context.set_details("Response details: " + str(response))
        return response

    @log_decorator(my_logger=logger)
    def get_user_id_by_name(self, request, context) -> uuid.UUID:
        user_name = request.user_name
        user_id = UserService.get_user_id_by_name(user_name)

        # Convert Pydantic model to Protobuf response
        response = user_service_pb2.UserIdResponse(
            user_id=str(user_id)
        )
        context.set_details("Response details: " + str(response))
        return response

    @log_decorator(my_logger=logger)
    def update_user_training_length(self, request, context):
        user_name = request.user_name
        training_length = request.training_length
        UserService.update_user_training_length(user_name, training_length)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def is_user_created(self, request, context) -> user_service_pb2.CheckResponse:
        user_name = request.user_name
        res = UserService.is_user_created(user_name)

        # Convert Pydantic model to Protobuf response
        response = user_service_pb2.CheckResponse(
            result=res
        )
        context.set_details("Response details: " + str(response))
        return response

    @log_decorator(my_logger=logger)
    def create_user_by_DTO(self, request, context):
        user_dto = UserAuthTelegramDTO.model_validate(request)
        UserService.create_user_by_DTO(user_dto)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def create_user(self, request, context) -> empty_pb2.Empty:
        UserService.create_user(
            request.name,
            request.password,
            request.email,
            request.telegram_user_id,
            request.training_length)
        return empty_pb2.Empty()
