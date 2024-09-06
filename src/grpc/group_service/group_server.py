from google.protobuf import empty_pb2
from src.dto.schema import GroupAddDTO
from src.grpc.error_handler import grpc_error_handler
from src.grpc.group_service import group_service_pb2
from src.grpc.group_service.group_service_pb2_grpc import GroupServiceServicer
from src.grpc.mapping_helper import convert_proto_to_pydantic
from src.log.logger import log_decorator, logger
from src.service.group_word_service import GroupWordService


class GroupServiceServicer(GroupServiceServicer):

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def get_groups_name_by_user_name(self, request, context):
        user_name = request.user_name
        res_group_list = GroupWordService.get_groups_name_by_user_name(user_name)
        result = group_service_pb2.GetGroupsNameByUserNameResponse(
            group_names=res_group_list
        )
        return result

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def create_group(self, request, context):
        group_dto = convert_proto_to_pydantic(request.new_group, GroupAddDTO)
        GroupWordService.create_group(group_dto)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def get_group_id_by_group_name(self, request, context):
        group_name = request.group_name
        res_uuid = GroupWordService.get_group_id_by_group_name(group_name)
        result = group_service_pb2.GetGroupIdByGroupNameResponse(group_id=str(res_uuid))
        return result

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def is_group_created(self, request, context):
        group_name = request.group_name
        is_group_created = GroupWordService.is_group_created(group_name)
        result = group_service_pb2.IsGroupCreatedResponse(created=is_group_created)
        return result

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def update_group(self, request, context):
        group_id = request.group_id
        new_group_name = request.new_group_name
        GroupWordService.update_group(group_id, new_group_name)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    @grpc_error_handler
    def delete_group(self, request, context):
        group_id = request.group_id
        GroupWordService.delete_group(group_id)
        return empty_pb2.Empty()