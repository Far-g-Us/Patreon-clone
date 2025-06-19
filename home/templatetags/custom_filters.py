import os

from django import template

register = template.Library()


@register.filter
def custom_filesizeformat(value):
    """
    Форматирует размер файла в удобочитаемый вид.
    Варианты: байты, КБ, МБ, ГБ
    """
    if value is None:
        return "0 байт"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "неизвестно"

    # Определяем единицы измерения
    units = ['байт', 'КБ', 'МБ', 'ГБ']
    unit_index = 0

    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024.0
        unit_index += 1

    # Форматируем вывод
    if unit_index == 0:
        return f"{int(value)} {units[unit_index]}"
    elif value < 10:
        return f"{value:.2f} {units[unit_index]}"
    elif value < 100:
        return f"{value:.1f} {units[unit_index]}"
    else:
        return f"{int(value)} {units[unit_index]}"

@register.filter
def filename(value):
    """Возвращает только имя файла из полного пути"""
    return os.path.basename(value)