from redisco import models


class State(models.Model):
    name = models.Attribute(required=True)
    code = models.Attribute(required=True)


class Person(models.Model):
    name = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fave_colors = models.ListField(str)
    id = models.IntegerField()
    state = models.ReferenceField(State)


ss = State.search
ps = Person.search


if __name__ == '__main__':

    # create records
    mh = State(name='Maharashtra', code='MH')
    mh.save()

    # Person(name="Swati", fave_colors=['red'], id=1).save()
    Person(name="Mahendra", fave_colors=['black', 'blue'], id=2, state=mh).save()
    # Person(name="Suhit", fave_colors=['maroon', 'blue'], id=3).save()
    # Person(name="Sanjukta", fave_colors=['black'], id=4).save()
    # Person(name="Kummi", fave_colors=['black']).save()
    # Person(name="Hemendra", fave_colors=['orange', 'blue']).save()

    # query
    print Person.objects.filter(name='Mahendra')
    print Person.search.search('@name:mahendra')


