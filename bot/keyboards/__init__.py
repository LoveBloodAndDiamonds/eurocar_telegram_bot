__all__ = ['get_main_keyboard', 'get_faq_keyboard', 'get_back_key', 'get_rent_class_keyboard',
           "get_rent_regions_keyboard"]

from .faq_keyboards import get_faq_keyboard, get_back_key
from .main_keyboard import get_main_keyboard
from .rent_keyboards import get_rent_class_keyboard, get_rent_regions_keyboard
