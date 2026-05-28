#siddharth tiwari cce sec 'B' 23fe10cce00085 
#I have written this code with python using 
#panda,matplotlib and seaborn and i have taken
#notice for any comment or necessary statistics to use in the code.
# from the given accident dataset,these were the code obtained from the situation.

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('/Users/siddharth/Desktop/data/accidents.csv')

# Display the first few rows of the dataset
print(df.head())

# 1. Frequency of Accidents Over Time

# Total number of accidents
total_accidents = df.shape[0]
print(f"Total number of accidents: {total_accidents}")

# Extract year, month, day of the week, and hour from the date column
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month
df['DayOfWeek'] = pd.to_datetime(df['Date']).dt.dayofweek
df['Hour'] = pd.to_datetime(df['Date']).dt.hour

# Plot distribution over years
plt.figure(figsize=(10, 6))
sns.countplot(x='Year', data=df)
plt.title('Distribution of Accidents Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Accidents')
plt.show()

# Plot distribution over months
plt.figure(figsize=(10, 6))
sns.countplot(x='Month', data=df)
plt.title('Distribution of Accidents Over Months')
plt.xlabel('Month')
plt.ylabel('Number of Accidents')
plt.show()

# Plot distribution over days of the week
plt.figure(figsize=(10, 6))
sns.countplot(x='DayOfWeek', data=df)
plt.title('Distribution of Accidents Over Days of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Accidents')
plt.show()

# Plot distribution over hours of the day
plt.figure(figsize=(10, 6))
sns.countplot(x='Hour', data=df)
plt.title('Distribution of Accidents Over Hours of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Accidents')
plt.show()

# 2. Geographical Distribution

# Top locations with the highest frequency of accidents
top_locations = df['Location'].value_counts().head(10)
print("Top locations with the highest frequency of accidents:\n", top_locations)

# Plot top locations
plt.figure(figsize=(10, 6))
top_locations.plot(kind='bar')
plt.title('Top Locations with the Highest Frequency of Accidents')
plt.xlabel('Location')
plt.ylabel('Number of Accidents')
plt.show()

# 3. Accident Severity Analysis

# Distribution of accident severities
severity_counts = df['Severity'].value_counts()
print("Distribution of accident severities:\n", severity_counts)

# Plot distribution of accident severities
plt.figure(figsize=(10, 6))
severity_counts.plot(kind='bar')
plt.title('Distribution of Accident Severities')
plt.xlabel('Severity')
plt.ylabel('Number of Accidents')
plt.show()

# Percentage of accidents resulting in fatalities or serious injuries
fatal_serious_percentage = (severity_counts['Fatal'] + severity_counts['Serious']) / total_accidents * 100
print(f"Percentage of accidents resulting in fatalities or serious injuries: {fatal_serious_percentage:.2f}%")

# 4. Demographic Insights

# Age and gender distributions
plt.figure(figsize=(12, 6))
sns.histplot(df['Age'], bins=20, kde=True)
plt.title('Age Distribution of Individuals Involved in Accidents')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

gender_counts = df['Gender'].value_counts()
print("Gender distribution:\n", gender_counts)

# Plot gender distribution
plt.figure(figsize=(10, 6))
gender_counts.plot(kind='bar')
plt.title('Gender Distribution of Individuals Involved in Accidents')
plt.xlabel('Gender')
plt.ylabel('Number of Individuals')
plt.show()

# 5. Environmental and Road Conditions

# Weather conditions and accident occurrences
weather_counts = df['Weather'].value_counts()
print("Weather conditions and accident occurrences:\n", weather_counts)

# Plot weather conditions
plt.figure(figsize=(10, 6))
weather_counts.plot(kind='bar')
plt.title('Weather Conditions and Accident Occurrences')
plt.xlabel('Weather Condition')
plt.ylabel('Number of Accidents')
plt.show()

# Road types and accident occurrences
road_type_counts = df['RoadType'].value_counts()
print("Road types and accident occurrences:\n", road_type_counts)

# Plot road types
plt.figure(figsize=(10, 6))
road_type_counts.plot(kind='bar')
plt.title('Road Types and Accident Occurrences')
plt.xlabel('Road Type')
plt.ylabel('Number of Accidents')
plt.show()

# Lighting conditions and accident occurrences
lighting_counts = df['Lighting'].value_counts()
print("Lighting conditions and accident occurrences:\n", lighting_counts)

# Plot lighting conditions
plt.figure(figsize=(10, 6))
lighting_counts.plot(kind='bar')
plt.title('Lighting Conditions and Accident Occurrences')
plt.xlabel('Lighting Condition')
plt.ylabel('Number of Accidents')
plt.show()

# 6. Vehicle and Driver Information

# Vehicle types and accident occurrences
vehicle_type_counts = df['VehicleType'].value_counts()
print("Vehicle types and accident occurrences:\n", vehicle_type_counts)

# Plot vehicle types
plt.figure(figsize=(10, 6))
vehicle_type_counts.plot(kind='bar')
plt.title('Vehicle Types and Accident Occurrences')
plt.xlabel('Vehicle Type')
plt.ylabel('Number of Accidents')
plt.show()

# Relationship between vehicle type and accident severity
plt.figure(figsize=(12, 6))
sns.countplot(x='VehicleType', hue='Severity', data=df)
plt.title('Relationship Between Vehicle Type and Accident Severity')
plt.xlabel('Vehicle Type')
plt.ylabel('Number of Accidents')
plt.show()

# Driver behavior and accident occurrences
driver_behavior_counts = df['DriverBehavior'].value_counts()
print("Driver behavior and accident occurrences:\n", driver_behavior_counts)

# Plot driver behavior
plt.figure(figsize=(10, 6))
driver_behavior_counts.plot(kind='bar')
plt.title('Driver Behavior and Accident Occurrences')
plt.xlabel('Driver Behavior')
plt.ylabel('Number of Accidents')
plt.show()

# 7. Temporal Patterns

# Peak times during the day
plt.figure(figsize=(10, 6))
sns.countplot(x='Hour', data=df)
plt.title('Peak Times During the Day for Accidents')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Accidents')
plt.show()

# Weekdays vs. weekends
df['Weekend'] = df['DayOfWeek'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
weekend_counts = df['Weekend'].value_counts()
print("Weekdays vs. weekends accident occurrences:\n", weekend_counts)

# Plot weekdays vs. weekends
plt.figure(figsize=(10, 6))
weekend_counts.plot(kind='bar')
plt.title('Weekdays vs. Weekends Accident Occurrences')
plt.xlabel('Day Type')
plt.ylabel('Number of Accidents')
plt.show()

# Seasonal variation
df['Season'] = pd.cut(df['Month'], bins=[0, 2, 5, 8, 11, 12], labels=['Winter', 'Spring', 'Summer', 'Autumn', 'Winter'])
season_counts = df['Season'].value_counts()
print("Seasonal variation in accident occurrences:\n", season_counts)

# Plot seasonal variation
plt.figure(figsize=(10, 6))
season_counts.plot(kind='bar')
plt.title('Seasonal Variation in Accident Occurrences')
plt.xlabel('Season')
plt.ylabel('Number of Accidents')
plt.show()

# 8. Contributing Factors

# Common contributing factors
contributing_factors_counts = df['ContributingFactor'].value_counts()
print("Common contributing factors:\n", contributing_factors_counts)

# Plot contributing factors
plt.figure(figsize=(10, 6))
contributing_factors_counts.plot(kind='bar')
plt.title('Common Contributing Factors to Accidents')
plt.xlabel('Contributing Factor')
plt.ylabel('Number of Accidents')
plt.show()

# Variation across severities
plt.figure(figsize=(12, 6))
sns.countplot(x='ContributingFactor', hue='Severity', data=df)
plt.title('Variation of Contributing Factors Across Accident Severities')
plt.xlabel('Contributing Factor')
plt.ylabel('Number of Accidents')
plt.show()

# 9. Injury and Fatality Analysis

# Distribution among road users
road_user_counts = df['RoadUser'].value_counts()
print("Distribution of injuries and fatalities among road users:\n", road_user_counts)

# Plot road users
plt.figure(figsize=(10, 6))
road_user_counts.plot(kind='bar')
plt.title('Distribution of Injuries and Fatalities Among Road Users')
plt.xlabel('Road User')
plt.ylabel('Number of Accidents')
plt.show()

# Correlation with factors
plt.figure(figsize=(12, 6))
sns.countplot(x='RoadUser', hue='Severity', data=df)
plt.title('Correlation Between Road User and Accident Severity')
plt.xlabel('Road User')
plt.ylabel('Number of Accidents')
plt.show()

# 10. Comparative Analysis

# Comparison between regions
region_counts = df['Region'].value_counts()
print("Comparison of accident statistics between regions:\n", region_counts)

# Plot regions
plt.figure(figsize=(10, 6))
region_counts.plot(kind='bar')
plt.title('Comparison of Accident Statistics Between Regions')
plt.xlabel('Region')
plt.ylabel('Number of Accidents')
plt.show()

# Urban vs. rural areas
urban_rural_counts = df['UrbanRural'].value_counts()
print("Accident characteristics between urban and rural areas:\n", urban_rural_counts)

# Plot urban vs. rural
plt.figure(figsize=(10, 6))
urban_rural_counts.plot(kind='bar')
plt.title('Accident Characteristics Between Urban and Rural Areas')
plt.xlabel('Area Type')
plt.ylabel('Number of Accidents')
plt.show()
