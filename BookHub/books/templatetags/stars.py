from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='stars')
def stars(value):
    value=list(value)
    
    if(len(value)==0):
        average=0
    else:
        average = sum(value) // len(value)
    startag=''

    for i in range(average):
        startag += '<span class="fa fa-star checked"></span>\n'

    for j in range(5 - average):
        startag += '<span class="fa fa-star"></span>\n'
    startag += '<p>' + str(average) + ' average based on ' + str(len(value)) + ' reviews.</p>'
    return format_html(startag) 

@register.filter(name='barchart')
def chart(value):
    value=list(value)
    ratingBarchart=''
    for i in range(5,0,-1):
        count = value.count(i)
        if(len(value)==0):
            avg=0
        else:
            avg=(count/len(value))*100
        ratingBarchart+='<div class="side">\
            <div>{2} star</div>\
        </div>\
        <div class="middle">\
            <div class="bar-container">\
                <div class="bar-5" style="width: {0}%; height: 18px; background-color: #04AA6D;"></div>\
            </div>\
        </div>\
        <div class="side right">\
            <div>{1}</div>\
        </div>'.format(3 if avg == 0 else avg,count,i)
    return format_html(ratingBarchart)

@register.filter(name='rating')
def stars(value):
    startag=''

    for i in range(value):
        startag += '<span class="fa fa-star checked"></span>\n'

    for j in range(5 - value):
        startag += '<span class="fa fa-star"></span>\n'
    return format_html(startag)