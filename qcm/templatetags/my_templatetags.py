from django import template
import re

register = template.Library()

@register.filter(name="index_liste")
def index_liste(reponses, indice):
	#reponses|index_liste:12
	print("L'indice est ",indice)
	try:
		return reponses[indice-1]
	except:
		return ''

@register.filter(name="strip_html_tag")
def strip_html_tag(value, args):
	try:
		return re.sub('<[^<]+?>', '', value)
	except:
		return value