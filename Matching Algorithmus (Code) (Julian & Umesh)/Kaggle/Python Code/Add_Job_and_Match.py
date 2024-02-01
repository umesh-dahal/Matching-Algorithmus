import pandas as pd
import math
import Dictionary_Dataset

# Combine arrays from Dictionary_Dataset.
combined_array = Dictionary_Dataset.programming_languages + \
    Dictionary_Dataset.frameworks + Dictionary_Dataset.titles

hardskills_array = Dictionary_Dataset.programming_languages + \
    Dictionary_Dataset.frameworks + Dictionary_Dataset.Others_skills

titles_array = Dictionary_Dataset.titles + Dictionary_Dataset.degree

degree_array = Dictionary_Dataset.degree + hardskills_array


# Load various other array from Dictionary_Dataset.
language_profile = Dictionary_Dataset.language_profile
language_job = Dictionary_Dataset.language_job
hardskills_profile = Dictionary_Dataset.hardskils_profile
hardskills_job = Dictionary_Dataset.hardskils_job
softskills_profile = Dictionary_Dataset.softskills_profile
softskills_job = Dictionary_Dataset.softskills_job
benefits_profiles = Dictionary_Dataset.benefits_profiles
benefits_job = Dictionary_Dataset.benefits_job


# Define dictionaries for different job as an array like in this case frontend_job, backend_job and program_job.
frontend_job = {
    "j_country": 1,
    "j_Html": 1,
    "j_Css": 1,
    'j_Communication': 1,
    'j_Problemsolving': 1,
    'j_Flexible work schedules': 1,
    'j_Retirement savings plans': 1,
    'j_Performance bonuses or profit-sharing': 1,
    'j_Stock options or equity grants': 1,
    'j_Dental and vision coverage': 1,
    'j_experience': 1,
    'j_fitting_degree': 1
}

backend_job = {
    "j_country": 1,
    'j_Java': 1,
    'j_Spring': 1,
    'j_Communication': 1,
    'j_Problemsolving': 1,
    'j_Flexible work schedules': 1,
    'j_Retirement savings plans': 1,
    'j_Performance bonuses or profit-sharing': 1,
    'j_Stock options or equity grants': 1,
    'j_Dental and vision coverage': 1,
    'j_experience': 1,
    'j_fitting_degree': 1
}

program_job = {
    "j_country": 1,
    'j_C++': 1.1,
    'j_C': 1.1,
    'j_Problemsolving': 1,
    'j_Flexible work schedules': 1,
    'j_Retirement savings plans': 1,
    'j_Performance bonuses or profit-sharing': 1,
    'j_Stock options or equity grants': 1,
    'j_Dental and vision coverage': 1,
    'j_experience': 1,
    'j_fitting_degree': 1
}


# Create main_array combining arrays for different job roles.
main_array = [frontend_job, backend_job, program_job]


# Read the CSV file from a DataFrame.
df = pd.read_csv(r'Profile_Person.csv', dtype=str, low_memory=False)


# calculate points for country, if country of applicant and company are not same then point will be 1000, which disqualifies the applicants.
def calculate_country_points(row, points):
    # Check if 'country' and 'j_country' are not the same
    if row['country'] != row['j_country']:
        points += 1000
    return points


# calculate points for degree, if degree of applicant and company are not same then point will be 1000, which disqualifies the applicants, else 20 points will be added.
def calculate_fitting_degree_points(row, points):
    # Convert 'j_fitting_degree' and 'fitting_degree' columns to integers if they are strings
    fitting_degree = float(row['fitting_degree']) if isinstance(row['fitting_degree'], str) else row['fitting_degree']
    j_fitting_degree = float(row['j_fitting_degree']) if isinstance(row['j_fitting_degree'], str) else row['j_fitting_degree']

    # Check if 'j_fitting_degree' has a value of 1 and 'fitting_degree' is 0
    if math.floor(j_fitting_degree) == 1 and fitting_degree == 0:
        if j_fitting_degree != int(j_fitting_degree):
            points += 1000
        points += 20
    return points


# calculate points for hardskills, if hardskills of applicant and company are not same then point will be 1000, which disqualifies the applicants, else 50 points will be added.
def hardskills_points(row, hardskills_job, hardskills_profile, points):
    for job_skill, profile_skill in zip(hardskills_job, hardskills_profile):
        # Convert column values to integers
        job_skill_val = float(row[job_skill]) if isinstance(row[job_skill], str) else row[job_skill]
        profile_skill_val = float(row[profile_skill]) if isinstance(row[profile_skill], str) else row[profile_skill]

        # Check if the values at the corresponding indices are 1 and 0 respectively
        if math.floor(job_skill_val) == 1 and profile_skill_val == 0:
            if job_skill_val != int(job_skill_val):
                points += 1000
            points += 50
    return points


# calculate points for softskills, if softskills of applicant and company are not same then point will be 1000, which disqualifies the applicants, else 10 points will be added.
def calculate_soft_skills_points(row, softskills_job, softskills_profile, points):
    for job_skill, profile_skill in zip(softskills_job, softskills_profile):
        # Convert column values to integers
        job_skill_val = float(row[job_skill]) if isinstance(row[job_skill], str) else row[job_skill]
        profile_skill_val = float(row[profile_skill]) if isinstance(row[profile_skill], str) else row[profile_skill]

        # Check if the values at the corresponding indices are 1 and 0 respectively
        if math.floor(job_skill_val) == 1 and profile_skill_val == 0:
            if job_skill_val != int(job_skill_val):
                points += 1000
            points += 10
    return points


# calculate points for experience, if experience of applicant and company are not same then point will be 1000, which disqualifies the applicants, else 20 points will be added.
def calculate_experience_points(row, points):
    experience = float(row['experience']) if isinstance(
    row['experience'], str) else row['experience']
    j_experience = float(row['j_experience']) if isinstance(
    row['j_experience'], str) else row['j_experience']
    # Check if 'j_experience' is greater than 'experience' by more than 1
    if math.floor(j_experience) > experience + 1:
        if j_experience != int(j_experience):
            points += 1000
        points += 20
    return points


# calculate points for benefits, if benefits of applicant and company are not same then point will be 1000, which disqualifies the applicants, else 20 points will be added.
def calculate_benefit_points(row, benefits_job, benefits_profiles, points):
    for job_benefit, profile_benefit in zip(benefits_job, benefits_profiles):
        # Convert column values to integers
        job_benefit_val = float(row[job_benefit]) if isinstance(row[job_benefit], str) else row[job_benefit]
        profile_benefit_val = float(row[profile_benefit]) if isinstance(row[profile_benefit], str) else row[profile_benefit]
        # Check if the values at the corresponding indices are 1 and 0 respectively
        if job_benefit_val == 1 and profile_benefit_val == 0:
            points += 10
    return points


# calculate points for all criteraia mention above
def calculate_points(row):
    points = 0
    points = calculate_benefit_points(row, benefits_job, benefits_profiles, points)
    points = calculate_country_points(row, points)
    points = hardskills_points(row, hardskills_job, hardskills_profile, points)
    points = calculate_soft_skills_points(row, softskills_job, softskills_profile, points)
    points = calculate_fitting_degree_points(row, points)
    points = calculate_experience_points(row, points)
    return points


# Create a new column in the DataFrame named 'match.' Assign a value of 0 to this column if the calculated points as determined previously exceed 100. 
#Conversely, set the 'match' column to 1 if the points are less than 100, indicating a match between profiles and job criteria.
def process_job_dict(job_dict, df):
    global file_counter  # Declare file_counter as a global variable
    # Update DataFrame based on the current job_dict
    for skill in job_dict.keys():
        df[skill] = job_dict[skill]

    # Calculate points for each row
    df['points'] = df.apply(lambda row: calculate_points(row), axis=1)

    # Convert 'match' column to 1 or 0 based on points
    df['match'] = (df['points'] < 100).astype(int)

    # Map DataFrame values to integers
    df['points'] = df['points'].astype(int)

    # Save the DataFrame to a CSV file
    filename = f'Profile_To_{file_counter}.csv'
    df.to_csv(filename, index=False)

    # Increment the file counter for the next iteration
    file_counter += 1


# This function processes a list of job dictionaries against a DataFrame, updating and saving the DataFrame for each job dictionary in the list. 
# The global variable file_counter keeps track of the file number for the output CSV files.
def process_main_array(main_array, df):
    global file_counter  # Declare file_counter as a global variable

    # Iterate over main_array and create a new CSV for each array
    for job_dict in main_array:
        # Clone the DataFrame to avoid modifying the original
        df_copy = df.copy()

        # Process the current job_dict
        process_job_dict(job_dict, df_copy)

        print("Finished processing")


# Function to initialize a DataFrame, set up counters, and process a list of job dictionaries
def initialize_and_process_dataframe(main_array, df):
    global file_counter  # Declare file_counter as a global variable

    # Initialize file counter
    file_counter = 1

    # Insert new columns for 'match' and 'points'
    df.insert(0, 'match', 0)
    df.insert(1, 'points', 0)

    # Convert DataFrame columns to float
    df = df.astype(float)

    # Call the function to process main_array
    process_main_array(main_array, df)

initialize_and_process_dataframe(main_array, df)
