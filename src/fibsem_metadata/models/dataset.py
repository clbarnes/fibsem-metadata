from typing import List, Optional
from .sample import Sample
from .acquisition import FIBSEMAcquisition
from .base import Base
from enum import Enum
from .source import Volume
from .view import View
from .publication import Publication


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class Dataset(Base):
    name: str
    description: str
    institutions: List[str]
    software_availability: SoftwareAvailability
    acquisition: Optional[FIBSEMAcquisition]
    sample: Optional[Sample]
    publications: List[Publication]
    volumes: List[Volume]
    views: List[View]


class DatasetCreate(Dataset):
    pass


class DatasetRead(Dataset):
    id: int


class DatasetUpdate(Dataset):
    pass
