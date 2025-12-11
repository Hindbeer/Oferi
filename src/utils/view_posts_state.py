from aiogram.fsm.state import State, StatesGroup


class ViewPostsState(StatesGroup):
    choose_view_type = State()
    viewing_pending_posts = State()
