import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status, HTTPException
from unittest.mock import AsyncMock

from src.app.main import app
from src.domain.entities.run import RunDto, RunCreateDto, RunResponse

from tests.conftest import async_client, mock_run_use_case


PIPELINE_ID = 1
RUN_ID = 10
BASE_URL = f"/pipeline/{PIPELINE_ID}"
TRIGGER_RUN_URL = f"{BASE_URL}/trigger_run"
ALL_RUNS_URL = f"{BASE_URL}/runs"
SPECIFIC_RUN_URL = f"{BASE_URL}/runs/{RUN_ID}"

# Sample data for testing
SAMPLE_RUN_CREATE_REQUEST = {"name": "test_run", "configuration": {"param1": "value1"}}
SAMPLE_RUN_CREATE_DTO = RunCreateDto(pipeline_id=PIPELINE_ID, status="test_run", metadata_="meta")
SAMPLE_RUN_DTO = RunDto(id=RUN_ID, pipeline_id=PIPELINE_ID, status="test_run", metadata_="meta")
SAMPLE_RUNS_LIST = [
    RunDto(id=11, pipeline_id=PIPELINE_ID, status="test_run", metadata_="meta"),
    RunDto(id=12, pipeline_id=PIPELINE_ID, status="test_run", metadata_="meta"),
]
SAMPLE_RUNS_RESPONSE = RunResponse(pipeline_id=PIPELINE_ID, runs=SAMPLE_RUNS_LIST)


@pytest.mark.asyncio
async def test_create_pipeline_run_success(async_client: AsyncClient):
    """Test successful creation of a pipeline run."""

    pass


@pytest.mark.asyncio
async def test_create_pipeline_run_pipeline_not_found(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test creation of a run when the pipeline does not exist."""
    pass


@pytest.mark.asyncio
async def test_get_all_pipeline_runs_success(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test successful retrieval of all runs for a pipeline."""
    pass


@pytest.mark.asyncio
async def test_get_all_pipeline_runs_pipeline_not_found(async_client: AsyncClient):
    """Test retrieval of all runs when the pipeline does not exist."""
    pass


@pytest.mark.asyncio
async def test_get_pipeline_run_success(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test successful retrieval of a specific pipeline run."""
    pass


@pytest.mark.asyncio
async def test_get_pipeline_run_pipeline_not_found(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test retrieval of a specific run when the pipeline does not exist."""
    pass


@pytest.mark.asyncio
async def test_get_pipeline_run_not_found(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test retrieval of a specific run that does not exist."""
    pass


@pytest.mark.asyncio
async def test_get_pipeline_run_belongs_to_different_pipeline(async_client: AsyncClient, mock_run_use_case: AsyncMock):
    """Test retrieval of a run that belongs to a different pipeline."""
    pass
