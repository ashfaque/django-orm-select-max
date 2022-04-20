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

        queryset = self.queryset.all().values("fk").distinct().annotate(
                                                                        version_no_1=Subquery(
                testmodel.objects.filter(fk=OuterRef('fk')).values_list('version_no',flat=True).order_by('-version_no')
                                                                                             )
                                                                        )

        print("queryset -----------------> ", queryset)
        print("queryset query -----------------> ", queryset.query)

        return Response(data = {
            'queryset':queryset,
            'query':str(queryset.query).replace('"','\'')
            }, status = 200)
