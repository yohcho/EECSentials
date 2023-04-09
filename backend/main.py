import openai
import stringcase
import pymongo


with open('hidden.txt') as file: 
    openai.api_key = file.read()



def first_get_api_response(prompt: str) -> str | None:
    text: str | None = None
    
    try: 
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
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

def update_list(message: str, pl: list[str]):
    pl.append(message) # list of prompts aka chat so far

def first_create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def first_get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = first_create_prompt(message, pl)
    bot_response: str = first_get_api_response(prompt)

    if bot_response: 
        update_list(bot_response, pl) # adds to chat dialog
        pos: int = bot_response.find('\nAI: ') # we only want what the AI says 
        bot_response = bot_response[pos + 5:] # bc the string above for find is 5 chars
    else: 
        bot_response = 'there was an error lol...' 

    return bot_response


#SECOND LAYER FOR TRACK CLASSIFICATION - GENERATING RESPONSE BASED ON DB QUERY

def second_get_api_response(prompt: str) -> str | None:
    text: str | None = None
    
    try: 
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
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

def second_create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    #watch out for if the below prints extra shit
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def second_get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = second_create_prompt(message, pl)
    bot_response: str = second_get_api_response(prompt)

    if bot_response: 
        update_list(bot_response, pl) # adds to chat dialog
        pos: int = bot_response.find('\nAI: ') # we only want what the AI says 
        bot_response = bot_response[pos + 5:] # bc the string above for find is 5 chars
    else: 
        bot_response = 'there was an error lol...' 

    return bot_response

def main():
    #below is essentially the training data (what we'd test out in openAI Playground)
    first_prompt_list: list[str] = ["The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:\nSure thing, here are shorter examples for each of the intents:\n\naiML:\n1) \"I'm excited about machine learning and its potential applications in healthcare.\"\n2) \"I want to learn more about neural networks and their use in natural language processing.\"\n3) \"I'm interested in AI's impact on job automation and want to explore ethical considerations.\"\nrobotics:\n1) \"I love building robots and want to learn more about control systems.\"\n2) \"I'm interested in designing robots for space exploration.\"\n3) \"I want to explore how robotics can be used in agriculture and farming.\"\nethics:\n1) \"I'm interested in the ethics of artificial intelligence.\"\n2) \"I want to explore the ethical considerations of using facial recognition technology.\"\n3) \"I'm interested in the ethical implications of autonomous vehicles.\"\neconComputation:\n1) \"I'm interested in using machine learning to predict financial markets.\"\n2) \"I want to explore the use of blockchain technology in supply chain management.\"\n3) \"I'm interested in using data analysis to identify inefficiencies in business processes.\"\ntheoryOfComputation:\n1) \"I'm fascinated by the concept of computational complexity.\"\n2) \"I want to learn more about automata theory and its applications.\"\n3) \"I'm interested in exploring the limits of what computers can and cannot do.\"\ncomputingInfrastructure:\n1) \"I'm interested in cloud computing and its impact on business operations.\"\n2) \"I want to learn more about distributed systems and their use in large-scale applications.\"\n3) \"I'm interested in exploring the latest advances in networking technology.\"\nsoftwareSystems:\n1) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"\n2) \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\n3) \"I want to design game engines that provide better physics simulation and animation capabilities.\"\n4) \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\n5) \"I want to develop software solutions for industrial automation that can improve efficiency and safety.\"\n6) \"I'm interested in developing software as a service applications that can provide scalable and cost-effective solutions for businesses.\"\nsoftwareDevelopment:\n1) \"I love programming and want to learn more about software development methodologies.\"\n2) \"I'm interested in developing mobile applications for social impact.\"\n3) \"I want to explore how software can be used to improve education and learning.\"\nbioinformatics:\n1) \"I'm interested in using machine learning to analyze genomic data.\"\n2) \"I want to learn more about computational biology and its applications.\"\n3) \"I'm interested in exploring the use of bioinformatics in drug discovery.\"\ncybersecurity:\n1) \"I'm interested in network security and want to learn more about cryptography.\"\n2) \"I want to explore the latest techniques in malware analysis and detection.\"\n3) \"I'm interested in exploring the ethical implications of cyber warfare.\"\nwebTechnologyApplications:\n1) \"I'm interested in developing web applications using the latest front-end frameworks.\"\n2) \"I want to explore the use of web technology in e-commerce and online marketplaces.\"\n3) \"I'm interested in building accessible and inclusive web applications.\"\ngaming:\n1) \"I'm interested in developing video games and want to learn more about game engines.\"\n2) \"I want to explore the intersection of gaming and artificial intelligence.\"\n3) \"I'm excited about the potential of virtual reality and want to explore its applications in gaming.\"\ndataInformation:\n1) \"I'm interested in data analysis and want to learn more about data visualization.\"\n2) \"I want to explore the use of big data in environmental sustainability.\"\n3) \"I'm interested in using data to improve healthcare outcomes.\"\nintroductory:\n1) \"I'm new to computer science and want to learn the basics of programming.\"\n2) \"I'm interested in exploring the different fields within computer science.\"\n3) \"I want to gain a broad understanding of computer science concepts and principles.\"\nelectrical:\n1) \"I'm interested in power electronics and their applications in renewable energy systems.\"\n2) \"I want to learn more about signal processing techniques and their use in audio and image processing.\"\n3) \"I'm fascinated by the principles of control systems and their applications in electrical engineering.\"\nsignalProcessingAndCommunications:\n1) \"I'm interested in exploring the principles of digital signal processing and their applications in communication systems.\"\n2) \"I want to learn more about wireless communication protocols and their use in IoT devices.\"\n3) \"I'm interested in the latest advances in quantum communication and its potential for secure information transfer.\"\n\nThe assistant's job is to classify the user question into one or more of these categories and return as a response ONLY the names of those categories that the prompt fits into (response returned by assistant must be in ALL LOWERCASE, including the first letter. categories should be separated by commas, with no punctuation at the end. the names of the categories should be exactly as given, in camelcase with no spaces between the words themselves. for example, if something is classified in software systems, the returned category should be spelled as softwareSystems)\n\n\nHuman: hello\nAI: Hi there! How can I help you today?\nHuman: i like video games\nAI: Gaming.\nHuman: \nAI: How can I help you?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\n\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: I'm interested in exploring the use of machine learning for music composition.\nAI: AiML, robotics.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: I'm fascinated by the use of gaming for education and training purposes.\nAI: Gaming, software development.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making. AiML, data information, software systems.\nAI: AiML, data information, software systems.\nHuman: no its not software systems\nAI: AiML, data information.\nHuman: \"I want to explore the use of web technology in political activism and social justice movements.\"\nAI: Web technology applications, software development.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\nAI: Software systems.\nHuman: \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\nAI: AiML, software systems.\nHuman: im interested in opertating systems and compiler construction Software systems, theory of computation."]

    while True: 
        user_input: str = input('You: ') 
        first_response: str = first_get_bot_response(user_input, first_prompt_list)

        print(first_prompt_list)
        print(first_response)
        
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

        print(lowcase_arr)

        # for final response

        # PLAN:  
        #          1)first output a list of ALL the EECS classes returned by the query(based on label(s)) 
        #            and the class names (hardcoding).
        #          2)prompt user for which class numbers they would like to hear more about(this will be max 5)
        #          3)query those classes from DB
        #          4)send the DB objects of ONLY those classes to openai API
        #          5)have bot ask what they would like to know more about
        #          6)user continues conversation with ai and asks whatever questions it wants
        #               - if user wants to hear about other classes, we will have openai API return a "move on" response,
        #                 and then we will come out of the openai dialgue and return to step 2, and repeat
        
        
        #STEP 1 - list output of all eecs according to labels

        myclient = pymongo.MongoClient("mongodb+srv://yohcho:qw123edc@cluster0.ggonojo.mongodb.net/?retryWrites=true&w=majority")
        db = myclient["EECSentials"]["Class"]

        query = {"labels":{"$in":lowcase_arr}}
        example = db.find(query)

        for result in example:
            result["tag"] = int(result["tag"])
            converted = str(int(result["tag"]))
            result["tag"] = converted
            print(("EECS " + converted), " - ", result["name"], ("\n"))


        repeat: str = "f"
        while repeat == "f": 

            print("List out course numbers of classes you would like to hear more about! (up to 5)")
        
            user_input: str = input('You: ') 

            user_input.replace(" ", "")

            classes: list[str] = user_input.split(",")


           
            int_classes: list[int] = []
            for numeric_string in classes:
                print(numeric_string)
                if (numeric_string != ''):
                    int_classes.append(int(float(numeric_string)))
            print(int_classes)

            query = {"tag":{"$in":int_classes}}
            example: str = list(db.find(query))

            yeah: str = ""
            print("about to print from query")
            for result in example: 
                yeah = yeah + str(result)
                print(yeah)

            #tiki = example.toString()

            repeat = "t"
            second_prompt_list: list[str] = ["The following is a conversation with an AI assistant that is supposed to help electrical engineering and computer science students select their courses. There will be some information after this that includes information on electrical engineering and computer science courses that are relevant to the student’s interests. This information is extracted from a database, and this is what is in each object: \ntag: class numer (string)\nname: class names (string)\nworkload: how much work it will be, as a percentage (number)\nprereqs: (array of arrays of tags/class names)\ndescription: (string)\nmedianGrade: (string)\nlabels: (array of strings)\ncredits: (number)\\n}\n\nso remember that those are what each thing means for each database object.\n\nThe human/user will not be the first one to chat. It will be you. So based on all the class database objects that will be listed below, you will provide a short and simple recommendation to the user that those are classes they can take. Give the course in the format(EECS [tag]) , then put name of the courses in parentheses next to that first format, and a brief one sentence description of each based on the description string in the object. \n\nsummarize how the workloads of each of the classes compare to each other. Then only after you give them this initial information do you prompt them for more questions. Ask the user if they would like to hear more specific information. If they ask you about any of the information  in the object, such as the number of credits, median grade, if they have to complete prereqs, look from the database objects about the class they ask about and tell them that information in an informative but casual way. If they want the entire course description, give the description exactly as it is in the database object. \n\nprereqs mean the perquisites for the course, so the courses you must take before taking the course. if they ask about prereqs for a specific course name/number, be sure to look under the prereqs array for that specific corresponding database object and tell them what is in that array.\n\nlabels refer to the categories that the classes are in. so include this in your response for context. After your first response, ask if they would like to hear more about the classes you listed, or if they want to hear about other classes you haven't listed. If they want to hear about classes that are not under the 'DATABASE OBJECTS' header which will be below, then you should return \"move on\"(all lowercase). you should say 'move on' even if they indicate that they want to hear about other classes. YOU MUST MOVE ON WITHOUT FAIL IF THEY WANT OTHER CLASSES!! MAKE SURE YOU DO THIS! PRINT 'move on' ONLY THOSE WORDS IN ALL LOWERCASE. \nif they ask about classes that are listed below the header, then you should answer based on all the information from the object and the conversation so far.\n\nDATABASE OBJECTS: \n\n"]
            second_prompt_list.append(yeah)
            print(second_prompt_list)

            while True: 
                
                second_response: str = second_get_bot_response(user_input, second_prompt_list)

                if second_response == "Sure! Move on" or second_response == "there was an error lol..." or second_response == "Move on.":
                    repeat = "f"
                    break
                print(second_response)
                user_input: str = input('You: ')
            

            second_prompt_list = second_prompt_list.remove(yeah)

        #if user_input == 'yes':
            
        #print(f'Bot: {first_response}')
        #print(prompt_list)

    #second_prompt_list: list[str] = "this will be the trainng data for the second layer"


if __name__ == '__main__':
    main()
