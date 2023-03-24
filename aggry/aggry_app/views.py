from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from urllib.parse import urlencode
import os
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Jobs
from .forms import JobSearchForm
from django.core.paginator import Paginator

 
   
def frontpage(request):
    jobs = Jobs.objects.filter(Q(job='建築施工管理') | Q(job='土木施工管理') | Q(job='設備施工管理')).all()
    if request.method == "POST":
        form = JobSearchForm(request.POST)
        if form.is_valid():            
            # リダイレクト先のパスを取得する
            redirect_url = reverse('aggry_app:home')
            # 職種と勤務地のパラメータを作成
            parameters = urlencode({'job': form.cleaned_data['job'], 'location': form.cleaned_data['location']})
            # URLにパラメータを付与する
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
    else:
        form = JobSearchForm()       
    return render(request, "aggry_app/frontpage.html", context = {
        "form": form,
        "jobs": jobs,
        })


def home(request):
    # 職種と勤務地で絞ったデータを取得
    jobs = Jobs.objects.filter(job=request.GET.get('job'), mod_location=request.GET.get('location')).all()
    
    # label1のパターンを作り、そのパターンと一致したら順にjob_2dに格納
    patterns = Jobs.objects.values_list('label1', flat=True).distinct().order_by('label1').reverse() # label1のパターン
    jobs_2d = [[] for _ in range(len(patterns))] # 空の二次元リストを作成
    for i, pattern in enumerate(patterns): # label1のパターンごとに一致するものを二次元リストに格納
        for job in jobs:
            if job.label1 == pattern:
                job.mod_detail = job.detail.replace(' ', '<br>').replace('　', '<br>').replace('\n', '<br>') # クリックされたら右側に表示する用の仕事内容
                job.mod_welfare = job.welfare.replace(' ', '<br>').replace('　', '<br>').replace('\n', '<br>') # クリックされたら右側に表示する用の仕事内容
                jobs_2d[i].append(job)
    jobs_2d = [x for x in jobs_2d if x]
    
    # 20求人ずつにページ分割
    paginator = Paginator(jobs_2d, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'aggry_app/home.html', context = {
        "jobs": jobs,
        "page_obj": page_obj,
        "request": request,
        "job": request.GET.get('job'),
        "location": request.GET.get('location'),
    })


def job_detail(request, id):
    job = Jobs.objects.get(id=id)
    return render(request, "aggry_app/job_detail.html", context = {
        "job": job
        })
    
def test(request):
    jobs = Jobs.objects.all()
    # patterns = Jobs.objects.filter(agent="株式会社コプロ・エンジニアード").values_list('job', flat=True).distinct().order_by('job')
    # print(patterns)
    return render(request, "aggry_app/test.html", context = {
        "jobs": jobs,
    })