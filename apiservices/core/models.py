from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Property(models.Model):
    """Model representing a property listing."""
    
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8,
        help_text="Property latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8,
        help_text="Property longitude coordinate"
    )
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Property price in USD"
    )
    bedrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Number of bedrooms"
    )
    bathrooms = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Number of bathrooms"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['price']),
            models.Index(fields=['bedrooms']),
            models.Index(fields=['bathrooms']),
        ]
    
    def __str__(self):
        return f"Property {self.id}: ${self.price} - {self.bedrooms}BR/{self.bathrooms}BA"


class PropertyRequirement(models.Model):
    """Model representing a property search requirement."""
    
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8,
        help_text="Search center latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8,
        help_text="Search center longitude coordinate"
    )
    
    min_budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Minimum budget in USD"
    )
    max_budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Maximum budget in USD"
    )
    
    min_bedrooms = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Minimum number of bedrooms"
    )
    max_bedrooms = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Maximum number of bedrooms"
    )
    
    min_bathrooms = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Minimum number of bathrooms"
    )
    max_bathrooms = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Maximum number of bathrooms"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.min_budget and self.max_budget and self.min_budget > self.max_budget:
            raise ValidationError("Minimum budget cannot be greater than maximum budget")
        
        if self.min_bedrooms and self.max_bedrooms and self.min_bedrooms > self.max_bedrooms:
            raise ValidationError("Minimum bedrooms cannot be greater than maximum bedrooms")
        
        if self.min_bathrooms and self.max_bathrooms and self.min_bathrooms > self.max_bathrooms:
            raise ValidationError("Minimum bathrooms cannot be greater than maximum bathrooms")
    
    def __str__(self):
        return f"Requirement {self.id}: ${self.min_budget}-${self.max_budget}"


class PropertyMatch(models.Model):
    """Model representing a property match result."""
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    requirement = models.ForeignKey(PropertyRequirement, on_delete=models.CASCADE)
    match_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    distance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    budget_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bedroom_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bathroom_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-match_percentage', '-created_at']
        unique_together = ['property', 'requirement']
        indexes = [
            models.Index(fields=['match_percentage']),
            models.Index(fields=['requirement', '-match_percentage']),
        ]
    
    def __str__(self):
        return f"Match {self.id}: {self.match_percentage}% - Property {self.property.id}"