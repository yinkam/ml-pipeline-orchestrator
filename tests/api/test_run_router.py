import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from src.app.main import app

PIPELINE_ID = 1
RUN_ID = 10
BASE_URL = "http://localhost/api/v1"
PIPELINE_ID_BASE_URL = f"/pipeline/{PIPELINE_ID}"
TRIGGER_RUN_URL = f"{PIPELINE_ID_BASE_URL}/trigger_run"
ALL_RUNS_URL = f"{PIPELINE_ID_BASE_URL}/runs"
SPECIFIC_RUN_URL = f"{PIPELINE_ID_BASE_URL}/runs/{RUN_ID}"

SAMPLE_RUN_CREATE_REQUEST = {"status": "test_run", "metadata_": "metadata"}


@pytest.mark.asyncio
class TestRunRoutes:
    async def test_create_pipeline_run_success(self):
        """Integration test for successful creation of a pipeline run."""

        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.post(TRIGGER_RUN_URL, json=SAMPLE_RUN_CREATE_REQUEST)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["pipeline_id"] == PIPELINE_ID


    async def test_get_all_pipeline_runs_success(self):
        """Integration test for successful retrieval of all runs for a pipeline."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(ALL_RUNS_URL)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "pipeline_id" in response_data
        assert response_data["pipeline_id"] == PIPELINE_ID
        assert "runs" in response_data
        assert isinstance(response_data["runs"], list)

    async def test_get_pipeline_run_success(self):
        """Integration test for successful retrieval of a specific pipeline run."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(SPECIFIC_RUN_URL)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == RUN_ID
        assert response_data["pipeline_id"] == PIPELINE_ID

    async def test_create_pipeline_run_pipeline_not_found(self):
        """Integration test for creation of a run when the pipeline does not exist."""
        non_existent_pipeline_id = 999
        url = f"/pipeline/{non_existent_pipeline_id}/trigger_run"
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.post(url, json=SAMPLE_RUN_CREATE_REQUEST)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Pipeline '{non_existent_pipeline_id}' not found"

    async def test_get_all_pipeline_runs_pipeline_not_found(self):
        """Integration test for retrieval of all runs when the pipeline does not exist."""

        non_existent_pipeline_id = 999
        url = f"/pipeline/{non_existent_pipeline_id}/runs"
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Pipeline '{non_existent_pipeline_id}' not found"

    async def test_get_pipeline_run_pipeline_not_found(self):
        """Integration test for retrieval of a specific run when the pipeline does not exist."""

        non_existent_pipeline_id = 999
        url = f"/pipeline/{non_existent_pipeline_id}/runs/{RUN_ID}"
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            response = await client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Pipeline '{non_existent_pipeline_id}' not found"

    async def test_get_pipeline_run_not_found(self):
        """Integration test for retrieval of a specific run that does not exist."""

        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            non_existent_run_id = 999
            url = f"/pipeline/{PIPELINE_ID}/runs/{non_existent_run_id}"
            response = await client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Run with ID {non_existent_run_id} not found."

    async def test_get_pipeline_run_belongs_to_different_pipeline(self):
        """Integration test for retrieval of a run that belongs to a different pipeline."""
        different_pipeline_id = 999

        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            url = f"/pipeline/{different_pipeline_id}/runs/{RUN_ID}"
            response = await client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == f"Run with ID {RUN_ID} does not belong to pipeline with ID {different_pipeline_id}"