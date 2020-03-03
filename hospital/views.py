from django.shortcuts import render,redirect,HttpResponse
import pandas as pd
from .models import Medicine

def details(request):
    # df=pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
    # sec_list = list(df['sectionname'].unique())
    # sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
    # sec_ent_dict = dict(zip(sec_ent_df['sectionname'], sec_ent_df['entity']))

    # for x in df.values:
    #     a,b=x
    #     Medicine(dis=a,med=b).save()
    qs=Medicine.objects.filter(code='')
    if qs:
        d={}
        if qs:
            for x in qs:
                if x.dis not in d:
                    d[x.dis]=[x.med]
                else:
                    d[x.dis].append(x.med)
        w={k:v for k,v in sorted(d.items())}
        return render(request,"details.html",{"res":w})
    else:
        return render(request,"details.html",{"msg":"all medicines have code"})


def presenting(request,data):
    qs1=Medicine.objects.filter(dis=data).filter(code='').order_by('med')
    print(list(qs1))
    if qs1:
        return render(request, "presentingcomplaint.html", {"res1":qs1,"name":data})
    return redirect("details")

def update(request,x):
    code=request.POST.get('code')
    qs=Medicine.objects.get(id=x)
    if qs:
        qs.code=code
        qs.save()
        return redirect("presenting",data=qs.dis)










