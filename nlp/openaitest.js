const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  apiKey: "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",
});
const openai = new OpenAIApi(configuration);

const chat = async()=>{
    const response = await openai.createCompletion({
        model: "text-davinci-003",
        prompt: `
            Classify the intent of the text that you receive into one of the following categories: 
              Searching for a class, 
              Asking about a class
              None of the above

            "What classes can I take this upcoming semester?"
        `,
        temperature: 0.7,
        max_tokens: 256,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0,
      });
      
    console.log(response.data.choices[0].text.trim())
}

chat()

