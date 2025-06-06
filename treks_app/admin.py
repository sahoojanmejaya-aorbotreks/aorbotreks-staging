from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Contact, Blog, TrekCategory, TrekOrganizer, Trek, TrekImage,
    Testimonial, FAQ, SafetyTip, TeamMember, HomepageBanner,
    SocialMedia, ContactInfo,WhatsNew, TopTrek)

admin.site.register(WhatsNew)
admin.site.register(TopTrek)

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'user_type', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('name', 'email', 'mobile', 'comment')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_featured', 'image_preview')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'is_featured')
        }),
        ('Content', {
            'fields': ('content', 'excerpt')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(TrekCategory)
class TrekCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class TrekImageInline(admin.TabularInline):
    model = Trek.additional_images.through
    extra = 1

@admin.register(TrekOrganizer)
class TrekOrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'is_verified', 'logo_preview')
    list_filter = ('is_verified',)
    search_fields = ('name', 'description', 'contact_email')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'

@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organizer', 'difficulty', 'price', 'is_featured', 'image_preview')
    list_filter = ('category', 'difficulty', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    inlines = [TrekImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'organizer', 'is_featured')
        }),
        ('Details', {
            'fields': ('description', 'short_description', 'duration', 'difficulty', 'location')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(TrekImage)
class TrekImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image_preview')
    search_fields = ('caption',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'trek_display', 'rating', 'date', 'is_featured', 'photo_preview')
    list_filter = ('rating', 'is_featured', 'date')
    search_fields = ('name', 'content', 'trek_name')
    readonly_fields = ('photo_preview',)
    
    def trek_display(self, obj):
        return obj.trek.title if obj.trek else obj.trek_name
    trek_display.short_description = 'Trek'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Photo'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_editable = ('order',)

@admin.register(SafetyTip)
class SafetyTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon_preview')
    search_fields = ('title', 'content')
    list_editable = ('order',)
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="30" />', obj.icon.url)
        return "-"
    icon_preview.short_description = 'Icon'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'photo_preview')
    search_fields = ('name', 'position', 'bio')
    list_editable = ('order',)
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Photo'

@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active', 'order')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'icon_preview')
    search_fields = ('platform',)
    list_editable = ('order',)
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="30" />', obj.icon.url)
        return "-"
    icon_preview.short_description = 'Icon'

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone')
    search_fields = ('company_name', 'address', 'email', 'phone')
