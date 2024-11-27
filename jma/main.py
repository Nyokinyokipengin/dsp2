import flet as ft
import requests
import json
import os

def main(page: ft.Page):

    def get_forecast(e):
        area_code = dropdown.value
        if area_code:
            response = requests.get(f'https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json')
            if response.status_code == 200:
                forecast_data = response.json()
                display_forecast(forecast_data)
            else:
                output.value = f"Error: {response.status_code}"
                page.update()

    def display_forecast(data):
        page.controls.clear()
        
        for entry in data:
            publishing_office = entry.get("publishingOffice", "不明")
            report_datetime = entry.get("reportDatetime", "不明")
            
            title = ft.Text(f"{publishing_office} {report_datetime}")
            page.controls.append(title)
            
            for time_series in entry.get("timeSeries", []):
                time_defines = time_series.get("timeDefines", [])
                for area in time_series.get("areas", []):
                    area_name = area.get("area", {}).get("name", "不明")
                    weather = area.get("weathers", ["情報なし"])[0]
                    wind = area.get("winds", ["情報なし"])[0]
                    wave = area.get("waves", ["情報なし"])[0] if "waves" in area else "情報なし"
                    pops = area.get("pops", ["情報なし"])[0] if "pops" in area else "情報なし"
                    temps = area.get("temps", ["情報なし"])[0] if "temps" in area else "情報なし"

                    weather_text = ft.Text(f"地域: {area_name}")
                    weather_detail_text = ft.Text(f"天気: {weather}, 風向: {wind}, 波: {wave}, 降水確率: {pops}, 気温: {temps}")
                    
                    page.controls.append(weather_text)
                    page.controls.append(weather_detail_text)

        page.update()

    # areas.jsonファイルを読み込む
    with open('jma/areas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # デバッグ用にデータをログ出力
    print("Loaded JSON data:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # ドロップダウンオプションのためのリスト
    area_options = []

    # 各セクション("centers", "offices", "class10s", "class15s", "class20s")のデータを追加
    for section in ["centers", "offices", "class10s", "class15s", "class20s"]:
        if section in data:
            print(f"Processing section: {section}")  # Debug: section processing
            for key, value in data[section].items():
                print(f"Processing key: {key}")  # Debug: key processing
                # 各地域の辞書情報からnameを取得
                area_name = value.get("name", "")
                print(f"Found name: {area_name}")  # Debug: name found
                if area_name:  # nameが存在する場合のみ追加
                    area_options.append(ft.dropdown.Option(text=area_name, key=key))

    print(f"Total options: {len(area_options)}")  # Debug: total options

    dropdown = ft.Dropdown(
        options=area_options,
        width=300,
        on_change=get_forecast
    )

    output = ft.Text()

    page.add(ft.Column([
        ft.Text("地域を選択してください："),
        dropdown,
        output
    ]))

ft.app(target=main)