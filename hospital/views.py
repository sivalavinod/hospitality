from django.shortcuts import render,redirect
from .models import Medicine
import psycopg2
import pandas as pd
from django.core.paginator import Paginator
import json



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

# def query_null(section):
#     if section in presenting_complts_type_sections :
#         query_null = "select * from (\
#             SELECT (jsonb_array_elements(medical_record_annotated->'{0}'))->>'text' AS entity,\
#             (jsonb_array_elements(medical_record_annotated->'{0}')::jsonb)->>'sct' AS sct \
#             from medical_record_documents where deleted=False and \
#             is_verified=True) as nn where sct is null or sct in ('0');".format(section)
#     # if section in diag_type_sections:
#     #     query_null = "select * from (\
#     #     SELECT appointment_id,\
#     #     jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'text' AS entity,\
#     #     jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'sct' AS sct\
#     #     from medical_record_documents where deleted=False and \
#     #     is_verified=True) as nn\
#     #     where sct is null or sct in ('0');".format(section)
#
#     df_null_sct = pd.read_sql_query(query_null, con=conn)
#     df_null_sct['entity_type'] = sec_names[section]
#     return df_null_sct

# Query to get Null SCT list
def query_null(section):
    if section in presenting_complts_type_sections + med_sections:
        query_null = "select * from (\
            SELECT appointment_id,(jsonb_array_elements(medical_record_annotated->'{0}'))->>'text' AS entity,\
            (jsonb_array_elements(medical_record_annotated->'{0}')::jsonb)->>'sct' AS sct \
            from medical_record_documents where deleted=False and \
            is_verified=True) as nn where sct is null or sct in ('0');".format(section)
    if section in diag_type_sections:
        query_null = "select * from (\
        SELECT appointment_id,\
        jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'text' AS entity,\
        jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'sct' AS sct\
        from medical_record_documents where deleted=False and \
        is_verified=True) as nn\
        where sct is null or sct in ('0');".format(section)

    df_null_sct = pd.read_sql_query(query_null, con=conn)
    df_null_sct['entity_type'] = sec_names[section]
    return df_null_sct

presenting_complts_type_sections = ['722446000','422432008','371542009','417662000','422843007']
med_sections=['721912009','761938008']
diag_type_sections=['439401001']
all_sections=presenting_complts_type_sections+med_sections+diag_type_sections

df = pd.read_sql_query('select * from public.medical_record_documents where deleted=False and \
                        is_verified=True and is_coded=1',con=conn)

def presenting_complaint(v,dict_sct):
    count = 1
    coded_sct_count = 0
    for etname in v:
        if etname['sct']==0 or etname['sct'] is None:
            if etname['text'].lower().strip() in dict_sct.keys():
                etname['sct'] = int(dict_sct[etname['text'].lower().strip()])
                coded_sct_count = coded_sct_count + 1
        else:
            coded_sct_count = coded_sct_count + 1
    if coded_sct_count==len(v):
        count = 0
#     cur.execute("UPDATE medical_record_documents SET medical_record_annotated =  %s  where appointment_id =  %s ",
#                 (json.dumps(lst, ensure_ascii=False),apid))
    return count

def medication(v,dict_sct):
    count = 1
    coded_sct_count = 0
    for etname in v:
        if etname['sct']==0 or etname['sct'] is None:
            if etname['text'].lower().strip() in dict_sct.keys():
                etname['sct'] = dict_sct[etname['text'].lower().strip()]
                coded_sct_count = coded_sct_count + 1
        else:
            coded_sct_count = coded_sct_count + 1
    if coded_sct_count==len(v):
        count = 0
    return count


def diagnosis(v,dict_sct):
    count = 1
    coded_sct_count = 0
    Total_sct = 0
    for etname in v:
        if etname['mandatory_fields']:
            for diag in etname['mandatory_fields']:
                Total_sct = Total_sct+1
                if diag['sct']==0 or diag['sct'] is None:
                    if diag['text'].lower().strip() in dict_sct.keys():
                        diag['sct'] = int(dict_sct[diag['text'].lower().strip()])
                        coded_sct_count = coded_sct_count + 1
                else:
                    coded_sct_count = coded_sct_count + 1
    if coded_sct_count==Total_sct:
        count = 0
#     cur.execute("UPDATE medical_record_documents SET medical_record_annotated =  %s  where appointment_id =  %s ",
#                 (json.dumps(lst, ensure_ascii=False),apid))
    return count



def query(section):
    if section in presenting_complts_type_sections + med_sections:
        query = "select * from (\
        SELECT appointment_id,(jsonb_array_elements(medical_record_annotated->'{0}'))->>'text' AS entity,\
        (jsonb_array_elements(medical_record_annotated->'{0}')::jsonb)->>'sct' AS sct \
        from medical_record_documents where deleted=False and \
        is_verified=True) as nn where sct is not null and sct not in ('0');".format(section)

    if section in diag_type_sections:
        query = "select * from (\
        SELECT appointment_id,\
        jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'text' AS entity,\
        jsonb_array_elements((jsonb_array_elements(medical_record_annotated->'{0}'))->'mandatory_fields')->>'sct' AS sct\
        from medical_record_documents where deleted=False and \
        is_verified=True) as nn\
        where sct is not null and sct!='0';".format(section)

    df_filled_sct = pd.read_sql_query(query, con=conn)
    #     df_filled_sct.to_csv('check.csv')
    dict_sct = dict(zip(df_filled_sct['entity'].str.lower(), df_filled_sct['sct']))
    return dict_sct

# cur.execute("UPDATE medical_record_documents SET medical_record_annotated = medical_record")

# cur.execute("ALTER TABLE medical_record_documents ADD COLUMN is_coded int")
# cur.execute("UPDATE medical_record_documents SET is_coded =1 ")

# df = pd.read_sql_query('select * from public.medical_record_documents where deleted=False and is_verified=True and is_coded=1',con=conn)
#
# dict_of_scts = {}
# for sec in all_sections:
#     dict_of_scts[sec] = query(sec)
#
# new_dict = {k:{} for k in sec_names.keys()}
# update_json(df,new_dict)

dict_of_scts = {}
for sec in all_sections:
    dict_of_scts[sec] = query(sec)

# Function to Update the json file
def update_json(df,update_dict):
    print("hi")
    for lst,apid,age in zip(df.medical_record_annotated,df.appointment_id,df.patient_age):
        None_count = 0
        for k,v in lst.items():
            if v:
                if k in presenting_complts_type_sections:
                    dict_of_scts[k].update(update_dict[k])
                    None_count = None_count + presenting_complaint(v,dict_of_scts[k])

                if k in diag_type_sections:
                    dict_of_scts[k].update(update_dict[k])
                    None_count = None_count + diagnosis(v,dict_of_scts[k])

                if k in med_sections:
                    dict_of_scts[k].update(update_dict[k])
                    None_count = None_count + medication(v,dict_of_scts[k])

        cur.execute("UPDATE medical_record_documents SET medical_record_annotated =  %s  where appointment_id =  %s ",
                    (json.dumps(lst, ensure_ascii=False),apid))

        if None_count>0:
            None_count=1
        cur.execute("UPDATE medical_record_documents SET is_coded =  %s where appointment_id =  %s ",(None_count,apid))
    print("hello")

def home(request):
    qs=Medicine.objects.all()
    return render (request,"home.html",{"d_names": qs})

def details(request):
    # df=pd.read_csv(r"C:\Users\vinu\Desktop\hospitality.csv",delimiter=',')
    full_null_list = pd.DataFrame([])
    for sec in all_sections:
        full_null_list = full_null_list.append(query_null(sec))
    full_null_list = full_null_list.drop_duplicates(['entity','entity_type'])
    if not full_null_list.empty:
        df=full_null_list.groupby('entity_type')['entity'].apply(list).reset_index()
        w = dict(zip(df['entity_type'],df['entity']))

    # for x in full_null_list.values:
    #     a,b,c=x
    #     check=Medicine.objects.filter(dis=c).filter(med=a)
    #     if check:
    #         pass
    #     else:
    #         Medicine(dis=c,med=a).save()
    # qs=Medicine.objects.filter(code='')
    # if qs:
    #     d={}
    #     if qs:
    #         for x in qs:
    #             if x.dis not in d:
    #                 d[x.dis]=[x.med]
    #             else:
    #                 d[x.dis].append(x.med)
    #     w={k:v for k,v in sorted(d.items())}
        return render(request,"details.html",{"res":w})
    else:
        return render(request,"details.html",{"msg":"all medicines have SCT code"})



def presenting(request,data):
    # pageno=request.GET.get("pageno")
    # updat=re?quest.GET.get("update")
    # qs1=Medicine.objects.filter(dis=data).filter(code='').order_by('med')
    # print(data)
    full_null_list = pd.DataFrame([])
    for sec in all_sections:
        full_null_list = full_null_list.append(query_null(sec))
    full_null_list = full_null_list.drop_duplicates(['entity', 'entity_type'])
    # r=full_null_list[full_null_list['entity_type']==data]
    # print(r.shape)
    if not full_null_list.empty:
        df = full_null_list.groupby('entity_type')['entity'].apply(list).reset_index()
        w = dict(zip(df['entity_type'], df['entity']))


        return render(request, "presentingcomplaint.html", {"res1": w[data], "names": data})
    # if qs1:
    #     return render(request, "presentingcomplaint.html", {"res1": qs1, "name": data})

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
    code=request.POST.get('cod')
    dis=request.GET.get('y')

    new_dict = {k: {} for k in sec_names.keys()}
    new_dict[[k for k, v in sec_names.items() if x == v][0]].update(
        {dis: code})

    update_json(df, new_dict)
      # qs=Medicine.objects.get(med=x)a
    # print(qs)
    # if qs:
    #     qs.code=code
    #     qs.save()
    return redirect("presenting", data=x)


def generate_table(request,t):
    nam=request.POST.get('nam')
    s_date=request.POST.get("start_date")
    e_date=request.POST.get("end_date")
    print(s_date)
    print(e_date)
    if nam:
        qs=Medicine.objects.get(med=nam).ordering
    # print(qs.id)
    # print(nam)
        return render(request,'generate_table.html',{"d_nam": qs})
    return render(request,'generate_table.html')






