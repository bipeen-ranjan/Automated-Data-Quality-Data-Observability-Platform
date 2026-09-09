from dataclasses import dataclass
from typing import Optional


@dataclass
class QualityResult:
    """
    Standard structure for a single data-quality check result.
    """

    check_name: str
    column: Optional[str]
    affected_count: int
    total_count: int
    rate: float
    severity: str
    message: str

    @property
    def passed(self):
        """
        Return True when no issues were detected.
        """
        return self.affected_count == 0