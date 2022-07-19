"""first migration on 06-MAY-2022

Revision ID: cb3eb6e3c25b
Revises: 
Create Date: 2022-05-06 17:50:28.292841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb3eb6e3c25b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nse_stock_info_1',
    sa.Column('symbol', sa.String(length=30), nullable=False),
    sa.Column('name_of_company', sa.String(length=1000), nullable=True),
    sa.Column('series', sa.String(length=2), nullable=True),
    sa.Column('date_of_listing', sa.Date(), nullable=True),
    sa.Column('paid_up_value', sa.Integer(), nullable=True),
    sa.Column('market_lot', sa.Integer(), nullable=True),
    sa.Column('isin_number', sa.String(length=12), nullable=True),
    sa.Column('face_value', sa.Integer(), nullable=True),
    sa.Column('industry', sa.String(length=100), nullable=True),
    sa.Column('nifty_500_ind', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('site_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('src_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_site_users_user_name'), 'site_users', ['user_name'], unique=True)
    op.create_table('stocks_nse_daily',
    sa.Column('symbol', sa.String(length=30), nullable=False),
    sa.Column('date_of_record', sa.Date(), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=True),
    sa.Column('high_price', sa.Float(), nullable=True),
    sa.Column('low_price', sa.Float(), nullable=True),
    sa.Column('close_price', sa.Float(), nullable=True),
    sa.Column('day_volume', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['nse_stock_info_1.symbol'], ),
    sa.PrimaryKeyConstraint('symbol', 'date_of_record')
    )
    op.create_index(op.f('ix_stocks_nse_daily_date_of_record'), 'stocks_nse_daily', ['date_of_record'], unique=False)
    op.create_index(op.f('ix_stocks_nse_daily_symbol'), 'stocks_nse_daily', ['symbol'], unique=False)
    op.create_table('user_portfolio',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=30), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('buy_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['nse_stock_info_1.symbol'], ),
    sa.ForeignKeyConstraint(['user_id'], ['site_users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'symbol')
    )
    op.create_index(op.f('ix_user_portfolio_symbol'), 'user_portfolio', ['symbol'], unique=False)
    op.create_index(op.f('ix_user_portfolio_user_id'), 'user_portfolio', ['user_id'], unique=False)
    op.create_table('user_wishlist',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['nse_stock_info_1.symbol'], ),
    sa.ForeignKeyConstraint(['user_id'], ['site_users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'symbol')
    )
    op.create_index(op.f('ix_user_wishlist_symbol'), 'user_wishlist', ['symbol'], unique=False)
    op.create_index(op.f('ix_user_wishlist_user_id'), 'user_wishlist', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_wishlist_user_id'), table_name='user_wishlist')
    op.drop_index(op.f('ix_user_wishlist_symbol'), table_name='user_wishlist')
    op.drop_table('user_wishlist')
    op.drop_index(op.f('ix_user_portfolio_user_id'), table_name='user_portfolio')
    op.drop_index(op.f('ix_user_portfolio_symbol'), table_name='user_portfolio')
    op.drop_table('user_portfolio')
    op.drop_index(op.f('ix_stocks_nse_daily_symbol'), table_name='stocks_nse_daily')
    op.drop_index(op.f('ix_stocks_nse_daily_date_of_record'), table_name='stocks_nse_daily')
    op.drop_table('stocks_nse_daily')
    op.drop_index(op.f('ix_site_users_user_name'), table_name='site_users')
    op.drop_table('site_users')
    op.drop_table('nse_stock_info_1')
    # ### end Alembic commands ###