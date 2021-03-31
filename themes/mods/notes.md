# Modifications to cinder theme




# To enable {{ variables }}

Addtional files:

- jinja.html
- custom
    - js
    - css

## content.html

{# JKB addition to parse jinja-style variables in generated html. https://github.com/mkdocs/mkdocs/issues/304 #}
{%- from "jinja.html" import jinja %}
{%- set jinja_allowed =  config.variables  %}
{{ jinja(page.content, jinja_allowed) }}


## base.html

{% if page.meta.banner %}
{% include config.extra.which_banner %}
{% endif %}

#### in {% block footer %}

{% if page.meta.contact_row %}
{% include config.extra.which_contact_row %}
{% endif %}

