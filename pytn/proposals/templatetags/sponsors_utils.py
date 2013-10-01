from django import template
register = template.Library()


@register.filter
def has_sponsors(levels):
    # import pdb; pdb.set_trace()
    return levels.exclude(sponsor=None)
