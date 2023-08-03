from django import  template

register = template.Library()


@register.filter
def if_id_in_set(id, set):
    return any(id == i.dest.id for i in set)