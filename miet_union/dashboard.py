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
                title=('Пользователи'),
                models=('miet_union.models.User',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Работники Профкома'),
                models=('miet_union.models.Worker',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Работники Профкома'),
                models=('miet_union.models.HelpForProforg',),
            )
        )
        self.children.append(
            modules.ModelList(
                title=('Работники Профкома'),
                models=('miet_union.models.MoneyHelp',),
            )
        )
        self.children.append(modules.Group(
            title=("Документы"),
            display="tabs",
            children=[
                modules.ModelList(
                    title=('Студенту'),
                    models=('miet_union.models.HelpForProforg',
                            'miet_union.models.HelpForStudentProforg',
                            'miet_union.models.TheMainActivitiesOfProforg',),
                ),
                modules.ModelList(
                    title=('Документы'),
                    models=('miet_union.models.ProtectionOfPersonalInformation',    # noqa
                            'miet_union.models.NormativeDocuments',
                            'miet_union.models.CommissionsOfProfcom',
                            'miet_union.models.UsefulLinks',),
                ),

            ]
        )
        )
