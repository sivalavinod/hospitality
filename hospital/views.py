from django.shortcuts import render,redirect,HttpResponse

import pandas as pd
from .models import Medicine
# Create your views here.
# def home(request):
#     return render(request,"home.html")


# def details(request):
#     df = pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
#     sec_list = list(df['sectionname'].unique())
#     sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
#     return render(request,"details.html",{"res":sec_list})

# def details(request):
#     # aa = request.GET('')
#     df = pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
#     sec_list = list(df['sectionname'].unique())
#     sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
#     sec_ent_dict = dict(zip(sec_ent_df['sectionname'], sec_ent_df['entity']))
#     x = sec_ent_dict["presentingcomplaint"]
#     y = sec_ent_dict["allergy"]
#     # for x in df.values:
#     #     a,b=x
#     Medicine(dis=x,med=y).save()
#     return render(request,"details.html",{"res":sec_list})


def details(request):
    df=pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
    # sec_list = list(df['sectionname'].unique())
    # sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
    # sec_ent_dict = dict(zip(sec_ent_df['sectionname'], sec_ent_df['entity']))

    # for x in df.values:
    #     a,b=x
    #     Medicine(dis=a,med=b).save()
    qs=Medicine.objects.all()
    d={}
    if qs:
        for x in qs:
            if x.dis not in d:
                d[x.dis]=[x.med]
            else:
                d[x.dis].append(x.med)
    return render(request,"details.html",{"res":d})


def presenting(request,data):
    # df = pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
    # sec_list = list(df['sectionname'].unique())
    # sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
    # sec_ent_dict = dict(zip(sec_ent_df['sectionname'], sec_ent_df['entity']))
    # print(data)
    qs1=Medicine.objects.filter(dis=data)
    if qs1:
        return render(request, "presentingcomplaint.html", {"res1":qs1,"name":data})
    # return render(request,"presentingcomplaint.html",{"res1":sec_ent_dict[data]})


def update(request,idno):
    med=request.POST.get('med')
    dis=request.POST.get('dis')
    code=request.POST.get('code')
    qs=Medicine.objects.filter(id=idno).update(dis=dis,med=med,code=code)
    if qs:
        return HttpResponse("Successfully updated")









