from django.shortcuts import render
from .myform import CalcForm
import math 
from django.http import JsonResponse

# Create your views here.
def f0_calc_view(request): 
    return render (request,'f0/f0.html')

def correction_factor(re_val): 
    if re_val < 4000 : 
        return 0.5
    elif re_val >= 10000 : 
        return 0.8333
    else : 
        return 0.0336*math.log10(re_val)+0.662


def f0_calculation(request): 
    tref = 121.1
    if request.method == 'POST': 
        form = CalcForm(request.POST)
        radio_choice = request.POST.get('radio_calc')
        form.fields.pop(radio_choice)
        if radio_choice == 'f0_val' : 
            if form.is_valid() : 
                z_val = form.cleaned_data['z_val']
                temp_val = form.cleaned_data['temp_val']
                t_val = form.cleaned_data['t_val']
                re_val = form.cleaned_data['re_val']
                corr = correction_factor(re_val)
                f0_val = (t_val/60)/(math.pow(10,(tref-temp_val)/z_val))
                f0_val_corr = (corr*(t_val/60))/((math.pow(10,(tref-temp_val)/z_val)))
                f0_val = round(f0_val,2)
                f0_val_corr = round(f0_val_corr,2)
                return JsonResponse({
                'result':f0_val, 
                'result_corr':f0_val_corr,
                'name': 'F0',
                'unit':'(in minutes)'
                })
            else :  
                # ºC
                return JsonResponse({'error_1':'invalid_input'})
        elif radio_choice == 't_val':
            if form.is_valid() : 
                z_val = form.cleaned_data['z_val']
                temp_val = form.cleaned_data['temp_val']
                f0_val = form.cleaned_data['f0_val']
                re_val = form.cleaned_data['re_val']
                corr = correction_factor(re_val)
                t_val = f0_val * ((math.pow(10,(tref-temp_val)/z_val)))
                t_val_corr = (f0_val * ((math.pow(10,(tref-temp_val)/z_val))))/corr
                t_val = round(t_val * 60,2)
                t_val_corr = round(t_val_corr*60,2)
                return JsonResponse({
                'result':t_val, 
                'result_corr':t_val_corr,
                'name': 'Sterilization Time',
                'unit':'(in seconds)'
                })
            else : 
                return JsonResponse({'error_1':'invalid_input'})
        else : 
            if form.is_valid() : 
                z_val = form.cleaned_data['z_val']
                t_val = form.cleaned_data['t_val']
                f0_val = form.cleaned_data['f0_val']
                re_val = form.cleaned_data['re_val']
                corr = correction_factor(re_val)
                temp_val = -1 * (math.log10((t_val/60)/f0_val) * z_val - tref)
                temp_val_corr = -1 * (math.log10((corr*t_val/60)/f0_val) * z_val - tref)
                temp_val = round(temp_val,2)
                temp_val_corr = round(temp_val_corr,2)
                return JsonResponse({
                'result':temp_val, 
                'result_corr':temp_val_corr,
                'name': 'Sterilization Temperature',
                'unit':'(in ºC)'
                })
            else : 
                return JsonResponse({'error_1':'invalid_input'})


                


        