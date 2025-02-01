from django.shortcuts import render


def calculate_bmi(weight, height):
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "text-blue-400"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "text-blue-600"
    elif 25 <= bmi < 30:
        return "Overweight", "text-blue-700"
    else:
        return "Obese", "text-blue-800"

def bmi_calculator(request):
    result = None

    if request.method == 'POST':
        try:
            weight = float(request.POST.get('weight'))
            height = float(request.POST.get('height'))
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender')

            bmi = calculate_bmi(weight, height)
            category, color_class = get_bmi_category(bmi)

            result = {
                'bmi': bmi,
                'category': category,
                'color_class': color_class,
                'weight': weight,
                'height': height,
                'age': age,
                'gender': gender
            }
        except (ValueError, TypeError):
            result = {'error': 'Please enter valid numbers'}

    return render(request, 'bmi_calculator.html', {'result': result})
# Create your views here.
