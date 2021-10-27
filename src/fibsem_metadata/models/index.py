from enum import Enum
from pydantic import BaseModel, validator
from typing import Any, Dict, Sequence, Optional
from pydantic.color import Color
from fibsem_metadata.models.multiscale.cosem import SpatialTransform
import click


class MeshTypeEnum(str, Enum):
    """
    Strings representing supported mesh formats
    """

    neuroglancer_legacy_mesh = "neuroglancer_legacy_mesh"
    neuroglancer_multilod_draco = "neuroglancer_multilod_draco"


class ArrayContainerTypeEnum(str, Enum):
    n5 = "n5"
    zarr = "zarr"
    precomputed = "precomputed"
    mrc = "mrc"
    hdf5 = "hdf5"
    tif = "tif"


class ContentTypeEnum(str, Enum):
    em = "em"
    lm = "lm"
    prediction = "prediction"
    segmentation = "segmentation"
    analysis = "analysis"


class SampleTypeEnum(str, Enum):
    scalar = "scalar"
    label = "label"


class ContrastLimits(BaseModel):
    start: int
    end: int
    min: int
    max: int


class DisplaySettings(BaseModel):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits
    color: Optional[Color] = "white"
    invertLUT: bool = False


class DataSource(BaseModel):
    name: str
    path: str
    format: str
    transform: SpatialTransform
    description: str = ""
    version: str = "0"
    tags: Sequence[str] = []


class MeshSource(DataSource):
    format: MeshTypeEnum
    ids: Sequence[int]


class VolumeSource(DataSource):
    format: ArrayContainerTypeEnum
    dataType: str
    sampleType: SampleTypeEnum = 'scalar'
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings
    subsources: Sequence[MeshSource] = []


class DatasetView(BaseModel):
    name: str
    description: str
    position: Optional[Sequence[float]]
    scale: Optional[float]
    orientation: Optional[Sequence[float]]
    volumeNames: Sequence[str]

    @validator('orientation')
    def orientation_must_have_unit_norm(cls, v: Optional[Sequence[float]]):
        if v is not None:
            if len(v) != 4:
                raise ValueError(f'Orientation must have length 4, got {v} with {len(v)}')
            length = sum([x ** 2 for x in v]) ** .5
            if length % 1.0 != 0:
                raise ValueError('Orientation vector does not have a unit length. Got {length}.')
        return v


class DatasetViewCollection(BaseModel):
    views: Sequence[DatasetView]


class DatasetIndex(BaseModel):
    name: str
    volumes: Sequence[VolumeSource]
    views: Sequence[DatasetView]


@click.command()
def main() -> None:
    print(DatasetIndex.schema_json(indent=2))


if __name__ == "__main__":
    main()
