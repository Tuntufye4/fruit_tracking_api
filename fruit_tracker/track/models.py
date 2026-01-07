from django.db import models

class Tracker(models.Model):
    batch_id = models.CharField(max_length=100)    
    fruit_type = models.CharField(max_length=50)
    grade = models.CharField(max_length=50, null=True)
    package_type = models.CharField(max_length=50, null=True)
    variety = models.CharField(max_length=50, null=True)      
    quantity_kg = models.FloatField()
    stage = models.CharField(max_length=50)
    previous_stage = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50)
    handled_by = models.CharField(max_length=50)         
    block_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)  
    gps_latitude = models.DecimalField(max_length=50, max_digits=10, decimal_places=6, null=True)
    gps_longitude = models.DecimalField(max_length=50, max_digits=10, decimal_places=6, null=True)
    

    class Meta:
        ordering = ["created_at"]    
        indexes = [     
            models.Index(fields=["batch_id"]),
        ]

    def __str__(self):
        return f"{self.batch_id} - {self.stage}"