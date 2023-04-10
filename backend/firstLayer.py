import openai

prompt = """"The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:

Class recommendation:
1) \"I'm excited about machine learning and its potential applications in healthcare.\"
2) \"I'm interested in cloud computing and its impact on business operations.\"
3) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"
4) \"I want to learn more about computational biology and its applications.\"
5) \"I'm interested in developing software as a service application that can provide scalable and cost-effective solutions for businesses.\"
6) \"What class teaches about cyber security and its applications?\"
7) \”What different topics could I explore?\"

Class information:
1) \"Tell me about EECS485.\"
2) \"I am interested in EECS 281.\"
3) \"Tell me about the class Web Systems.\"
4) \”What classes do I need to take before EECS485?\”
5) \”What classes are related to 489?\”

Major Requirements and Declaration:
1) \"What classes do I need to take to graduate?\"
2) \"What are the graduation requirements?\"
3) \"What classes do I need to take before declaring the Computer Science major?\"
4) \”I want to get a Computer Science minor?\”
5) \”I want to declare in computer science.\”

The assistant's job is to classify the user question into one of these categories or none of the above and return as a response ONLY the name of the categories that the prompt fits into (response returned by assistant must be in ALL LOWERCASE, including the first letter. The names of the categories should be exactly as given, in camelcase with no spaces between the words themselves. for example, if something is classified in Major Requirements and Declaration, the returned category should be spelled as majorRequirementsAndDeclaration). Use “none of the above” very sparingly and try your best to put the user question into one of the categories.

Human: I want to declare for computer science
AI: majorRequirementsAndDeclaration.
Human: I want to find some interesting classes
AI: classRecommendation
Human: I want to learn more about Web Systems
AI: classInformation
Human: Tell me about EECS376
AI: classInformation

Human: i like playing video games and also robot stuff is cool i want to take classes that help me explore that
AI: classRecommendation
Human: I'm interested in exploring the use of machine learning for music composition.
AI: classRecommendation
Human: \"I'm interested in the use of edge computing to improve IoT device performance.\"
AI: classRecommendation
Human: \"Tell me about the battle of 1776\"
AI: noneOfTheAbove
Human: """

with open('hidden.txt') as file: 
    api_key = file.read()
    openai.api_key = api_key

tests = [
    "I want to learn software engineering",
    "What do I need to declare my major",
    "Tell me about EECS 376"
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
    