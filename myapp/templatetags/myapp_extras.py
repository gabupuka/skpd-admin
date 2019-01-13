from django.template.defaulttags import register

@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def if_none(item, new_value):
    if item is None:
        return new_value
    else:
        return item
