.PHONY: proto clean install test lint format

# Generate Python code from proto files
proto:
	.venv/bin/python -m grpc_tools.protoc \
		-I../grpc/proto \
		--python_out=./sova_sdk/generated \
		--grpc_python_out=./sova_sdk/generated \
		--pyi_out=./sova_sdk/generated \
		../grpc/proto/auth.proto \
		../grpc/proto/dto.proto \
		../grpc/proto/searcher.proto \
		../grpc/proto/block_engine.proto
	# Fix imports in generated files
	sed -i '' 's/^import dto_pb2/from . import dto_pb2/' sova_sdk/generated/searcher_pb2.py
	sed -i '' 's/^import dto_pb2/from . import dto_pb2/' sova_sdk/generated/block_engine_pb2.py

# Clean generated files
clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf sova_sdk/generated/*.py sova_sdk/generated/*.pyi
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Install package in development mode
install:
	pip install -e .

# Run tests
test:
	pytest tests/ -v

# Lint code
lint:
	pylint sova_sdk/

# Format code
format:
	black sova_sdk/
	isort sova_sdk/

# Setup development environment
setup:
	python3 -m venv .venv
	.venv/bin/pip install -e .
	.venv/bin/pip install pytest black pylint isort
