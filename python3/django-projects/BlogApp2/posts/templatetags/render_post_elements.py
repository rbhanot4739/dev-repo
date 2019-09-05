from django import template

register = template.Library()


@register.inclusion_tag("posts/render_post.html")
def render_post_container(obj, page_type=''):
    return {
        'obj': obj,
        'page_type': page_type
    }
