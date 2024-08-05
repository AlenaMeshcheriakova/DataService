import uuid
from datetime import datetime
from typing import Type, TypeVar, Dict, Any
from pydantic import BaseModel

from google.protobuf import timestamp_pb2, wrappers_pb2

from src.dto.learning_set import LearningSet
from src.dto.schema import UserCreateFullDTO, WordDTO
from src.grpc.process_service import process_service_pb2
from src.grpc.user_service import user_service_pb2
from src.grpc.word_service import word_service_pb2

# Define type variables for generic conversion
PydanticModelType = TypeVar('PydanticModelType', bound=BaseModel)
ProtoMessageType = TypeVar('ProtoMessageType')


def datetime_to_timestamp(dt: datetime) -> timestamp_pb2.Timestamp():
    """Convert a datetime object to a google.protobuf.Timestamp object."""
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(dt)
    return ts


def parse_timestamp(proto_timestamp: timestamp_pb2.Timestamp) -> datetime:
    """Converts a Protobuf Timestamp to a Python datetime object."""
    return datetime.fromtimestamp(proto_timestamp.seconds + proto_timestamp.nanos / 1e9)

def parse_value(value: Any, target_type: Type) -> Any:
    """Converts a value to the target_type, handling common types."""
    if target_type == datetime and isinstance(value, timestamp_pb2.Timestamp):
        return parse_timestamp(value)
    elif target_type == uuid.UUID and isinstance(value, str):
        return uuid.UUID(value)
    elif target_type == str and isinstance(value, bytes):
        return value.decode('utf-8')
    return value

def get_annotations(pydantic_model: Type[BaseModel]):
    """Get annotations from the Pydantic model and its superclasses."""
    annotations = {}

    # Traverse the class hierarchy
    for cls in pydantic_model.mro():
        if issubclass(cls, BaseModel) and cls is not BaseModel:
            annotations.update(cls.__annotations__)

    return annotations

def convert_proto_to_pydantic(proto_msg: Any, pydantic_model: Type[BaseModel]) -> BaseModel:
    """Converts a Protobuf message to a Pydantic model."""
    pydantic_fields = get_annotations(pydantic_model)
    pydantic_data = {}

    for field_name, field_type in pydantic_fields.items():
        if hasattr(proto_msg, field_name):
            proto_value = getattr(proto_msg, field_name)
            pydantic_data[field_name] = parse_value(proto_value, field_type)

    return pydantic_model(**pydantic_data)


def pydantic_to_protobuf(pydantic_model: Any, protobuf_class: Type[Any], field_mapping: Dict[str, str]) -> Any:
    """Convert a Pydantic model to a Protobuf message based on a field mapping."""

    # Create an instance of the Protobuf message
    proto_message = protobuf_class()

    for pydantic_field, protobuf_field in field_mapping.items():
        value = getattr(pydantic_model, pydantic_field, None)

        if isinstance(value, datetime):
            timestamp = datetime_to_timestamp(value)
            if protobuf_field == "created_at":
                proto_message.created_at.CopyFrom(timestamp)
            elif protobuf_field == "updated_at":
                proto_message.updated_at.CopyFrom(timestamp)
            else:
                proto_message.__setattr__(protobuf_field, timestamp)
        elif isinstance(value, uuid.UUID):
            setattr(proto_message, protobuf_field, str(value))
        elif isinstance(value, str):
            # Handle StringValue wrapper field
            setattr(proto_message, protobuf_field, value)
        elif isinstance(value, bool):
            # Handle BoolValue wrapper field
            setattr(proto_message, protobuf_field, value)
        elif value is None:
            # TODO: Check it - Can be Problem with serialisation
            proto_message.ClearField(protobuf_field)
        else:
            # Direct assignment for other types
            setattr(proto_message, protobuf_field, value)
    return proto_message

def learning_set_to_protobuf(learning_set: LearningSet) -> Any:
    # Convert Pydantic model to Protobuf response
    user_mapping = {k: k for k, v in learning_set.user.dict().items()}
    word_mapping = {k: k for k, v in learning_set.words[0].dict().items()}

    words_list = []
    for word in learning_set.words:
        response_line = pydantic_to_protobuf(word, word_service_pb2.WordDTOResponse,
                                             word_mapping)
        words_list.append(response_line)

    response_words = word_service_pb2.GetListWordDTOResponse(
        word=words_list
    )

    resulted_learning_set = process_service_pb2.LearningSetDTO(
        user=pydantic_to_protobuf(learning_set.user, user_service_pb2.UserCreateFullDTOResponse, user_mapping),
        words=response_words,
        current_training_position=learning_set.current_training_position
    )

    return resulted_learning_set


def learning_set_from_protobuf(request: Any) -> LearningSet:
    # Convert Pydantic model to Protobuf response
    # Convert to UserCreateFullDTO
    user_protobuff = request.user
    user = convert_proto_to_pydantic(user_protobuff, UserCreateFullDTO)
    # Convert to List[WordDTO]
    words_protobuff = request.words  # GetListWordDTOResponse
    words = []
    for word_protobuff in words_protobuff.word:
        word_dto = convert_proto_to_pydantic(word_protobuff, WordDTO)
        words.append(word_dto)
    # Get training_position
    current_training_position = request.current_training_position

    # Create LearningSet
    learning_set = LearningSet(user, words, current_training_position)
    return learning_set