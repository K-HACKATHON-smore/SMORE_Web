from django.shortcuts import render, redirect, get_object_or_404
from account.models import User
from django.utils import timezone
from smore.models import Item, ItemImage
from smore.models import ExperRec
from collections import OrderedDict
from .fusioncharts import FusionCharts
from django.http import HttpResponse
from .models import *


# Create your views here.
def home(request):
    items = Item.objects.all()
    itemImage = ItemImage.objects.all().first()
    return render(request, 'home.html',{'items':items, 'image':itemImage})

def create(request):
    if request.method == "POST" :
        new_item = Item()
        new_item.item_name = request.POST['item_name']
        new_item.body = request.POST['body']
        new_item.pub_date = timezone.datetime.now()

        user_id = request.user.id

        user = User.objects.get(id = user_id)

        new_item.author = user

        new_item.save()
        for img in request.FILES.getlist('image'):
            image = ItemImage()
            image.itemFK = new_item
            image.image = img
            image.save()
        return redirect('home')

    else :
        return render(request,'new.html')

def detail(request, id):
    item = get_object_or_404(Item, pk = id)
    itemImage = ItemImage.objects.all().filter(itemFK = id)
    return render(request, 'detail.html', {'item':item, 'image':itemImage})

def edit(request, id):
    if request.method == "POST":
        edit_item = Item.objects.get(id = id)
        edit_item.item_name = request.POST["item_name"]
        edit_item.body = request.POST["body"]
        edit_item.save()
        delete_img = ItemImage.objects.all().filter(itemFK = id)
        delete_img.delete()
        for img in request.FILES.getlist('image'):
            image = ItemImage()
            image.itemFK = edit_item
            image.image = img
            image.save()
        
        return redirect('detail', edit_item.id)
    else:
        item = Item.objects.get(id = id)
        return render(request, 'edit.html', {'item': item})

def delete(request, id):
    delete_item = Item.objects.get(id = id)
    delete_item.delete()
    return redirect('home')

def experience(request):
    expers = ExperRec.objects.all()
    return render(request, 'experience.html',{'expers':expers})

def exper_create(request):
    if request.method == "POST" :
        new_exper = ExperRec()
        new_exper.exper_title = request.POST['exper_title']
        new_exper.exper_body = request.POST['exper_body']
        new_exper.exper_period = request.POST['exper_period']
        new_exper.exper_pub_date = timezone.datetime.now()
        new_exper.exper_image=request.FILES['exper_image']

        user_id = request.user.id

        user = User.objects.get(id = user_id)

        new_exper.exper_author = user

        new_exper.save()
        return redirect('experience')

    else :
        return render(request,'exper_create.html')
        
def exper_detail(request, id):
    exper = get_object_or_404(ExperRec, pk = id)
    return render(request, 'exper_detail.html', {'exper':exper})

def exper_edit(request, id):
    if request.method == "POST":
        edit_exper = ExperRec.objects.get(id = id)
        edit_exper.exper_title = request.POST["exper_title"]
        edit_exper.exper_body = request.POST["exper_body"]
        edit_exper.exper_image=request.FILES['exper_image']

        edit_exper.save()
        return redirect('detail', edit_exper.id)
    else:
        exper = ExperRec.objects.get(id = id)
        return render(request, 'exper_edit.html', {'exper': exper})

def exper_delete(request, id):
    delete_exper = ExperRec.objects.get(id = id)
    delete_exper.delete()
    return redirect('experience')

def com_chart(request):
    dataSource = OrderedDict()
    dataSource2 = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "[2021] ?????? ?????? ??????"
    chartConfig["subCaption"] = "2021?????? ??????"
    chartConfig["xAxisName"] = "??????"
    chartConfig["yAxisName"] = "?????? ?????????"
    chartConfig["numberSuffix"] = "??????"
    chartConfig["theme"] = "fusion"
    chartConfig["palettecolors"] = "e4dbb2"
    chartConfig2 = OrderedDict()
    chartConfig2["caption"] = "[2020] ?????? ?????? ??????"
    chartConfig2["subCaption"] = "2020?????? ??????"
    chartConfig2["xAxisName"] = "??????"
    chartConfig2["yAxisName"] = "?????? ?????????"
    chartConfig2["numberSuffix"] = "??????"
    chartConfig2["theme"] = "fusion"
    chartConfig2["palettecolors"] = "e4dbb2"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["1???"] = 1205
    chartData["2???"] = 936
    chartData["3???"] = 1249
    chartData["4???"] = 1347
    chartData["5???"] = 1572
    chartData["6???"] = 932
    chartData["7???"] = 1134
    chartData["8???"] = 1536
    chartData["9???"] = 1357
    chartData["10???"] = 898
    chartData["11???"] = 1428
    chartData["12???"] = 1333

    chartData2 = OrderedDict()
    chartData2["1???"] = 1506
    chartData2["2???"] = 1496
    chartData2["3???"] = 1557
    chartData2["4???"] = 898
    chartData2["5???"] = 1472
    chartData2["6???"] = 1921
    chartData2["7???"] = 1884
    chartData2["8???"] = 972
    chartData2["9???"] = 1175
    chartData2["10???"] = 1423
    chartData2["11???"] = 1478
    chartData2["12???"] = 1249

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    dataSource2["chart"] = chartConfig2
    dataSource2["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)

    for key, value in chartData2.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource2["data"].append(data)



    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1"  , "650", "340", "chart-1", "json", dataSource)
    column2D2 = FusionCharts("column2d", "ex2"  , "650", "340", "chart-3", "json", dataSource2)

    chartObj = FusionCharts( 'bar2d', 'ex3', '650', '340', 'chart-4', 'json', """{
  "chart": {
    "caption": "?????? ?????? ??????",
    "yaxisname": "?????? ??????",
    "paletteColors": "#e4dbb2,#cfc183",
    "aligncaptionwithcanvas": "0",
    "plottooltext": "<b>$label</b> ??? <b>$dataValue</b> ??? ?????????",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "?????????????????? ???????????????",
      "value": "41"
    },
    {
      "label": "????????? ?????????",
      "value": "39"
    },
    {
      "label": "?????? ?????? ??????",
      "value": "38"
    },
    {
      "label": "?????? ?????? ??????",
      "value": "32"
    },
    {
      "label": "????????? ?????????",
      "value": "26"
    },
    {
      "label": "????????? ?????? ??? ???????????????",
      "value": "25"
    },
    {
      "label": "????????? ??????????????? ?????? ??????(??????)",
      "value": "20"
    },
  ]
}""")
    chartObj2 = FusionCharts( 'doughnut2d', 'ex5', '650', '350', 'chart-5', 'json', """{
  "chart": {
    "caption": "????????? ?????????",
    "subcaption": "2021??? ????????? ??????",
    "showpercentvalues": "1",
    "defaultcenterlabel": "????????? ??????  ",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    "plottooltext": "???????????? <b>$percentValue</b>??? <b>$label</b>?????????",
    "centerlabel": "<b>$label</b>: $value",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "20??? ??????",
      "value": "10000",
    },
    {
      "label": "20??? ??????",
      "value": "5300"
    },
    {
      "label": "30??? ??????",
      "value": "10500"
    },
    {
      "label": "30??? ??????",
      "value": "18900"
    },
    {
      "label": "??? ???",
      "value": "4000"
    }
  ]
}""")
    chartObj3 = FusionCharts( 'doughnut2d', 'ex6', '650', '350', 'chart-6', 'json', """{
  "chart": {
    "caption": "????????? ??????",
    "subcaption": "2021??? ????????? ??????",
    "showpercentvalues": "1",
    "defaultcenterlabel": "??????",
    "aligncaptionwithcanvas": "0",
    "captionpadding": "0",
    "decimals": "1",
    "plottooltext": " ???????????? <b>$percentValue</b>??? <b>$label</b>?????????.",
    "centerlabel": "<b>$label</b>: $value",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "??????",
      "value": "2100"
    },
    {
      "label": "??????",
      "value": "3200"
    }
  ]
}""")
    chartObj4 = FusionCharts( 'line', 'ex7', '650', '350', 'chart-7', 'json', """{
  "chart": {
    "caption": "????????? ???",
    "yaxisname": "???",
    "paletteColors": "#cfc183",
    "subcaption": "[2016-2021]",
    "numbersuffix": " ???",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "2016",
      "value": "89"
    },
    {
      "label": "2017",
      "value": "1452"
    },
    {
      "label": "2018",
      "value": "6740"
    },
    {
      "label": "2019",
      "value": "20453"
    },
    {
      "label": "2020",
      "value": "64201"
    },
    {
      "label": "2021",
      "value": "80132"
    }
  ]
}""")
    return  render(request, 'com_chart.html', {'output' : column2D.render(), 'output2':column2D2.render(), 'output3': chartObj.render(), 'output4': chartObj2.render(),'output5': chartObj3.render(),'output6': chartObj4.render(),'chartTitle': '?????? ?????? ?????????', 'chartTitle2': '?????? ?????? ?????????2'})

def product_chart(request):

  # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
   dataSource = OrderedDict() 
   # The `chartConfig` dict contains key-value pairs data for chart attribute
   chartConfig = OrderedDict()
   chartConfig["caption"] = "?????? ?????? ??????"
   chartConfig["subCaption"] = ""
   chartConfig["xAxisName"] = "month"
   chartConfig["yAxisName"] = "?????? ??????(??????)"
   chartConfig["numberSuffix"] = ""
   chartConfig["theme"] = "fusion"  
   chartConfig["palettecolors"] = "e4dbb2"
   # The `chartData` dict contains key-value pairs data
   chartData = OrderedDict()
   chartData["Jan"] = 290
   chartData["Feb"] = 260
   chartData["Mar"] = 180
   chartData["Apr"] = 140
   chartData["May"] = 115
   chartData["Jun"] = 100
   chartData["Jul"] = 30
   chartData["Aug"] = 30
   chartData["Sep"] = 30
   chartData["Oct"] = 300
   chartData["Nov"] = 450
   chartData["Dec"] = 30  
   dataSource["chart"] = chartConfig
   dataSource["data"] = []  
   # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
   # The data for the chart should be in an array wherein each element of the array is a JSON object
   # having the `label` and `value` as keys.  
   # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
   for key, value in chartData.items():
       data = {}
       data["label"] = key
       data["value"] = value
       dataSource["data"].append(data)  
   # Create an object for the column 2D chart using the FusionCharts class constructor
   # The chart data is passed to the `dataSource` parameter.

   column2D = FusionCharts("column2d", "ex1"  , "610", "340", "chart-1", "json", dataSource)
  # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
   dataSource = OrderedDict() 
   # The `chartConfig` dict contains key-value pairs data for chart attribute
   chartConfig = OrderedDict()
   chartConfig["caption"] = "?????? ?????? ??????"
   chartConfig["subCaption"] = ""
   chartConfig["xAxisName"] = "month"
   chartConfig["yAxisName"] = "?????? ??????(??????)"
   chartConfig["numberSuffix"] = ""
   chartConfig["theme"] = "fusion"  
  #  chartConfig["bgcolor"] = "263812"  
   chartConfig["palettecolors"] = "d6c98d"
   # The `chartData` dict contains key-value pairs data
   chartData = OrderedDict()
   chartData["Jan"] = 320
   chartData["Feb"] = 270
   chartData["Mar"] = 120
   chartData["Apr"] = 180
   chartData["May"] = 175
   chartData["Jun"] = 134
   chartData["Jul"] = 214
   chartData["Aug"] = 142
   chartData["Sep"] = 97
   chartData["Oct"] = 214
   chartData["Nov"] = 351
   chartData["Dec"] = 227  
   dataSource["chart"] = chartConfig
   dataSource["data"] = []  
   # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
   # The data for the chart should be in an array wherein each element of the array is a JSON object
   # having the `label` and `value` as keys.  
   # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
   for key, value in chartData.items():
       data = {}
       data["label"] = key
       data["value"] = value
       dataSource["data"].append(data)  
   # Create an object for the column 2D chart using the FusionCharts class constructor
   # The chart data is passed to the `dataSource` parameter.

   column2D2 = FusionCharts("column2d", "ex6"  , "610", "340", "chart-6", "json", dataSource) 
   chartObj = FusionCharts( 'pie2d', 'ex2', '300', '300', 'chart-2', 'json', """{
  "chart": {
    "caption": "????????? ????????????",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion",
  },
"data": [{
    "label": "??????",
    "value": "60"
}, {
    "label": "??????",
    "value": "40"
}]
}""")
   chartObj2 = FusionCharts( 'pie2d', 'ex3', '300', '300', 'chart-3', 'json', """{
  "chart": {
    "caption": "????????? ????????????",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion",
  },
"data": [{
    "label": "??????",
    "value": "80"
}, {
    "label": "??????",
    "value": "20"
}]
}""")
   chartObj3 = FusionCharts( 'pie2d', 'ex4', '300', '300', 'chart-4', 'json', """{
  "chart": {
    "caption": "????????? ?????????",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion"
  },
"data": [{
    "label": "10???",
    "value": "30"
}, {
    "label": "20???",
    "value": "40"
}, {
    "label": "30???",
    "value": "20"
}, {
    "label": "40???",
    "value": "7"
},{
    "label": "50?????????",
    "value": "3"
}]
}""")
   chartObj4 = FusionCharts( 'pie2d', 'ex5', '300', '300', 'chart-5', 'json', """{
  "chart": {
    "caption": "????????? ?????????",
    "plottooltext": "$label, <b>$percentValue</b> ",
    "numberPrefix": "",
    "showPercentInTooltip": "0",
    "decimals": "1",
    "useDataPlotColorForLabels": "1",
    "theme": "fusion"
  },
"data": [{
    "label": "10???",
    "value": "20"
}, {
    "label": "20???",
    "value": "35"
}, {
    "label": "30???",
    "value": "20"
}, {
    "label": "40???",
    "value": "17"
},{
    "label": "50?????????",
    "value": "8"
}]
}""")
   return  render(request, 'product_chart.html', {'output' : column2D.render(),'output2' :  chartObj.render(),'output3' :  chartObj2.render(),'output4' :  chartObj3.render(),'output5' :  chartObj4.render(),'output6' : column2D2.render(),}) 
   
def main_chart(request):
  dataSource = OrderedDict()

  chartConfig = OrderedDict()
  chartConfig["caption"] = "[2021] ?????? ?????? ??????"
  chartConfig["subCaption"] = "2021?????? ??????"
  chartConfig["xAxisName"] = "??????"
  chartConfig["yAxisName"] = "?????? ?????????"
  chartConfig["numberSuffix"] = "??????"
  chartConfig["theme"] = "fusion"
  chartConfig["palettecolors"] = "e4dbb2"

  chartData = OrderedDict()
  chartData["1???"] = 1620
  chartData["2???"] = 980
  chartData["3???"] = 1239
  chartData["4???"] = 1634
  chartData["5???"] = 1957
  chartData["6???"] = 932
  chartData["7???"] = 1153
  chartData["8???"] = 1573
  chartData["9???"] = 0
  chartData["10???"] = 0
  chartData["11???"] = 0
  chartData["12???"] = 0
  dataSource["chart"] = chartConfig
  dataSource["data"] = []

  for key, value in chartData.items():
      data = {}
      data["label"] = key
      data["value"] = value
      dataSource["data"].append(data)
  column2D = FusionCharts("column2d", "ex1" , "650", "340", "chart-1", "json", dataSource)
  chartObj = FusionCharts( 'line', 'ex2', '650', '340', 'chart-2', 'json', """{
  "chart": {
    "caption": "?????? 10?????? ?????? ??????",
    "yaxisname": "??????",
    "subcaption": "07.27 ~ 08.06",
    "numbersuffix": " ??????",
    "paletteColors": "#cfc183,#cca356",
    "rotatelabels": "1",
    "setadaptiveymin": "1",
    "theme": "fusion"
  },
  "data": [
    {
      "label": "07.27",
      "value": "12229"
    },
    {
      "label": "07.28",
      "value": "8249"
    },
    {
      "label": "07.29",
      "value": "9245"
    },
    {
      "label": "07.30",
      "value": "15584"
    },
    {
      "label": "07.31",
      "value": "18529"
    },
    {
      "label": "08.01",
      "value": "14289"
    },
    {
      "label": "08.02",
      "value": "19562"
    },
    {
      "label": "08.03",
      "value": "16240"
    },
    {
      "label": "08.04",
      "value": "24153"
    },
    {
      "label": "08.05",
      "value": "24091"
    },
    {
      "label": "08.06",
      "value": "31032"
    }
  ]
}""")
  chartObj2 = FusionCharts( 'doughnut2d', 'ex3', '600', '400', 'chart-3', 'json', """{
    "chart": {
      "caption": "???????????? ?????? ????????????",
      "subcaption": "2021??? ?????????",
      "showpercentvalues": "1",
      "defaultcenterlabel": "????????? ??????",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "????????? ????????? <b>$percentValue</b>??? <b>$label</b>?????????",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "#?????????",
        "value": "10000"
      },
      {
        "label": "#???????????????",
        "value": "5300"
      },
      {
        "label": "#?????????",
        "value": "10500"
      },
      {
        "label": "#????????????",
        "value": "8900"
      },
      {
        "label": "??? ???",
        "value": "4000"
      }
    ]
  }""")
  
  chartObj3 = FusionCharts( 'msline', 'ex4', '650', '340', 'chart-4', 'json', """{
  "chart": {
    "caption": "????????? ?????? ??? ??? ????????? ???",
    "yaxisname": "???",
    "subcaption": "08.01 ~ 08.06",
    "showhovereffect": "1",
    "numbersuffix": "???",
    "paletteColors": "#cfc183,#cca356",
    "drawcrossline": "1",
    "plottooltext": "$seriesName : <b>$dataValue</b>",
    "theme": "fusion"
  },
  "categories": [
    {
      "category": [
        {
          "label": "08.01"
        },
        {
          "label": "08.02"
        },
        {
          "label": "08.03"
        },
        {
          "label": "08.04"
        },
        {
          "label": "08.05"
        },
        {
          "label": "08.06"
        }
      ]
    }
  ],
  "dataset": [
    {
      "seriesname": "????????? ?????? ???",
      "data": [
        {
          "value": "12"
        },
        {
          "value": "24"
        },
        {
          "value": "16"
        },
        {
          "value": "14"
        },
        {
          "value": "20"
        },
        {
          "value": "17"
        }
      ]
    },
    {
      "seriesname": "????????? ???",
      "data": [
        {
          "value": "160"
        },
        {
          "value": "128"
        },
        {
          "value": "134"
        },
        {
          "value": "142"
        },
        {
          "value": "154"
        },
        {
          "value": "111"
        }
      ]
    }
  ]
}""")
  return render(request, 'main_chart.html', {'output' : column2D.render(), 'output2': chartObj.render(), 'output3': chartObj2.render(),'output4': chartObj3.render()})

def research_chart(request):
    chartObj = FusionCharts( 'bar2d', 'ex1','610', '340', 'chart-1', 'json', """{
    "chart": {
      "caption": "?????? ????????? ????????? ??????",
      "yaxisname": "?????? ??????",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "????????? ???????????? ????????? ?????????",
        "value": (31/100)*100
      },
      {
        "label": "???????????? ?????? ?????????????????????",
        "value": "12"
      },
      {
        "label": "???????????? ????????? ?????????",
        "value": "41"
      },
      {
        "label": "SNS ????????? ?????????",
        "value": "31"
      },
      {
        "label": "??? ???",
        "value": "31"
      }
    ]
  }""")
    chartObj2 = FusionCharts( 'bar2d', 'ex2', '610', '340', 'chart-2', 'json', """{
    "chart": {
      "caption": "?????? ????????? ??????",
      "yaxisname": "?????? ??????",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "????????? ?????????(?????????)",
        "value": (31/100)*100
      },
      {
        "label": "?????? ?????????",
        "value": "12"
      },
      {
        "label": "?????? ??????",
        "value": "41"
      },
      {
        "label": "?????? ??????",
        "value": "31"
      },
      {
        "label": "??? ???",
        "value": "31"
      }
    ]
  }""")
    chartObj3 = FusionCharts( 'bar2d', 'ex3',  '610', '340', 'chart-3', 'json', """{
    "chart": {
      "caption": "?????? ????????? ?????????",
      "yaxisname": "?????? ??????",
      "aligncaptionwithcanvas": "0",
      "plottooltext": "<b>$dataValue</b> %",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "?????? ???????????? ????????? ???????????? ??????",
        "value": (31/100)*100
      },
      {
        "label": "????????? ?????? ??????",
        "value": "12"
      },
      {
        "label": "??????????????? ????????? ?????????",
        "value": "41"
      },
      {
        "label": "?????? ????????? ?????????",
        "value": "31"
      },
      {
        "label": "??? ???",
        "value": "31"
      }
    ]
  }""")
    chartObj4 = FusionCharts( 'doughnut2d', 'ex4', '600', '400', 'chart-4', 'json', """{
    "chart": {
      "caption": "3?????? ?????? ??? ?????? ??????",
      "subcaption": "?????? ??????",
      "showpercentvalues": "1",
      "defaultcenterlabel": "????????? ??????",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "????????? <b>$percentValue</b>??? ?????? ????????? <b>$label</b> ????????? ???????????????.",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "1??? ??????",
        "value": "10400"
      },
      {
        "label": "2??? ??????",
        "value": "5300"
      },
      {
        "label": "3??? ??????",
        "value": "10500"
      }
    ]
  }""")
    chartObj5 = FusionCharts( 'doughnut2d', 'ex5', '600', '400', 'chart-5', 'json', """{
    "chart": {
      "caption": "?????? ????????? ????????? ??? ?????? ????????????",
      "subcaption": "?????? ??????",
      "showpercentvalues": "1",
      "defaultcenterlabel": "????????? ??????",
      "aligncaptionwithcanvas": "0",
      "captionpadding": "0",
      "decimals": "1",
      "plottooltext": "????????? <b>$percentValue</b>??? ?????? ??????????????? <b>$label</b> ????????? ???????????????.",
      "centerlabel": "<b>$label</b>: $value",
      "theme": "fusion"
    },
    "data": [
      {
        "label": "#???????????????",
        "value": "10400"
      },
      {
        "label": "#????????????",
        "value": "5300"
      },
      {
        "label": "#?????????_?????????",
        "value": "10500"
      },
      {
        "label": "#????????????",
        "value": "10500"
      },
      {
        "label": "#?????????_??????",
        "value": "10500"
      },
      {
        "label": "#??????_??????",
        "value": "10500"
      }
    ]
  }""")
    return render(request, 'research_chart.html',{'output' : chartObj.render(),'output2' : chartObj2.render(),'output3' : chartObj3.render(),'output4' : chartObj4.render(),'output5' : chartObj5.render()})