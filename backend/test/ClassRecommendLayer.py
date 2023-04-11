import openai

prompt = """"The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:

Track:
1) \"I'm excited about machine learning and its potential applications in healthcare.\"
2) \"I'm interested in cloud computing and its impact on business operations.\"
3) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"
4) \"I want to learn more about computational biology and its applications.\"
5) \"I'm interested in developing software as a service application that can provide scalable and cost-effective solutions for businesses.\"
6) \"What class teaches about cyber security and its applications?\"
7) \"What different topics could I explore?\"
8) \"What are the most popular EECS classes for bioinformatics?\"
9) \"What are the most popular python classes?\"
10) \"I want to take a class with SQL in it next semester.\"
11) \"I am interested in hacking.\"

Too General:
1) \"What classes should I take?\"
3) \"What are the most popular EECS classes at UMich?\"
4) \”Recommend me some classes.\”
5) \”I want some ideas for interesting classes I can take.\”

The assistant's job is to classify the user question into one of these 
categories and return as a response ONLY the name of 
the categories that the prompt fits into (response returned by assistant must 
be in ALL LOWERCASE, including the first letter. The names of the categories 
should be exactly as given, in camelcase with no spaces between the words 
themselves. for example, if something is classified in Too General, the returned category should be spelled as 
tooGeneral).

Human: I am interested in cybersecurity related classes.
AI: track
Human: I need help figuring out a class to take next semester.
AI: tooGeneral
Human: I'm interested in exploring the use of machine learning for different industries.
AI: track
Human: I'm interested in the use of edge computing to improve IoT device performance.
AI: track
Human: """

with open('hidden.txt') as file: 
    api_key = file.read()
    openai.api_key = api_key

tests = [
    "I want to major in computer science",
    "I am interested in hacking",
    "I want to work in artificial intelligence",
    "I am interested in bioinformatics classes",
    "what is an easy class i can take"
]

for test in tests:
    slash = r'\"'
    input = f"{slash}{test}{slash}\n"
    newInst = prompt+input+ "AI: "
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=newInst,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
