from django.template.defaulttags import register

@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def if_none_or_empty(item, new_value):
    if item is None or not item:
        return new_value
    else:
        return item

@register.filter
def in_group(user, group_name):
    return user.groups.all().filter(name=group_name).exists()
