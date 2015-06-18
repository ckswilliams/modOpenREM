# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from openremproject import settings as project_settings
from datetime import datetime


def populate_study_workload_chart_time(self, orm):

    for studyData in orm.GeneralStudyModuleAttr.objects.all():
        studyDate = datetime.date(datetime(1900,1,1,0,0,0,0))
        studyTime = studyData.study_time
        if studyTime:
            studyDatetime = datetime.combine(studyDate, studyTime)
        else:
            studyDatetime = None
        studyData.study_workload_chart_time = studyDatetime
        studyData.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remapp', '0001_initial'),
    ]

    if 'postgresql' in project_settings.DATABASES['default']['ENGINE']:
        operations = [
            migrations.RunPython(populate_study_workload_chart_time),
            migrations.RunSQL([
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
                ");",
                "DROP AGGREGATE median(anyelement);"
                "DROP FUNCTION _final_median(anyarray);"]
            ),
        ]
    else:
        operations = [
            migrations.RunPython(populate_study_workload_chart_time),
        ]
