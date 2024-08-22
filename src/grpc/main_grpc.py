import grpc
from concurrent import futures

from cfg.сonfig import settings
from src.grpc.group_service import group_service_pb2_grpc
from src.grpc.group_service.group_server import GroupServiceServicer
from src.grpc.level_service import level_service_pb2_grpc
from src.grpc.level_service.level_server import LevelServiceServicer
from src.grpc.word_type_service import word_type_service_pb2_grpc
from src.grpc.word_type_service.word_type_server import WordTypeServiceServicer
from src.redis.redis_client import RedisImplementation
from src.grpc.process_service import process_service_pb2_grpc
from src.grpc.process_service.process_server import ProcessServiceServicer
from src.grpc.user_service import user_service_pb2_grpc
from src.grpc.user_service.user_server import UserServiceServicer
from src.grpc.word_service import word_service_pb2_grpc
from src.grpc.word_service.word_server import WordServiceServicer
from src.log.logger import CustomLogger


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceGRPCServicer_to_server(UserServiceServicer(), server)
    word_service_pb2_grpc.add_WordServiceServicer_to_server(WordServiceServicer(), server)
    level_service_pb2_grpc.add_LevelServiceGRPCServicer_to_server(LevelServiceServicer(), server)
    group_service_pb2_grpc.add_GroupServiceServicer_to_server(GroupServiceServicer(), server)
    word_type_service_pb2_grpc.add_WordTypeServiceServicer_to_server(WordTypeServiceServicer(), server)
    process_service_pb2_grpc.add_ProcessServiceServicer_to_server(ProcessServiceServicer(), server)
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    server.start()

    # Initialize custom logger
    logger_instance = CustomLogger()
    logger = logger_instance.get_logger(__name__)
    logger.info(f"Server started on port {settings.GRPC_PORT}.")

    # Initialize Redis
    RedisImplementation(host=settings.get_REDIS_HOST,
                        port=settings.get_REDIS_PORT,
                        decode_responses=settings.get_REDIS_DECODE_RESPONSES)

    server.wait_for_termination()

if __name__ == '__main__':
    serve()