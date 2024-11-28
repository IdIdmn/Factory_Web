from django import template 

register = template.Library() 

@register.filter(name='dict') 
def dict(list, key): 
    return list.get(key)