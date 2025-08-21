from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.shortcuts import render
from django.utils import timezone
from django.utils.text import Truncator



@api_view(['POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def contact_submit(request):
    try:
        # Get data from POST request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            mobile = data.get('mobile')
            user_type = data.get('userType')
            comment = data.get('comment')
        else:
            # Handle form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            user_type = request.POST.get('userType')
            comment = request.POST.get('comment')
        
        # Validate required fields
        if not all([name, email, mobile, comment]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
            
        # Create a new Contact object
        contact = Contact(
            name=name,
            email=email,
            mobile=mobile,
            user_type=user_type,
            comment=comment
        )
        contact.save()
        
        return JsonResponse({'message': 'Contact form submitted successfully'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from .models import (
    Contact, Blog, TrekCategory, TrekOrganizer, Trek, 
    Testimonial, FAQ, SafetyTip, TeamMember, HomepageBanner,
    SocialMedia, ContactInfo,WhatsNew, TopTrek
)


# Create your views here.
def home(request):
    featured_treks = Trek.objects.filter(is_featured=True)[:6]
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    featured_blogs = Blog.objects.filter(is_featured=True)[:3]
    banners = HomepageBanner.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.all().order_by('category', 'order')
    whats_new = WhatsNew.objects.all().order_by('-created_at')[:5]
    top_treks = TopTrek.objects.all()[:]

    
    faq_categories = {}
    for faq in faqs:
        if faq.category not in faq_categories:
            faq_categories[faq.category] = []
        faq_categories[faq.category].append(faq)
    
    context = {
        'featured_treks': featured_treks,
        'featured_testimonials': featured_testimonials,
        'featured_blogs': featured_blogs,
        'banners': banners,
        'faq_categories': faq_categories,
        'whats_new': whats_new,
        'top_treks': top_treks,
    }
    return render(request, 'index.html', context)

# def home(request):
#     whats_new = WhatsNew.objects.all().order_by('-created_at')[:5]
#     top_treks = TopTrek.objects.all()[:]

#     context = {
#         'whats_new': whats_new,
#         'top_treks': top_treks,
#     }
#     return render(request, 'test.html', context)


def about(request):
    team_members = TeamMember.objects.all().order_by('order')
    context = {
        'team_members': team_members,
    }
    return render(request, 'about.html', context)

# def blogs(request):
#     all_blogs = Blog.objects.all().order_by('-created_at')
#     paginator = Paginator(all_blogs, 9)  # Show 9 blogs per page
    
#     page_number = request.GET.get('page')
#     blogs = paginator.get_page(page_number)
    
#     context = {
#         'blogs': blogs,
#     }
#     return render(request, 'blogs.html', context)

# def blog_detail(request, slug):
#     blog = get_object_or_404(Blog, slug=slug)
#     recent_blogs = Blog.objects.exclude(id=blog.id).order_by('-created_at')[:3]
    
#     context = {
#         'blog': blog,
#         'recent_blogs': recent_blogs,
#     }
#     return render(request, 'blog_detail.html', context)

# def blogs(request):
#     all_blogs = Blog.objects.all().order_by('-created_at')  # use created_at
#     paginator = Paginator(all_blogs, 9)
#     page_number = request.GET.get('page')
#     blogs_page = paginator.get_page(page_number)

#     context = {
#         'blogs': blogs_page,
#     }
#     return render(request, 'blogs.html', context)



# def blog_detail(request, slug):
#     blog = get_object_or_404(Blog, slug=slug)

#     # SEO context (fallback if fields empty)
#     seo = {
#         "title": blog.meta_title if blog.meta_title else blog.title,
#         "description": blog.meta_description if blog.meta_description else blog.excerpt[:150],
#         "keywords": blog.meta_keywords,
#         "image": blog.image_url if blog.image_url else "/static/images/default-blog.jpg",
#         "url": request.build_absolute_uri(blog.get_absolute_url()),
#         "author": blog.author,
#         "published": blog.created_at,
#         "updated": blog.updated_at,
#     }

#     return render(request, "blog_detail.html", {"blog": blog, "seo": seo})

# def blogs(request):
#     all_blogs = Blog.objects.all().order_by('-created_at')
#     paginator = Paginator(all_blogs, 9)
#     page_number = request.GET.get('page')
#     blogs_page = paginator.get_page(page_number)

#     seo = {
#         "title": "Blogs | Aorbo Treks",
#         "description": "Read travel blogs, trekking guides, and adventure stories by Aorbo Treks.",
#         "keywords": "trekking, blogs, adventure, travel, hiking",
#         "image": request.build_absolute_uri("/static/images/default-blog.jpg"),
#         "url": request.build_absolute_uri(),
#         "author": "Aorbo Treks",
#         "published": blogs_page[0].created_at if blogs_page else None,
#         "updated": blogs_page[0].updated_at if blogs_page else None,
#     }

#     return render(request, "blogs.html", {"blogs": blogs_page, "seo": seo})

# def blog_detail(request, slug):
#     blog = get_object_or_404(Blog, slug=slug)

#     seo = {
#         "title": blog.meta_title or blog.title,
#         "description": blog.meta_description or (blog.excerpt[:150] if blog.excerpt else blog.content[:150]),
#         "keywords": blog.meta_keywords or f"trekking, travel, adventure, {blog.title}",
#         "image": blog.image_url if blog.image_url else request.build_absolute_uri("/static/images/default-blog.jpg"),
#         "url": request.build_absolute_uri(blog.get_absolute_url()),
#         "author": getattr(blog, "author", "Aorbo Treks"),  # fallback if no author field
#         "published": blog.created_at,
#         "updated": getattr(blog, "updated_at", blog.created_at),
#     }

#     return render(request, "blog_detail.html", {"blog": blog, "seo": seo})
    

# def blogs(request):
#     all_blogs = Blog.objects.all().order_by('-created_at')
#     paginator = Paginator(all_blogs, 9)
#     page_number = request.GET.get('page')
#     blogs_page = paginator.get_page(page_number)

#     seo = {
#         "title": "Blogs | Aorbo Treks",
#         "description": "Read travel blogs, trekking guides, and adventure stories by Aorbo Treks.",
#         "keywords": "trekking, blogs, adventure, travel, hiking",
#         "image": request.build_absolute_uri("/static/images/default-blog.jpg"),  # ✅ absolute
#         "url": request.build_absolute_uri(),  # ✅ absolute full URL (with domain)
#         "author": "Aorbo Treks",
#         "published": blogs_page[0].created_at if blogs_page else None,
#         "updated": blogs_page[0].updated_at if blogs_page else None,
#     }

#     return render(request, "blogs.html", {"blogs": blogs_page, "seo": seo})

# def blog_detail(request, slug):
#     blog = get_object_or_404(Blog, slug=slug)

#     seo = {
#         "title": blog.meta_title or blog.title,
#         "description": blog.meta_description or (blog.excerpt[:150] if blog.excerpt else blog.content[:150]),
#         "keywords": blog.meta_keywords or f"trekking, travel, adventure, {blog.title}",
#         "image": request.build_absolute_uri(blog.image.url) if blog.image else request.build_absolute_uri("/static/images/default-blog.jpg"),  # ✅ absolute
#         "url": request.build_absolute_uri(blog.get_absolute_url()),  # ✅ absolute
#         "author": getattr(blog, "author", "Aorbo Treks"),
#         "published": blog.created_at,
#         "updated": getattr(blog, "updated_at", blog.created_at),
#     }

#     return render(request, "blog_detail.html", {"blog": blog, "seo": seo})


def blogs(request):
    all_blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(all_blogs, 9)
    page_number = request.GET.get('page')
    blogs_page = paginator.get_page(page_number)

    # Safely pick first blog for published/updated dates (if exists)
    first_blog = blogs_page.object_list[0] if blogs_page.object_list else None

    seo = {
        "title": "Blogs | Aorbo Treks",
        "description": "Read travel blogs, trekking guides, and adventure stories by Aorbo Treks.",
        "keywords": "trekking, blogs, adventure, travel, hiking",
        "image": request.build_absolute_uri("/static/images/default-blog.jpg"),  # ✅ absolute
        "url": request.build_absolute_uri(),  # ✅ absolute full URL (with domain)
        "author": "Aorbo Treks",
        "published": first_blog.created_at if first_blog else None,
        "updated": getattr(first_blog, "updated_at", None) if first_blog else None,
    }

    return render(request, "blogs.html", {"blogs": blogs_page, "seo": seo})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    seo = {
        "title": blog.meta_title or blog.title,
        "description": blog.meta_description or Truncator(blog.excerpt or blog.content).chars(150),
        "keywords": blog.meta_keywords or f"trekking, travel, adventure, {blog.title}",
        "image": request.build_absolute_uri(blog.image.url) if blog.image else request.build_absolute_uri("/static/images/default-blog.jpg"),  # ✅ absolute
        "url": request.build_absolute_uri(blog.get_absolute_url()),  # ✅ absolute
        "author": getattr(getattr(blog, "author", None), "name", "Aorbo Treks"),  # ✅ handles relation or fallback
        "published": blog.created_at,
        "updated": getattr(blog, "updated_at", blog.created_at),
    }

    return render(request, "blog_detail.html", {"blog": blog, "seo": seo})


def treks(request):
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    all_treks = Trek.objects.all()
    
    # Apply filters if provided
    if category_id:
        all_treks = all_treks.filter(category_id=category_id)
    if difficulty:
        all_treks = all_treks.filter(difficulty=difficulty)
    
    # Get all categories for filter dropdown
    categories = TrekCategory.objects.all()
    
    paginator = Paginator(all_treks, 12)  # Show 12 treks per page
    page_number = request.GET.get('page')
    treks = paginator.get_page(page_number)
    
    context = {
        'treks': treks,
        'categories': categories,
        'selected_category': category_id,
        'selected_difficulty': difficulty,
        'difficulty_choices': Trek.DIFFICULTY_CHOICES,
    }
    return render(request, 'treks.html', context)

def trek_detail(request, slug):
    trek = get_object_or_404(Trek, slug=slug)
    testimonials = trek.testimonials.all()
    similar_treks = Trek.objects.filter(category=trek.category).exclude(id=trek.id)[:3]
    
    context = {
        'trek': trek,
        'testimonials': testimonials,
        'similar_treks': similar_treks,
    }
    return render(request, 'trek_detail.html', context)

def safety(request):
    safety_tips = SafetyTip.objects.all().order_by('order')
    context = {
        'safety_tips': safety_tips,
    }
    return render(request, 'safety.html', context)

def contact(request):
    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        contact_info = None
        
    social_media = SocialMedia.objects.all().order_by('order')
    
    context = {
        'contact_info': contact_info,
        'social_media': social_media,
    }
    return render(request, 'contact.html', context)

def privacy_policy(request):
    return render(request, 'privacypolicy.html')
def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')
def user_agreement(request):
    return render(request, 'user_agreement.html')

def index(request):
    whats_new = WhatsNew.objects.all().order_by('-date_posted')[:3]
    top_treks = TopTrek.objects.all()[:4]
    return render(request, 'index.html', {
        'whats_new': whats_new,
        'top_treks': top_treks,
    })

