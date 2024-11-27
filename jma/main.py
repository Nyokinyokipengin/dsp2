import flet as ft
import requests
import json
import os

def main(page: ft.Page):

    def get_forecast(e):
        area_code = dropdown.value
        if area_code:
            response = requests.get(f'https://www.jma.go.jp/bosai/forecast/data/forecast/' + area_code + '.json')
            if response.status_code == 200:
                forecast_data = response.json()
                # 取得したデータを表示する
                output.value = json.dumps(forecast_data, indent=2, ensure_ascii=False)
                page.update()
            else:
                output.value = f"Error: {response.status_code}"
                page.update()

    # areas.jsonファイルを読み込む
    with open('jma/areas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ドロップダウンオプションのためのリスト
    area_options = []

    # デバイス情報を取得
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