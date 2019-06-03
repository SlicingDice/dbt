{% macro default__create_table_as(temporary, relation, sql) -%}
  create table [{{ relation|replace("_", "-") }}] as (
    {{ sql }}
  );
{% endmacro %}