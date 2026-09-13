def parse_db_records(db_records: list[tuple], columns: dict):

    extracted_data = []

    for record in db_records:
        extracted_element = {}
        for col_name, index in columns.items():
            extracted_element[col_name] = record[index]
        extracted_data.append(extracted_element)

    return extracted_data