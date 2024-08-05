import grpc
from concurrent import futures

from cfg.сonfig import settings
from src.redis.redis_client import RedisImplementation
from src.grpc.process_service import process_service_pb2_grpc
from src.grpc.process_service.process_server import ProcessServiceServicer
from src.grpc.user_service import user_service_pb2_grpc
from src.grpc.user_service.user_server import UserServiceServicer
from src.grpc.word_service import word_service_pb2_grpc
from src.grpc.word_service.word_service import WordServiceServicer
from src.log.logger import CustomLogger


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceGRPCServicer_to_server(UserServiceServicer(), server)
    word_service_pb2_grpc.add_WordServiceServicer_to_server(WordServiceServicer(), server)
    process_service_pb2_grpc.add_ProcessServiceServicer_to_server(ProcessServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # Initialize custom logger
    logger_instance = CustomLogger()
    logger = logger_instance.get_logger(__name__)
    logger.info("Server started on port 50051.")

    # Initialize Redis
    RedisImplementation(host=settings.get_REDIS_HOST,
                        port=settings.get_REDIS_PORT,
                        decode_responses=settings.get_REDIS_DECODE_RESPONSES)

    server.wait_for_termination()

if __name__ == '__main__':
    serve()