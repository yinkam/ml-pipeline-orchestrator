# tests/conftest.py (or a similar test setup file)
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from src.app.main import app as main_app
from src.interfaces.api.v1.endpoints.run import run_router
from src.domain.use_cases.run import RunUseCase  # Import the actual use case

@pytest.fixture
async def test_app() -> FastAPI:
    """Fixture to create a test FastAPI application."""
    app = main_app  # Use your main application instance
    app.include_router(run_router) # Ensure the router is included
    return app


# @pytest.fixture
# async def async_client(test_app: FastAPI) -> AsyncClient:
#     """Fixture to create an async test client for the test app."""
#     async with AsyncClient(app=test_app, base_url="http://test") as client:
#         return client

@pytest.fixture
def mock_run_use_case() -> AsyncMock:
    """Fixture to create a mock RunUseCase."""
    return AsyncMock(spec=RunUseCase)

@pytest.fixture
async def async_client(test_app: FastAPI) -> AsyncClient:
    """Fixture to create an async test client with mocked dependencies."""
    test_app.include_router(run_router)

    # Override the dependency for RunUseCase
    # test_app.dependency_overrides[RunUseCase] = lambda: mock_run_use_case

    async with AsyncClient(app=test_app, base_url="http://test") as client:
        return client