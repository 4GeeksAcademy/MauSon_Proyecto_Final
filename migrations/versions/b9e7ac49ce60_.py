"""empty message

Revision ID: b9e7ac49ce60
Revises: 
Create Date: 2025-01-17 18:47:01.835508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b9e7ac49ce60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('account_type', sa.String(length=50), nullable=True),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('transaction_limit', sa.Integer(), nullable=True),
    sa.Column('features', sa.String(length=255), nullable=True),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('price', sa.String(length=50), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombres', sa.String(length=255), nullable=False),
    sa.Column('primer_apellido', sa.String(length=255), nullable=False),
    sa.Column('segundo_apellido', sa.String(length=255), nullable=True),
    sa.Column('nacionalidad', sa.String(length=100), nullable=True),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('direccion', sa.String(length=255), nullable=True),
    sa.Column('localidad', sa.String(length=255), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('telefono_movil', sa.String(length=20), nullable=True),
    sa.Column('telefono_fijo', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('empresa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('razon_social', sa.String(length=255), nullable=True),
    sa.Column('cif', sa.String(length=50), nullable=True),
    sa.Column('tipo', sa.String(length=50), nullable=True),
    sa.Column('domicilio', sa.String(length=255), nullable=True),
    sa.Column('municipio', sa.String(length=255), nullable=True),
    sa.Column('provincia', sa.String(length=255), nullable=True),
    sa.Column('cod_postal', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('web', sa.String(length=255), nullable=True),
    sa.Column('url_anuncio', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('reserva_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permissions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('traveler01_id', sa.Integer(), nullable=True),
    sa.Column('traveler01_relac', sa.String(length=100), nullable=True),
    sa.Column('traveler02_id', sa.Integer(), nullable=True),
    sa.Column('traveler02_relac', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['traveler01_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['traveler02_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reserva',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_entrada', sa.Date(), nullable=True),
    sa.Column('fecha_salida', sa.Date(), nullable=True),
    sa.Column('alojamiento', sa.Integer(), nullable=True),
    sa.Column('nro_rooms', sa.Integer(), nullable=True),
    sa.Column('nro_viajeros', sa.String(length=50), nullable=True),
    sa.Column('metodo_pago', sa.String(length=50), nullable=True),
    sa.Column('traveler_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['alojamiento'], ['empresa.id'], ),
    sa.ForeignKeyConstraint(['traveler_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensible_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nif_tipo', sa.String(length=50), nullable=True),
    sa.Column('nif_nunero', sa.String(length=50), nullable=True),
    sa.Column('nif_country', sa.String(length=100), nullable=True),
    sa.Column('firmas', sa.String(length=255), nullable=True),
    sa.Column('medio_pago_tipo', sa.String(length=50), nullable=True),
    sa.Column('medio_pago_nro', sa.Integer(), nullable=True),
    sa.Column('medio_pago_expira', sa.Date(), nullable=True),
    sa.Column('fecha_pago', sa.Date(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensible_data')
    op.drop_table('reserva')
    op.drop_table('group')
    op.drop_table('user_permission')
    op.drop_table('empresa')
    op.drop_table('contact')
    op.drop_table('user')
    op.drop_table('plan')
    op.drop_table('account')
    # ### end Alembic commands ###
