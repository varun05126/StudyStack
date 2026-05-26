import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="markdownify")
def markdownify(text):
    if not text:
        return ""
    return mark_safe(markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "nl2br"]
    ))
