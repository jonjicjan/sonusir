import { supabase } from '../supabase';

interface CreateCourseData {
  title: string;
  description: string;
  imageUrl?: string;
}

export async function createCourse({ title, description, imageUrl }: CreateCourseData) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) throw new Error('Not authenticated');

  const { error } = await supabase
    .from('courses')
    .insert([
      {
        title,
        description,
        image_url: imageUrl,
        instructor_id: user.id,
      },
    ]);

  if (error) throw error;
}