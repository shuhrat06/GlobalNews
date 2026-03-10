from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db.models import Count, Q

def format_articles(articles):
    for article in articles:
        article.read_time_minute = int(article.read_time.total_seconds() // 60)
        views = article.views
        if views >= 1000000000:
            article.f_views = f"{views/1000000000:.2f}B"
        elif views >= 1000000:
            article.f_views = f"{views/1000000:.2f}M"
        elif views >= 1000:
            article.f_views = f"{views/1000:.2f}k"
        comments = article.comment_set.count()
        article.comments_count = comments
        if comments >= 1000000000:
            article.comments_count = f"{comments/1000000000:.2f}B"
        elif comments >= 1000000:
            article.comments_count = f"{comments/1000000:.2f}M"
        elif comments >= 1000:
            article.comments_count = f"{comments/1000:.2f}k"

class HomePageView(View):
    def get(self, request):
        all_articles = Article.objects.filter(published=True)
        articles = all_articles.order_by('-important','-views')[:9]
        format_articles(articles)

        main_articles = articles[:3]
        other_articles = articles[3:]
        
        categories = Category.objects.annotate(
            count = Count('article')
        ).order_by('-count')[:6]

        lattest_articles =all_articles.order_by('-created_at')
        category = request.GET.get('category',categories[0].name)
        filtered_articles = lattest_articles.filter(category__name=category)[:6]
        format_articles(filtered_articles)
        
        most_viewed_articles = all_articles.order_by('-views')[:6]

        trending_tags = Tag.objects.annotate(
            count = Count('article')
        ).order_by('-count')[:12]

        context={
            'articles': main_articles,
            'other_articles': other_articles,
            'lattest_articles': lattest_articles[:10],
            'article_categories': categories,
            'filtered_articles': filtered_articles,
            'most_viewed_articles': most_viewed_articles,
            'trending_tags': trending_tags
        }
        return render(request,'index.html',context)

class NewsLetterPostEmailView(View):
    def post(self, request):
        email = request.POST.get('email')
        Newsletter.objects.create(email=email)
        return redirect('home-page')
    
class ArticleContentView(View):
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)

        session_key = f"viewed_article_{article.id}"

        if not request.session.get(session_key):
            article.views += 1
            article.save(update_fields=['views'])
            request.session[session_key] = True
        
        article.read_time_minute = int(article.read_time.total_seconds() // 60)
        views = article.views
        if views >= 1000000000:
            article.f_views = f"{views/1000000000:.2f}B"
        elif views >= 1000000:
            article.f_views = f"{views/1000000:.2f}M"
        elif views >= 1000:
            article.f_views = f"{views/1000:.2f}k"
        comments = article.comment_set.count()
        article.comments_count = comments
        if comments >= 1000000000:
            article.comments_count = f"{comments/1000000000:.2f}B"
        elif comments >= 1000000:
            article.comments_count = f"{comments/1000000:.2f}M"
        elif comments >= 1000:
            article.comments_count = f"{comments/1000:.2f}k"

        tags = article.tags.all()
        related_articles = Article.objects.filter(
            tags__in=tags
        ).exclude(id=article.id).distinct()
        format_articles(related_articles)

        contents = Content.objects.filter(article=article)
        context = {
            'article': article, 
            'contents': contents,
            'related_articles': related_articles
        }
        return render(request, 'detail-page.html',context)

class PostCommentView(View):
    def post(self, request, slug):
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        Comment.objects.create(
            name = name,
            email = email,
            text = text,
            article = Article.objects.get(slug=slug)
        )
        return redirect('article-content', slug=slug)

class ArticleByCategoriesView(View):
    def get(self, request, slug):
        search = request.GET.get('search')
        category = Category.objects.get(slug=slug)
        articles = Article.objects.filter(published = True)
        articles = articles.filter(category=category)
        if search:
            articles=articles.filter(
                Q(title__icontains=search) | Q(intro__icontains=search)
            )
        format_articles(articles)
        context = {
            'f_category': category,
            'f_articles': articles,
            'search': search
        }
        return render(request,'filtered_articles.html',context)
    
class SearchArticleView(View):
    def get(self, request):
        search = request.GET.get('search', None)
        context = {
            'search_articles': None,
            'search': search
            }
        if search:
            articles = Article.objects.filter(published = True)
            articles=articles.filter(
                Q(title__icontains=search) | Q(intro__icontains=search)
            )
            format_articles(articles)
            context['search_articles'] = articles

        return render(request, "search_articles.html",context)
    
class AboutUsView(View):
    def get(self, request):
        context = {'about': True}
        return render(request,'about.html', context)