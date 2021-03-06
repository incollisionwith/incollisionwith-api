"""more ref data; SmallInteger

Revision ID: 71a12c7783fe
Revises: 
Create Date: 2016-01-10 21:08:06.051443

"""

# revision identifiers, used by Alembic.
revision = '71a12c7783fe'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carriageway_hazards',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('first_point_of_impact',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hit_object_in_carriageway',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hit_object_off_carriageway',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('light_conditions',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pedestrian_crossing_human',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pedestrian_crossing_physical',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('road_class',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('pattern', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('road_surface',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('road_type',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skidding_and_overturning',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('special_conditions',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('urban_rural',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle_leaving_carriageway',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weather',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('accident_severity')
    op.add_column('accident', sa.Column('carriageway_hazards_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('light_conditions_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('pedestrian_crossing_human_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('pedestrian_crossing_physical_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_1', sa.String(), nullable=True))
    op.add_column('accident', sa.Column('road_1_class', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_1_number', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_2', sa.String(), nullable=True))
    op.add_column('accident', sa.Column('road_2_class', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_2_number', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_surface_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_type', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('road_type_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('special_conditions_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('speed_limit', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('urban_rural_id', sa.SmallInteger(), nullable=True))
    op.add_column('accident', sa.Column('weather_id', sa.SmallInteger(), nullable=True))
    op.drop_index('idx_accident_location', table_name='accident')
    op.create_foreign_key(None, 'accident', 'road_type', ['road_type_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'road_class', ['road_1_class'], ['id'])
    op.create_foreign_key(None, 'accident', 'special_conditions', ['special_conditions_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'pedestrian_crossing_physical', ['pedestrian_crossing_physical_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'road_surface', ['road_surface_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'weather', ['weather_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'carriageway_hazards', ['carriageway_hazards_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'road_type', ['road_type'], ['id'])
    op.create_foreign_key(None, 'accident', 'pedestrian_crossing_human', ['pedestrian_crossing_human_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'light_conditions', ['light_conditions_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'urban_rural', ['urban_rural_id'], ['id'])
    op.create_foreign_key(None, 'accident', 'road_class', ['road_2_class'], ['id'])
    op.add_column('vehicle', sa.Column('age_of_vehicle', sa.SmallInteger(), nullable=True))
    op.add_column('vehicle', sa.Column('engine_capacity', sa.Integer(), nullable=True))
    op.add_column('vehicle', sa.Column('first_point_of_impact_id', sa.SmallInteger(), nullable=True))
    op.add_column('vehicle', sa.Column('hit_object_in_carriageway_id', sa.SmallInteger(), nullable=True))
    op.add_column('vehicle', sa.Column('hit_object_off_carriageway_id', sa.SmallInteger(), nullable=True))
    op.add_column('vehicle', sa.Column('leaving_carriageway_id', sa.SmallInteger(), nullable=True))
    op.add_column('vehicle', sa.Column('make', sa.String(), nullable=True))
    op.add_column('vehicle', sa.Column('model', sa.String(), nullable=True))
    op.add_column('vehicle', sa.Column('skidding_and_overturning_id', sa.SmallInteger(), nullable=True))
    op.create_foreign_key(None, 'vehicle', 'hit_object_off_carriageway', ['hit_object_off_carriageway_id'], ['id'])
    op.create_foreign_key(None, 'vehicle', 'first_point_of_impact', ['first_point_of_impact_id'], ['id'])
    op.create_foreign_key(None, 'vehicle', 'skidding_and_overturning', ['skidding_and_overturning_id'], ['id'])
    op.create_foreign_key(None, 'vehicle', 'hit_object_in_carriageway', ['hit_object_in_carriageway_id'], ['id'])
    op.create_foreign_key(None, 'vehicle', 'vehicle_leaving_carriageway', ['leaving_carriageway_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_constraint(None, 'vehicle', type_='foreignkey')
    op.drop_column('vehicle', 'skidding_and_overturning_id')
    op.drop_column('vehicle', 'model')
    op.drop_column('vehicle', 'make')
    op.drop_column('vehicle', 'leaving_carriageway_id')
    op.drop_column('vehicle', 'hit_object_off_carriageway_id')
    op.drop_column('vehicle', 'hit_object_in_carriageway_id')
    op.drop_column('vehicle', 'first_point_of_impact_id')
    op.drop_column('vehicle', 'engine_capacity')
    op.drop_column('vehicle', 'age_of_vehicle')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.drop_constraint(None, 'accident', type_='foreignkey')
    op.create_index('idx_accident_location', 'accident', ['location'], unique=False)
    op.drop_column('accident', 'weather_id')
    op.drop_column('accident', 'urban_rural_id')
    op.drop_column('accident', 'speed_limit')
    op.drop_column('accident', 'special_conditions_id')
    op.drop_column('accident', 'road_type_id')
    op.drop_column('accident', 'road_type')
    op.drop_column('accident', 'road_surface_id')
    op.drop_column('accident', 'road_2_number')
    op.drop_column('accident', 'road_2_class')
    op.drop_column('accident', 'road_2')
    op.drop_column('accident', 'road_1_number')
    op.drop_column('accident', 'road_1_class')
    op.drop_column('accident', 'road_1')
    op.drop_column('accident', 'pedestrian_crossing_physical_id')
    op.drop_column('accident', 'pedestrian_crossing_human_id')
    op.drop_column('accident', 'light_conditions_id')
    op.drop_column('accident', 'carriageway_hazards_id')
    op.create_table('accident_severity',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('label', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('injury_definition', sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_table('weather')
    op.drop_table('vehicle_leaving_carriageway')
    op.drop_table('urban_rural')
    op.drop_table('special_conditions')
    op.drop_table('skidding_and_overturning')
    op.drop_table('road_type')
    op.drop_table('road_surface')
    op.drop_table('road_class')
    op.drop_table('pedestrian_crossing_physical')
    op.drop_table('pedestrian_crossing_human')
    op.drop_table('light_conditions')
    op.drop_table('hit_object_off_carriageway')
    op.drop_table('hit_object_in_carriageway')
    op.drop_table('first_point_of_impact')
    op.drop_table('carriageway_hazards')
    ### end Alembic commands ###
