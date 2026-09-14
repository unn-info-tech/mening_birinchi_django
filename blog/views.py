from django.http import HttpResponse
from django.shortcuts import render, redirect  # ← render import qiling
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Post  # ← Model ni import qiling
from .forms import PostForma
from django.contrib.auth import login
from .forms import RoyxatdanOtishForma
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Profil
from .forms import FoydalanuvchiYangilashForma, ProfilYangilashForma


def royxatdan_otish(request):
    if request.method == 'POST':
        forma = RoyxatdanOtishForma(request.POST)
        if forma.is_valid():
            user = forma.save()
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
    else:
        forma = RoyxatdanOtishForma()

    return render(request, 'blog/royxatdan_otish.html', {'forma': forma})



def kirish(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
        else:
            messages.error(request, '❌ Noto\'g\'ri foydalanuvchi nomi yoki parol!')

    return render(request, 'blog/kirish.html')





def chiqish(request):
    logout(request)
    messages.info(request, '👋 Xayr! Tez orada qaytib keling!')
    return redirect('bosh_sahifa')


@login_required
def profil(request, username):
    foydalanuvchi = get_object_or_404(User, username=username)
    postlar = Post.objects.filter(muallif=foydalanuvchi, nashr_etilgan=True).order_by('-yaratilgan_sana')

    context = {
        'profil_egasi': foydalanuvchi,
        'postlar': postlar,
        'postlar_soni': postlar.count()
    }
    return render(request, 'blog/profil.html', context)



@login_required
def profil_tahrirlash(request):
    if request.method == 'POST':
        f_forma = FoydalanuvchiYangilashForma(request.POST, instance=request.user)
        p_forma = ProfilYangilashForma(request.POST, request.FILES, instance=request.user.profil)

        if f_forma.is_valid() and p_forma.is_valid():
            f_forma.save()
            p_forma.save()
            messages.success(request, '✅ Profilingiz yangilandi!')
            return redirect('profil', username=request.user.username)
    else:
        f_forma = FoydalanuvchiYangilashForma(instance=request.user)
        p_forma = ProfilYangilashForma(instance=request.user.profil)

    context = {
        'f_forma': f_forma,
        'p_forma': p_forma
    }
    return render(request, 'blog/profil_tahrirlash.html', context)


from django.core.paginator import Paginator

def bosh_sahifa(request):
    postlar_list = Post.objects.select_related('muallif').filter(
        nashr_etilgan=True
    ).order_by('-yaratilgan_sana')

    # Har sahifada 5 ta post
    paginator = Paginator(postlar_list, 5)

    sahifa_raqami = request.GET.get('sahifa')
    postlar = paginator.get_page(sahifa_raqami)

    return render(request, 'blog/bosh.html', {'postlar': postlar})



def post_batafsil(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ko'rildi sonini oshiramiz
    post.korildi += 1
    post.save()

    context = {'post': post}
    return render(request, 'blog/post_batafsil.html', context)




@login_required
def post_yaratish(request):
    if request.method == 'POST':
        forma = PostForma(request.POST, request.FILES)  # Rasm fayllarini qabul qilish uchun request.FILES qo'shildi
        if forma.is_valid():
            post = forma.save(commit=False)
            post.muallif = request.user  # Avtomatik!
            post.save()
            messages.success(request, '✅ Post yaratildi!')
            return redirect('bosh_sahifa')
    else:
        forma = PostForma()

    return render(request, 'blog/post_yaratish.html', {'forma': forma})


@login_required
def post_tahrirlash(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Faqat muallif tahrirlay oladi
    if post.muallif != request.user:
        messages.error(request, '❌ Siz faqat o\'z postingizni tahrirlashingiz mumkin!')
        return redirect('post_batafsil', post_id=post.id)

    if request.method == 'POST':
        forma = PostForma(request.POST, instance=post)
        if forma.is_valid():
            forma.save()
            messages.success(request, '✅ Post yangilandi!')
            return redirect('post_batafsil', post_id=post.id)
    else:
        forma = PostForma(instance=post)

    context = {'forma': forma, 'post': post}
    return render(request, 'blog/post_tahrirlash.html', context)


@login_required
def post_ochirish(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '✅ Post o\'chirildi!')
        return redirect('bosh_sahifa')

    return render(request, 'blog/post_ochirish.html', {'post': post})

def ommabop_postlar(request):
    postlar = Post.objects.filter(
        nashr_etilgan=True
    ).order_by('-korildi')[:5]  # Eng ko'p ko'rilgan 5 ta

    context = {'postlar': postlar}
    return render(request, 'blog/ommabop.html', context)



def biz_haqimizda(request):  # ← Yangi
    return render(request, 'blog/biz_haqimizda.html')


def aloqa(request):
    return render(request, 'blog/aloqa.html')