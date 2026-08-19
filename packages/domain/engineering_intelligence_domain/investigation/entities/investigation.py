from dataclasses import dataclass
from datetime import datetime
from enums import StreEnum
from uuid import UUID, uuid4

class InvestigationStatus(StreEnum):
    CREATED = "created"
    PLANNING = "planning"
    INVESTIGATING = "investigating"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Investigation:
    id: UUID
    status: InvestigationStatus
    created_at: datetime

@classmethod
def create(cls) -> "Investigation":
    return cls(
        id=uuid4(),
        status=InvestigationStatus.CREATED,
        created_at=datetime.now(datetime.timezone.utc)
    )

def start(self) -> None:
    if self.status != InvestigationStatus.CREATED:
        raise ValueError("Investigation can only be started from the 'created' status.")
    self.status = InvestigationStatus.PLANNING
