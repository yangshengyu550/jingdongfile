from django.shortcuts import render

from jd import models

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

import MySQLdb
def get_data(sql):#获取数据库的数据
    conn = MySQLdb.connect('127.0.0.1','root','123456','jingdong',port=3306)   
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall() # 搜取所有结果
    cur.close()
    conn.close()
    return results
def order(request):# 向页面输出
    sql = "select * from jingdong" 
    m_data = get_data(sql)
    return render(request,'index.html',{'order':m_data})

"""
def goods(request):
    list=models.goods.object.all()
    Paginator=Paginator(list,30,5)
    page=request.GET.get('page')
    try:
        m_data=Paginator.page(page)
    except PageNotAnInteger:
        m_data=Paginator.page(1)
    except PageNotAnInteger:
        m_data=Paginator.page(Paginator.num_pages)
    return render(request,'index.html',{'list':m_data})
"""