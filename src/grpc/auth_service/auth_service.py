from fastapi import HTTPException
from cfg.сonfig import settings
from src.dto.schema import UserResponse, RegisterRequest
from src.grpc.auth_service import auth_service_pb2
from src.grpc.auth_service.client_auth_manager import GRPCClientAuthManager
from src.log.logger import log_decorator, CustomLogger

class AuthService:

    server_address = settings.get_AUTH_GRPC_conn

    @staticmethod
    @log_decorator(my_logger=CustomLogger())
    def register(register_request: RegisterRequest) -> UserResponse:
        with GRPCClientAuthManager(AuthService.server_address) as auth_manager:
            stub = auth_manager.get_stub()
            request = auth_service_pb2.RegisterRequest(
                username=register_request.username,
                password=register_request.password,
                email=register_request.email,
                telegram_user_id=register_request.telegram_user_id
            )
            response = stub.register(request)
            response_message = UserResponse(
                username=response.username,
                message=response.message
            )
            return response_message
