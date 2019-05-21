{% macro default__create_table_as(temporary, relation, sql) -%}
  create table {{ relation }} as (
    {{ sql }}
  );
{% endmacro %}