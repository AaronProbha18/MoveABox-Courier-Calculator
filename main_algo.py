import math

# Define state mapping
state_mapping = {
    "N1": ["new delhi", "haryana", "madhya pradesh", "uttar pradesh", "rajasthan"],
    "N2": ["himachal pradesh", "jammu & kashmir", "ladakh", "punjab", "uttrakhand"],
    "S1": ["andhra pardesh", "karnataka", "tamil nadu", "telangana"],
    "S2": ["kerala", "lakshadweep"],
    "E": ["andaman and nicobar", "bihar", "chhattisgarh", "jharkhand", "odisha", "west bengal"],
    "W1": ["maharashtra", "goa", "daman and diu"],
    "W2": ["gujarat", "dadra & nagar haveli"],
    "NE": ["assam", "manipur", "meghalaya", "nagaland", "rest of assam", "tripura", "arunachal pradesh"]
}

# Define price mapping for Freeflow_Air
air_price_mapping = {
    "N1": [132, 130, 126, 123, 119],
    "N2": [132, 130, 126, 123, 119],
    "S1": [119, 117, 114, 110, 106],
    "S2": [121, 119, 116, 112, 108],
    "E": [139, 137, 134, 131, 128],
    "W1": [123, 121, 117, 114, 110],
    "W2": [123, 121, 117, 114, 110],
    "NE": [177, 172, 167, 164, 162]
}

# Define price mapping for Freeflow_Surface
surface_price_mapping = {
    "N1": [73, 72, 70, 68, 66],
    "N2": [73, 72, 70, 68, 66],
    "S1": [66, 65, 63, 61, 59],
    "S2": [67, 66, 64, 62, 60],
    "E": [77, 76, 74, 73, 71],
    "W1": [68, 67, 65, 63, 61],
    "W2": [68, 67, 65, 63, 61],
    "NE": [98, 95, 93, 91, 90]
}

# Define bucket mapping
bucket_mapping = {
    1: (1, 39),
    2: (40, 60),
    3: (60, 120),
    4: (120, 160),
    5: (160, 200)
}

def get_zone(destination):
    destination = destination.lower()  # Convert destination to lowercase
    for zone, states in state_mapping.items():
        if any(state in destination for state in states):
            return zone
    return None

def get_bucket(weight):
    for bucket, weight_range in bucket_mapping.items():
        if weight_range[0] <= weight < weight_range[1]:
            return bucket
    return None

def calculate_volumetric_weight(length, width, height):
    volume = (length * width * height) / 4700  # Convert dimensions from cm to m and calculate volume in m^3
    return math.ceil(volume)  # Round up the volumetric weight

def get_packaging_cost(chargeable_weight):
    if chargeable_weight > 24:
        return 300
    elif chargeable_weight > 10:
        return 200
    elif chargeable_weight > 0:
        return 100
    else:
        return 0

def get_pickup_cost(chargeable_weight):
    if chargeable_weight > 24:
        return 300
    elif chargeable_weight > 10:
        return 200
    elif chargeable_weight > 0:
        return 100
    else:
        return 0

def estimate_price(weight, length, width, height, destination, service, packaging=False, pickup=False):
    zone = get_zone(destination)
    if zone is None:
        return "Invalid destination"

    total_volumetric_weight = 0
    for box_length, box_width, box_height in zip(length, width, height):
        volumetric_weight = calculate_volumetric_weight(box_length, box_width, box_height)
        total_volumetric_weight += volumetric_weight

    chargeable_weight = max(weight, total_volumetric_weight)
    bucket = get_bucket(chargeable_weight)
    if bucket is None:
        return "Invalid weight"

    if service == "air":
        price_per_kg = air_price_mapping[zone][bucket - 1]
        total_price = price_per_kg * chargeable_weight
    elif service == "surface":
        price_per_kg = surface_price_mapping[zone][bucket - 1]
        total_price = price_per_kg * chargeable_weight
    else:
        return "Invalid service"

    if packaging:
        packaging_cost = get_packaging_cost(chargeable_weight)
        total_price += packaging_cost

    if pickup:
        pickup_cost = get_pickup_cost(chargeable_weight)
        total_price += pickup_cost

    return f"Price per KG ({service.capitalize()}): {price_per_kg}\nTotal Price ({service.capitalize()}): {total_price}"

# Driver code
weight = int(input("Enter Weight (KGs): "))
num_boxes = int(input("Enter Number of Box(es): "))
length = []
width = []
height = []
for i in range(num_boxes):
    print(f"Enter for Box {i + 1}:")
    length.append(int(input("Enter Length (Cm): ")))
    width.append(int(input("Enter Width (Cm): ")))
    height.append(int(input("Enter Height (Cm): ")))

destination = input("Enter Destination Place: ")
packaging = input("Do you need Packaging (Y/N)? ").upper() == "Y"
pickup = input("Do you need Pickup (Y/N)? ").upper() == "Y"

air_price = estimate_price(weight, length, width, height, destination, "air", packaging, pickup)
surface_price = estimate_price(weight, length, width, height, destination, "surface", packaging, pickup)

print(air_price)
print(surface_price)