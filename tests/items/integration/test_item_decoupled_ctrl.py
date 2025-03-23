import pytest
from litestar.testing import TestClient

from app.utils.lock_test import lock_test


@pytest.mark.separate
@pytest.mark.integration
class TestItemDecoupledCtrlIntegration:
    @pytest.fixture(autouse=True)
    def lock(self, lock_test):
        pass

    def test_post_item(
        self,
        fixture_integration_test_client_with_auth: TestClient,
        fixture_new_item: dict,
    ):
        client = fixture_integration_test_client_with_auth

        # POST item 1, passing the dictionary directly as the request body
        response = client.post("/items_decoupled", json=fixture_new_item)
        assert response.is_success

        response = client.get("/items")
        response_json = response.json()
        assert response.is_success
        assert len(response_json) == 1  # Adjusted to match one item for this test case
        assert response_json[0]["Id"] is not None

    def test_delete_item(
        self,
        fixture_integration_test_client_with_auth: TestClient,
        fixture_new_item: dict,
    ):
        response = fixture_integration_test_client_with_auth.post(
            "/items_decoupled",
            json=fixture_new_item,  # Pass the dictionary directly
        )
        assert response.is_success

        response = fixture_integration_test_client_with_auth.get("/items")
        assert response.is_success
        item_id = response.json()[0]["Id"]

        response = fixture_integration_test_client_with_auth.delete(
            f"/items_decoupled/{item_id}"
        )
        assert response.is_success

        response = fixture_integration_test_client_with_auth.get("/items")
        assert response.is_success
        assert len(response.json()) == 0

    def test_patch_item(
        self,
        fixture_integration_test_client_with_auth: TestClient,
        fixture_new_item: dict,
        fixture_update_item: dict,
    ):
        response = fixture_integration_test_client_with_auth.post(
            "/items_decoupled",
            json=fixture_new_item,  # Pass the dictionary directly
        )
        assert response.is_success

        response = fixture_integration_test_client_with_auth.get("/items")
        assert response.is_success
        item_id = response.json()[0]["Id"]

        update_item = fixture_update_item
        update_item["Id"] = item_id  # Modify the update item to include the ID
        response = fixture_integration_test_client_with_auth.patch(
            "/items_decoupled",
            json=update_item,  # Send the updated item as JSON
        )
        assert response.is_success

        response = fixture_integration_test_client_with_auth.get("/items")
        item = response.json()[0]

        assert item["Id"] == item_id
        assert item["ValueStr"] == update_item["ValueStr"]
        assert item["ValueInt"] == update_item["ValueInt"]
        assert item["ValueFloat"] == update_item["ValueFloat"]
