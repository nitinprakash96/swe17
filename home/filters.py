from django import template

register = template.Library()

@register.filter(name='privatef')
def privatef(obj):
	# print obj
	return obj["_id"]