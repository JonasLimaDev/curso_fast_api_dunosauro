from sqlalchemy import Select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="jonas",
        email="jonas@email.com",
        password="senha_forte@123",
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        Select(User).where(User.email == "jonas@email.com")
    )

    assert result.username == "jonas"
