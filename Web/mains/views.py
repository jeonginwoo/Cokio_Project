from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BurgerTable, SideTable, DDTable
#from .serializers import MenuSerializer
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'main/index.html')

# class MenuDetailView(APIView):
#     def get(self,request,menu_key):
#         try:
#             menu = Menu.objects.get(name=menu_key)
#             serializer = MenuSerializer(menu)
#             return Response(serializer.data)
#         except Menu.DoesNotExist:
#             return Response({"error" : "Menu not found"}, status= 404)

# 결제 페이지 이동
def purchase(request):
    return render(request, 'main/purchase.html')

# 프론트에서 음성 인식으로 Request를 받았을 때 처리함
def speechRecognition(request):
    if request.method == 'POST':
        recordData = request.body

        # 이 부분에 추후 Wisper 모델 적용 및 DB 쿼리 작성 예정
        with open('../test_record_data.mp3', 'wb') as mpeg:
            mpeg.write(recordData)

        data = {"message": "Response OK!"}

        return JsonResponse(data)

    # Request의 method가 POST 방식이 아닌 GET 방식임
    return JsonResponse({'message': 'This request is GET method', "status": 405}, status = 405)

# 프론트에서 텍스트로 Request를 받았을 때 처리함
def textInput(request):
    if request.method == 'POST':
        try:
            text_data = request.body
            text_data = json.loads(text_data)

            # 이 부분에 추후 모델 적용 및 DB 쿼리 작성

            data = {"message": text_data['value']}

            return JsonResponse(data)
        except: # Requset 형식이 올바른 JSON 형식이 아님
            return JsonResponse({"message": "Invalid JSON format!", "status": 400}, status = 400)

    # Request의 method가 POST 방식이 아닌 GET 방식임
    return JsonResponse({'message': 'This request is GET method', "status": 405}, status = 405)

def testBurger(request):
    print(request)
    burger_list = BurgerTable.objects.all()
    context = {'burger_list': burger_list}
    return render(request, 'main/list/burger_list.html', context)

def testSide(request):
    print(request)
    side_list = SideTable.objects.all()
    context = {'side_list': side_list}
    return render(request, 'main/list/side_list.html', context)

def testDD(request):
    print(request)
    dd_list = DDTable.objects.all()
    context = {'dd_list': dd_list}
    return render(request, 'main/list/dd_list.html', context)

def testQuery(request):
    d = {}
    a = ['S_menu_name 너겟킹', 'I_sliced_cheese 1', 'I_shredded_cheese 1']

    for i in a:
        j = i.split()
        if len(j) == 1:
            j.append('0')
        j[1] = j[1].replace('_', ' ')
        d[j[0]] = j[1]

    # SideTable.objects.filter(menu_name__startswith='너겟킹') # 너겟킹으로 시작하는 메뉴 찾기.
    # BurgerTable.objects.filter(spicy__gt=0) # 맵기가 0보다 큰 메뉴 찾기

    query_string = ''

    # 특정 메뉴 찾기
    if 'M_menu_name' in d:
        menu_list = BurgerTable.objects.filter(menu_name__startswith=d['M_menu_name'])
        context = {'menu_list':menu_list}
        return render(request, 'main/testQuery.html', context)
    elif 'S_menu_name' in d:
        menu_list = SideTable.objects.filter(menu_name__startswith=d['S_menu_name'])
        context = {'menu_list':menu_list}
        return render(request, 'main/testQuery.html', context)
    elif 'DD_menu_name' in d:
        menu_list = DDTable.objects.filter(menu_name__startswith=d['DD_menu_name'])
        context = {'menu_list':menu_list}
        return render(request, 'main/testQuery.html', context)
    
    # 특정 메뉴가 아닌 경우 추천
    else:
        query_string = f"SELECT * FROM BurgerTable WHERE "
        for q in d.keys():
            if q == 'N':
                query_string += ""
            if q == 'A':
                query_string += ""
        menu_list = BurgerTable.objects.raw(query_string)
        context = {'menu_list':menu_list}
        return render(request, 'main/testQuery.html', context)
