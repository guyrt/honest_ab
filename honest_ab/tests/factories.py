from factory import DjangoModelFactory, Sequence, SubFactory
from honest_ab.models import ExperimentDomain, Experiment


class ExperimentDomainFactory(DjangoModelFactory):
    class Meta:
        model = ExperimentDomain

    name = Sequence(lambda x: "expdomain" + str(x))
    slug = Sequence(lambda x: "expdomain" + str(x))


class ExperimentFactory(DjangoModelFactory):
    class Meta:
        model = Experiment

    name = Sequence(lambda x: "exp" + str(x))
    #slug = Sequence(lambda x: "exp" + str(x))  # fails for some reason. need to sort out.

    domain = SubFactory(ExperimentDomainFactory)

    buckets = "0:99,100:199"
    percentage_of_traffic = .2
