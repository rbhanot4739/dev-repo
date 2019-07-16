from django import template

register = template.Library()


@register.inclusion_tag("common/render_html_form.html")
def render_form(form, button_label):
    return {
        'form': form,
        'button_label': button_label
    }
