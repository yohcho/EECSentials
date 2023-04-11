import openai
import json
import pymongo
import stringcase
from bson.objectid import ObjectId

openai.api_key="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"
myclient = pymongo.MongoClient("mongodb+srv://yohcho:qw123edc@cluster0.ggonojo.mongodb.net/?retryWrites=true&w=majority")
db = myclient["EECSentials"]["Class"]
dbSession = myclient["EECSentials"]["Session"]

#layer1 functions
def majorRequirementsAndDeclaration(message):
    prompt="""The following is a conversation with an AI assistant. The assistant is designed to help students understand the different requirements there are. Here is a list of the different requirements:

Minor Declaration Requirements:
To be eligible for the Academic Minor, students must have completed two prerequisite courses. For the Math requirement, a grade of C or higher in MATH 115 or any course that satisfies the EECS 203 prerequisite is necessary. In terms of programming, a grade of C or higher or current enrollment in EECS 180 (AP), EECS 183, ENGR 101, ENGR 151, or ROB 102 is required. Additionally, a grade of C or higher or current enrollment in EECS 203, EECS 280, or EECS 281 is necessary.

Minor Completion Requirements:
The Academic Minor Program requires completion of 15-16 credits of courses, consisting of three core courses and one approved CS Minor Elective Course. The three core courses are EECS 203 (or MATH 465/565), EECS 280 and EECS 28. In addition to the core courses, students must complete one 4-credit elective, selected from the list of approved CS Minor Elective Courses.

Major Declaration Requirements:
To declare a major in CS-Eng, you must be a College of Engineering student and fulfill certain criteria. These include completing at least one full term or 12 total credits at UM Ann Arbor, having an overall UM GPA of 2.0 or better in courses taken at the UM Ann Arbor campus and being in good standing, and completing or earning credit for at least one course in calculus, calculus-based physics or chemistry lectures, and required engineering courses.

Graduation and Major Completion Requirements:
The Computer Science in Engineering program has a set of requirements that need to be fulfilled in order to complete the major. The core courses include EECS 203 (or MATH 465/565*), EECS 280, EECS 281, EECS 370, EECS 376, and EECS 496 (or equivalent). Additionally, students must take a course in probability and statistics and technical communications. A minimum of 26 credits in technical electives are also required, with at least 16 of these credits being in approved Upper Level CS Technical Electives. The remaining credits may be chosen from the approved Flexible Technical Electives lists. Students are also required to complete a Major Design Experience (MDE), which is a capstone design project recommended to be taken during one of the final two semesters. The technical writing requirement must be taken in the same or later semester as the MDE. The technical writing and oral presentation course is TCHNCLCM 497. More details on how to complete MDE on an MDP project are available on the program's website.

The assistant's job is to classify the user question into one of these categories and return a informative but casual paragraph about the requirements.

Human: 
"""
    slash = r'\"'
    input = f"{slash}{message}{slash}\n"
    newInst = prompt+input+ "AI: "

    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=newInst,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    text = res['choices'][0]['text']
    
    return text

def classRecommendation(message):
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
12) \"Recommend me a class about AI.\"
12) \"Suggest me a class on cybersecurity.\"
13) \"Recommend me some classes on operating systems.\"

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
    slash = r'\"'
    input = f"{slash}{message}{slash}\n"
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
    type=res['choices'][0]['text']
    if "tooGeneral" in type:
        return "Tell me a topic you are interested in or a class you enjoyed."
    return trackClassification(message)
    
def classInformation(message):
    entities = entityExtract(message)
    action = classifyClassInformation(message)
    if action=="generalInformation":
        return handleClassInformationGeneral(message,entities)
    return entities

def classConversation(message,session):
    userSession = dbSession.find_one({"_id":ObjectId(session)})
    second_prompt_list = userSession['dialogue']
    if len(userSession['dialogue']) == 1:
        classes = entityExtract(message)
        query = {"tag":{"$in":classes}}
        example: str = list(db.find(query))
        yeah: str = ""
        for result in example: 
            yeah = yeah + str(result)
        second_prompt_list.append(yeah)
    second_response: str = second_get_bot_response(message, second_prompt_list)
    response_arr: list[str] = second_response.split(" ")
    if "Sure! Move on" in second_response or second_response == "there was an error lol..." or "Move on" in second_response or len(response_arr) < 10:
        return -1
    dbSession.update_one({"_id":ObjectId(session)},{'$set':{"dialogue":second_prompt_list}})
    return {
        "text":second_response,
        "sessionID":session
    }

#layer2 functions
def classifyClassInformation(message):
    return "generalInformation"

def trackClassification(message):
    first_prompt_list = ["The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:\nSure thing, here are shorter examples for each of the intents:\n\naiML:\n1) \"I'm excited about machine learning and its potential applications in healthcare.\"\n2) \"I want to learn more about neural networks and their use in natural language processing.\"\n3) \"I'm interested in AI's impact on job automation and want to explore ethical considerations.\"\nrobotics:\n1) \"I love building robots and want to learn more about control systems.\"\n2) \"I'm interested in designing robots for space exploration.\"\n3) \"I want to explore how robotics can be used in agriculture and farming.\"\nethics:\n1) \"I'm interested in the ethics of artificial intelligence.\"\n2) \"I want to explore the ethical considerations of using facial recognition technology.\"\n3) \"I'm interested in the ethical implications of autonomous vehicles.\"\neconComputation:\n1) \"I'm interested in using machine learning to predict financial markets.\"\n2) \"I want to explore the use of blockchain technology in supply chain management.\"\n3) \"I'm interested in using data analysis to identify inefficiencies in business processes.\"\ntheoryOfComputation:\n1) \"I'm fascinated by the concept of computational complexity.\"\n2) \"I want to learn more about automata theory and its applications.\"\n3) \"I'm interested in exploring the limits of what computers can and cannot do.\"\ncomputingInfrastructure:\n1) \"I'm interested in cloud computing and its impact on business operations.\"\n2) \"I want to learn more about distributed systems and their use in large-scale applications.\"\n3) \"I'm interested in exploring the latest advances in networking technology.\"\nsoftwareSystems:\n1) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"\n2) \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\n3) \"I want to design game engines that provide better physics simulation and animation capabilities.\"\n4) \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\n5) \"I want to develop software solutions for industrial automation that can improve efficiency and safety.\"\n6) \"I'm interested in developing software as a service applications that can provide scalable and cost-effective solutions for businesses.\"\nsoftwareDevelopment:\n1) \"I love programming and want to learn more about software development methodologies.\"\n2) \"I'm interested in developing mobile applications for social impact.\"\n3) \"I want to explore how software can be used to improve education and learning.\"\nbioinformatics:\n1) \"I'm interested in using machine learning to analyze genomic data.\"\n2) \"I want to learn more about computational biology and its applications.\"\n3) \"I'm interested in exploring the use of bioinformatics in drug discovery.\"\ncybersecurity:\n1) \"I'm interested in network security and want to learn more about cryptography.\"\n2) \"I want to explore the latest techniques in malware analysis and detection.\"\n3) \"I'm interested in exploring the ethical implications of cyber warfare.\"\nwebTechnologyApplications:\n1) \"I'm interested in developing web applications using the latest front-end frameworks.\"\n2) \"I want to explore the use of web technology in e-commerce and online marketplaces.\"\n3) \"I'm interested in building accessible and inclusive web applications.\"\ngaming:\n1) \"I'm interested in developing video games and want to learn more about game engines.\"\n2) \"I want to explore the intersection of gaming and artificial intelligence.\"\n3) \"I'm excited about the potential of virtual reality and want to explore its applications in gaming.\"\ndataInformation:\n1) \"I'm interested in data analysis and want to learn more about data visualization.\"\n2) \"I want to explore the use of big data in environmental sustainability.\"\n3) \"I'm interested in using data to improve healthcare outcomes.\"\nintroductory:\n1) \"I'm new to computer science and want to learn the basics of programming.\"\n2) \"I'm interested in exploring the different fields within computer science.\"\n3) \"I want to gain a broad understanding of computer science concepts and principles.\"\nelectrical:\n1) \"I'm interested in power electronics and their applications in renewable energy systems.\"\n2) \"I want to learn more about signal processing techniques and their use in audio and image processing.\"\n3) \"I'm fascinated by the principles of control systems and their applications in electrical engineering.\"\nsignalProcessingAndCommunications:\n1) \"I'm interested in exploring the principles of digital signal processing and their applications in communication systems.\"\n2) \"I want to learn more about wireless communication protocols and their use in IoT devices.\"\n3) \"I'm interested in the latest advances in quantum communication and its potential for secure information transfer.\"\n\nThe assistant's job is to classify the user question into one or more of these categories and return as a response ONLY the names of those categories that the prompt fits into (response returned by assistant must be in ALL LOWERCASE, including the first letter. categories should be separated by commas, with no punctuation at the end. the names of the categories should be exactly as given, in camelcase with no spaces between the words themselves. for example, if something is classified in software systems, the returned category should be spelled as softwareSystems)\n\n\nHuman: hello\nAI: Hi there! How can I help you today?\nHuman: i like video games\nAI: Gaming.\nHuman: \nAI: How can I help you?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\n\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: I'm interested in exploring the use of machine learning for music composition.\nAI: AiML, robotics.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: I'm fascinated by the use of gaming for education and training purposes.\nAI: Gaming, software development.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making. AiML, data information, software systems.\nAI: AiML, data information, software systems.\nHuman: no its not software systems\nAI: AiML, data information.\nHuman: \"I want to explore the use of web technology in political activism and social justice movements.\"\nAI: Web technology applications, software development.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\nAI: Software systems.\nHuman: \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\nAI: AiML, software systems.\nHuman: im interested in opertating systems and compiler construction Software systems, theory of computation."]
    first_response: str = first_get_bot_response(message, first_prompt_list)

    first_response = first_response.split('.')
    first_response = ''.join(first_response)

    first_response.replace(" ", "")

    lowcase_arr: list[str] = first_response.split(",")

    x: int = 0
    for y in lowcase_arr:
        print(y + "\n")
        res = lowcase_arr[x][0].lower() + lowcase_arr[x][1:]
        lowcase_arr[x] = str(res)
        print(y + "\n")
        lowcase_arr[x] = lowcase_arr[x].strip()
        print(y + "\n")
        lowcase_arr[x] = lowcase_arr[x].replace(" ", "_")
        lowcase_arr[x] = stringcase.camelcase(lowcase_arr[x])
        x = x + 1

    query = {"labels":{"$in":lowcase_arr}}
    returnClasses = db.find(query)

    newUserSession = dbSession.insert_one({
        "dialogue":["The following is a conversation with an AI assistant that is supposed to help electrical engineering and computer science students select their courses. There will be some information after this that includes information on electrical engineering and computer science courses that are relevant to the student’s interests. This information is extracted from a database, and this is what is in each object: \ntag: class numer (string)\nname: class names (string)\nworkload: how much work it will be, as a percentage (number)\nprereqs: (array of arrays of tags/class names)\ndescription: (string)\nmedianGrade: (string)\nlabels: (array of strings)\ncredits: (number)\\n}\n\nso remember that those are what each thing means for each database object.\n\nThe human/user will not be the first one to chat. It will be you. So based on all the class database objects that will be listed below, you will provide a short and simple recommendation to the user that those are classes they can take. Give the course in the format(EECS [tag]) , then put name of the courses in parentheses next to that first format, and a brief one sentence description of each based on the description string in the object. \n\nsummarize how the workloads of each of the classes compare to each other. Then only after you give them this initial information do you prompt them for more questions. If they ask you about any of the information  in the object, such as the number of credits, median grade, if they have to complete prereqs, look from the database objects about the class they ask about and tell them that information in an informative but casual way. If they want the entire course description, give the description exactly as it is in the database object. \n\nprereqs mean the perquisites for the course, so the courses you must take before taking the course. if they ask about prereqs for a specific course name/number, be sure to look under the prereqs array for that specific corresponding database object and tell them what is in that array.\n\nlabels refer to the categories that the classes are in. so include this in your response for context. If the user want to hear about class numbers that don't match any of the tags of what is under the 'DATABASE OBJECTS' header which will be below, then you should return \"move on\"(all lowercase). you should say 'move on' even if they indicate that they want to hear about other classes. YOU MUST MOVE ON WITHOUT FAIL IF THEY WANT OTHER CLASSES OR IF YOU DON'T HAVE THE CORRESPONDING COURSE DATA!! MAKE SURE YOU DO THIS AND MAKE SURE TO DOUBLE AND TRIPLE CHECK THAT THE CLASSES THE USER IS ASKING FOR IS PART OF THE DATABASE OBJECTS! PRINT 'move on' ONLY THOSE WORDS IN ALL LOWERCASE. \nif they ask about classes that are listed below the header, then you should answer based on all the information from the object and the conversation so far.\n\nDATABASE OBJECTS: \n\n"],
    })
    classesList = []
    for result in returnClasses:
        result["tag"] = int(result["tag"])
        converted = str(int(result["tag"]))
        result["tag"] = converted
        classesList.append("EECS " + converted+" - "+result["name"]+"\n")
    return {
        "classInfo":True,
        "classes":classesList,
        "sessionId":str(newUserSession.inserted_id)
    }

#layer3 functions
def entityExtract(message):
    prompt="""The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. The job of the assistant is to figure out what class/classes the user is trying to learn more information about. From the input, the assistant needs to extract what class the user is talking about.The user can either identify the class using a tag (ex. EECS494, 494, EECS 494) or by the name of the class. The assistant’s job is to return the tag that is corresponding to the class the user is talking about. Here is the list of all tags and their names:

110  -  Discover CS
183  -  Elementary Programming Concepts
200  -  Elec Eng Sys Des I
201  -  Computer Science Pragmatics
203  -  Discrete Mathematics
215  -  Introduction to Electronic Circuits
216  -  Introduction to Signals and Systems
230  -  Engineering Electromagnetics
250  -  Electronic Sensing Systems
270  -  Introduction to Logic Design
280  -  Programming and Introductory Data Structures
281  -  Data Structures and Algorithms
285  -  Practical Programming in Java
300  -  Electrical Engineering Systems Design II
301  -  Probabilistic Methods in Engineering
311  -  Analog Circuits
312  -  Digital Integrated Circuits
314  -  Electrical Circuits, Systems and Applications
320  -  Introduction to Semiconductor Devices
330  -  Introduction to Antennas and Wireless Systems
334  -  Principles of Optics
351  -  Introduction to Digital Signal Processing
367  -  Introduction to Autonomous Robotics
370  -  Introduction to Computer Organization
373  -  Introduction to Embedded System Design
376  -  Foundations of Computer Science
388  -  Introduction to Computer Security
390  -  Programming Paradigms
402  -  Computer Programming for Scientists and Engineers
403  -  Graduate Foundations of Data Structures and Algorithms
409  -  Data Science Seminar
410  -  Patent Fundamentals for Engineers
411  -  Microwave Circuits I
413  -  Monolith Amplifier Circuits
414  -  Intro to MEMS
417  -  Electrical Biophysics
418  -  Power Electronics
419  -  Electric Machinery and Drives
421  -  Properties of Transistors
423  -  Micro / Nano Device Fabrication and Characterization
425  -  Integrated Microsystems Laboratory
427  -  Very Large Scale Integrated Design I
428  -  Introduction to Quantum Nanotechnology
429  -  Semiconductor Optoelectronic Devices
430  -  Radiowave Propagation and LInk Design
434  -  Principles of Photonics
435  -  Fourier Optics
438  -  Advanced Lasers Lab
440  -  System Design of a Search Engine
441  -  Mobile App Development for Entrepreneurs
442  -  Computer Vision
444  -  Analysis of Social Networks
445  -  Introduction to Machine Learning
448  -  Human-Centered ML
449  -  Conversational AI
452  -  Digital Signal Processing Design Laboratory
453  -  Principles of ML
455  -  Wireless Communication Systems
456  -  Internet Foundations
458  -  Biomedical Instrumentation and Design
460  -  Control Systems Analysis and Design
461  -  Embedded Control Systems
463  -  Power Systems Design and Operation
464  -  Hands-on Robotics
465  -  Introduction to Algorithmic Robotics
467  -  Autonomous Robotics Design Experience
470  -  Computer Architecture
471  -  Applied Parallel Programming with GPUs
473  -  Advanced Embedded Systems
475  -  Introduction to Cryptography
476  -  Data Mining
477  -  Introduction to Algorithms
478  -  Logic Circuit Synthesis and Optimization
480  -  Social Computing Systems
481  -  Software Engineering
482  -  Introduction to Operating Systems
483  -  Compiler Construction
484  -  Database Management Systems
485  -  Web Systems
486  -  Informational Retrieval and Web Search
487  -  Introduction to Natural Language Processing
489  -  Computer Networks
490  -  Programming Languages
491  -  Introduction to Distributed Systems
492  -  Introduction to Artificial Intelligence
493  -  User Interface Development
494  -  Computer Game Design and Development
495  -  Software Development for Accessibility
497  -  Human-Centered Software and Design and Development
542  -  Advanced Topics in Computer Vision
543  -  Knowledge-Based Systems
545  -  Machine Learning
550  -  Information Theory
567  -  Robotic Kinematics and Dynamis
568  -  Mobile Robotics
574  -  Computational Complexity
575  -  Advanced Cryptography
586  -  Design and Analysis of Algorithms
595  -  Natural Language Processing

If the user input doesn’t have a tag and has the name of a class instead, the assistant must choose one of the classes above based on similarity. Here are some examples:

Human:"Tell me about EECS270 and 281."
AI: 270, 281
Human:"I am interested in EECS 183.” 
AI:183
Human:"Tell me about the class Web Systems." 
AI:485
Human:"What classes do I need to take before EECS376?" 
AI:376
Human:"What are the prerequisities for EECS 542?" 
AI:542
Human:"What classes are similar to EECS 489?"
AI:489
Human:"What classes are related to EECS494?"
AI:494
Human:"I want to learn more about 445 and 449"
AI:445,449
Human:"I am interested in 281 and EECS370"
AI:281,370
Human:"""
    slash = r'"'
    input = f"{slash}{message}{slash}\n"
    newInst = prompt+input+ "AI: "

    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=newInst,
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    classes = res['choices'][0]['text']
    classes.replace(" ", "")
    classes = classes.split(",")
    int_classes = []
    for numeric_string in classes:
        if (numeric_string != ''):
            int_classes.append(int(float(numeric_string)))
    return int_classes

def handleClassInformationGeneral(message,entities):
    query = {"tag":{"$in":entities}}
    returnClasses = db.find(query)
    yeah: str = ""
    for result in returnClasses: 
        yeah = yeah + str(result)
    newUserSession = {
        "dialogue":["The following is a conversation with an AI assistant that is supposed to help electrical engineering and computer science students select their courses. There will be some information after this that includes information on electrical engineering and computer science courses that are relevant to the student’s interests. This information is extracted from a database, and this is what is in each object: \ntag: class numer (string)\nname: class names (string)\nworkload: how much work it will be, as a percentage (number)\nprereqs: (array of arrays of tags/class names)\ndescription: (string)\nmedianGrade: (string)\nlabels: (array of strings)\ncredits: (number)\\n}\n\nso remember that those are what each thing means for each database object.\n\nThe human/user will not be the first one to chat. It will be you. So based on all the class database objects that will be listed below, you will provide a short and simple recommendation to the user that those are classes they can take. Give the course in the format(EECS [tag]) , then put name of the courses in parentheses next to that first format, and a brief one sentence description of each based on the description string in the object. \n\nsummarize how the workloads of each of the classes compare to each other. Then only after you give them this initial information do you prompt them for more questions. If they ask you about any of the information  in the object, such as the number of credits, median grade, if they have to complete prereqs, look from the database objects about the class they ask about and tell them that information in an informative but casual way. If they want the entire course description, give the description exactly as it is in the database object. \n\nprereqs mean the perquisites for the course, so the courses you must take before taking the course. if they ask about prereqs for a specific course name/number, be sure to look under the prereqs array for that specific corresponding database object and tell them what is in that array.\n\nlabels refer to the categories that the classes are in. so include this in your response for context. If the user wants to hear about class numbers that don't match any of the tags of what is under the 'DATABASE OBJECTS' header which will be below, then you should return \"move on\"(all lowercase). you should say 'move on' even if they indicate that they want to hear about other classes. YOU MUST MOVE ON WITHOUT FAIL IF THEY WANT OTHER CLASSES OR IF YOU DON'T HAVE THE CORRESPONDING COURSE DATA!! MAKE SURE YOU DO THIS AND MAKE SURE TO DOUBLE AND TRIPLE CHECK THAT THE CLASSES THE USER IS ASKING FOR IS PART OF THE DATABASE OBJECTS! PRINT 'move on' ONLY THOSE WORDS IN ALL LOWERCASE. \nif they ask about classes that are listed below the header, then you should answer based on all the information from the object and the conversation so far.\n\nDATABASE OBJECTS: \n\n",yeah],
    }
    second_response: str = second_get_bot_response(message, newUserSession["dialogue"])
    newCreatedSession = dbSession.insert_one(newUserSession)
    return {
        "text":second_response,
        "sessionID":str(newCreatedSession.inserted_id)
    }

def first_get_api_response(prompt):
    text=""
    try: 
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

        choices = response.get('choices')[0]
        text = choices.get('text')
    except Exception as e: 
        print('ERROR: ', e)

    return text

def update_list(message, pl):
    pl.append(message) # list of prompts aka chat so far

def first_create_prompt(message: str, pl: list[str]):
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def first_get_bot_response(message: str, pl: list[str]):
    prompt: str = first_create_prompt(message, pl)
    bot_response: str = first_get_api_response(prompt)

    if bot_response: 
        update_list(bot_response, pl) # adds to chat dialog
        pos: int = bot_response.find('\nAI: ') # we only want what the AI says 
        bot_response = bot_response[pos + 5:] # bc the string above for find is 5 chars
    else: 
        bot_response = 'there was an error lol...' 

    return bot_response

def second_get_api_response(prompt: str):
    text: str | None = None
    
    try: 
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')
        #print(response)
    except Exception as e: 
        print('ERROR: ', e)

    return text

def second_create_prompt(message: str, pl: list[str]):
    p_message: str = f'\nHuman: {message}'
    #watch out for if the below prints extra shit
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def second_get_bot_response(message: str, pl: list[str]):
    prompt: str = second_create_prompt(message, pl)
    bot_response: str = second_get_api_response(prompt)

    if bot_response: 
        update_list(bot_response, pl) # adds to chat dialog
        pos: int = bot_response.find('\nAI: ') # we only want what the AI says 
        bot_response = bot_response[pos + 5:] # bc the string above for find is 5 chars
    else: 
        bot_response = 'there was an error lol...' 

    return bot_response

#main
def lambda_handler(event, context):
    prompt = """"The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:

    Class recommendation:
    1) \"I'm excited about machine learning and its potential applications in healthcare.\"
    2) \"I'm interested in cloud computing and its impact on business operations.\"
    3) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"
    4) \"I want to learn more about computational biology and its applications.\"
    5) \"I'm interested in developing software as a service application that can provide scalable and cost-effective solutions for businesses.\"
    6) \"What class teaches about cyber security and its applications?\"
    7) \"Recommend me a class\"
    8) \"What class should I take next semester?\"
    9) \"What's an easy, fun class to take?\"

    Class information:
    1) \"Tell me about EECS485.\"
    2) \"I am interested in EECS 281.\"
    3) \"Tell me about the class Web Systems.\"
    4) \"What classes do I need to take before EECS485?\"
    5) \"What are the prerequisities for EECS485?\"
    6) \"What classes are similar to 489?\"
    7) \"What classes are related to 489?\"
    8) \"Is 281 a good class?\"
    9) \"Is EECS483 a good class?\"
    9) \"Is EECS 4375 a good class?\"

    Major Requirements and Declaration:
    1) \"What classes do I need to take to graduate?\"
    2) \"What are the graduation requirements?\"
    3) \"What classes do I need to take before declaring the Computer Science major?\"
    4) \"I want to get a Computer Science minor.\"
    5) \"I want to declare in computer science.\"

    General Information
    1) \"What different topics could I explore?\"
    2) \"What can you help me with?\"

    The assistant's job is to classify the user question into one of these categories or none of the above and return as a response ONLY the name of the categories that the prompt fits into (response returned by assistant must be in ALL LOWERCASE, including the first letter. The names of the categories should be exactly as given, in camelcase with no spaces between the words themselves. for example, if something is classified in Major Requirements and Declaration, the returned category should be spelled as majorRequirementsAndDeclaration). Use “none of the above” very sparingly and try your best to put the user question into one of the categories.

    Human: I want to declare for computer science
    AI: majorRequirementsAndDeclaration.
    Human: I want to find some interesting classes
    AI: classRecommendation
    Human: I want to learn more about the class Web Systems
    AI: classInformation
    Human: Tell me about EECS376
    AI: classInformation
    Human: What are the prerequisites for EECS489
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

    message = event["queryStringParameters"]["message"]
    session = event["queryStringParameters"]["session"]
    if session!="false":
        val = classConversation(message,session)
        if val!=-1:
            return val
    
    slash = r'\"'
    input = f"{slash}{message}{slash}\n"
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
    intent = res['choices'][0]['text']

    if "classInformation" in intent:
        response = classInformation(message)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    elif "classRecommendation" in intent:
        response = classRecommendation(message)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    elif "majorRequirementsAndDeclaration" in intent:
        response = majorRequirementsAndDeclaration(message)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    return {
        'statusCode': 200,
        'body': json.dumps("Sorry I can't help you with that.")
    }
