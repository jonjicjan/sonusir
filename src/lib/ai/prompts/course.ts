export const COURSE_DESCRIPTION_PROMPT = {
    role: "system" as const,
    content: "You are a helpful course description generator. Create engaging and informative course descriptions."
  };
  
  export const generateCoursePrompt = (title: string) => ({
    role: "user" as const,
    content: `Generate a brief, engaging course description for a course titled: ${title}`
  });