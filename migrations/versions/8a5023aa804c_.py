"""empty message

<<<<<<<< HEAD:migrations/versions/8a5023aa804c_.py
Revision ID: 8a5023aa804c
Revises: 
Create Date: 2025-01-22 18:05:29.091032
========
Revision ID: acb7b4b41766
Revises: 
Create Date: 2025-01-22 20:03:45.905030
>>>>>>>> 103c07718405e2cb0a735c7fbb7366900b739597:migrations/versions/acb7b4b41766_.py

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
<<<<<<<< HEAD:migrations/versions/8a5023aa804c_.py
revision = '8a5023aa804c'
========
revision = 'acb7b4b41766'
>>>>>>>> 103c07718405e2cb0a735c7fbb7366900b739597:migrations/versions/acb7b4b41766_.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('language', sa.String(length=50), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('primer_apellido', sa.String(length=255), nullable=False),
    sa.Column('segundo_apellido', sa.String(length=255), nullable=False),
    sa.Column('sexo', sa.String(length=50), nullable=False),
    sa.Column('nacionalidad', sa.String(length=100), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
    sa.Column('direccion', sa.String(length=255), nullable=False),
    sa.Column('localidad', sa.String(length=255), nullable=False),
    sa.Column('pais', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('telefono_movil', sa.String(length=20), nullable=False),
    sa.Column('telefono_fijo', sa.String(length=20), nullable=False),
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
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_name', sa.String(length=255), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
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
    op.create_table('contact_group',
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('contact_id', 'group_id')
    )
    op.create_table('reserva',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_entrada', sa.Date(), nullable=True),
    sa.Column('fecha_salida', sa.Date(), nullable=True),
    sa.Column('alojamiento', sa.Integer(), nullable=True),
    sa.Column('nro_rooms', sa.Integer(), nullable=True),
    sa.Column('nro_viajeros', sa.Integer(), nullable=True),
    sa.Column('titular_medio_pago', sa.String(length=255), nullable=True),
    sa.Column('medio_pago_tipo', sa.Enum('EFECTIVO', 'TARJETA', 'PLATAFORMA_DE_PAGO', 'TRANSFERENCIA', name='mediopagotipo'), nullable=False),
    sa.Column('medio_pago_nro', sa.Integer(), nullable=True),
    sa.Column('medio_pago_expira', sa.Date(), nullable=True),
    sa.Column('fecha_pago', sa.Date(), nullable=True),
    sa.Column('traveler_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['alojamiento'], ['empresa.id'], ),
    sa.ForeignKeyConstraint(['traveler_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensitive_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nif_tipo', sa.Enum('DNI', 'TIE', 'PASAPORTE', name='tiponif'), nullable=False),
    sa.Column('nif_numero', sa.String(length=50), nullable=False),
    sa.Column('nif_country', sa.String(length=100), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensitive_data')
    op.drop_table('reserva')
    op.drop_table('contact_group')
    op.drop_table('user_permission')
    op.drop_table('group')
    op.drop_table('empresa')
    op.drop_table('contact')
    op.drop_table('user')
    # ### end Alembic commands ###
