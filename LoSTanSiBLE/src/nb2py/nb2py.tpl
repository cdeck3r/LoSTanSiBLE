{#

##
## Template designed for LoSTanSiBLE
##
## Features
## * no-effect jupyter magics:  %matplotlib, system
## * imports matplotlib at the beginning, SVG output
## * replaces papermill functionality by surrogate
##
## Author: cdeck3r
##

#}

{# handling papermill #}
{% set vars={} %}
{% set _ = vars.update({'pmfound':False}) %}

{% extends 'python.tpl'%}

##
## import matplotlib before all other imports
##
{%- block header -%}
{{ super() }}

{# jupyter magics #}

##
## injected python code ##
##

class get_ipython:
    # makes the jupyter magics without effect
    def run_line_magic(self, par1=None, par2=None, par3=None, par4=None, par5=None):
        pass

    # makes the jupyter magics without effect
    def system(self, par1=None):
        pass

# matplotlib import
# done before others

import matplotlib
matplotlib.use('SVG')

##
## /injected python code ##
##

{% endblock header %}

##
## 'papermill' surrogate class at the begin
## all other directives as usual
##
{% block any_cell %}


{% if 'papermill' in cell['metadata'].get('tags', []) %}

{% if not vars.pmfound %}
    {# first found papermill is assumed to be the import directive #}
    {# replaced by 'papermill' surrogate class #}

    {% set _ = vars.update({'pmfound':True}) %}

    ##
    ## injected python code ##
    ##

import pandas as pd

class pm:
    # internal dataframe storing the records
    pmDf = pd.DataFrame()

    @staticmethod
    def record(key, value):
        # access
        # pm.pmDf
        pass

    @staticmethod
    def save():
        pass
    ##
    ## /injected python code ##
    ##
{% else %} {# if pmfound #}
    {{ super() }}
    ## persist 'papermill' records
    ##
    ## injected python code ##
    ##

pm.save()

    ##
    ## /injected python code ##
    ##
{% endif %} {# if pmfound #}
{% else %} {# if papermill #}
    {{ super() }}
{% endif %} {# if papermill #}

{% endblock any_cell %}

##
## persist 'papermill' records
##
{%- block footer -%}

{% if vars.pmfound %}
    ##
    ## injected python code ##
    ##

pm.save()

    ##
    ## /injected python code ##
    ##
{% endif %}

{{ super() }}

{% endblock footer %}
