import grpc
from functools import wraps
import psycopg2
from psycopg2 import errors

def grpc_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        context = args[2]
        # context = kwargs.get('context')
        if context is None:
            raise ValueError("Context must be provided as a keyword argument.")

        try:
            return func(*args, **kwargs)

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except errors.UniqueViolation as e:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
        except IndexError as e:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, str(e))
        except OverflowError as e:
            context.abort(grpc.StatusCode.OUT_OF_RANGE, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Unexpected error: {str(e)}")
    return wrapper