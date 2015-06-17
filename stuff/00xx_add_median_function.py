# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remapp', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE FUNCTION _final_median(anyarray) RETURNS NUMERIC AS $$"
            "  WITH q AS"
            "  ("
            "     SELECT val"
            "     FROM UNNEST($1) val"
            "     WHERE val IS NOT NULL"
            "     ORDER BY 1"
            "  ),"
            "  cnt AS"
            "  ("
            "    SELECT COUNT(*) AS c FROM q"
            "  )"
            "  SELECT AVG(val * 10000000000.0)"
            "  FROM"
            "  ("
            "    SELECT val FROM q"
            "    LIMIT  2 - MOD((SELECT c FROM cnt), 2)"
            "    OFFSET GREATEST(CEIL((SELECT c FROM cnt) / 2.0) - 1, 0)"
            "  ) q2;"
            "$$ LANGUAGE SQL IMMUTABLE;"
            "CREATE AGGREGATE median(anyelement) ("
            "  SFUNC=array_append,"
            "  STYPE=anyarray,"
            "  FINALFUNC=_final_median,"
            "  INITCOND='{}'"
            ");"
        ),
    ]
