"""empty message

Revision ID: e876d80c1564
Revises: 5b6dab42ccf3
Create Date: 2021-01-27 19:08:12.873530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e876d80c1564'
down_revision = '5b6dab42ccf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Pedal_manufacturer_id_fkey', 'Pedal', type_='foreignkey')
    op.create_foreign_key(None, 'Pedal', 'Manufacturer', ['manufacturer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Pedal', type_='foreignkey')
    op.create_foreign_key('Pedal_manufacturer_id_fkey', 'Pedal', 'Pedal', ['manufacturer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
