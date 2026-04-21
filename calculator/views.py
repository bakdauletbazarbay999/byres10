from tokenize import String

from django.shortcuts import render, redirect
from datetime import datetime

from openpyxl.styles.builtins import title


def index(request):
    return render(request, "calculator/index.html")

def lab1(request):
    distance = ""
    scale_value = ""
    cm_value = ""

    if request.method == "POST":
        if "clear" in request.POST:
            scale_value = ""
            cm_value = ""
            distance = ""
        else:
            scale_value = request.POST.get("scale", "")
            cm_value = request.POST.get("cm", "")
            try:
                scale = float(scale_value.replace(",", "."))
                cm = float(cm_value.replace(",", "."))
                distance = f"{scale * cm:.2f} км."



            except ValueError:
                distance = "Қате енгізу!"


    return render(request, "calculator/lab1.html", {
        "distance": distance,
        "scale_value": scale_value,
        "cm_value": cm_value,
    })
def lab2(request, Item="ball"):
    images = {
        "ball": "/static/images/dop.jpg",
        "tent": "/static/images/palatka.jpg",
        "bicycle": "/static/images/velik.jpg",
        "skate": "/static/images/skate.jpg",
        "backpack": "/static/images/sumka.jpg",
    }
    image = images.get(Item, "/static/images/ball.jpg")
    return render(request, "calculator/lab2.html", {"item": Item, "image": image})

def lab3(request):
    brands = {
        "Nike": ["Футболка", "Кроссовка", "Барсетка", "Носки", "Сороконожки"],
        "Adidas": ["Футболка", "Сумка", "Рюкзак", "Куртка", "Кроссовка"],
        "The North Face": ["Куртка", "Футболка", "Кепка", "Ботинка", "Худи"],
        "Demix": ["Рюкзак", "Трико", "Шапка", "Футболка", "Насос"],
        "Salomon": ["Ботинка", "Шапка", "Бандана", "Носки", "Рюкзак"]
    }

    selected_brand = request.GET.get("brand")
    selected_item = request.GET.get("item")

    if not selected_brand:
        selected_brand = "Nike"

    items = brands[selected_brand]

    if not selected_item or selected_item not in [f"{i} {selected_brand}" for i in items]:
        selected_item = f"{items[0]} {selected_brand}"

    images = {
        # Nike
        "Футболка Nike": "/static/images/nifut.jpg",
        "Кроссовка Nike": "/static/images/nikros.jpg",
        "Барсетка Nike": "/static/images/nibar.jpg",
        "Носки Nike": "/static/images/ninos.jpg",
        "Сороконожки Nike": "/static/images/nisor.jpg",
        # Adidas
        "Футболка Adidas": "/static/images/adifut.jpg",
        "Сумка Adidas": "/static/images/adisum.jpg",
        "Рюкзак Adidas": "/static/images/adiruk.jpg",
        "Куртка Adidas": "/static/images/adikurt.jpg",
        "Кроссовка Adidas": "/static/images/adikros.jpg",
        # The North Face
        "Куртка The North Face": "/static/images/thekurt.jpg",
        "Футболка The North Face": "/static/images/thefut.jpg",
        "Кепка The North Face": "/static/images/thekep.jpg",
        "Ботинка The North Face": "/static/images/thebat.jpg",
        "Худи The North Face": "/static/images/thehud.jpg",
        # Demix
        "Рюкзак Demix": "/static/images/desum.jpg",
        "Трико Demix": "/static/images/dewal.jpg",
        "Шапка Demix": "/static/images/dewap.jpg",
        "Футболка Demix": "/static/images/defut.jpg",
        "Насос Demix": "/static/images/denas.jpg",
        # Salomon
        "Ботинка Salomon": "/static/images/salbat.jpg",
        "Шапка Salomon": "/static/images/salwap.jpg",
        "Бандана Salomon": "/static/images/salban.jpg",
        "Носки Salomon": "/static/images/salnos.jpg",
        "Рюкзак Salomon": "/static/images/salsum.jpg",
    }

    image = images.get(selected_item)


    return render(request, "calculator/lab3.html", {
        "brands": brands.keys(),
        "items": items,
        "selected_brand": selected_brand,
        "selected_item": selected_item,
        "image": image
    })

def lab4(request):
    subjects = {
        "Информатика": "Айгүл Тлеуова",
        "Математика": "Бауыржан Сейітов",
        "Физика": "Марат Қасым",
        "Программалау": "Дана Әбдірайым",
        "Алгоритмдер": "Ержан Мұратов",
        "Жасанды интеллект": "Алия Нұржан",
        "Деректер қоры": "Руслан Қалиев",
    }

    selected_subjects = {}
    error = ""
    default_subject = ["Информатика", "Математика"]

    if request.method == "POST":
        if "execute" in request.POST:
            for sub in subjects:
                if sub in request.POST:
                    selected_subjects[sub] = subjects[sub]
            if not selected_subjects:
                error = "-- Пән таңдалмады, кемінде бір пән таңдаңыз! --"
        elif "clear" in request.POST:
            selected_subjects = {}
            error = ""

    #if not selected_subjects and not error and request.method != "POST":
        #for sub in default_subject:
            #selected_subjects[sub] = subjects[sub]

    return render(request, "calculator/lab4.html", {
        "subjects": subjects,
        "selected_subjects": selected_subjects,
        "error": error
    })



import base64

from datetime import datetime
from django.shortcuts import render, redirect

HAIRSTYLES = {
    'Полубокс': 2500,
    'Андеркат': 3000,
    'Нулевка': 2000,
    'Каскад': 3500,
    'Фейд': 3200,
}

MASTERS = {
    'Мария (Новичок)': 1.0,
    'Екатерина (Мастер)': 1.2,
    'Анна (Профессионал)': 1.5,
}

WELCOME_IMG = '/static/images/Добро.jpg'

HAIRSTYLE_IMAGES = {
}


def soj(request):
    cart = request.session.get('cart', [])
    message = ''
    show_receipt = False
    total_sum = 0
    total_sum_label = 'Общая стоимость'
    total_sum1 = 0
    vat_rate = 0.12
    total_no_vat = 0
    vat_amount = 0

    fio = request.POST.get('fio', '') or request.GET.get('fio', '')
    hairstyle = request.POST.get('hairstyle', '') or request.GET.get('hairstyle', '')
    master = request.POST.get('master', '') or request.GET.get('master', '')
    print_check = request.POST.get('print_check')
    new_hairstyle = request.POST.get('hairstyle', '')
    new_master = request.POST.get('master', '')
    selected_index = request.session.get('selected_index', None)


    prev_hairstyle = request.session.get('selected_hairstyle', '')

    if new_hairstyle != prev_hairstyle:
        new_master = ''

    hairstyle = new_hairstyle
    master = new_master

    request.session['selected_hairstyle'] = new_hairstyle

    selected_hairstyle = hairstyle
    selected_master = master
    current_price = 0

    if hairstyle and master:
        base_price = HAIRSTYLES.get(hairstyle, 0)
        coeff = MASTERS.get(master, 1)
        current_price = int(base_price * coeff)
    elif hairstyle:
        current_price = HAIRSTYLES.get(hairstyle, 0)

    action = request.POST.get('action')

    if action == 'add':
        if not fio.strip():
            message = 'Введите ФИО клиента'

        elif not hairstyle:
            message = 'Выберите прическу'

        elif not master:
            message = 'Выберите мастера'

        else:
            base = HAIRSTYLES[hairstyle]
            coeff = MASTERS[master]
            price = int(base * coeff)

            cart.append({'fio': fio.strip(), 'hairstyle': hairstyle, 'master': master, 'price': price})
            request.session['cart'] = cart
            message = 'Добавлено в корзину'
            selected_index = None

    elif action == 'remove':
        idx = int(request.POST.get('index', -1))
        if 0 <= idx < len(cart):
            del cart[idx]
            request.session['cart'] = cart
            message = 'Выбранный заказ удалён'
            selected_index = None
        else:
            message = 'Выберите заказ для удаления'

    elif action == 'clear':
        cart = []
        request.session['cart'] = cart
        message = ''
        fio = ''
        hairstyle = ''
        master = ''
        selected_hairstyle = ''
        selected_master = ''
        current_price = 0
        selected_index = None
        return redirect('soj')

    elif action == 'calculate':
        total_sum1 = sum(i['price'] for i in cart)

        if total_sum1 == 0:
            message = 'Корзина пуста — расчёт невозможен'
            total_sum_label = 'Общая стоимость'
        else:
            vat_rate = 0.12
            total_no_vat = total_sum1 / (1 + vat_rate)
            vat_amount = total_sum1 - total_no_vat
            total_no_vat = round(total_no_vat, 2)
            vat_amount = round(vat_amount, 2)
            total_sum_label = 'Общая стоимость с НДС'

            if print_check:
                show_receipt = True
                message = 'Расчёт выполнен и чек напечатан'
            else:
                show_receipt = False
                message = 'Расчёт выполнен без печати'

    total_sum = sum(i['price'] for i in cart)
    selected_image = HAIRSTYLE_IMAGES.get(selected_hairstyle, WELCOME_IMG) if selected_hairstyle else WELCOME_IMG
    request.session['selected_index'] = selected_index

    context = {
        'vat_rate': int(vat_rate * 100),
        'total_no_vat': total_no_vat,
        'vat_amount': vat_amount,
        'total_sum': round(total_sum, 2),
        'total_sum1': round(total_sum1, 2),

        'hairstyles': HAIRSTYLES,
        'masters': MASTERS,
        'cart': cart,
        'message': message,
        'selected_hairstyle': selected_hairstyle,
        'selected_master': selected_master,
        'current_price': current_price,
        'show_receipt': show_receipt,
        'datetime': datetime.now(),
        'WELCOME_IMG': WELCOME_IMG,
        'selected_image': selected_image,
        'selected_index': selected_index,
        'total_sum_label': total_sum_label,
        'fio': fio,
    }
    return render(request, 'calculator/soj.html', context)










import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
URL = "https://www.technodom.kz/bytovaja-tehnika/uhod-za-domom/pylesosy"
products = []


def parse_pylesosy():

    global products
    products = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    BASE_URL = "https://www.technodom.kz/bytovaja-tehnika/uhod-za-domom/pylesosy"

    MAX_PAGES = 4

    for page in range(1, MAX_PAGES + 1):

        url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"

        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        items = soup.find_all("a", class_="ProductItem_itemLink__cud7j")

        if not items:
            break

        for item in items:
            name_tag = item.find("p", class_="Typography ProductCardH_title__H_Toe ProductCardH_loading__5ljE8 Typography__M")
            name = name_tag.text.strip() if name_tag else ""

            price_tag = item.find("p", {"data-testid": "product-price"})
            price = price_tag.get_text(strip=True) if price_tag else ""

            link = ""
            href = item.get("href", "")
            if href:
                link = "https://www.technodom.kz" + href if not href.startswith("http") else href

            # Brand, SKU, Code
            brand = ""
            sku = ""
            code = ""
            if "pylesos-" in link:
                brand_part = link.split("pylesos-")[1]
                parts = brand_part.split('-')
                if len(parts) >= 2:
                    brand = parts[0].capitalize()
                    code = parts[-1]
                    sku_parts = parts[1:-1]
                    sku = ' '.join([p.capitalize() for p in sku_parts])

            img_tag = item.find("img")
            img_url = ""
            if img_tag:
                img_url = img_tag.get("data-src", "") or img_tag.get("src", "")
                if img_url.startswith("//"):
                    img_url = "https:" + img_url

            products.append({
                "name": name,
                "brand": brand,
                "price": price,
                "sku": sku,
                "code": code,
                "link": link,
                "image": img_url
            })

def export_excel():
    df = pd.DataFrame(products)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output


def lab5_1(request):
    if "run" in request.GET:
        parse_pylesosy()

    if "clear" in request.GET:
        products.clear()

    if "excel" in request.GET:
        file = export_excel()
        response = HttpResponse(
            file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename=\"pylesosy.xlsx\"'
        return response
    return render(request, "calculator/lab5_1.html", {"products": products})


# 5.2
import requests

IranCities = [
    "Tehran", "Mashhad", "Isfahan", "Karaj", "Tabriz",
    "Shiraz", "Qom", "Ahvaz", "Kermanshah", "Urmia",
    "Rasht", "Zahedan", "Kerman", "Yazd", "Ardabil",
    "Hamadan", "Bandar Abbas", "Qazvin", "Sanandaj", "Zanjan"
]

Results = []
Filtered = []
Nom = 0
def lab5_2(request):
    global Results, Filtered, Nom
    City = ""
    Clear = True

    if request.method == "POST":

        if "run" in request.POST:
            Results = []
            Filtered = []
            Nom = 0
            for city in IranCities:
                GetWeather(city)

        elif "task" in request.POST:
            Filtered = []

            for item in Results:
                try:
                    if item['humidity'] > 40 and "rain" in item['desc'].lower():
                        Filtered.append(item)
                except:
                    pass

            if not Filtered:
                Results = [{
                    'nomer': "-",
                    'city': "Табылған жоқ",
                    'temp': "-",
                    'humidity': "-",
                    'desc': "сіз іздеген ауа-райы болып жатқан қала жоқ"
                }]
            else:
                Results = Filtered

        elif "clear" in request.POST:
            Results = []
            Filtered = []
            Nom = 0

    return render(request, 'calculator/lab5_2.html', {
        'results': Results,
    })
def GetWeather(City):
    global Results, Nom

    My_API_Key = "6bab4d6713adbf3a428b1f2a7454395d"
    link1 = "http://api.openweathermap.org/data/2.5/weather?q="
    link2 = "&units=metric&APPID=" + My_API_Key

    link = link1 + City + ",IR" + link2
    data = requests.get(link).json()

    try:
        Temp = data['main']['temp']
        Humidity = data['main']['humidity']
        Desc = data['weather'][0]['description']
    except:
        Temp = "?"
        Humidity = "?"
        Desc = "?"

    Nom += 1
    Info = {
        'nomer': Nom,
        'city': City,
        'temp': Temp,
        'humidity': Humidity,
        'desc': Desc,
    }

    Results.append(Info)
    return Results









from django.shortcuts import render, redirect
import requests, bs4
from django.shortcuts import render, redirect

def lab6(request):
    words = []
    lower_words = []
    saved = False

    step = request.session.get('lab6_step', 1)

    if request.method == 'GET' and 'reset' in request.GET:
        request.session['lab6_step'] = 1
        return redirect('/')

    if request.method == 'POST':

        if request.FILES.get('file') and step == 1:
            uploaded_file = request.FILES['file']
            content = uploaded_file.read().decode('utf-8')
            words = [line.strip() for line in content.splitlines() if line.strip()]
            step = 2

        elif 'convert_to_lower' in request.POST and step == 2:
            try:
                with open("input.txt", 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]

                for line in lines:
                    lower_words.append(line.title())
#swapcase
                step = 3
            except FileNotFoundError:
                words = ["❗ input.txt файлы табылмады!"]

        elif 'save_file' in request.POST and step == 3:
            try:
                with open("input.txt", 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]

                converted_list = [line.title() for line in lines]

                content_lines = []
                content_lines.append("Файлдан оқылған мәліметтер:")
                content_lines.extend(lines)
                content_lines.append("")
                content_lines.append("Кіші әріпке өзгертілген:")
                content_lines.extend(converted_list)

                content = "\n".join(content_lines)

                output_path = r"C:\Users\bakda\PycharmProjects\DjangoProject777\output.txt"
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(content)

                saved = True
                step = 1
                words = []
                lower_words = []

            except Exception as e:
                words = [f"❗ Қате: {str(e)}"]

    request.session['lab6_step'] = step

    context = {
        "words": words,
        "lower_words": lower_words,
        "saved": saved,
        "step": step,
    }
    return render(request, "calculator/lab6.html", context)


def lab7(request):
    brands = ["LG", "Samsung", "Bosch", "Indesit", "Atlant"]
    washer_types = ["Алдыңғы жүктеу", "Үстіңгі жүктеу"]
    colors = ["White", "Black", "Silver"]

    rows = request.session.get("lab7_rows", [])
    errors = []

    #selected_brand = "",  {% if b == selected_brand %}selected{% endif %}
    #selected_washer_type = ""
    #selected_color = ""

    if request.method == "POST":

        if "add_row" in request.POST:
            brand = request.POST.get("brand")
            washer_type = request.POST.get("washer_type")
            capacity = request.POST.get("capacity")
            color = request.POST.get("color")
            price = request.POST.get("price")

            #selected_brand = brand
            #selected_color = color
            #selected_washer_type = washer_type

            if not (brand and washer_type and capacity and color and price):
                errors.append("Барлық мәліметтерді толтырыңыз!")
            else:
                try:
                    c_val = float(capacity)
                    p_val = float(price)
                    rows.append({
                        "no": len(rows) + 1,
                        "brand": brand,
                        "washer_type": washer_type,
                        "capacity": c_val,
                        "color": color,
                        "price": p_val,
                    })
                    request.session["lab7_rows"] = rows
                except:
                    errors.append("Сандарды дұрыс енгізіңіз!")

        elif "clear_all" in request.POST:
            rows = []
            request.session["lab7_rows"] = []

        elif "filter" in request.POST:
            return redirect("lab7_result")

    return render(request, "calculator/lab7.html", {
        "brands": brands,
        "washer_types": washer_types,
        "colors": colors,
        "rows": rows,
        "errors": errors,
        #"selected_brand": selected_brand,
        #"selected_washer_type": selected_washer_type,
        #"selected_color": selected_color,
    })


def lab7_result(request):
    rows = request.session.get("lab7_rows", [])
    filtered = []

    required_type = "Алдыңғы жүктеу"

    for r in rows:
        if (
            120000 <= float(r["price"]) <= 250000 and
            r["washer_type"] == required_type
        ):
            filtered.append(r)

    if request.method == "POST":
        if "clear" in request.POST:
            filtered = []
        elif "exit" in request.POST:
            return redirect("lab7")

    return render(request, "calculator/lab7_result.html", {
        "filtered": filtered,
    })


def lab7_tapsyrma(request):
    return render(request, "calculator/lab7_tapsyrma.html")


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ChatHistory, ClearPoint  # 🔥 ClearPoint-ты импорттаймыз 🔥
from .ai_logic import get_hyundai_ai_response




def chat_view(request):
    # ClearPoint жазбасы бар екеніне көз жеткіземіз, жоқ болса жасаймыз.
    clear_point, created = ClearPoint.objects.get_or_create(pk=1)

    if request.method == 'POST':
        user_input = request.POST.get('message')
        if user_input:
            ai_answer = get_hyundai_ai_response(user_input)

            ChatHistory.objects.create(
                user_query=user_input,
                ai_response=ai_answer
            )
        return redirect('chat_home')

        # 🔥 ФИЛЬТРАЦИЯ: last_cleared уақытынан КЕЙІН жасалған жазбаларды ғана көрсетеміз 🔥
    history = ChatHistory.objects.filter(
        created_at__gte=clear_point.last_cleared
    ).order_by('-created_at')

    return render(request, 'calculator/chat.html', {'history': history})


def clear_history(request):
    """
    "Тарихты тазалау" батырмасы. Деректерді жоймайды, тек ClearPoint уақытын жаңалайды.
    """
    # 🔥 ClearPoint жазбасын тауып, оның уақытын Қазіргі уақытқа жаңартамыз
    clear_point, created = ClearPoint.objects.get_or_create(pk=1)
    clear_point.last_cleared = timezone.now()
    clear_point.save()

    return redirect('chat_home')


def history_view(request):
    """
    Толық Тарих беті. Ешқандай фильтрсіз барлық жазбаларды көрсетеді.
    """
    full_history = ChatHistory.objects.all().order_by('-created_at')[:100]

    return render(request, 'calculator/history_list.html', {'history': full_history})


from django.shortcuts import render, redirect


# ... басқа импорттар

def delete_full_history(request):
    """
    Деректер базасынан барлық ChatHistory жазбаларын толығымен жояды.
    Бұл функция Тарих бетін тазалауға арналған.
    """
    # ChatHistory кестесіндегі барлық жазбаларды жою
    ChatHistory.objects.all().delete()

    # Тазаланғаннан кейін, Тарих бетіне қайта оралу
    return redirect('full_history')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, MenuCategory, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse


def index6(request):
    categories = MenuCategory.objects.all()
    popular = Dish.objects.filter(is_active=True).order_by('-id')[:6]
    return render(request, 'calculator/index6.html', {'categories': categories, 'popular': popular})


def menu_list(request, category_slug=None):
    category = None
    categories = MenuCategory.objects.all()
    dishes = Dish.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(MenuCategory, slug=category_slug)
        dishes = dishes.filter(category=category)
    return render(request, 'calculator/menu.html', {'category': category, 'categories': categories, 'dishes': dishes})


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id, is_active=True)
    form = AddToCartForm(initial={'dish_id': dish.id})
    return render(request, 'calculator/dish_detail.html', {'dish': dish, 'form': form})


def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            dish_id = str(form.cleaned_data['dish_id'])
            qty = form.cleaned_data['quantity']
            cart = request.session.get('cart', {})
            if dish_id in cart:
                cart[dish_id] += qty
            else:
                cart[dish_id] = qty
            request.session['cart'] = cart
            messages.success(request, "Таңдалды: себетке қосылды.")
    return redirect('menu')


from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal



def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0')

    TWO_PLACES = Decimal('.01')

    for dish_id, qty in cart.items():
        dish = get_object_or_404(Dish, id=int(dish_id))

        subtotal = dish.price * qty

        items.append({
            'dish': dish,
            'qty': qty,
            'subtotal': subtotal.quantize(TWO_PLACES),
        })
        total += subtotal

    return render(request, 'calculator/cart.html', {
        'items': items,
        'total': total.quantize(TWO_PLACES),
    })

def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id = str(dish_id)
    if dish_id in cart:
        del cart[dish_id]
        request.session['cart'] = cart
        messages.info(request, "Өлшем жойылды.")
    return redirect('view_cart')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dish, Order, OrderItem


@login_required
def checkout(request):
    # 1. Сессиядан себетті алу
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Себет бос!")
        return redirect('menu')

    # 2. Тапсырысты (Order) базаға сақтау
    total_cost = 0
    # Жалпы соманы есептеу
    for dish_id, quantity in cart.items():
        try:
            dish = Dish.objects.get(id=int(dish_id))
            total_cost += dish.price * quantity
        except Dish.DoesNotExist:
            continue

    # Негізгі тапсырыс нысанын құру
    order = Order.objects.create(
        client=request.user,
        total_cost=total_cost,
        status='new'
    )

    # 3. Тапсырыстың әр тағамын (OrderItem) сақтау
    for dish_id, quantity in cart.items():
        try:
            dish = Dish.objects.get(id=int(dish_id))
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=quantity,
                price=dish.price
            )
        except Dish.DoesNotExist:
            continue

    # 4. Сәтті рәсімделген соң себетті ТАЗАРТУ
    request.session['cart'] = {}
    request.session.modified = True

    # Хабарлама шығару
    messages.success(request, f"Тапсырысыңыз №{order.id} сәтті рәсімделді!")

    # 5. МІНДЕТТІ: "Тапсырыстарым" бетіне бағыттау (redirect)
    # Осы жол болмаса, аппақ бет шыға береді
    return redirect('my_orders')
from django.db.models import Exists, OuterRef


@login_required(login_url='/registration/login/')
def my_orders(request):
    # OrderItem бар екенін тексеретін сүзу. 'items' атауы бұл жерде қажет емес,
    # себебі біз OrderItem моделіне тікелей сұраныс жасаймыз.
    orders = Order.objects.filter(
        # OrderItem.objects.filter(...) дұрыс болғандықтан, бұрынғы синтаксис қатесін ғана түзетеміз.
        Exists(OrderItem.objects.filter(order=OuterRef('pk'))),
        client=request.user
    ).order_by('-created_at')

    return render(request, 'calculator/my_orders.html', {'orders': orders})
@user_passes_test(lambda u: u.is_staff)
def director_dashboard(request):
    total_orders = Order.objects.count()
    total_income = \
        Order.objects.filter(status__in=['ready', 'delivered', 'preparing']).aggregate(total=Sum('total_cost'))[
            'total'] or 0
    popular_dishes = Dish.objects.annotate(num_orders=Count('orderitem')).order_by('-num_orders')[:5]

    all_orders = Order.objects.all().order_by('-created_at')

    context = {
        'total_orders': total_orders,
        'total_income': total_income,
        'popular_dishes': popular_dishes,
        'all_orders': all_orders,
    }
    return render(request, 'calculator/director_dashboard.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # тіркелген соң автоматты кіру
            messages.success(request, "Тіркелу сәтті өтті! Қош келдіңіз.")
            return redirect('index6')  # басты бетке бағыттаймыз
        else:
            messages.error(request, "Қате! Форманы дұрыс толтырыңыз.")
    else:
        form = UserCreationForm()

    return render(request, 'calculator/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('index6')

        else:
            return render(request, 'calculator/login.html', {'error': 'Логин немесе пароль қате'})

    return render(request, 'calculator/login.html')
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('/calculator/login/')
    return render(request, 'calculator/register.html')


def profile_view(request):
    return render(request, 'calculator/profile.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            profile_instance = request.user.profile
        except:
            profile_form = None
        else:
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=profile_instance
            )

        if user_form.is_valid() and (not profile_form or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                user_form.save()
                profile_form.save()
            messages.success(request, "Профиль сәтті жаңартылды.")
            return redirect('profile')  # қайта жүктеу
        else:
            messages.error(request, "Профильді жаңартуда қате шықты.")

    else:
        user_form = UserUpdateForm(instance=request.user)
        try:
            profile_form = ProfileUpdateForm(instance=request.user.profile)
        except:
            profile_form = None

    return render(request, 'calculator/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def quick_add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    qty = 1

    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)

    if dish_id_str in cart:
        cart[dish_id_str] += qty
    else:
        cart[dish_id_str] = qty

    request.session['cart'] = cart

    messages.success(request, f"{dish.name} (1 дана) себетке қосылды.")
    return redirect('menu')



@user_passes_test(lambda u: u.is_staff)
def change_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    valid_statuses = ['processing', 'delivered', 'canceled']

    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        messages.success(request, f"Тапсырыс №{order_id} статусы сәтті өзгертілді: {order.get_status_display()}")
    else:
        messages.error(request, "Қате: Жарамсыз статус.")

    return redirect('director_dashboard')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from decimal import Decimal



@require_POST
def change_cart_item_quantity(request):
    if not request.user.is_authenticated:
        messages.error(request, "Себетті өзгерту үшін тіркелу қажет.")
        return redirect('view_cart')

    try:
        dish_id = str(request.POST.get('dish_id'))
        action = request.POST.get('action')

        cart = request.session.get('cart', {})

        if dish_id in cart:
            qty = cart[dish_id]

            if action == 'add':
                new_qty = qty + 1
            elif action == 'remove':
                new_qty = qty - 1
            else:
                messages.error(request, "Жарамсыз әрекет.")
                return redirect('view_cart')

            if new_qty > 0:
                cart[dish_id] = new_qty
            else:
                del cart[dish_id]

            request.session['cart'] = cart
            request.session.modified = True
            return redirect('view_cart')

        messages.error(request, "Элемент себетте жоқ.")
        return redirect('view_cart')

    except Exception as e:
        messages.error(request, f"Қате: {e}")
        return redirect('view_cart')