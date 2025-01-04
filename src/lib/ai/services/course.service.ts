import { openai } from '../config';
import { COURSE_DESCRIPTION_PROMPT, generateCoursePrompt } from '../prompts/course';

export async function generateCourseDescription(title: string): Promise<string> {
  try {
    const completion = await openai.chat.completions.create({
      messages: [
        COURSE_DESCRIPTION_PROMPT,
        generateCoursePrompt(title)
      ],
      model: "gpt-3.5-turbo",
    });

    return completion.choices[0]?.message?.content || '';
  } catch (error: any) {
    // Handle rate limit error specifically
    if (error?.status === 429) {
      throw new Error('AI service is currently unavailable due to rate limiting. Please try again in a few minutes.');
    }
    console.error('Error generating course description:', error);
    throw new Error('Failed to generate description. Please try again.');
  }
}