import Levenshtein
import re
from datetime import date
import numpy as np
import pandas as pd
import json
import Dictionary_Dataset


def load_data(file_path, num_lines):
    data = []
    with open(file_path, encoding='utf-8') as inputfile:
        for _ in range(num_lines):
            line = inputfile.readline()
            try:
                json_data = json.loads(line)
                data.append(json_data)
            except json.JSONDecodeError:
                continue
    return data


def drop_columns(df, columns_to_drop):
    return df.drop(columns=columns_to_drop)


def trim_columns(df, trim_column, columns):
    df[trim_column] = df[trim_column].apply(
        lambda x: [{k: column[k] for k in columns} for column in x])
    return df


def convert_to_csv(df):
    df.to_csv('csvfile.csv', encoding='utf-8', index=False)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(r'csvfile.csv')
    return df


def split_experiences(df):
    # Convert string representation of list to actual list
    df['experiences'] = df['experiences'].apply(eval)

    max_experience_count = df['experiences'].apply(len).max()

    for i in range(max_experience_count):
        starts_at_col = f'starts_at_{i + 1}'
        ends_at_col = f'ends_at_{i + 1}'
        title_col = f'title_{i + 1}'
        company_col = f'company_{i + 1}'
        description_col = f'description_{i + 1}'
        duration_col = f'duration_{i + 1}'

        starts_at = df['experiences'].apply(lambda x: str(x[i]['starts_at']['year']) + '-' + str(
            x[i]['starts_at']['month']) + '-' + str(x[i]['starts_at']['day']) if len(x) > i and x[i][
            'starts_at'] is not None else None)
        ends_at = df['experiences'].apply(
            lambda x: str(x[i]['ends_at']['year']) + '-' + str(x[i]['ends_at']['month']) + '-' + str(
                x[i]['ends_at']['day']) if len(x) > i and x[i]['ends_at'] is not None else str(
                date.today()) if i == 0 else None)
        title = df['experiences'].apply(
            lambda x: x[i]['title'] if len(x) > i else None)
        company = df['experiences'].apply(
            lambda x: x[i]['company'] if len(x) > i else None)
        description = df['experiences'].apply(
            lambda x: x[i]['description'] if len(x) > i else None)
        duration = pd.to_datetime(ends_at) - pd.to_datetime(starts_at)

        df[starts_at_col] = starts_at
        df[ends_at_col] = ends_at
        df[title_col] = title
        df[company_col] = company
        df[description_col] = description
        df[duration_col] = duration

    return df


def split_education(df):
    # Convert string representation of list to actual list
    df['education'] = df['education'].apply(eval)
    max_education_count = df['education'].apply(len).max()

    for i in range(max_education_count):
        df[f'field_of_study_{i + 1}'] = df['education'].apply(
            lambda x: x[i]['field_of_study'] if len(x) > i and x[i]['field_of_study'] is not None else None)
        df[f'degree_name_{i + 1}'] = df['education'].apply(
            lambda x: x[i]['degree_name'] if len(x) > i else None)
        df[f'school_{+ 1}'] = df['education'].apply(
            lambda x: x[i]['school'] if len(x) > i else None)

    return df


def convert_languages(df):
    df['languages'] = df['languages'].apply(
        lambda x: x.strip("[]").replace("'", "").split(","))
    return df


def get_unique_languages(df):
    unique_languages = set([language.strip().lower(
    ) for languages_list in df['languages'] for language in languages_list])
    return unique_languages


def add_language_columns(df, unique_languages):
    for language in unique_languages:
        df[language] = df['languages'].apply(
            lambda x: 1 if language.strip().lower() in [lang.strip().lower() for lang in x] else 0)
    return df


def search_and_update_column(df, search_string, column_name):
    df[column_name] = df.select_dtypes(include='object').apply(
        lambda col: col.str.contains(
            search_string, na=False, flags=re.IGNORECASE)
    ).max(axis=1).astype(int)
    return df


def create_hardskill_columns(df, hardskills_array):
    create_columns(df, hardskills_array)

    for item in hardskills_array:
        search_skill(df, item)

    return df


def create_leadership_column(df, management_keywords):
    df['leadership'] = 0
    for col in df.columns:
        if col.startswith('title'):
            for i, value in enumerate(df[col]):
                if isinstance(value, str) and any(manage.lower() in value.lower() for manage in management_keywords):
                    df.at[i, 'leadership'] = 1

    return df


def calculate_levenshtein_distance(str1, str2):
    return Levenshtein.distance(str1.lower(), str2.lower())


def update_it_experience(df, titles):
    for index, row in df.iterrows():
        matched_titles = []
        matched_durations = []

        for col in df.filter(like='title').columns:
            for title in titles:
                distance = calculate_levenshtein_distance(
                    title, str(row[col]))
                if distance <= 2.5:
                    matched_titles.append(title)
                    duration_col = df.columns[df.columns.get_loc(col) + 3]
                    duration_str = str(row[duration_col])
                    numeric_part = re.search(r'\d+', duration_str)

                    if title.strip() and len(title) >= 2 and numeric_part:
                        days = int(numeric_part.group())
                        years = days / 365.25
                        matched_durations.append(years)
                    break

        non_empty_matched_titles = [
            title for title in matched_titles if title.strip() and len(title) >= 2]

        if non_empty_matched_titles:
            df.at[index, 'itname'] = ', '.join(non_empty_matched_titles)
            df.at[index, 'itmatch'] = len(non_empty_matched_titles)
            df.at[index, 'ittime_years'] = sum(matched_durations)

            total_years = sum(matched_durations)
            if total_years == 0:
                df.at[index, 'experience'] = 0
            elif total_years > 10:
                df.at[index, 'experience'] = 3
            elif total_years > 5:
                df.at[index, 'experience'] = 2
            else:
                df.at[index, 'experience'] = 1
        else:
            df.at[index, 'itname'] = 0
            df.at[index, 'itmatch'] = 0
            df.at[index, 'ittime_years'] = 0
            df.at[index, 'experience'] = 0

    return df


def update_it_edu(df, degree_array):
    df['fitting_degree'] = df.apply(
        lambda row: match_degree(row, degree_array), axis=1)
    df['fd'] = df.apply(lambda row: get_best_match_degree(
        row, degree_array), axis=1)
    return df


def match_degree(row, degree_array):
    best_match_distance = float('inf')
    best_match_degree = ""

    for col in row.index:
        if col.lower().startswith('field_of_study') or col.lower().startswith('degree_name'):
            for item in degree_array:
                distance = calculate_levenshtein_distance(
                    item.lower(), str(row[col]).lower())
                threshold = 6
                if distance <= threshold and distance < best_match_distance:
                    best_match_distance = distance
                    best_match_degree = item

    return 1 if best_match_degree else 0


def get_best_match_degree(row, degree_array):
    best_match_distance = float('inf')
    best_match_degree = ""

    for col in row.index:
        if col.lower().startswith('field_of_study') or col.lower().startswith('degree_name'):
            for item in degree_array:
                distance = calculate_levenshtein_distance(
                    item.lower(), str(row[col]).lower())
                threshold = 6

                if distance <= threshold and distance < best_match_distance:
                    best_match_distance = distance
                    best_match_degree = item

    return best_match_degree


def create_columns(df, columns):
    for column in columns:
        df[column] = 0
    return df


def update_softskills(SOFT_SKILLS, df):
    for skill in SOFT_SKILLS:
        df = search_skill(df, skill)


def search_skill(df, skill):
    df[skill] = df.apply(lambda row: row.apply(lambda x: 1 if (isinstance(x, str) and re.search(
        r"(?<![\w/])" + re.escape(skill.lower()) + r"(?![\w/])", x.lower())) else 0)).max(axis=1)
    return df


def generate_random_values_for_skill(df, skill, probability):
    random_values = np.random.rand(len(df))
    df[skill] = (random_values <= probability).astype(int)
    return df


def assign_additional_benefits(df, BENEFITS_PROBABILITY, BENEFITS):
    for benefit in BENEFITS:
        df = generate_random_values_for_skill(
            df, benefit, BENEFITS_PROBABILITY)

    return df


def assign_additional_softskills(df, SOFT_SKILLS_PROBABILITY, SOFT_SKILLS):
    for skill in SOFT_SKILLS:
        df = generate_random_values_for_skill(
            df, skill, SOFT_SKILLS_PROBABILITY)
    return df


def filter_columns(df, desired_columns):
    df = df[desired_columns]
    return df


def map_abbreviations_to_numbers(df, column_name):
    unique_abbreviations = df[column_name].unique()
    abbreviation_to_number = {abbr: num for num,
    abbr in enumerate(unique_abbreviations, 1)}
    df[column_name] = df[column_name].map(abbreviation_to_number)
    return df


def full_name_to_number(df):
    df = df.assign(full_name=range(1, len(df) + 1))
    return df


def add_job_columns(df, job_list):
    for attribute in job_list:
        df["j_" + attribute] = 0
    return df


def main():
    hardskils_array = Dictionary_Dataset.programming_languages + \
                      Dictionary_Dataset.frameworks + Dictionary_Dataset.Others_skills
    COLLUMNS_TO_DROP = Dictionary_Dataset.columns_to_drop
    PATH = r"C:\Users\daume\Downloads\Dataset Linkedin Profile\10000_random_us_people_profiles.txt"
    LINE_LIMIT = 100
    SOFT_SKILLS_PROBABILITY = 0.25
    BENEFITS_PROBABILITY = 0.15
    MANAGEMENT_KEYWORDS = Dictionary_Dataset.managment
    TITLES = Dictionary_Dataset.titles
    DEGREE_ARRAY = Dictionary_Dataset.degree
    SOFT_SKILLS = Dictionary_Dataset.soft_skills
    BENEFITS = Dictionary_Dataset.benefits
    TRIM_EXP = ['starts_at', 'ends_at', 'title', 'description', 'company']
    TRIM_EDU = ['field_of_study', 'degree_name', 'school']
    desired_columns = Dictionary_Dataset.desired_columns
    job_list = Dictionary_Dataset.job
    # Load data
    data = load_data(
        PATH, LINE_LIMIT)

    # Convert to DataFrame
    df = pd.json_normalize(data)

    # Drop columns
    df = drop_columns(df, COLLUMNS_TO_DROP)

    # Trim experiences and education columns
    df = trim_columns(df, "experiences", TRIM_EXP)
    df = trim_columns(df, "education", TRIM_EDU)

    df = convert_to_csv(df)

    # Split experiences column
    df = split_experiences(df)

    # Split education column
    df = split_education(df)

    # Convert string representation of list to actual list for 'languages' column
    df = convert_languages(df)

    # Get unique languages
    unique_languages = get_unique_languages(df)

    # Add new columns for each unique language
    df = add_language_columns(df, unique_languages)

    # Create a new column for every hardskill
    df = create_hardskill_columns(df, hardskils_array)

    df = search_and_update_column(df, r'c#', 'C#')

    # Search for "c++" in the description columns and update the 'C++' column
    df = search_and_update_column(df, r'c\+\+', 'C++')

    # Create a new column called "leadership"
    df = create_leadership_column(df, MANAGEMENT_KEYWORDS)

    # Update 'itname', 'itmatch', 'ittime_years', and 'experience' columns
    df = update_it_experience(df, TITLES)

    # Update 'fitting_degree' and 'fd' columns
    df = update_it_edu(df, DEGREE_ARRAY)

    # Create columns for skills and benefits
    df = create_columns(df, SOFT_SKILLS)
    df = create_columns(df, BENEFITS)

    # Search for skills in the 'description' columns
    update_softskills(SOFT_SKILLS, df)

    assign_additional_softskills(df, SOFT_SKILLS_PROBABILITY, SOFT_SKILLS)

    # Generate random values for benefits with the specified probabilities
    df = assign_additional_benefits(df, BENEFITS_PROBABILITY, BENEFITS)

    df = filter_columns(df, desired_columns)
    df = map_abbreviations_to_numbers(df, 'country')
    df = full_name_to_number(df)
    df = add_job_columns(df, job_list)

    # Save the updated DataFrame to a new CSV file
    df.to_csv('Profile_Person.csv', index=False)
    print(df.columns)
    print("Code ran successfully.")


if __name__ == "__main__":
    main()