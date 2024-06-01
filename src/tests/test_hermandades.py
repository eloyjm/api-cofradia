from unittest.mock import MagicMock
import pytest
from src.app.routers import hermandades
import unittest
from sqlalchemy import Enum


class TestHermandades(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = MagicMock()
    
    @pytest.mark.asyncio
    async def test_get_hermandades(self):
        self.mock_db.query.return_value.all.return_value = [{"id": "1538b1d6-35aa-4a25-954f-3ac896877f95", "name": "Hermandad 1"}]

        result = await hermandades.get_hermandades(self.mock_db)

        assert result == self.mock_db.query().all()

    @pytest.mark.asyncio
    async def test_get_hermandades_by_id(self):
        self.mock_db.query.return_value.filter.return_value.first.return_value = {"id": "1538b1d6-35aa-4a25-954f-3ac896877f95", "name": "Hermandad 1"}

        result = await hermandades.get_hermandades_by_id(self.mock_db, "1538b1d6-35aa-4a25-954f-3ac896877f95")

        assert result == self.mock_db.query().filter().first()
