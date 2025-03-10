from aiogram import Router
from .user_handler import router as user_router
from .register_bron_handler import router as reg_router
from .buy_payments_order_handler import router as buy_router
from .close_order_handler import router as close_router

router = Router()

router.include_routers(
    user_router,
    reg_router,
    buy_router,
    close_router
)