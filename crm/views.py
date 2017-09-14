import csv
import hashlib
from io import TextIOWrapper
from collections import namedtuple

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

from django import forms
from django.forms import Form, ModelForm, modelformset_factory

from .forms import ItemAutoSelectForm, BorrowerAutoSelectForm
from .models import Company, People, ShareHolder, Item, ItemBorrowingRecord


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
    return [i[0] for i in consts if i[1] == label.strip()][0]


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
        data['expired_at'] = None if data['expired_at'] == '长期' else data['expired_at']
        data['ss_date'] = data['ss_date'].strip() or None

        data['industry'] = const2str(Company.INDUSTRIES, data['industry'])
        data['type'] = const2str(Company.TYPES, data['type'])
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


@staff_member_required
def borrow_view(request):
    ids = request.GET.get("ids").split(",")
    ct = request.GET.get("ct")
    model = ContentType.objects.get_for_id(ct).model_class()
    Formset = modelformset_factory(
        ItemBorrowingRecord,
        fields=('item', 'reason', 'qty', 'note'),
        extra=len(ids))
    if request.method == "GET":
        borrower_form = BorrowerAutoSelectForm()
        formset = Formset(
            queryset=ItemBorrowingRecord.objects.none(),
            initial=[{'item': item}
                     for item in model.available.filter(id__in=ids)])
        context = {
            'borrower_form': borrower_form,
            'formset': formset
        }

        return render(request, "crm/borrow.html", context=context)
    borrower_form = BorrowerAutoSelectForm(request.POST)
    formset = Formset(request.POST)

    if formset.is_valid() and borrower_form.is_valid():
        instances = formset.save(commit=False)
        borrower = User.objects.get(
            username=borrower_form.cleaned_data['user'])
        for obj in instances:
            if obj.item.can_borrow():
                obj.lender = request.user
                obj.borrower = borrower
                obj.save()
                obj.item.borrow_to(borrower)
        return redirect(reverse("admin:crm_itemborrowingrecord_changelist"))
    context = {
        'formset': formset
    }
    return render(request, "crm/borrow.html", context=context)


@staff_member_required
def item_bulk_add_view(request):
    Formset = modelformset_factory(
        Item, fields=("item", "qty", "note"), extra=3)

    if request.method == "GET":
        formset = Formset(queryset=Item.objects.none())
        company_form = ItemAutoSelectForm(
            initial={'receiver': request.user.username})
    else:
        formset = Formset(request.POST)
        company_form = ItemAutoSelectForm(request.POST)
        if formset.is_valid() and company_form.is_valid():
            instances = formset.save(commit=False)
            company = Company.objects.get(
                title=company_form.cleaned_data['company'])
            receiver = User.objects.get(
                username=company_form.cleaned_data['receiver'])
            for obj in instances:
                obj.company = company
                obj.receiver = receiver
                obj.save()
            if request.POST.get("gen_receipt", False):
                return redirect(reverse("crm:item-receipt") + "?ids={0}".format(
                    ",".join(map(lambda x: str(x.pk), instances))))
            return redirect(reverse("admin:crm_item_changelist"))
    context = {'opts': {'app_label': 'crm',
                        'model_name': 'Item', 'verbose_name': '客户资料'},
               "formset": formset,
               "company_form": company_form}
    return render(request, "crm/item_bulk_add.html", context=context)


@staff_member_required
def item_receipt_view(request):
    """生成收据"""
    ids = request.GET.get("ids", "").split(',')
    items = Item.objects.filter(id__in=ids)
    company = ""
    created = ""
    receiver = ""
    if items:
        company = items[0].company_title
        created = items[0].created.strftime("%Y年%m月%d日")
        receiver = items[0].receiver.username
    sn = int(hashlib.sha256(",".join(sorted(ids)).encode(
        'utf-8')).hexdigest(), 16) % 10 ** 4
    total = sum([item.qty for item in items])
    context = {"items": items,
               "sn": sn, "total": total, "company": company,
               "created": created, "receiver": receiver}
    return render(request, "crm/item_receipt.html", context=context)
