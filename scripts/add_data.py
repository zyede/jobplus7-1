import os
import json
from faker import Faker
from random import randint
from jobplus.models import db, User, Personal, Company, Job, JobWanted

f = Faker(locale='zh_CN')

#生成随即汉字
def Unicode():
    val = randint(0x4e00, 0x9fbf)
    return chr(val)

#生成user
def iter_user():
    for i in range(60):
        yield User(
                name=str(f.random_int())+f.user_name(),
                email=f.ascii_email(),
                password='000000',
                role=f.random_element(elements=(10,20,30)),
                )


#生成公司和个人信息,文件路径暂时未生成，logo,简历
def iter_personal():
    for user in User.query:
        print('user.role',user.role)
        if user.role == 10:
            yield Personal(
                    user_id=user.id,
                    name=f.name(),
                    phone=f.phone_number(),
                    jobyear=f.random_int(0,100),
                    )
        elif user.role == 20:

            with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'datas.json')) as e:
                companys = json.load(e)
                for company in companys:
                    yield Company(
                        user_id=user.id,
                        name=company['company_name'],
                        #name=Unicode()+f.company(),
                        address=company['city'],
                        url='https://www.baidu.com',
                        phone=f.phone_number(),
                        summary=f.sentence(),
                        field=company['field'],
                        financing=company['financing'],
                        logo=company['company_image_url'],
                    )

#职位信息
def iter_job():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'datas.json')) as e:
        jobs = json.load(e)
        for job in jobs:
            yield Job(
                name=job['job_name'],
                min_pay=job['min_pay'],
                max_pay=job['max_pay'],
                address=job['city'],
                label=job['field'],
                jobyear=job['jobyear'],
                education=job['education'],
                state=job['num_of_people'],
            )

'''
    for company in Company.query:
        for i in range(randint(0,10)):
            pay_int = f.random_int(0,100)*1000
            yield Job(
                    company_id=company.id,
                    name=f.job(),
                    min_pay= pay_int,
                    max_pay=f.random_int(0,100)*1000+pay_int,
                    address=f.address(),
                    label=f.random_element(elements=('互联网','销售','管理')),
                    jobyear=f.random_int(0,100),
                    education=f.random_element(elements=('无限制','专科','本科','博士')),
                    state=f.random_element(elements=(1,2,3)),
                    )
'''

# 生成投递表
def iter_jobwanted():
    for personal in Personal.query:
        for job in Job.query:
            if randint(0,1) == 0:
                yield JobWanted(
                    job_id=job.id,
                    personal_id=personal.id,
                    company_id= job.company_id,
                    state=f.random_element(elements=(1,2,3))
                )


def run():
    for user in iter_user():
        db.session.add(user)
    for company in iter_personal():
        db.session.add(company)
    for job in iter_job():
        db.session.add(job)
    for jobwanted in iter_jobwanted():
        db.session.add(jobwanted)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

