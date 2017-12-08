import factory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Tag'
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: 'tag%d' % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda n: 'user%d' % n)
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'project.Category'
        django_get_or_create = ('title',)
    title = factory.Sequence(lambda n: 'Title%d' % n)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'project.Project'
    title = factory.Sequence(lambda n: 'title%d' % n)
    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class FolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'project.Folder'

    name = factory.Sequence(lambda n: 'folder%d' % n)
    project = factory.SubFactory(ProjectFactory)
