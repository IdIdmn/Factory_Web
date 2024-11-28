from django import template 

register = template.Library() 

@register.filter(name='dict') 
def dict(list, key): 
    return list.get(key)


@register.filter(name="get_field")
def get_field(form, field_name):
    return form[field_name] if field_name in form.fields else None