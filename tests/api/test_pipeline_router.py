import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status
from typing import Dict, List

from src.app.main import app
from src.domain.entities.pipeline import PipelineDto, PipelineCreateDto

BASE_URL = "http://localhost/api/v1"
PIPELINE_BASE_URL = "/pipelines"
PIPELINE_ID = 1
SPECIFIC_PIPELINE_URL = f"{PIPELINE_BASE_URL}/{PIPELINE_ID}"

SAMPLE_PIPELINE_CREATE_REQUEST = {"name": "test_pipeline", "description": "Test pipeline description"}
SAMPLE_PIPELINE_DTO = PipelineDto(id=PIPELINE_ID, name="test_pipeline", description="Test pipeline description", workflow="workflow")


@pytest.mark.asyncio
class TestPipelineRoutes:
    async def test_create_pipeline_success(self):
        """Integration test for successful creation of a pipeline."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.post(PIPELINE_BASE_URL, json=SAMPLE_PIPELINE_CREATE_REQUEST)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["name"] == SAMPLE_PIPELINE_CREATE_REQUEST["name"]
        assert response_data["description"] == SAMPLE_PIPELINE_CREATE_REQUEST["description"]

    async def test_get_all_pipelines_success(self):
        """Integration test for successful retrieval of all pipelines."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(PIPELINE_BASE_URL)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "pipelines" in response_data
        assert isinstance(response_data["pipelines"], list)

    async def test_get_pipeline_success(self):
        """Integration test for successful retrieval of a single pipeline."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(SPECIFIC_PIPELINE_URL)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == PIPELINE_ID
        assert response_data["name"] == "test_pipeline"
        assert response_data["description"] == "Test pipeline description"

    async def test_get_pipeline_not_found(self):
        """Integration test for retrieving a non-existent pipeline."""
        non_existent_pipeline_id = 999
        url = f"{PIPELINE_BASE_URL}/{non_existent_pipeline_id}"
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Pipeline '{non_existent_pipeline_id}' not found"
