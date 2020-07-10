from django.shortcuts import render
import pandas as pd

path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
# json file with all countries
df = pd.read_json("https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json")

def index(request):
    data = pd.read_csv(path)
    grouped = data[['Country/Region', data.columns[-1]]].groupby('Country/Region').sum().reset_index()
    grouped.columns = ['Country/Region', 'cases']
    grouped.sort_values(by='cases', ascending=False, inplace=True)
    countries = grouped['Country/Region'].values.tolist()
    cases = grouped['cases'].values.tolist()
    dataForMap = mapDataCal(grouped, countries)
    total = sum(cases)
    context = {
        'countries': countries,
        'cases': cases,
        'total': total,
        'dataForMap': dataForMap
    }

    return render(request=request, template_name='index.html', context=context)


def mapDataCal(grouped, countries):
    dataList = []
    for i in countries:
        temp = {}
        try:
            tempdf = df[df["name"] == i]
            # get current record on df and change value with cases
            temp["code3"] = list(tempdf["code3"].values)[0]
            temp["name"] = i
            temp["value"] = grouped[grouped['Country/Region'] == i].cases.to_list()[0]
            temp["code"] = list(tempdf["code"].values)[0]
        except Exception as e:
            pass
        dataList.append(temp)

    return dataList