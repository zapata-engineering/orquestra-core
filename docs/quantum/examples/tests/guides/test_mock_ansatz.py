import pytest
from orquestra.vqa.api.ansatz_test import AnsatzTests

from ...guides.mock_ansatz import MockAnsatz


class TestMockAnsatz(AnsatzTests):
    @pytest.fixture()
    def number_of_params(self):
        return 3

    @pytest.fixture
    def ansatz(self):
        return MockAnsatz(
            number_of_layers=1,
            number_of_qubits=3,
        )

    @pytest.fixture
    def target_unitary(self, number_of_params):
        return create_X_target_unitary(number_of_params)
