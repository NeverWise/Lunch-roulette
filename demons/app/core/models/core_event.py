# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CoreEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.ForeignKey('CorePlace', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_event'


class CoreEventColleagues(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(CoreEvent, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_event_colleagues'
        unique_together = (('event', 'user'),)
