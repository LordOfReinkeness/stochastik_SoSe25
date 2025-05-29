def extract_csv_data(file_path, field_name):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # print(reader.fieldnames)
        data = [row[field_name] for row in reader if row[field_name]]
    return data

# CSV-Datei laden (ersetze 'daten.csv' durch den tatsächlichen Dateipfad)
csv_file = './data/Fahrraeder_taeglich.csv'
# csv_file = 'data.csv'
raeder = extract_csv_data(csv_file, 'Raeder')
einwaerts = extract_csv_data(csv_file, 'stadteinwaerts')
auswaerts = extract_csv_data(csv_file, 'stadtauswaerts')
temp = extract_csv_data(csv_file, 'GefuehlteTemperatur')
regen = extract_csv_data(csv_file, 'Regen')
zeit = extract_csv_data(csv_file, 'Zeit')

zeit_dt = pd.to_datetime(zeit, format='%d.%m.%Y %H:%M')
raeder = [float(x) for x in raeder]
temp = [float(x) for x in temp]
einwaerts = [float(x) for x in einwaerts]
auswaerts = [float(x) for x in auswaerts]
regen = [float(x) for x in regen]

proTag = [r - (e + a) for r, e, a in zip(raeder, einwaerts, auswaerts)]