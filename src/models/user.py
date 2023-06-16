# import sqlalchemy as sa
# # import sqlalchemy.orm as orm
# from sqlalchemy.orm import Mapped, mapped_column
#
# from src.database import Base
#
#
# class User(Base):
#     """
#     User model
#     """
#
#     user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
#     """ Telegram user id """
#     user_name: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
#     """ Telegram user name """
#     first_name: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
#     """ Telegram profile first name """
#     second_name: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
#     """ Telegram profile second name """
#     # user_chat_fk: Mapped[int] = mapped_column(
#     #     sa.ForeignKey("chat.id"), unique=False, nullable=False
#     # )
#     # user_chat: Mapped[Chat] = orm.relationship("Chat", uselist=False, lazy="joined")
#     # """ Telegram chat with user """
