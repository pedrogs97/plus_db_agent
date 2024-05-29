from tortoise import Tortoise, run_async

from src.config import TORTOISE_ORM


async def init():
    await Tortoise.init(config=TORTOISE_ORM)


async def close():
    await Tortoise.close_connections()


# Exemplo de função para criar um usuário
async def create_user(username: str, email: str):
    from src.models import UserModel

    user = await UserModel.create(username=username, email=email)
    return user


# Exemplo de função para obter todos os usuários
async def get_all_users():
    from src.models import UserModel

    users = await UserModel.all()
    return users


if __name__ == "__main__":
    run_async(init())
