# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from collections.abc import Iterable
from typing import Any, Optional

from braket.circuits.instruction import Instruction
from braket.circuits.measure import Measure
from braket.circuits.noise_model.circuit_instruction_criteria import CircuitInstructionCriteria
from braket.circuits.noise_model.criteria import Criteria, CriteriaKey, CriteriaKeyResult
from braket.circuits.noise_model.criteria_input_parsing import parse_qubit_input
from braket.registers.qubit_set import QubitSetInput


class MeasureCriteria(CircuitInstructionCriteria):
    """This class models noise Criteria based on Measure instructions."""

    def __init__(self, qubits: Optional[QubitSetInput] = None):
        """Creates Measure-based Criteria.

        Args:
            qubits (Optional[QubitSetInput]): A set of relevant qubits. If no qubits are
                provided, all (possible) qubits are considered to be relevant.
        """
        self._qubits = parse_qubit_input(qubits, 1)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._qubits})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(qubits={self._qubits})"

    def applicable_key_types(self) -> Iterable[CriteriaKey]:
        """Returns an Iterable of criteria keys."""
        return [CriteriaKey.QUBIT]

    def get_keys(self, key_type: CriteriaKey) -> CriteriaKeyResult | set[Any]:
        """Gets the keys for a given CriteriaKey."""
        if key_type == CriteriaKey.QUBIT:
            return CriteriaKeyResult.ALL if self._qubits is None else set(self._qubits)
        return set()

    def to_dict(self) -> dict:
        """Converts this object to a dictionary."""
        qubits = list(self._qubits) if self._qubits is not None else None
        return {"__class__": self.__class__.__name__, "qubits": qubits}

    def instruction_matches(self, instruction: Instruction) -> bool:
        """Returns true if an Instruction matches the criteria."""
        if not isinstance(instruction.operator, Measure):
            return False
        return CircuitInstructionCriteria._check_target_in_qubits(self._qubits, instruction.target)

    @classmethod
    def from_dict(cls, criteria: dict) -> Criteria:
        """Deserializes a dictionary into a Criteria object."""
        return MeasureCriteria(criteria["qubits"])


Criteria.register_criteria(MeasureCriteria)
