# english_chatbot
A straightforward chatbot designed to be an English learning companion. It utilizes the OpenAI API and aims to maintain natural English conversations while assisting the user in enhancing their conversational skills.

To consume the API, you have two possible endpoints:

-***get_response***: simply returns an object with the chatbot's response (**bot_msg**) and the transcription of the user's message (**user_msg**)

-***get_audio***: this endpoint only supports GET requests, and expects a query param called 'msg'. It converts the string contained in that param to an MP3 audio, and sends it back to the client. For example, is you want to obtain an audio conversion of "Hello world." you should send a request in this way:

**/get_audio?msg=Hello%20world.**

You could pass the bot_msg property obtained earlier so you can convert the chatbot's response into an audio format.
