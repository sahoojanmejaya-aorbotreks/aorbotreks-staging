from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=20)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.email}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description for blog listings")
    image = models.ImageField(upload_to='blogs/')
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

class TrekCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Trek Categories"
    
    def __str__(self):
        return self.name

class TrekOrganizer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='organizers/')
    website = models.URLField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Trek(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
        ('extreme', 'Extreme'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='treks/')
    additional_images = models.ManyToManyField('TrekImage', blank=True, related_name='trek_images')
    category = models.ForeignKey(TrekCategory, on_delete=models.CASCADE, related_name='treks')
    organizer = models.ForeignKey(TrekOrganizer, on_delete=models.CASCADE, related_name='treks')
    duration = models.CharField(max_length=50, help_text="e.g., '2 days, 1 night'")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('trek_detail', kwargs={'slug': self.slug})

class TrekImage(models.Model):
    image = models.ImageField(upload_to='trek_images/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.caption or f"Image {self.id}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    trek = models.ForeignKey(Trek, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    trek_name = models.CharField(max_length=200, blank=True, help_text="Only required if trek is not selected")
    date = models.DateField()
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.trek or self.trek_name}"

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('booking', 'Booking & Payment'),
        ('treks', 'Treks & Activities'),
        ('safety', 'Safety & Equipment'),
        ('Cancellation & Refund', 'Cancellation & Refund'),
        ('Payment-Related', 'Payment-Related'),
        ('Customer-support', 'Customer-Support'),
    ]
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question

class SafetyTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    icon = models.ImageField(upload_to='safety_icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class HomepageBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class SocialMedia(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.ImageField(upload_to='social_icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display")
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Social Media Links"
    
    def __str__(self):
        return self.platform

class ContactInfo(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    map_url = models.URLField(blank=True, help_text="Google Maps URL")
    
    class Meta:
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return self.company_name

# models.py
class WhatsNew(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='whatsnew/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TopTrek(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='toptreks/')

    def __str__(self):
        return self.name


