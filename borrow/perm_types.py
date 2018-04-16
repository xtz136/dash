class Base:
    package = 'default'

    view = ''
    add = ''
    change = ''
    delete = ''

    def __init__(self):
        default = dict(package=self.package, obj=self.__class__.__name__.lower())

        self.view = '{package}.{perm}_{obj}'.format(perm='view', **default)
        self.add = '{package}.{perm}_{obj}'.format(perm='add', **default)
        self.change = '{package}.{perm}_{obj}'.format(perm='change', **default)
        self.delete = '{package}.{perm}_{obj}'.format(perm='delete', **default)

        self.view_codename = '{perm}_{obj}'.format(perm='view', **default)
        self.add_codename = '{perm}_{obj}'.format(perm='add', **default)
        self.change_codename = '{perm}_{obj}'.format(perm='change', **default)
        self.delete_codename = '{perm}_{obj}'.format(perm='delete', **default)


class Company(Base):
    package = 'crm'


class EntityList(Base):
    package = 'borrow'


class RevertList(Base):
    package = 'borrow'


company_perm = Company()
entity_list_perm = EntityList()
revert_list_perm = RevertList()
