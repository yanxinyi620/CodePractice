# My_test_yanxinyi

Testing some ideas!

## proto

cd /d/Github/CodePractice/code_wb/ppc_grpc/proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
python -m grpc_tools.protoc --python_out=. --pyi_out=. --grpc_python_out=. -I. helloworld.proto
