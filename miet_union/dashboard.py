from admin_tools.dashboard import modules, Dashboard


class CustomIndexDashBoard(Dashboard):
    columns = 3
    title = ('Консоль администратора')

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(
            modules.ModelList(
                title=('Новости портала'),
                models=('miet_union.models.News',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Почта для рассылки'),
                models=('miet_union.models.EmailSubscription',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Все зарегистрированные пользователи сайта'),
                models=('miet_union.models.User',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Работники Профкома'),
                models=('miet_union.models.Worker',),
            )
        )
        self.children.append(modules.Group(
            title=("Документы"),
            display="tabs",
            children=[
                modules.ModelList(
                    title=('Студенту'),
                    models=('documents.models.HelpForProforg',
                            'documents.models.HelpForStudentProforg',
                            'documents.models.TheMainActivitiesOfProforg',),
                ),
                modules.ModelList(
                    title=('Документы'),
                    models=('documents.models.ProtectionOfPersonalInformation',    # noqa
                            'documents.models.NormativeDocuments',
                            'documents.models.CommissionsOfProfcom',
                            'documents.models.UsefulLinks',),
                ),

            ]
        )
        )
