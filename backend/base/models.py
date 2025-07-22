from django.db import models

class BaseModelQuerySet(models.QuerySet):
    """
    Custom QuerySet for BaseModel that provides additional methods.
    """

    def active(self):
        """
        Returns only the objects that are not soft deleted (is_active=True).
        """
        return self.filter(is_active=True)

    def deleted(self):
        """
        Returns only the objects that have been soft deleted (is_active=False).
        """
        return self.filter(is_active=False)

    def soft_delete(self):
        """
        Marks the object as removed by setting the is_active field to False.
        """
        self.update(is_active=False)
    
    def hard_delete(self):
        """
        Permanently deletes the objects from the database.
        """
        return self.delete()
    
    def restore(self):
        """
        Restores soft deleted objects by setting is_active to True.
        """
        return self.update(is_active=True)


class BaseModel(models.Model):
    """
    Base model that provides common fields for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    objects = BaseModelQuerySet.as_manager()
    all_objects = models.Manager()  # For accessing all objects,
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        """
        Marks the object as removed by setting the is_active field to False.
        """
        self.is_active = False
        self.save(update_fields=['is_active'])
        return True
        
    def hard_delete(self):
        """
        Permanently deletes the object from the database.
        """
        self.delete()
        
    def restore(self):
        """
        Restores the object by setting is_active to True.
        """
        self.is_active = True
        self.save(update_fields=['is_active'])
        return True

    