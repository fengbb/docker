# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0011_auto_20151230_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerIp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip', models.GenericIPAddressField(verbose_name='container主机可以获取的IP')),
                ('used', models.IntegerField(verbose_name='是否已经使用', default=0)),
            ],
            options={
                'verbose_name': '容器IP',
                'verbose_name_plural': '容器IP管理',
            },
        ),
    ]
