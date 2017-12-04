import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)
    username = 'john'
    is_active = True


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'project.Project'
    title = factory.Sequence(lambda n: 'title%d' % n)
    owner = factory.SubFactory(UserFactory)


class FolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'project.Folder'

    name = factory.Sequence(lambda n: 'folder%d' % n)
    project = factory.SubFactory(ProjectFactory)
