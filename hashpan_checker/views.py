import logging

import loguru
import requests
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from hashpan_checker.forms import HashpanForm
from hashpan_checker.serializers import TransportOrderSerializer


HASHPAN_REQUEST_URL = "http://nova.ctrans.ru/apidop?card_mask={card_mask}"
MAX_PAGE_SIZE = 10000
BLACKLISTED_PANS_URL = "https://securepayments.sberbank.ru/tkp_Barnaul/lists/black_pans?page={page_num}&page_size={max_size}"


class HashpanView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "card_orders.html"

    def get(self, request):
        """
        Отобразить пустой список и 2 поля с кнопкой
        """
        serializer = TransportOrderSerializer()
        return Response({"payments": []})

    def post(self, request):
        """
        1. Сделать запрос на внешний апи
        2. Получить список объектов по введённым параметрам
        3. Отрисовать, группируя по hashpan
        """
        form = HashpanForm(request.POST)
        if not form.is_valid():
            loguru.logger.debug(f"Got form errors: {form.errors}")
            return Response(status=400)

        first_six_letters = form.cleaned_data["first_six_letters"]
        last_four_letters = form.cleaned_data["last_four_letters"]
        loguru.logger.debug(
            f"Swallowed form with data {first_six_letters=}, {last_four_letters=}"
        )
        card_mask = first_six_letters + "XXXXXX" + last_four_letters
        response = requests.get(HASHPAN_REQUEST_URL.format(card_mask=card_mask))
        loguru.logger.debug(f"Got response: {response.json()}")

        serializer = TransportOrderSerializer(data=response.json(), many=True)
        if not serializer.is_valid():
            loguru.logger.debug(f"Not a valid serializer \n {serializer.errors}")
            return Response(data={"errors": serializer.errors}, status=400)

        hashpans = self.get_blacklisted_pans()
        payments = serializer.data
        for obj in payments:
            obj["is_blocked"] = obj["hashpan"] in hashpans
        loguru.logger.debug(f"Rendering data: {serializer.data}")
        return render(request, "card_orders.html", {"payments": payments})

    def get_blacklisted_pans(self):
        hashpans = []
        zero_page = requests.get(
            BLACKLISTED_PANS_URL.format(max_size=MAX_PAGE_SIZE, page_num=0), verify=False
        )
        zero_page_dict = zero_page.json()
        total_pages = zero_page_dict["totalPages"]
        zero_page_values = [obj["a"] for obj in zero_page_dict["listValues"]]
        hashpans.extend(zero_page_values)
        for i in range(1, total_pages):
            page = requests.get(
                BLACKLISTED_PANS_URL.format(max_size=MAX_PAGE_SIZE, page_num=i),
                verify=False,
            )
            page_dict = page.json()
            page_values = [obj["a"] for obj in page_dict["listValues"]]
            hashpans.extend(page_values)
        loguru.logger.debug(f"{hashpans=}")
        return set(hashpans)
