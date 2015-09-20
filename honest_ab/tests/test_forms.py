from django.test import TestCase

from honest_ab.forms import BucketSet, ExperimentDomainUsage
from honest_ab.tests.factories import ExperimentDomainFactory, ExperimentFactory


class BucketSetTests(TestCase):

    def test_non_overlapping(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(100, 199)
        self.assertEqual(1, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 99)
        self.assertEqual(ret_set[0].num_experiments, 4)

    def test_simple_overlap(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(45, 145)
        self.assertEqual(2, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 44)
        self.assertEqual(ret_set[0].num_experiments, 4)

        self.assertEqual(ret_set[1].start, 45)
        self.assertEqual(ret_set[1].end, 99)
        self.assertEqual(ret_set[1].num_experiments, 5)

    def test_simple_overlap_reverse(self):
        bucket = BucketSet(45, 145, 4)
        ret_set = bucket.compare_with(0, 99)
        self.assertEqual(2, len(ret_set))
        self.assertEqual(ret_set[1].start, 45)
        self.assertEqual(ret_set[1].end, 99)
        self.assertEqual(ret_set[1].num_experiments, 5)

        self.assertEqual(ret_set[0].start, 100)
        self.assertEqual(ret_set[0].end, 145)
        self.assertEqual(ret_set[0].num_experiments, 4)

    def test_proper_subset(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(3, 67)
        self.assertEqual(3, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 2)
        self.assertEqual(ret_set[0].num_experiments, 4)

        self.assertEqual(ret_set[2].start, 3)
        self.assertEqual(ret_set[2].end, 67)
        self.assertEqual(ret_set[2].num_experiments, 5)

        self.assertEqual(ret_set[1].start, 68)
        self.assertEqual(ret_set[1].end, 99)
        self.assertEqual(ret_set[1].num_experiments, 4)

    def test_proper_superset(self):
        bucket = BucketSet(3, 67, 4)
        ret_set = bucket.compare_with(0, 99)
        self.assertEqual(1, len(ret_set))
        self.assertEqual(ret_set[0].start, 3)
        self.assertEqual(ret_set[0].end, 67)
        self.assertEqual(ret_set[0].num_experiments, 5)

    def test_left_sided_superset(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(0, 199)
        self.assertEqual(1, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 99)
        self.assertEqual(ret_set[0].num_experiments, 5)

    def test_left_sided_subset(self):
        bucket = BucketSet(0, 999, 4)
        ret_set = bucket.compare_with(0, 199)
        self.assertEqual(2, len(ret_set))
        self.assertEqual(ret_set[1].start, 0)
        self.assertEqual(ret_set[1].end, 199)
        self.assertEqual(ret_set[1].num_experiments, 5)

        self.assertEqual(ret_set[0].start, 200)
        self.assertEqual(ret_set[0].end, 999)
        self.assertEqual(ret_set[0].num_experiments, 4)

    def test_right_sided_superset(self):
        bucket = BucketSet(5, 99, 4)
        ret_set = bucket.compare_with(0, 99)
        self.assertEqual(1, len(ret_set))
        self.assertEqual(ret_set[0].start, 5)
        self.assertEqual(ret_set[0].end, 99)
        self.assertEqual(ret_set[0].num_experiments, 5)

    def test_same(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(0, 99)
        self.assertEqual(1, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 99)
        self.assertEqual(ret_set[0].num_experiments, 5)

    def test_single_overlap(self):
        bucket = BucketSet(0, 99, 4)
        ret_set = bucket.compare_with(99, 154)
        self.assertEqual(2, len(ret_set))
        self.assertEqual(ret_set[0].start, 0)
        self.assertEqual(ret_set[0].end, 98)
        self.assertEqual(ret_set[0].num_experiments, 4)

        self.assertEqual(ret_set[1].start, 99)
        self.assertEqual(ret_set[1].end, 99)
        self.assertEqual(ret_set[1].num_experiments, 5)


class FullExperimentalDomainTests(TestCase):

    def test_add_single_experiment(self):
        domain = ExperimentDomainFactory.create()
        experiment = ExperimentFactory(domain=domain)
        experiment.slug = "slug1"
        experiment.save()

        domain_usage = ExperimentDomainUsage(domain)
        starts = [0, 100, 200]
        ends = [99, 199, 999]
        num_exp = [1, 1, 0]
        for i, bucket_set in enumerate(domain_usage.usage):
            self.assertEqual(starts[i], bucket_set.start)
            self.assertEqual(ends[i], bucket_set.end)
            self.assertEqual(num_exp[i], bucket_set.num_experiments)
