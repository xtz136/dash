import csv
from io import TextIOWrapper
from collections import namedtuple

from django.shortcuts import render
from django.contrib.auth.models import User
from django import forms

from .forms import CompanyForm
from .models import Company, People, ShareHolder


class ImportFileForm(forms.Form):
    file = forms.FileField()
    model = forms.ChoiceField(
        initial='Company',
        choices=(
            ('Company', '公司'),
        )
    )


company_fields = (("no,title,type,registered_capital,industry,"
                   "taxpayer_type,scale_size,credit_rating,address,"
                   "op_address,uscc,business_license,website,salesman,"
                   "bookkeeper,registered_at,expired_at,status,ss_number,"
                   "ss_date,taxpayer_bank,taxpayer_account,ss_bank,ss_account,"
                   "individual_bank,individual_account,national_tax_office,"
                   "national_tax_id,national_tax_sn,national_tax_staff,national_tax_phone,"
                   "local_tax_office,local_tax_id,local_tax_sn,local_tax_staff,local_tax_phone,") +
                  ",".join("name_{i},share_{i},sfz_{i},phone_{i}".format(i=i)
                           for i in range(5))).split(',')

CompanyRecord = namedtuple('CompanyRecord', company_fields)


def get_or_create_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username)
    return user


def const2str(consts, label):
    return [i[0] for i in consts if i[1] == label][0]


def handle_import_company(f):
    rows = map(CompanyRecord._make, csv.reader(f))
    print(next(rows))
    for row in rows:
        data = row._asdict()
        data['salesman'] = get_or_create_user(data['salesman'])
        data['bookkeeper'] = get_or_create_user(data['bookkeeper'])
        data['national_tax_office'] = None
        data['local_tax_office'] = None
        data.pop('no')
        data['registered_at'] = data['registered_at'].strip() or None
        data['expired_at'] = data['expired_at'].strip() or None
        data['ss_date'] = data['ss_date'].strip() or None

        data['industry'] = const2str(Company.INDUSTRIES, data['industry'])
        data['taxpayer_type'] = const2str(
            Company.TAXPAYER_TYPES, data['taxpayer_type'])
        data['status'] = const2str(
            Company.STATUS, data['status'])
        data['scale_size'] = 'small'

        peoples = [p for p in [
            {'name': data.pop('name_{0}'.format(i)).strip(),
             'share': float(data.pop('share_{0}'.format(i)).replace('%', '') or 0),
             'sfz': data.pop('sfz_{0}'.format(i)),
             'phone': data.pop('phone_{0}'.format(i)),
             } for i in range(5)] if p['name'] != '']
        shares = [p.pop('share') for p in peoples]
        peoples = list(map(get_or_create_peopel, peoples))

        try:
            company = Company.objects.get(title=data['title'])
        except Company.DoesNotExist:
            company = Company(**data)
            company.save()

        # 法人
        get_or_create_shareholder(company=company, people=peoples.pop(
            0), share=shares.pop(0), role='legal')

        if peoples:
            [get_or_create_shareholder(company=company, people=peoples.pop(
                0), share=shares.pop(0), role='share')]


def get_or_create_shareholder(**data):
    company = data['company']
    people = data['people']

    try:
        return ShareHolder.objects.get(company=company, people=people)
    except ShareHolder.DoesNotExist:
        return ShareHolder.objects.create(**data)


def get_or_create_peopel(people):
    if people['sfz']:
        try:
            p = People.objects.get(sfz=people['sfz'])
            return p
        except People.DoesNotExist:
            pass
    return People.objects.create(**people)


def import_model_view(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.data['model'] == 'Company':
                results = handle_import_company(TextIOWrapper(
                    request.FILES['file'].file, encoding=request.encoding))
    form = ImportFileForm()
    return render(request, 'crm/import.html', {'form': form})
