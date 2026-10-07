{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

{% set force_include = objname in show_inherited|default([]) %}
{% set force_exclude = objname in exclude_inherited|default([]) %}
{% if attributes %}
   .. rubric:: Attributes

{% for member in attributes %}
{% if not force_exclude and (force_include or include_inherited_attributes|default(false) or member not in inherited_members) or force_exclude and member not in inherited_members %}
   .. autoattribute:: {{ name }}.{{ member }}

{% endif %}
{% endfor %}
{% endif %}
{% if methods %}
   .. rubric:: Methods

   .. autosummary::
      :toctree:

{% for member in methods %}
{% if not force_exclude and (force_include or include_inherited_methods|default(false) or member not in inherited_members) or force_exclude and member not in inherited_members %}
      ~{{ name }}.{{ member }}
{% endif %}
{% endfor %}
{% endif %}

.. minigallery:: {{ fullname }}
   :add-heading: Examples
