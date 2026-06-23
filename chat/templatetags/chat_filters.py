import bleach
import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Tags and attributes we allow in rendered markdown
ALLOWED_TAGS = [
    "p","br","strong","em","ul","ol","li","code","pre","blockquote",
    "h1","h2","h3","h4","a","table","thead","tbody","tr","th","td","hr",
]
ALLOWED_ATTRS = {"a": ["href","title"], "code": ["class"]}


@register.filter(name="render_markdown", is_safe=True)
def render_markdown(value):
    """Convert markdown text to safe HTML for display in templates."""
    if not value:
        return ""
    html = md.markdown(
        value,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    )
    clean = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
    return mark_safe(clean)
