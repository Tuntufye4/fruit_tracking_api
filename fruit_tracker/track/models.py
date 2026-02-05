from django.db import models


class Tracker(models.Model):
    # QR CODE VALUE
    batch_id = models.CharField(max_length=120)

    # PRODUCT DETAILS
    fruit_type = models.CharField(max_length=50)
    grade = models.CharField(max_length=50, null=True)
    package_type = models.CharField(max_length=50, null=True)
    variety = models.CharField(max_length=50, null=True)

    quantity_kg = models.FloatField()

    # SUPPLY CHAIN FLOW
    stage = models.CharField(max_length=50)
    previous_stage = models.CharField(max_length=50, null=True)

    location = models.CharField(max_length=100)
    handled_by = models.CharField(max_length=100)

    # GPS PROOF (ANTI-FRAUD)
    gps_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    gps_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    # BLOCKCHAIN SECURITY
    block_hash = models.CharField(max_length=64, null=True)       

    # ✅ STAGE VERIFICATION SYSTEM
    verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)            

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["batch_id"]),
        ]

    def __str__(self):
        return f"{self.batch_id} - {self.stage} - Verified: {self.verified}"
      