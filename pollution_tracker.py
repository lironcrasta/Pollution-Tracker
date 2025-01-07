import csv
from datetime import datetime

# Define AQI thresholds for different pollutants
AQI_THRESHOLDS = {
    "PM2.5": {"standard": 35, "max_aqi": 500},
    "PM10": {"standard": 50, "max_aqi": 500},
    "CO2": {"standard": 500, "max_aqi": 500},
    "SO2": {"standard": 75, "max_aqi": 500}
}

# Define pollution categories and suggestions
POLLUTION_CATEGORIES = {
    (0, 50): ("Good", "Air quality is satisfactory. Maintain clean energy practices."),
    (51, 100): ("Moderate", "Consider carpooling or using public transport to reduce emissions."),
    (101, 150): ("Unhealthy for Sensitive Groups", "Limit outdoor activities for sensitive groups; consider using air purifiers indoors."),
    (151, 200): ("Unhealthy", "Avoid outdoor activities; reduce vehicle usage, consider working from home."),
    (201, 300): ("Very Unhealthy", "Avoid going outside; use air purifiers and masks indoors; reduce industrial activities."),
    (301, 500): ("Hazardous", "Stay indoors; minimize all emissions; consider emergency air quality measures.")
}

# Load pollutant values from a text file
def load_pollutant_data(file_path):
    try:
        pollutant_data = {}
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split(": ")
                pollutant_data[key] = float(value)
        return pollutant_data
    except FileNotFoundError:
        print("Error: Input file not found.")
        return None
    except ValueError:
        print("Error: Invalid data format.")
        return None

# Calculate AQI for a single pollutant
def calculate_individual_aqi(value, standard, max_aqi):
    return min(max_aqi, (value / standard) * 100)

# Determine the AQI category and suggestion based on the overall AQI
def get_aqi_category_and_suggestion(aqi):
    for (low, high), (category, suggestion) in POLLUTION_CATEGORIES.items():
        if low <= aqi <= high:
            return category, suggestion
    return "Invalid AQI", "No suggestions available."

# Main function to calculate AQI from pollutant data
def calculate_overall_aqi(pollutant_data):
    aqi_values = {}

    for pollutant, value in pollutant_data.items():
        if pollutant in AQI_THRESHOLDS:
            standard = AQI_THRESHOLDS[pollutant]["standard"]
            max_aqi = AQI_THRESHOLDS[pollutant]["max_aqi"]
            aqi_values[pollutant] = calculate_individual_aqi(value, standard, max_aqi)

    overall_aqi = max(aqi_values.values())
    category, suggestion = get_aqi_category_and_suggestion(overall_aqi)
    return overall_aqi, category, suggestion, aqi_values

# Write results to an output text file
def write_results_to_file(output_path, overall_aqi, category, suggestion, aqi_values):
    with open(output_path, 'w') as file:
        file.write(f"Overall AQI: {overall_aqi}\n")
        file.write(f"Category: {category}\n")
        file.write(f"Suggestion: {suggestion}\n")
        file.write("Individual AQI Values:\n")
        for pollutant, aqi in aqi_values.items():
            file.write(f"  {pollutant}: {aqi}\n")
    print("Results have been written to:", output_path)

# Log AQI data for tracking pollution over time
def log_aqi_data(log_file, overall_aqi, category, suggestion, aqi_values):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_data = [timestamp, overall_aqi, category, suggestion] + list(aqi_values.values())

    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_data)
    print("Logged data to:", log_file)

# Main program
def main(input_file, output_file, log_file):
    pollutant_data = load_pollutant_data(input_file)

    if pollutant_data:
        overall_aqi, category, suggestion, aqi_values = calculate_overall_aqi(pollutant_data)
        write_results_to_file(output_file, overall_aqi, category, suggestion, aqi_values)
        log_aqi_data(log_file, overall_aqi, category, suggestion, aqi_values)

        # Display AQI and suggestion
        print("\nAQI calculation complete.")
        print(f"Overall AQI: {overall_aqi}")
        print(f"Pollution Category: {category}")
        print(f"Suggestion: {suggestion}")
        print("Individual AQI Values:", aqi_values)

# Run the main function
if __name__ := "__main__":
    input_file = "pollutant_data.txt"  # Input file path (plain text)
    output_file = "aqi_results.txt"    # Output file path (plain text)
    log_file = "aqi_log.csv"           # Log file path (CSV)
    main(input_file, output_file, log_file)
