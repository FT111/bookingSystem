import json, random

def generate_seats(num_seats=200, seats_per_row=20):
    rows = []
    for i in range(num_seats):
        seat_id = i + 1
        row_letter = chr(ord('A') + (i // seats_per_row))
        seat_name = f"{row_letter}{(i % seats_per_row) + 1}"
        status = "available" if i % random.randint(1,5) != 0 else "reserved"
        seat_info = {"id": seat_id, "name": seat_name, "status": status}
        rows.append(seat_info)
    return rows

# Generate the seats
seats_data = generate_seats()

# Serialize to JSON
json_data = json.dumps({"seats": seats_data}, indent=4)
print(json_data)