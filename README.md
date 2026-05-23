This is a email agent, that parses through the email sent by a user then uses openAI to extract what the user wants to ask.
Then it decides if the question can be answered using the existing documents or if it needs human intervention.
Once it decides Human intervention it sends an email to the user saying someone will get back to them otherwise it goes through a RAG cgain and gets the relevant information the user asked for.
after this it writes an email for the user with the answer and sends it using sendgrid.
