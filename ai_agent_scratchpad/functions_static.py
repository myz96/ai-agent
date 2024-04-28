import time
import random
import string
from functools import lru_cache

def generate_custom_id(num_chars):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_chars))

# Tested up to 4000 characters, OpenAI seemed to adequately handle this
EXAMPLE_EMAIL_THREAD_ID = generate_custom_id(10)
EXAMPLE_VALUE_PROP = "EdApp's online learning management system (LMS) is uniquely designed to cater to the needs of corporate entities, specifically those in roles such as Director of Learning and Development, Chief Learning Officer (CLO), Corporate Training Manager, Organizational Development Specialist, and Learning Experience Designer. The platform's focus on microlearning and the delivery of bite-sized courses makes it an ideal solution for busy professionals who need to stay updated with the latest knowledge and skills in their respective fields. In the context of cybersecurity courses, EdApp's LMS can provide immense value. Cybersecurity is a rapidly evolving field, and staying updated with the latest threats and countermeasures is crucial. Traditional training methods may not be effective or efficient in this context, as they often involve lengthy, infrequent sessions that can be hard to schedule and may not retain the attention of learners. EdApp's microlearning approach, on the other hand, allows learners to interact with highly-targeted lessons that they can easily digest and retain. This ensures that they are always up-to-date with the latest cybersecurity knowledge. EdApp's LMS also includes a variety of features that can enhance the learning experience and improve outcomes. The Achievement feature, for instance, can motivate learners by rewarding them for completing lessons and courses. This can increase engagement and course completion rates, leading to better knowledge retention and application. The Leaderboard feature adds a competitive element to the learning process. By allowing learners to compete with their peers, it can further motivate them to complete courses and achieve higher scores. This can be particularly effective in a corporate setting, where healthy competition can drive performance. The Practical Assessment feature allows for on-the-job training and assessment, which can be particularly valuable in a field like cybersecurity. By applying their knowledge in real-world scenarios, learners can better understand and retain the concepts they have learned. Moreover, the assessments are automatically tracked in the admin portal, making it easy for managers to monitor progress and performance. The Certificate feature provides formal recognition of accomplished development, which can be a powerful motivator for learners. It also helps organizations track and validate individual skills, supporting workforce planning and compliance efforts. Finally, the Reporting & Analytics feature allows organizations to track every training interaction automatically. This can provide valuable insights into how learners are progressing through courses, and can support data-driven decision making. In conclusion, EdApp's LMS can provide a comprehensive, efficient, and engaging solution for delivering cybersecurity courses in a corporate setting. Its focus on microlearning, combined with its range of features designed to motivate learners and track progress, makes it an ideal choice for organizations looking to enhance their cybersecurity training efforts."
EXAMPLE_EMAIL_THREAD_CONTENT = """These times are available for me to meet this week. Please let me know if any of these times work for you.: Monday, 22th April:8:00 AM 9:00 AM 11:30 AM Tuesday, 23th April: 8:30 AM 9:00 AM 10:30 AM Wednesday, 24th April: 8:30 AM 11:30 AM 12:00 PM"""

@lru_cache(maxsize=128)
def extract_profile_information_static(name):
    """Extracts profile information from a private CRM. Use this tool when you need to extract profile information from a prospect lead."""
    print(f"Getting profile information for {name}...")
    time.sleep(3)
    profileinfojson = {
        "name": name,
        "company": "Example Company Inc.",
    }
    return profileinfojson

@lru_cache(maxsize=128)
def retrieve_relevant_value_prop_static(name):
    """Retrieves relevant value propositions from a private vector database. Use this tool when you need to retrieve relevant value propositions for a prospect lead."""
    profileinfojson = extract_profile_information_static(name)
    print(f"Retrieving relevant value propositions for {profileinfojson["name"]}...")
    time.sleep(3)
    return EXAMPLE_VALUE_PROP

@lru_cache(maxsize=128)
def get_email_thread_id_static(name):
    """Finds the appropriate email thread ID."""
    profileinfojson = extract_profile_information_static(name)
    print(f"Getting email thread ID for {profileinfojson["name"]}...")
    time.sleep(3)
    return EXAMPLE_EMAIL_THREAD_ID

@lru_cache(maxsize=128)
def retrieve_email_thread_content_static(name):
    """Retrieves email thread content from a private email database. Use this tool when you need to retrieve the content of previous emails."""
    email_thread_id = get_email_thread_id_static(name)
    print(f"Retrieving email thread content using {email_thread_id}...")
    print(f"--- [CHECK] Is the email thread ID the same? {email_thread_id == EXAMPLE_EMAIL_THREAD_ID} ---")
    time.sleep(3)
    if email_thread_id == EXAMPLE_EMAIL_THREAD_ID:
        return EXAMPLE_EMAIL_THREAD_CONTENT
    return f"No email found with ID {email_thread_id}."
    
@lru_cache(maxsize=128)
def compose_outreach_email_static(name):
    """Composes an outreach email that combines all relevant information about the prospect."""
    print("Composing outreach email...")
    profileinfojson = extract_profile_information_static(name)
    email_thread_id = get_email_thread_id_static(name)
    email_thread_content = retrieve_email_thread_content_static(name)
    relevant_value_prop = retrieve_relevant_value_prop_static(name)
    time.sleep(3)
    print(f"--- [CHECK] Is the email thread ID the same? {email_thread_id == EXAMPLE_EMAIL_THREAD_ID} ---")
    print(f"--- [CHECK] Has the previous email thread content been maintained? {email_thread_content == EXAMPLE_EMAIL_THREAD_CONTENT} ---")
    print(f"--- [CHECK] Has the full value proposition been maintained? {relevant_value_prop == EXAMPLE_VALUE_PROP} ---")
    if email_thread_id == EXAMPLE_EMAIL_THREAD_ID:
        outreach_email = f"""I am gathering and aggregating all information required to write a personalised outreach email. I am using the following information... \n Profile Information: {profileinfojson} \n Relevant Value Propositions: {relevant_value_prop} \n Previous Email Thread Content: {email_thread_content}"""
        return outreach_email
    return f"No email found with ID {email_thread_id}."
