import json
import pytest
from types import SimpleNamespace
from sqlalchemy_utils import force_instant_defaults
from fastapi.testclient import TestClient
from tests.common import Session
from app.main import app
from app.database import db_session
from app.settings import settings


class ApiTest:
    client: TestClient
    session: Session

    @pytest.fixture(autouse=True)
    def setup(self, request, settings):
        self.client = TestClient(
            app, headers={"Authorization": f"Token {settings.access_token}"}
        )
        self.session = Session()

        def override_db_session():
            try:
                yield self.session
            finally:
                self.session.close()

        app.dependency_overrides[db_session] = override_db_session  # noqa

        def teardown():
            self.session.rollback()
            Session.remove()

        request.addfinalizer(teardown)

    def objectify(
        self, *dicts: dict, default=None
    ) -> SimpleNamespace | list[SimpleNamespace]:
        def convert(data: dict):
            return json.loads(
                json.dumps(data), object_hook=lambda d: SimpleNamespace(**d)
            )

        objects = [convert(d) for d in dicts]
        if len(objects) == 1:
            return next(iter(objects), default)
        return objects

    def post(
        self,
        url: str,
        objectify: bool = True,
        status: int = None,
        internal: bool = False,
        **kwargs,
    ):
        if internal:
            kwargs.update(headers={"X-Internal": settings.ms.internal_key})
        response = self.client.post(url, **kwargs)
        if status is not None:
            assert response.status_code == status
        if objectify:
            return self.objectify(response.json())
        return response.json()


class UnitTest:
    @pytest.fixture(autouse=True)
    def setup(self):
        force_instant_defaults()
