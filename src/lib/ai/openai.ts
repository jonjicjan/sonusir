import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,  // API key from environment variable
  dangerouslyAllowBrowser: true  // Allow browser usage, though not recommended for production
});

export async function generateCourseDescription(title: string): Promise<string> {
  try {
    const completion = await openai.chat.completions.create({
      messages: [
        {
          role: "system",
          content: "You are a helpful course description generator. Create engaging and informative course descriptions."
        },
        {
          role: "user",
          content: `Generate a brief, engaging course description for a course titled: ${title}`
        }
      ],
      model: "gpt-3.5-turbo",  // Using GPT-3.5 model
    });

    return completion.choices[0]?.message?.content || '';  // Return the generated description or an empty string if no content
  } catch (error) {
    console.error('Error generating course description:', error);
    return '';  // Return empty string in case of an error
  }
}
