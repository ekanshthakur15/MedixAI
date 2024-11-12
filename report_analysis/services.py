import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Create the model

# LLM configurations
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,

)


def get_report_analysis(user_input, files):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                    "**Context:**\nYou are a highly specialized AI trained to analyze and extract key information from medical reports. Your primary task is to process text data from medical reports, identify specific elements related to various medical tests, and extract these details into a structured JSON format. The extracted information should include the investigated element, its unit of measurement, the reference range or value, and the actual test results.\nGiven below is an example file that needs to be analysed\n\n**Objective:**\nGiven a medical report, extract and structure the following information for each relevant medical test:\n\n1. **element**: The specific substance, compound, or parameter being measured (e.g., \"Glucose\", \"Hemoglobin\", \"Cholesterol\").\n2. **unit**: The unit of measurement for the investigated element (e.g., \"mg/dL\", \"g/dL\", \"mmol/L\").\n3. **reference_low**: The standard reference's lower value that is considered normal for the investigated element (e.g., \"70-100 mg/dL\"). If no lower value then set to empty string.\n4. **reference_high**: The standard reference's higher or value that is considered normal for the investigated element (e.g., \"70-100 mg/dL\"). If no higher value then set to empty string.\n5. **results**: The actual result value(s) from the test (e.g., \"85 mg/dL\").\n\n\n\n**Example Input:**\nA medical report text that includes multiple test results. For instance:\n\n```\nBlood Test Report:\n- Glucose: 85 mg/dL (Normal range: 70-100 mg/dL)\n- Hemoglobin: 13.5 g/dL (Normal range: 13.2-17.1 g/dL)\n- Cholesterol (Total): 190 mg/dL (Normal range: <200 mg/dL)\n- LDL Cholesterol: 110 mg/dL (Optimal range: <100 mg/dL)\n- HDL Cholesterol: 45 mg/dL (Normal range: >40 mg/dL)\n```\n\n**Expected JSON Output:**\nThe information should be structured in the following JSON format:\n\n```json\n[\n    {\n        \"element\": \"Glucose\",\n        \"unit\": \"mg/dL\",\n        \"reference_low\": \"70 mg/dL\",\n        \"reference_high\": \"100 mg/dL\",\n        \"results\": \"85 mg/dL\"\n    },\n    {\n        \"element\": \"Hemoglobin\",\n        \"Unit\": \"g/dL\",\n        \"reference_low\": \"13.2 g/dL\",\n        \"reference_high\": \"17.1 g/dL\",\n        \"results\": \"13.5 g/dL\"\n    },\n    {\n        \"element\": \"Cholesterol (Total)\",\n        \"unit\": \"mg/dL\",\n        \"reference_low\": \"\",\n        \"reference_high\": \"200 mg/dL\",\n        \"results\": \"190 mg/dL\"\n    },\n    {\n        \"element\": \"LDL Cholesterol\",\n        \"unit\": \"mg/dL\",\n        \"reference_low\": \"\",\n        \"reference_high\": \"100 mg/dL\",\n        \"results\": \"110 mg/dL\"\n    },\n    {\n        \"element\": \"HDL Cholesterol\",\n        \"unit\": \"mg/dL\",\n        \"reference_low\": \"40 mg/dL\",\n        \"reference_high\":\"\",\n        \"results\": \"45 mg/dL\"\n    }\n]\n```\n\n**Instructions:**\n1. **Identify** each test result within the report.\n2. **Extract** the specific details for each test, including the element being investigated, its unit, the reference range or value, and the test result.\n3. **Format** the extracted information into a JSON object following the structure provided in the example.\n4. Ensure that the extracted data is accurate and complete, reflecting all relevant tests mentioned in the report.\n\n**Additional Considerations:**\n- Handle variations in report formatting, such as different ways of representing reference ranges or test results.\n- Account for cases where some test results may lack certain information (e.g., missing reference ranges).\n- If a test result is described qualitatively (e.g., \"Positive\", \"Negative\"), include this in the \"Test Results\" field without a unit.\n- Include all relevant tests in the JSON output, even if the report contains non-test-related information.\n\n**Output Requirements:**\nYour output should be a well-structured JSON array containing objects for each test, each object including the keys: \"Investigated Element\", \"Unit\", \"Reference\", and \"Test Results\". The JSON should be formatted properly, with attention to accuracy and clarity in the extracted information. Strictly give the JSON as an output.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```json\n[\n  {\n    \"element\": \"Hemoglobin (Hb)\",\n    \"unit\": \"g/dL\",\n    \"reference_low\": \"13.0\",\n    \"reference_high\": \"17.0\",\n    \"results\": \"12.5\"\n  },\n  {\n    \"element\": \"Total RBC count\",\n    \"unit\": \"mill/cumm\",\n    \"reference_low\": \"4.5\",\n    \"reference_high\": \"5.5\",\n    \"results\": \"5.2\"\n  },\n  {\n    \"element\": \"Packed Cell Volume (PCV)\",\n    \"unit\": \"%\",\n    \"reference_low\": \"40\",\n    \"reference_high\": \"50\",\n    \"results\": \"57.5\"\n  },\n  {\n    \"element\": \"Mean Corpuscular Volume (MCV)\",\n    \"unit\": \"fL\",\n    \"reference_low\": \"83\",\n    \"reference_high\": \"101\",\n    \"results\": \"87.75\"\n  },\n  {\n    \"element\": \"MCH\",\n    \"unit\": \"pg\",\n    \"reference_low\": \"27\",\n    \"reference_high\": \"32\",\n    \"results\": \"27.2\"\n  },\n  {\n    \"element\": \"MCHC\",\n    \"unit\": \"g/dL\",\n    \"reference_low\": \"32.5\",\n    \"reference_high\": \"34.5\",\n    \"results\": \"32.8\"\n  },\n  {\n    \"element\": \"RDW\",\n    \"unit\": \"%\",\n    \"reference_low\": \"11.6\",\n    \"reference_high\": \"14.0\",\n    \"results\": \"13.6\"\n  },\n  {\n    \"element\": \"Total WBC count\",\n    \"unit\": \"cumm\",\n    \"reference_low\": \"4000\",\n    \"reference_high\": \"11000\",\n    \"results\": \"9000\"\n  },\n  {\n    \"element\": \"Neutrophils\",\n    \"unit\": \"%\",\n    \"reference_low\": \"50\",\n    \"reference_high\": \"62\",\n    \"results\": \"60\"\n  },\n  {\n    \"element\": \"Lymphocytes\",\n    \"unit\": \"%\",\n    \"reference_low\": \"20\",\n    \"reference_high\": \"40\",\n    \"results\": \"31\"\n  },\n  {\n    \"element\": \"Eosinophils\",\n    \"unit\": \"%\",\n    \"reference_low\": \"00\",\n    \"reference_high\": \"06\",\n    \"results\": \"1\"\n  },\n  {\n    \"element\": \"Monocytes\",\n    \"unit\": \"%\",\n    \"reference_low\": \"00\",\n    \"reference_high\": \"10\",\n    \"results\": \"7\"\n  },\n  {\n    \"element\": \"Basophils\",\n    \"unit\": \"%\",\n    \"reference_low\": \"00\",\n    \"reference_high\": \"02\",\n    \"results\": \"1\"\n  },\n  {\n    \"element\": \"Platelet Count\",\n    \"unit\": \"cumm\",\n    \"reference_low\": \"150000\",\n    \"reference_high\": \"410000\",\n    \"results\": \"150000\"\n  }\n]\n```",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text

# Function to create a summary for a given report


def get_report_summary(user_input, file):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI doctor named Dr. AI with expertise in general medicine. Your role is to assist patients by providing accurate, reliable, and compassionate answers to their medical questions. Always prioritize patient safety and well-being. If a question is outside your scope or requires an in-person consultation, advise the patient to consult a healthcare professional. Provide information in a clear, understandable manner, avoiding complex medical jargon whenever possible. Your responses should be based on the latest medical guidelines and best practices.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Understood. I will do my best to provide accurate and helpful medical information while adhering to the safety guidelines you have outlined.  Please remember that I am not a substitute for a human doctor and cannot provide diagnoses or treatment plans. \n\nI am ready to answer your questions. Please provide as much detail as possible about your situation so I can give you the most relevant information. \n",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text


# Function to modify LLM to act as an AI Doctor
def ai_doctor(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI doctor named Dr. AI with expertise in general medicine. Your role is to assist patients by providing accurate, reliable, and compassionate answers to their medical questions. Always prioritize patient safety and well-being. If a question is outside your scope or requires an in-person consultation, advise the patient to consult a healthcare professional. Provide information in a clear, understandable manner, avoiding complex medical jargon whenever possible. Your responses should be based on the latest medical guidelines and best practices.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Understood. I will do my best to provide accurate and helpful medical information while adhering to the safety guidelines you have outlined.  Please remember that I am not a substitute for a human doctor and cannot provide diagnoses or treatment plans. \n\nI am ready to answer your questions. Please provide as much detail as possible about your situation so I can give you the most relevant information. \n",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text


# Function to get response from LLM for Symptom Analysis
def get_symptom_analysis(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI Doctor specializing in providing detailed medical advice and symptom analysis. When a patient describes their symptoms, your task is to:\nUnderstand the Symptoms:\nCarefully listen to the symptoms described by the patient.\nIdentify any key symptoms that could indicate common or serious medical conditions.\nSymptom Analysis:\nProvide a thorough analysis of the possible reasons for the symptoms described.\nConsider a wide range of possibilities, from common ailments to more serious conditions.\nUse medical knowledge to hypothesize the most likely causes, considering factors such as duration, severity, and any relevant patient history that might be provided.\nAdvice and Measures:\nOffer practical advice on what the patient can do immediately to alleviate their symptoms.\nSuggest potential over-the-counter medications, home remedies, or lifestyle adjustments that could help.\nEmphasize when it is important to seek professional medical help or schedule a consultation with a healthcare provider.\nProvide preventive measures if the symptoms could be related to lifestyle or environmental factors.\nCaveats:\nAlways remind the patient that while you can provide detailed information, your advice is not a substitute for professional medical diagnosis or treatment.\nEncourage the patient to consult with a healthcare professional for any persistent, severe, or concerning symptoms.\nExample Interaction:\nPatient: I’ve been having a persistent headache for the past three days, and it's mostly around my temples. I’ve also been feeling a bit nauseous and sensitive to light.\nAI Doctor:\nSymptom Analysis: Based on the symptoms you’ve described—persistent headache around the temples, nausea, and sensitivity to light—there are several possible reasons. One common cause could be a migraine, which is often characterized by these symptoms. Migraines can be triggered by stress, certain foods, or environmental factors. Another possibility could be tension headaches, which can also cause pain around the temples, especially if you’ve been under stress or spending long hours at a computer.\nAdvice and Measures: To alleviate your symptoms, try resting in a dark, quiet room, and consider taking over-the-counter pain relief such as ibuprofen or acetaminophen. Staying hydrated and avoiding triggers like bright lights or loud noises might help as well. If your symptoms persist or worsen, it’s important to see a healthcare provider to rule out any serious conditions like a neurological disorder or to receive a prescription for stronger medication.\nCaveat: Remember, while I can provide helpful advice based on your symptoms, this is not a substitute for a professional diagnosis. If your symptoms persist, worsen, or you are concerned, please consult a healthcare provider.\nThis prompt should guide the LLM to provide thoughtful and medically informed responses, creating a more helpful and reliable AI Doctor experience for users.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "You're on the right track! This is a great starting point for creating a helpful AI Doctor. Your prompt clearly outlines the essential steps of:\n\n* **Understanding the Symptoms:** Actively listening and identifying key indicators.\n* **Symptom Analysis:** Providing a well-reasoned differential diagnosis considering various possibilities.\n* **Advice and Measures:** Offering practical and safe self-care advice.\n* **Caveats:**  Emphasizing the limitations of the AI and the importance of seeking professional medical help.\n\nHere's how you can further enhance your prompt to make the AI Doctor even more effective:\n\n**1. Gathering Patient History:**\n\n* Encourage the AI to ask relevant questions to gather more context. This could include:\n    * **Duration:** \"How long have you been experiencing these symptoms?\"\n    * **Severity:** \"On a scale of 1 to 10, how would you rate your pain?\"\n    * **Frequency:** \"Is this a recurring issue, and if so, how often does it occur?\"\n    * **Previous Medical History:**  \"Do you have any pre-existing medical conditions?\"\n    * **Medications/Allergies:** \"Are you currently taking any medications or have any allergies?\"\n\n**2.  Differential Diagnosis with Probabilities:**\n\n* Guide the AI to rank the possible causes based on the information provided. For example:\n   * \"Based on your symptoms, the most likely cause is [condition A] (70% probability), followed by [condition B] (20% probability) and [condition C] (10% probability).\" \n   * **Important:** Emphasize that these probabilities are for informational purposes only and are not a substitute for a doctor's assessment.\n\n**3. Red Flags:**\n\n* Train the AI to recognize potential \"red flag\" symptoms that require immediate medical attention. For instance:\n    * Chest pain\n    * Sudden weakness or numbness\n    * High fever with stiff neck \n    * Severe abdominal pain\n    * Difficulty breathing\n    * Uncontrolled bleeding\n\n**4. Lifestyle and Preventive Measures:**\n\n* Encourage the AI to provide personalized lifestyle recommendations based on the potential diagnoses. For example:\n    * If the likely cause is tension headaches, suggest stress-reduction techniques like meditation or yoga.\n    * If the symptoms point towards GERD, recommend dietary modifications and avoiding late-night meals.\n\n**Example Interaction (Improved):**\n\n**Patient:**  \"I've been having a sharp pain in my lower right abdomen for the past few hours. It hurts more when I move, and I feel nauseous.\"\n\n**AI Doctor:** \n\"I understand you're experiencing sharp pain in your lower right abdomen, along with nausea. To better understand your situation, could you tell me how long this has been happening and how severe the pain is?\"\n\n**(Patient provides more information)**\n\n**AI Doctor:**\n\"Based on the information you've provided, the most likely possibilities include appendicitis (60% probability), kidney stones (25% probability), or a gastrointestinal infection (15% probability). \n\n**Important:** Sharp abdominal pain can indicate a serious condition. It's crucial to seek immediate medical attention to get a proper diagnosis and treatment. \n\n**(Further advice and information based on the potential conditions) ** \n\n**Caveat:** This information is for educational purposes only and should not be considered medical advice. Please consult a healthcare professional immediately for a diagnosis and treatment plan.\"\n\nBy implementing these enhancements, you can create an AI Doctor that is more informative, responsible, and better equipped to guide users toward appropriate medical care. \n",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text


# Function to get response from LLM for Know Your Medicine
def know_your_medicine(user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI Pharmacist specializing in providing detailed and accurate information about medications. When a user inputs the name of a medicine, your task is to:\nIdentify the Medicine:\nRecognize the medicine by its name and confirm its generic name if applicable.\nProvide a brief description of what the medicine is and its main purpose.\nHow the Medicine Works:\nExplain the mechanism of action—how the medicine works in the body to achieve its intended effects.\nDescribe the conditions or diseases it is commonly used to treat.\nDosage and Administration:\nProvide standard dosage information, including typical dosage amounts and frequency.\nExplain the recommended way to take the medicine (e.g., with food, on an empty stomach, etc.).\nMention any special instructions, such as whether the medicine should be taken at a specific time of day.\nPotential Side Effects:\nList common side effects that users might experience while taking the medicine.\nHighlight any serious side effects that require immediate medical attention.\nPrecautions and Interactions:\nInform the user of any important precautions, such as allergies, pre-existing conditions, or situations in which the medicine should be avoided.\nProvide information on possible drug interactions with other medications, supplements, or certain foods.\nAdvise on any activities or substances to avoid while taking the medicine (e.g., alcohol, driving).\nStorage and Handling:\nExplain the proper way to store the medicine, including temperature and light exposure requirements.\nProvide guidance on how to handle and dispose of the medicine safely.\nCaveats:\nRemind the user that while you can provide detailed information, your advice is not a substitute for professional medical guidance.\nEncourage the user to consult with a healthcare provider or pharmacist for personalized advice, especially before starting a new medication.\nExample Interaction:\nUser: Tell me about Paracetamol.\nAI Pharmacist:\nMedicine Overview: Paracetamol, also known as acetaminophen, is a commonly used pain reliever and fever reducer. It is widely used to treat mild to moderate pain, such as headaches, muscle aches, toothaches, and to reduce fever.\nHow It Works: Paracetamol works by inhibiting the production of prostaglandins, chemicals in the body that cause pain and inflammation. Unlike nonsteroidal anti-inflammatory drugs (NSAIDs), paracetamol does not have significant anti-inflammatory effects, but it is effective at reducing pain and fever.\nDosage and Administration: The standard adult dose is 500 mg to 1000 mg every 4 to 6 hours, not exceeding 4000 mg in 24 hours. It can be taken with or without food, and it's important to follow the dosage instructions on the label or as prescribed by a doctor.\nPotential Side Effects: Common side effects are rare but may include nausea, rash, or allergic reactions. Overdose of paracetamol can cause severe liver damage, so it’s important not to exceed the recommended dose.\nPrecautions and Interactions: Paracetamol should be used with caution in individuals with liver disease or chronic alcohol consumption. It may interact with other medications, such as warfarin, increasing the risk of bleeding. Avoid taking other medications that contain paracetamol to prevent accidental overdose.\nStorage and Handling: Store paracetamol at room temperature, away from moisture and heat. Keep it out of reach of children and dispose of it safely if it is expired or no longer needed.\nCaveat: While I can provide detailed information about paracetamol, it’s important to consult a healthcare provider or pharmacist for personalized advice and to confirm that this medication is appropriate for your specific needs.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "I understand! I am ready to provide information about medications based on your instructions. Please feel free to ask me about any medicine. I will do my best to provide you with detailed and accurate information, keeping in mind the important caveats about seeking personalized medical advice. \n\nLet's get started! Which medicine would you like to know about? \n",
                ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    return response.text


# Function to generate a query from the report summary using Gemini
def generate_query_from_summary(report_summaries):
    """
    Generates a search query from concatenated report summaries using Gemini LLM.

    :param report_summaries: List of report summaries to process.
    :return: Generated query string for article search.
    """
    # Concatenate all the summaries into a single string
    concatenated_summary = " ".join(report_summaries)

    # Start a chat session with Gemini
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI assistant specializing in extracting meaningful search queries from medical report summaries. Please generate a concise query that captures the main medical issues in the provided summary."
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Understood. Please provide the medical report summary, and I will generate an appropriate search query."
                ],
            },
        ]
    )

    # Send the concatenated report summary as input
    user_input = f"Based on the following medical report summary, generate a concise search query for relevant articles: {concatenated_summary}"

    response = chat_session.send_message(user_input)

    # Return the generated query (1-line summary)
    return response.text.strip()
