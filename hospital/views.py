from django.shortcuts import render,redirect,HttpResponse
from .models import Medicine
import psycopg2
import pandas as pd
from django.core.paginator import Paginator

db="valkyrie_02032020"
conn=psycopg2.connect(database=db,user='postgres',password='vinod',host='127.0.0.1',port='5432')
conn.autocommit = True
cur=conn.cursor()

scts = ['722446000','721912009','422432008','439401001','185389009','271907004','371542009','363679005',
        '108252007','4241000179101','417662000','761938008','422843007','71388002','160476009',
        '223464006','38678006', '3457005', '284366008']

fsns = ['allergy','current_med','family_history','diagnosis','follow_up_when','general_examination','hospital_history',
        'image_investigation','lab_investigation','lab_test_name','medical_conditions','prescribed_medication',
        'presenting_complaint','procedure_recommended','social_history','special_instruction','supportive_treatment',
        'cross_referral', 'systemic_examination']

sec_names = dict(zip(scts,fsns))

# def query_null(section):
#     if section in ['422843007','3457005','71388002']:
#         qs="select * from (SELECT (jsonb_array_elements(medical_record->'{0}')::jsonb)->>'text' AS entity,(jsonb_array_elements(medical_record->'{0}')::jsonb)->>'sct' AS sct from medical_record_documents where deleted=False and is_verified=True) as nn where sct is null or sct in ('0');".format(section)
#         null_sct=pd.read_sql_query(qs,con=conn)
#         null_sct['ent_type'] = 'presenting_complaint'
#         null_sct = null_sct.drop_duplicates('entity')
#     return null_sct
#
#
# def details(request):
#     # df=pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
#     df = query_null('422843007')
#     # sec_list = list(df['sectionname'].unique())
#     # sec_ent_df = pd.DataFrame(df.groupby('sectionname')['entity'].apply(list)).reset_index()
#     # # sec_ent_dict = dict(zip(sec_ent_df['sectionname'], sec_ent_df['entity']))
#
#     # for x in df.values:
#     #     a,b,c=x
#     #     Medicine(dis=c,med=a).save()
#     qs=Medicine.objects.filter(code='')
#     if qs:
#         d={}
#         if qs:
#             for x in qs:
#                 if x.dis not in d:
#                     d[x.dis]=[x.med]
#                 else:
#                     d[x.dis].append(x.med)
#         w={k:v for k,v in sorted(d.items())}
#         return render(request,"details.html",{"res":w})
#     else:
#         return render(request,"details.html",{"msg":"all medicines have code"})
#

def query_null(section):
    if section in presenting_complts_type_sections :
        query_null = "select * from (\
            SELECT (jsonb_array_elements(medical_record->'{0}'))->>'text' AS entity,\
            (jsonb_array_elements(medical_record->'{0}')::jsonb)->>'sct' AS sct \
            from medical_record_documents where deleted=False and \
            is_verified=True) as nn where sct is null or sct in ('0');".format(section)
    # if section in diag_type_sections:
    #     query_null = "select * from (\
    #     SELECT appointment_id,\
    #     jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'text' AS entity,\
    #     jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'sct' AS sct\
    #     from medical_record_documents where deleted=False and \
    #     is_verified=True) as nn\
    #     where sct is null or sct in ('0');".format(section)

    df_null_sct = pd.read_sql_query(query_null, con=conn)
    df_null_sct['enity_type'] = sec_names[section]
    return df_null_sct

presenting_complts_type_sections = ['722446000','422432008','371542009','417662000','422843007']
def details(request):
    # df=pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
    # full_null_list = pd.DataFrame([])
    # for sec in presenting_complts_type_sections:
    #     full_null_list = full_null_list.append(query_null(sec))
    #
    # full_null_list = full_null_list.drop_duplicates(['entity','enity_type'])
    # print(full_null_list.shape)
    # for x in full_null_list.values:
    #     a,b,c=x
    #     check=Medicine.objects.filter(med=a)
    #     if check:
    #         pass
    #     else:
    #         Medicine(dis=c,med=a).save()

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
        return render(request,"details.html",{"msg":"all medicines have SCT code"})



def presenting(request,data):
    # pageno=request.GET.get("pageno")
    # updat=re?quest.GET.get("update")
    qs1=Medicine.objects.filter(dis=data).filter(code='').order_by('med')
    if qs1:
        return render(request, "presentingcomplaint.html", {"res1": qs1, "name": data})

    # if qs1:
    #     sq = Paginator(qs1, 10)
    #     if pageno==None:
    #         s=sq.page(1)
    #         return render(request, "presentingcomplaint.html", {"res1": s, "name": data})
    #     # elif update:
    #     #     s=sq.page(updat)
    #     #     return render(request, "presentingcomplaint.html", {"res1": s, "name": data})
    #
    #     else:
    #         s=sq.page(pageno)
    #         return render(request, "presentingcomplaint.html", {"res1": s, "name": data})
    return redirect("details")


def update(request,x):
    code=request.POST.get('code')
    qs=Medicine.objects.get(id=x)
    if qs:
        qs.code=code
        qs.save()
        return redirect("presenting",data=qs.dis)


# def select(request,data):
#     select=request.POST.get("get")
#     q=Medicine.objects.filter(code='')
#     w = {k: v for k, v in sorted(q.items())}
#     qs1 = Medicine.objects.filter(dis=data).filter(code='').order_by('med')
#     if qs1:
#         sq = Paginator(qs1, select)
#         if select == None:
#             s = sq.page(1)
#             return render(request, "presentingcomplaint.html", {"res1": s,"res":w})
#         else:
#             s = sq.page(select)
#             return render(request, "presentingcomplaint.html", {"res1": s,"res":w})
#
#     return redirect("details")