import django_tables2 as tables
import itertools

class UserAnswerTable(tables.Table):
    place = tables.Column(empty_values=())
    user__username = tables.Column()
    points = tables.Column()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_place(self):
        return next(self.counter)
