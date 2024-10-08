# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/grpc/process_service/process_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from src.grpc.word_service import word_service_pb2 as src_dot_grpc_dot_word__service_dot_word__service__pb2
from src.grpc.user_service import user_service_pb2 as src_dot_grpc_dot_user__service_dot_user__service__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.src/grpc/process_service/process_service.proto\x12\x0eprocessservice\x1a\x1bgoogle/protobuf/empty.proto\x1a(src/grpc/word_service/word_service.proto\x1a(src/grpc/user_service/user_service.proto\"a\n\x1bStartLearningProcessRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12/\n\tword_type\x18\x02 \x01(\x0e\x32\x1c.processservice.WordTypeEnum\"[\n\x15GetLearningSetRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12/\n\tword_type\x18\x02 \x01(\x0e\x32\x1c.processservice.WordTypeEnum\"\xbc\x01\n\x1dUpdateLearningProgressRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07word_id\x18\x02 \x01(\t\x12\x13\n\x0bgerman_word\x18\x03 \x01(\t\x12\x33\n\x0buser_action\x18\x04 \x01(\x0e\x32\x1e.processservice.UserActionEnum\x12/\n\tword_type\x18\x05 \x01(\x0e\x32\x1c.processservice.WordTypeEnum\"\x9e\x01\n\x0eLearningSetDTO\x12\x35\n\x04user\x18\x01 \x01(\x0b\x32\'.user_service.UserCreateFullDTOResponse\x12\x32\n\x05words\x18\x02 \x01(\x0b\x32#.wordservice.GetListWordDTOResponse\x12!\n\x19\x63urrent_training_position\x18\x03 \x01(\x05*<\n\x0cWordTypeEnum\x12\x0c\n\x08STANDARD\x10\x00\x12\n\n\x06\x43USTOM\x10\x01\x12\x12\n\x0eTEST_WORD_TYPE\x10\x02*L\n\x0eUserActionEnum\x12\x10\n\x0c\x41LREADY_KNOW\x10\x00\x12\x14\n\x10\x42\x41\x43K_TO_LEARNING\x10\x01\x12\x12\n\x0eUNKNOWN_ACTION\x10\x02\x32\x89\x03\n\x0eProcessService\x12\x65\n\x16start_learning_process\x12+.processservice.StartLearningProcessRequest\x1a\x1e.processservice.LearningSetDTO\x12Y\n\x10get_learning_set\x12%.processservice.GetLearningSetRequest\x1a\x1e.processservice.LearningSetDTO\x12\x61\n\x18update_learning_progress\x12-.processservice.UpdateLearningProgressRequest\x1a\x16.google.protobuf.Empty\x12R\n\x18\x61\x64\x64_learning_set_to_cash\x12\x1e.processservice.LearningSetDTO\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'src.grpc.process_service.process_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WORDTYPEENUM']._serialized_start=723
  _globals['_WORDTYPEENUM']._serialized_end=783
  _globals['_USERACTIONENUM']._serialized_start=785
  _globals['_USERACTIONENUM']._serialized_end=861
  _globals['_STARTLEARNINGPROCESSREQUEST']._serialized_start=179
  _globals['_STARTLEARNINGPROCESSREQUEST']._serialized_end=276
  _globals['_GETLEARNINGSETREQUEST']._serialized_start=278
  _globals['_GETLEARNINGSETREQUEST']._serialized_end=369
  _globals['_UPDATELEARNINGPROGRESSREQUEST']._serialized_start=372
  _globals['_UPDATELEARNINGPROGRESSREQUEST']._serialized_end=560
  _globals['_LEARNINGSETDTO']._serialized_start=563
  _globals['_LEARNINGSETDTO']._serialized_end=721
  _globals['_PROCESSSERVICE']._serialized_start=864
  _globals['_PROCESSSERVICE']._serialized_end=1257
# @@protoc_insertion_point(module_scope)
