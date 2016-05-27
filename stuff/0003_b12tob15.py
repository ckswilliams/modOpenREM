# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remapp', '0002_openrem_upgrade_add_new_tables_and_populate_and_add_median_function'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinDoseMapCalcSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_skin_dose_maps', models.BooleanField(default=False, verbose_name=b'Enable skin dose maps?')),
                ('calc_on_import', models.BooleanField(default=True, verbose_name=b'Calculate skin dose map on import?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='projectionxrayradiationdose',
            name='acquisition_device_type',
        ),
        migrations.AddField(
            model_name='dicomstorescp',
            name='controlled',
            field=models.BooleanField(default=False, verbose_name=b'Is this server controlled by OpenREM'),
        ),
        migrations.AddField(
            model_name='irradeventxraydata',
            name='reference_point_definition_text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectionxrayradiationdose',
            name='acquisition_device_type_cid',
            field=models.ForeignKey(related_name='tid10001_type', blank=True, to='remapp.ContextID', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotDXRequestFreq',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotDXRequestMeanDAP',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotDXStudyFreq',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotDXStudyMeanDAP',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotHistogramBins',
            field=models.PositiveSmallIntegerField(default=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotHistograms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotMGAGDvsThickness',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotMGStudyPerDayAndHour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotRFInitialSortingChoice',
            field=models.CharField(default=b'freq', max_length=4, choices=[(b'dap', b'DAP'), (b'freq', b'Frequency'), (b'name', b'Name')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotRFStudyDAP',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotRFStudyFreq',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotRFStudyPerDayAndHour',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plotSeriesPerSystem',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dicomstorescp',
            name='aetitle',
            field=models.CharField(max_length=16, null=True, verbose_name=b'AE Title of this node - 16 or fewer letters and numbers, no spaces', blank=True),
        ),
        migrations.AlterField(
            model_name='dicomstorescp',
            name='keep_alive',
            field=models.BooleanField(default=False, verbose_name=b'Should this server be kept auto-started and kept alive (using celery beat)'),
        ),
        migrations.AlterField(
            model_name='dicomstorescp',
            name='name',
            field=models.CharField(unique=True, max_length=64, verbose_name=b'Name of local store node - fewer than 64 characters, spaces allowed'),
        ),
        migrations.AlterField(
            model_name='dicomstorescp',
            name='port',
            field=models.IntegerField(null=True, verbose_name=b'Port: 104 is standard for DICOM but over 1024 requires fewer admin rights', blank=True),
        ),
    ]
