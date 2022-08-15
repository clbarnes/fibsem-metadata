"""init

Revision ID: 410ba6718e3c
Revises: 13c22f4fd9a4
Create Date: 2022-06-30 13:36:48.546986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "410ba6718e3c"
down_revision = "13c22f4fd9a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "content_type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_content_type_id"), "content_type", ["id"], unique=False)
    op.create_table(
        "fibsem_acquisition",
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("instrument", sa.String(), nullable=True),
        sa.Column("institution", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column(
            "grid_spacing", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("dimensions", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=True),
        sa.Column("bias_voltage", sa.Float(), nullable=True),
        sa.Column("scan_rate", sa.Float(), nullable=True),
        sa.Column("current", sa.Float(), nullable=True),
        sa.Column("primary_energy", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "publication",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sample",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("protocol", sa.String(), nullable=True),
        sa.Column("contributions", sa.String(), nullable=True),
        sa.Column("organism", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("type", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("subtype", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("treatment", postgresql.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("institutions", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("software_availability", sa.String(), nullable=True),
        sa.Column("acquisition_id", sa.Integer(), nullable=True),
        sa.Column("sample_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["acquisition_id"],
            ["fibsem_acquisition.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sample_id"],
            ["sample.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dataset_acquisition_id"), "dataset", ["acquisition_id"], unique=False
    )
    op.create_index(op.f("ix_dataset_name"), "dataset", ["name"], unique=True)
    op.create_index(
        op.f("ix_dataset_sample_id"), "dataset", ["sample_id"], unique=False
    )
    op.create_table(
        "publication_to_dataset",
        sa.Column("publication_id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.ForeignKeyConstraint(
            ["publication_id"],
            ["publication.id"],
        ),
        sa.PrimaryKeyConstraint("publication_id", "dataset_id"),
    )
    op.create_index(
        op.f("ix_publication_to_dataset_dataset_id"),
        "publication_to_dataset",
        ["dataset_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_publication_to_dataset_publication_id"),
        "publication_to_dataset",
        ["publication_id"],
        unique=False,
    )
    op.create_table(
        "view",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("dataset_name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("position", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("scale", sa.Float(), nullable=True),
        sa.Column("orientation", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_name"],
            ["dataset.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_view_dataset_name"), "view", ["dataset_name"], unique=False
    )
    op.create_index(op.f("ix_view_name"), "view", ["name"], unique=False)
    op.create_table(
        "volume",
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("format", sa.String(), nullable=True),
        sa.Column("transform", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sample_type", sa.String(), nullable=True),
        sa.Column("content_type", sa.String(), nullable=True),
        sa.Column(
            "display_settings", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("dataset_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_name"],
            ["dataset.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_volume_dataset_name"), "volume", ["dataset_name"], unique=False
    )
    op.create_index(op.f("ix_volume_id"), "volume", ["id"], unique=False)
    op.create_index(op.f("ix_volume_name"), "volume", ["name"], unique=False)
    op.create_table(
        "crop",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("shape", postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column("completion_stage", sa.String(), nullable=True),
        sa.Column(
            "transform_world", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "transform_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["volume.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_crop_completion_stage"), "crop", ["completion_stage"], unique=False
    )
    op.create_index(op.f("ix_crop_description"), "crop", ["description"], unique=False)
    op.create_index(op.f("ix_crop_name"), "crop", ["name"], unique=True)
    op.create_table(
        "mesh",
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("format", sa.String(), nullable=True),
        sa.Column("transform", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("volume_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["volume_id"],
            ["volume.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_mesh_name"), "mesh", ["name"], unique=False)
    op.create_index(op.f("ix_mesh_volume_id"), "mesh", ["volume_id"], unique=False)
    op.create_table(
        "view_to_volume",
        sa.Column("view_id", sa.Integer(), nullable=False),
        sa.Column("volume_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["view_id"],
            ["view.id"],
        ),
        sa.ForeignKeyConstraint(
            ["volume_id"],
            ["volume.id"],
        ),
        sa.PrimaryKeyConstraint("view_id", "volume_id"),
    )
    op.create_table(
        "labelclass",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("value", sa.Integer(), nullable=True),
        sa.Column(
            "annotation_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("crop_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["crop_id"],
            ["crop.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_labelclass_name"), "labelclass", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_labelclass_name"), table_name="labelclass")
    op.drop_table("labelclass")
    op.drop_table("view_to_volume")
    op.drop_index(op.f("ix_mesh_volume_id"), table_name="mesh")
    op.drop_index(op.f("ix_mesh_name"), table_name="mesh")
    op.drop_table("mesh")
    op.drop_index(op.f("ix_crop_name"), table_name="crop")
    op.drop_index(op.f("ix_crop_description"), table_name="crop")
    op.drop_index(op.f("ix_crop_completion_stage"), table_name="crop")
    op.drop_table("crop")
    op.drop_index(op.f("ix_volume_name"), table_name="volume")
    op.drop_index(op.f("ix_volume_id"), table_name="volume")
    op.drop_index(op.f("ix_volume_dataset_name"), table_name="volume")
    op.drop_table("volume")
    op.drop_index(op.f("ix_view_name"), table_name="view")
    op.drop_index(op.f("ix_view_dataset_name"), table_name="view")
    op.drop_table("view")
    op.drop_index(
        op.f("ix_publication_to_dataset_publication_id"),
        table_name="publication_to_dataset",
    )
    op.drop_index(
        op.f("ix_publication_to_dataset_dataset_id"),
        table_name="publication_to_dataset",
    )
    op.drop_table("publication_to_dataset")
    op.drop_index(op.f("ix_dataset_sample_id"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_name"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_acquisition_id"), table_name="dataset")
    op.drop_table("dataset")
    op.drop_table("sample")
    op.drop_table("publication")
    op.drop_table("fibsem_acquisition")
    op.drop_index(op.f("ix_content_type_id"), table_name="content_type")
    op.drop_table("content_type")
    # ### end Alembic commands ###
