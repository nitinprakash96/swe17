from django import template

register = template.Library()

@register.filter(name='privatef')
def privatef(obj):
	return obj["_id"]