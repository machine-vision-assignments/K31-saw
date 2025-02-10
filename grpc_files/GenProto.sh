#!/bin/bash

python -m grpc_tools.protoc -I./ -IK31_grpc/packages/Grpc.Tools/2.62.0/build/native/include -IK31_grpc/packages/Grpc.Tools/2.62.0/build/native/include/google/protobuf --python_out=./K31_py --pyi_out=./K31_py --grpc_python_out=./K31_py k31.proto