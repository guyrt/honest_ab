from operator import attrgetter
from django import forms


class GoalAchievedForm(forms.Form):

    model = forms.CharField()
    model_pk = forms.IntegerField()


class ExperimentModelAdminForm(forms.ModelForm):

    def clean_percentage_of_traffic(self):
        self._get_allowable_buckets()
        # put buckets in cleaned_data.

        return self.cleaned_data

    def _get_allowable_buckets(self):
        percentage = self.cleaned_data['percentage_of_traffic']
        domain = self.cleaned_data['domain']
        domain_usage = ExperimentDomainUsage(domain)

        # Get list of open buckets on domain.

        # Find zero sets

        # If can't find enough, throw


class BucketSet(object):

    def __init__(self, start, end, num_experiments=0):
        self.start = start
        self.end = end
        self.num_experiments = num_experiments

    def __str__(self):
        return " ".join((str(i) for i in (self.start, self.end, self.num_experiments)))

    def compare_with(self, start, end):

        return_set = []
        remaining_set = [self.start, self.end, self.num_experiments]
        if self.start < start <= self.end:
            remaining_set[0] = start
            remaining_set[2] = self.num_experiments + 1
            return_set.append(BucketSet(self.start, start - 1, self.num_experiments))
        if self.start <= end < self.end:
            remaining_set[1] = end
            remaining_set[2] = self.num_experiments + 1
            return_set.append(BucketSet(end + 1, self.end, self.num_experiments))
        if self.start >= start and self.end <= end:
            remaining_set[2] = self.num_experiments + 1
        return_set.append(BucketSet(*remaining_set))
        return return_set


class ExperimentDomainUsage(object):

    def __init__(self, domain):
        self.usage = [BucketSet(0, domain.num_buckets - 1)]

        for exp in domain.experiment_set.filter(active=1):
            # add exp information
            for bucket_range in exp.buckets.split(','):
                start, end = (int(a) for a in bucket_range.split(':'))
                new_buckets = []
                for bucketset in self.usage:
                    new_bucketsets = bucketset.compare_with(start, end)
                    if new_bucketsets:
                        new_buckets.extend(new_bucketsets)
                    else:
                        new_buckets.append(bucketset)
                self.usage = new_buckets
        self.usage = sorted(self.usage, key=attrgetter('start'))
