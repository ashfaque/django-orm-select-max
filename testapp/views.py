from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *
from django.db.models import F, Q, Sum, fields, ExpressionWrapper, Value, Case, When, Subquery, OuterRef, FloatField, DecimalField, Count
from rest_framework.response import Response


# ! Show maximum `version_no` for distinct `fk`.
class Test(APIView):
    permission_classes = [AllowAny]
    queryset = testmodel.objects.all()

    def get(self, request, *args, **kwargs):

        queryset = self.queryset.all().values("fk").distinct().annotate(                                                 # ? Takes `self.queryset` which is outside of get method queryset defined above at line 11. Fetch only `fk` in `values('fk') and distinct() gives only unique value for each duplicates. So we got 1 & 2.
                                                                        version_no_1=Subquery(                           # ? Inside `annotate()` we have `version_no_1` which will be shown in the response if `queryset` which is inside get method, is sent to Response().
                testmodel.objects.filter(fk=OuterRef('fk')).values_list('version_no',flat=True).order_by('-version_no')  # ? Inside Subquery() we filtered out and fetched only those objects whose `fk` is equals to the `fk` we got outside the Subquery() in the 1st line of this queryset (see line 15). And in values_list() it fetches `version_no` of those `fk`. But it runs individually. So for fk=1 it runs one time fetched one version_no for it. For fk=2 it runs another time and fetched one version_no for it. And as its order_by version_no descending. It will fetch the latest version.
                                                                                             )                           # ? The Subquery() loops only 2 times as there are only 2 values of `fk` i.e., 1, 2 in 1st line (see line 15).
                                                                        )

        print("queryset -----------------> ", queryset)
        print("queryset query -----------------> ", queryset.query)

        return Response(data = {
            'queryset':queryset,
            'query':str(queryset.query).replace('"','\'')
            }, status = 200)
