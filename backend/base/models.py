from django.db import models
from django.utils import timezone


class BaseModelQuerySet(models.QuerySet):
    """
    Custom QuerySet for BaseModel that provides additional methods.
    """

    def active(self):
        """
        Returns only the objects that are not soft deleted (removed).
        """
        return self.filter(removed_at__isnull=True)

    def deleted(self):
        """
        Returns only the objects that have been soft deleted (removed).
        """
        return self.filter(removed_at__isnull=False)

    def soft_delete(self):
        """
        Marks the object as removed by setting the removed_at field to the current time.
        """
        self.update(removed_at=timezone.now())
    
    def hard_delete(self):
        """
        Permanently deletes the objects from the database.
        """
        return self.delete()
    
    def restore(self):
        """
        Restores soft deleted objects by setting removed_at to None.
        """
        return self.update(removed_at=None)


class BaseModel(models.Model):
    """
    Base model that provides common fields for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    
    objects = BaseModelQuerySet.as_manager()
    all_objects = models.Manager()  # For accessing all objects,
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        """
        Marks the object as removed by setting the removed_at field to the current time.
        """
        if self.removed_at is None:
            self.removed_at = timezone.now()
            self.save(update_fields=['removed_at'])
            return True
        return False
        
    def hard_delete(self):
        """
        Permanently deletes the object from the database.
        """
        self.delete()
        
    def restore(self):
        """
        Restores the object by setting removed_at to None.
        """
        if self.removed_at is not None:
            self.removed_at = None
            self.save(update_fields=['removed_at'])
            return True
        return False
    
    @property
    def is_deleted(self):
        """
        Returns True if the object is soft deleted, otherwise False.
        """
        return self.removed_at is not None
    