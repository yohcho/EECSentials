import openai

openai.api_key = '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'



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

def first_update_list(message: str, pl: list[str]):
    pl.append(message) # list of prompts aka chat so far

def first_create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    first_update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def first_get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = first_create_prompt(message, pl)
    bot_response: str = first_get_api_response(prompt)

    if bot_response: 
        first_update_list(bot_response, pl) # adds to chat dialog
        pos: int = bot_response.find('\nAI: ') # we only want what the AI says 
        bot_response = bot_response[pos + 5:] # bc the string above for find is 5 chars
    else: 
        bot_response = 'there was an error lol...' 

    return bot_response

def main():
    #below is essentially the training data (what we'd test out in openAI Playground)
    prompt_list: list[str] = ["The following is a conversation with an AI assistant. The assistant is designed to help students pick electrical engineering/computer science courses. Here is a list of intents and example user prompts:\nSure thing, here are shorter examples for each of the intents:\n\naiML:\n1) \"I'm excited about machine learning and its potential applications in healthcare.\"\n2) \"I want to learn more about neural networks and their use in natural language processing.\"\n3) \"I'm interested in AI's impact on job automation and want to explore ethical considerations.\"\nrobotics:\n1) \"I love building robots and want to learn more about control systems.\"\n2) \"I'm interested in designing robots for space exploration.\"\n3) \"I want to explore how robotics can be used in agriculture and farming.\"\nethics:\n1) \"I'm interested in the ethics of artificial intelligence.\"\n2) \"I want to explore the ethical considerations of using facial recognition technology.\"\n3) \"I'm interested in the ethical implications of autonomous vehicles.\"\neconComputation:\n1) \"I'm interested in using machine learning to predict financial markets.\"\n2) \"I want to explore the use of blockchain technology in supply chain management.\"\n3) \"I'm interested in using data analysis to identify inefficiencies in business processes.\"\ntheoryOfComputation:\n1) \"I'm fascinated by the concept of computational complexity.\"\n2) \"I want to learn more about automata theory and its applications.\"\n3) \"I'm interested in exploring the limits of what computers can and cannot do.\"\ncomputingInfrastructure:\n1) \"I'm interested in cloud computing and its impact on business operations.\"\n2) \"I want to learn more about distributed systems and their use in large-scale applications.\"\n3) \"I'm interested in exploring the latest advances in networking technology.\"\nsoftwareSystems:\n1) \"I want to develop an operating system for embedded systems that is optimized for power efficiency.\"\n2) \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\n3) \"I want to design game engines that provide better physics simulation and animation capabilities.\"\n4) \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\n5) \"I want to develop software solutions for industrial automation that can improve efficiency and safety.\"\n6) \"I'm interested in developing software as a service applications that can provide scalable and cost-effective solutions for businesses.\"\nsoftwareDevelopment:\n1) \"I love programming and want to learn more about software development methodologies.\"\n2) \"I'm interested in developing mobile applications for social impact.\"\n3) \"I want to explore how software can be used to improve education and learning.\"\nbioinformatics:\n1) \"I'm interested in using machine learning to analyze genomic data.\"\n2) \"I want to learn more about computational biology and its applications.\"\n3) \"I'm interested in exploring the use of bioinformatics in drug discovery.\"\ncybersecurity:\n1) \"I'm interested in network security and want to learn more about cryptography.\"\n2) \"I want to explore the latest techniques in malware analysis and detection.\"\n3) \"I'm interested in exploring the ethical implications of cyber warfare.\"\nwebTechnologyApplications:\n1) \"I'm interested in developing web applications using the latest front-end frameworks.\"\n2) \"I want to explore the use of web technology in e-commerce and online marketplaces.\"\n3) \"I'm interested in building accessible and inclusive web applications.\"\ngaming:\n1) \"I'm interested in developing video games and want to learn more about game engines.\"\n2) \"I want to explore the intersection of gaming and artificial intelligence.\"\n3) \"I'm excited about the potential of virtual reality and want to explore its applications in gaming.\"\ndataInformation:\n1) \"I'm interested in data analysis and want to learn more about data visualization.\"\n2) \"I want to explore the use of big data in environmental sustainability.\"\n3) \"I'm interested in using data to improve healthcare outcomes.\"\nintroductory:\n1) \"I'm new to computer science and want to learn the basics of programming.\"\n2) \"I'm interested in exploring the different fields within computer science.\"\n3) \"I want to gain a broad understanding of computer science concepts and principles.\"\nelectrical:\n1) \"I'm interested in power electronics and their applications in renewable energy systems.\"\n2) \"I want to learn more about signal processing techniques and their use in audio and image processing.\"\n3) \"I'm fascinated by the principles of control systems and their applications in electrical engineering.\"\nsignalProcessingAndCommunications:\n1) \"I'm interested in exploring the principles of digital signal processing and their applications in communication systems.\"\n2) \"I want to learn more about wireless communication protocols and their use in IoT devices.\"\n3) \"I'm interested in the latest advances in quantum communication and its potential for secure information transfer.\"\n\nThe assistant's job is to classify the user question into one or more of these categories and return as a response ONLY the names of those categories that the prompt fits into (response returned by assistant must be in ALL LOWERCASE, including the first letter. categories separated by commas, with no punctuation at the end)\n\n\nHuman: hello\nAI: Hi there! How can I help you today?\nHuman: i like video games\nAI: Gaming.\nHuman: \nAI: How can I help you?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\n\nAI: Gaming, robotics.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: i like playing video games and also robot stuff is cool i want to take classes that help me explore that\nAI: Gaming, robotics.\nHuman: I'm interested in exploring the use of machine learning for music composition.\nAI: AiML, robotics.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: I'm fascinated by the use of gaming for education and training purposes.\nAI: Gaming, software development.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making.\nAI: AiML, data information, software systems.\nHuman: \nAI: Is there anything else I can help you with?\nHuman: I want to explore the use of data analysis in understanding human behavior and decision-making. AiML, data information, software systems.\nAI: AiML, data information, software systems.\nHuman: no its not software systems\nAI: AiML, data information.\nHuman: \"I want to explore the use of web technology in political activism and social justice movements.\"\nAI: Web technology applications, software development.\nHuman: \"I'm interested in the use of edge computing to improve IoT device performance.\"\nAI: Computing infrastructure, software systems.\nHuman: \"I'm interested in developing software solutions for improving the performance of computational science simulations.\"\nAI: Software systems.\nHuman: \"I'm interested in exploring the use of AI in search engine algorithms to improve the relevance of search results.\"\nAI: AiML, software systems.\nHuman: im interested in opertating systems and compiler construction Software systems, theory of computation."]

    while True: 
        user_input: str = input('You: ') 
        response: str = first_get_bot_response(user_input, prompt_list)
        print(f'Bot: {response}')
        #print(prompt_list)


if __name__ == '__main__':
    main()