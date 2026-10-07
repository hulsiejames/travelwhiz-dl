{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}

.. currentmodule:: {{ fullname }}

{% for heading, objects in [("Functions", functions), ("Classes", classes), ("Exceptions", exceptions), ("Submodules", modules)] %}
{% if objects %}
.. rubric:: {{ heading }}

.. autosummary::
   :toctree:
   :recursive:

{% for member in objects %}
   {{ member }}
{% endfor %}

{% endif %}
{% endfor %}
{% if attributes %}
.. rubric:: Module data

{% for member in attributes %}
.. autodata:: {{ member }}

{% endfor %}
{% endif %}
