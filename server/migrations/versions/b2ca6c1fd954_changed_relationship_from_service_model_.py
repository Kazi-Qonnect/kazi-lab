"""Changed relationship from service model to provider service

Revision ID: b2ca6c1fd954
Revises: cfd0b7c4b176
Create Date: 2024-06-19 16:30:27.322078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2ca6c1fd954'
down_revision = 'cfd0b7c4b176'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('provider_services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('county_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'counties', ['county_id'], ['id'])

    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.drop_constraint('services_county_id_fkey', type_='foreignkey')
        batch_op.drop_column('county_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.add_column(sa.Column('county_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('services_county_id_fkey', 'counties', ['county_id'], ['id'])

    with op.batch_alter_table('provider_services', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('county_id')

    # ### end Alembic commands ###
