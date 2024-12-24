"""create members table

Revision ID: c52ee2b5146d
Revises: 075f1853f8dc
Create Date: 2024-12-24 12:43:35.201470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c52ee2b5146d'
down_revision = '075f1853f8dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('nome_guerra', sa.String(), nullable=False),
    sa.Column('patente', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('rg', sa.String(), nullable=False),
    sa.Column('dt_nasc', sa.Date(), nullable=False),
    sa.Column('lotacao', sa.String(), nullable=False),
    sa.Column('matricula', sa.String(), nullable=False),
    sa.Column('cfp_cfsd', sa.String(), nullable=False),
    sa.Column('telefone', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('genero', sa.String(), nullable=False),
    sa.Column('pm_bm', sa.String(), nullable=False),
    sa.Column('dependentes', sa.Integer(), nullable=False),
    sa.Column('situacao', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('matricula')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    # ### end Alembic commands ###