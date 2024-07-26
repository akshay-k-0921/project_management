import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone


#to generate base datas such as auto id and creator
def base_data(self, request,):
    if self._state.adding:
        self.auto_id = (self.__class__.objects.aggregate(max_auto_id=Max('auto_id')).get('max_auto_id') or 0) + 1
        if request.user.is_authenticated:
            self.creator = request.user
    else:
        if request.user.is_authenticated:
            self.updater = request.user
        self.date_updated = timezone.now()


# Managers to get deleted instances and active instances
class ActiveManager(models.Manager):
   def get_queryset(self):
       return super(ActiveManager, self).get_queryset().exclude(is_deleted=True)


class DeletedManager(models.Manager):
   def get_queryset(self):
       return super(DeletedManager, self).get_queryset().filter(is_deleted=True)
   

#Base Model
class BaseModel(models.Model):


   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   auto_id = models.PositiveIntegerField(db_index=True, unique=True,editable=False)
   creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,editable=False,related_name="creator_%(app_label)s_%(class)s_objects", limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
   updater = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,editable=False, related_name="updater_%(app_label)s_%(class)s_objects", limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
   date_added = models.DateTimeField(db_index=True, auto_now_add=True)
   date_updated = models.DateTimeField(null=True, blank=True,editable=False)
   is_deleted = models.BooleanField(default=False)


   # Model managers
   objects = models.Manager()
   active_objects = ActiveManager()
   deleted_objects = DeletedManager()


   class Meta:
       abstract = True