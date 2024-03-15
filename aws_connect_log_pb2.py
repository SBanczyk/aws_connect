# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aws_connect_log.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='aws_connect_log.proto',
  package='aws_connect',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15\x61ws_connect_log.proto\x12\x0b\x61ws_connect\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa9\x01\n\x08\x41uditLog\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04user\x18\x02 \x01(\t\x12,\n\x06\x61\x63tion\x18\x03 \x01(\x0e\x32\x1c.aws_connect.AuditLog.Action\x12\x13\n\x0binstance_id\x18\x04 \x01(\t\"\x1d\n\x06\x41\x63tion\x12\x08\n\x04STOP\x10\x00\x12\t\n\x05START\x10\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_AUDITLOG_ACTION = _descriptor.EnumDescriptor(
  name='Action',
  full_name='aws_connect.AuditLog.Action',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STOP', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='START', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=212,
  serialized_end=241,
)
_sym_db.RegisterEnumDescriptor(_AUDITLOG_ACTION)


_AUDITLOG = _descriptor.Descriptor(
  name='AuditLog',
  full_name='aws_connect.AuditLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='aws_connect.AuditLog.timestamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='aws_connect.AuditLog.user', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='action', full_name='aws_connect.AuditLog.action', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='aws_connect.AuditLog.instance_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUDITLOG_ACTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=241,
)

_AUDITLOG.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_AUDITLOG.fields_by_name['action'].enum_type = _AUDITLOG_ACTION
_AUDITLOG_ACTION.containing_type = _AUDITLOG
DESCRIPTOR.message_types_by_name['AuditLog'] = _AUDITLOG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AuditLog = _reflection.GeneratedProtocolMessageType('AuditLog', (_message.Message,), {
  'DESCRIPTOR' : _AUDITLOG,
  '__module__' : 'aws_connect_log_pb2'
  # @@protoc_insertion_point(class_scope:aws_connect.AuditLog)
  })
_sym_db.RegisterMessage(AuditLog)


# @@protoc_insertion_point(module_scope)
