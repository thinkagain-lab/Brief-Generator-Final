"""Add image_file, name, bio fields to User model

Revision ID: 587713c13b07
Revises: 
Create Date: 2024-08-16 15:52:03.560477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '587713c13b07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))

    # ### end Alembic commands ###


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     briefs = db.relationship('Brief', backref='author', lazy=True)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     name = db.Column(db.String(100), nullable=True)
#     bio = db.Column(db.Text, nullable=True)
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('name')
        batch_op.drop_column('image_file')

    # ### end Alembic commands ###
