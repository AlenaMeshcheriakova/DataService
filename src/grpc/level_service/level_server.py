import uuid

from google.protobuf import empty_pb2

from src.grpc.level_service.level_service_pb2_grpc import LevelServiceGRPC
from src.grpc.mapping_helper import pydantic_to_protobuf, convert_protobuf_level_enum_to_python_enum
from src.service.level_service import LevelService
from src.grpc.level_service import level_service_pb2


from src.log.logger import log_decorator, logger

class LevelServiceServicer(LevelServiceGRPC):
    @log_decorator(my_logger=logger)
    def create_levels(self, request, context):
        LevelService.create_levels()
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def create_level(self, request, context):
        LevelService.create_level(request.level_enum)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def get_levels(self, request, context):
        level_list = LevelService.get_levels()

        # Create a mapping template
        level_mapping = {k: k for k, v in level_list.pop().dict().items()}

        res_levels = []
        for level in level_list:
            response_line = pydantic_to_protobuf(level, level_service_pb2.LevelDTO, level_mapping)
            res_levels.append(response_line)

        level_list = level_service_pb2.LevelList(
            levels=res_levels
        )
        return level_list

    @log_decorator(my_logger=logger)
    def get_level_id_by_name(self, request, context):
        level_enum = request.level_enum
        res_id = LevelService.get_level_id_by_name(convert_protobuf_level_enum_to_python_enum(level_enum))
        return level_service_pb2.LevelIdResponse(id=str(res_id))

    @log_decorator(my_logger=logger)
    def get_level_by_id(self, request, context):
        level_id = request.level_id
        level = LevelService.get_level_by_id(uuid.UUID(level_id))

        # Create a mapping template
        level_mapping = {k: k for k, v in level.dict().items()}
        return pydantic_to_protobuf(level, level_service_pb2.LevelDTO, level_mapping)

    @log_decorator(my_logger=logger)
    def update_level(self, request, context):
        level_id = uuid.UUID(request.level_id)
        updated_data = request.updated_data  # Assuming this is passed as a dict-like object.
        LevelService.update_level(level_id, updated_data)
        return empty_pb2.Empty()

    @log_decorator(my_logger=logger)
    def delete_level(self, request, context):
        level_id = uuid.UUID(request.level_id)
        LevelService.delete_level(level_id)
        return empty_pb2.Empty()