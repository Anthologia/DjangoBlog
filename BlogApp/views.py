from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from django.utils import timezone
from .forms import BlogForm

# Create your views here.
def home(request):
    blogs = Blog.objects.all()

    for blog in blogs:
        like_num = len(blog.like.all())
        if blog.like.filter(username = request.user):
            liker = request.user
        else:
            liker = blog.like.last()
    
    return render(request, 'home.html', {'blogs':blogs,'likes':like_num, 'liker':liker})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id)
    like_num = len(blog.like.all())
    if blog.like.filter(username = request.user):
        liker = request.user
    else:
        liker = blog.like.last()
    comments = Comment.objects.filter(blog=blog)
    return render(request, 'detail.html', {'blog':blog, 'comments':comments, 'likes':like_num, 'liker':liker})

def commenting(request, blog_id):
    new_comment = Comment()
    new_comment.blog = get_object_or_404(Blog, pk = blog_id)
    new_comment.author = request.user
    new_comment.body = request.POST.get('body')
    new_comment.save()
    return redirect('/blog/' + str(blog_id))

def deletingcomment(request, comment_id):
    delete_comment = get_object_or_404(Comment, pk = comment_id)
    delete_comment.delete()
    return redirect('/blog/' + str(delete_comment.blog.id))
    

def like(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id)
    blog.like.add(request.user)
    blog.save()
    # save 하나 안하나 똑같은 거 같은데 왜 하지?
    return redirect('/blog/' + str(blog_id))

def unlike(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id)
    blog.like.remove(request.user)
    blog.save()
    return redirect('/blog/' + str(blog_id))

def new(request):
    # 1. 데이터가 입력된 후 제출 버튼을 누르고 데이터 저장 = POST
    # 2. 정보가 입력되지 않은 빈칸으로 되어있는 페이지 보여주기 = GET
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.pub_date = timezone.now()
            content.save()
            return redirect("home")
    
    else: # GET 방식
        form = BlogForm()
        return render(request, 'new.html', {'form':form})

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.body = request.POST['body']
    new_blog.pub_date = timezone.datetime.now()
    new_blog.save()
    
    return redirect('/blog/'+str(new_blog.id))

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'edit.html', {'blog':edit_blog})

def update(request, blog_id):
    update_blog = get_object_or_404(Blog, pk = blog_id)
    update_blog.title = request.POST['title']
    update_blog.body = request.POST['body']
    update_blog.pub_date = timezone.datetime.now()
    update_blog.save()
    
    return redirect('detail', update_blog.id)

def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk = blog_id)
    delete_blog.delete()

    return redirect('home')