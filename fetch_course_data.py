import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=option)


def load_course_links(file_name):
    links = []
    with open(file_name, "r") as file:
        for line in file:
            link = line.strip()
            links.append(link)
    return links


def get_course_name(soup):
    names = soup.findAll("h2", class_="elementor-heading-title elementor-size-default")
    return names[1].get_text(strip=True) if len(names) > 1 else "Unknown"


def get_modules(soup):
    modules = soup.findAll("p", id="grupe-stud")
    module_dict = {}

    for module in modules:
        a_tag = module.find("a")
        if a_tag:
            link = a_tag["href"]
            name = a_tag.get_text()
            module_dict[link] = name

    return module_dict


def get_subjects(soup):
    courses = soup.findAll("a", id="viewPredmetA_00_17_A320")
    subjects = []
    for course in courses:
        subject_data = {}
        subject_data["ime"] = course.text.strip()

        # Retrieve goal, outcome, and content via Selenium
        subject_data["cilj"], subject_data["ishod"], subject_data["sadrzaj"] = (
            retrieve_information_about_subject(course.get("href"))
        )
        subjects.append(subject_data)
    return subjects


def get_subjects_including_modules(modules_dict, soup):
    subjects = []
    courses = soup.findAll("a", id="viewPredmetA_00_17_A320")
    for course in courses:
        link = course["href"]
        if link not in modules_dict:
            subject_data = {}
            subject_data["ime"] = course.text.strip()
            subject_data["cilj"], subject_data["ishod"], subject_data["sadrzaj"] = (
                retrieve_information_about_subject(link)
            )
            subjects.append(subject_data)
        else:
            response = requests.get(link)
            if response.status_code == 200:
                soup_module = BeautifulSoup(response.text, "html.parser")
                courses_in_module = soup_module.findAll(
                    "a", id="viewPredmetA_00_17_A320"
                )
                for course_in_module in courses_in_module:
                    subject_data = {}
                    if not any(
                        subject["ime"] == course_in_module.text.strip()
                        for subject in subjects
                    ):
                        subject_data["ime"] = course_in_module.text.strip()
                        link = course_in_module["href"]
                        (
                            subject_data["cilj"],
                            subject_data["ishod"],
                            subject_data["sadrzaj"],
                        ) = retrieve_information_about_subject(link)
                        subjects.append(subject_data)
            else:
                print(f"Error loading page: {link}")

    return subjects


def retrieve_information_about_subject(subject_link):
    driver.get(subject_link)
    wait = WebDriverWait(driver, 30)

    # Wait for and retrieve goal
    wait.until(EC.presence_of_element_located((By.ID, "e-n-tab-content-1111")))
    goal_content = driver.find_element(By.ID, "e-n-tab-content-1111").text

    # Wait for and retrieve outcome
    outcome_button = driver.find_element(By.ID, "e-n-tabs-title-1113")
    outcome_button.click()
    wait.until(EC.presence_of_element_located((By.ID, "e-n-tab-content-1113")))
    outcome_content = driver.find_element(By.ID, "e-n-tab-content-1113").text

    # Wait for and retrieve content
    content_button = driver.find_element(By.ID, "e-n-tabs-title-1114")
    content_button.click()
    wait.until(EC.presence_of_element_located((By.ID, "e-n-tab-content-1114")))
    content = driver.find_element(By.ID, "e-n-tab-content-1114").text

    return goal_content, outcome_content, content


def get_basic_course_info(soup):
    panels = soup.find_all("div", class_="panel-body")
    panel_data = {}
    for panel in panels:
        p_tags = panel.find_all("p")
        if p_tags:
            for p in p_tags:
                strong_tags = p.find_all("strong")
                if len(strong_tags) >= 2:
                    key = strong_tags[0].get_text(strip=True)
                    value = strong_tags[1].get_text(strip=True)
                    panel_data[key] = value
    return panel_data


if __name__ == "__main__":
    links = load_course_links("data/course_links.txt")
    all_courses_data = {}

    for link in links:
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Getting course name
            course_name = get_course_name(soup)
            print(course_name)

            # Getting basic course info
            basic_course_info = get_basic_course_info(soup)

            # Getting all subjects and related information
            subjects = get_subjects(soup)

            # Construct the final JSON structure
            course_data = {course_name: {**basic_course_info, "Predmeti": subjects}}
            all_courses_data.update(course_data)

        else:
            print(f"Error loading page: {link}")

    links_modules = load_course_links("data/course_links_with_modules.txt")

    for link in links_modules:
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Getting course name
            course_name = get_course_name(soup)

            # Getting basic course info
            basic_course_info = get_basic_course_info(soup)

            modules_dict = get_modules(soup)
            subjects = get_subjects_including_modules(modules_dict, soup)

            course_data = {course_name: {**basic_course_info, "Predmeti": subjects}}
            all_courses_data.update(course_data)
        else:
            print(f"Error loading page: {link}")

    with open("data/course_data.json", "w", encoding="utf-8") as f:
        json.dump(all_courses_data, f, ensure_ascii=False, indent=4)

    driver.quit()
