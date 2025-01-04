import React, { useState } from 'react';
import { generateCourseDescription } from '../../lib/ai/services/course.service';

export default function CourseForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerateDescription = async () => {
    setLoading(true);
    const generatedDescription = await generateCourseDescription(title);
    setDescription(generatedDescription);
    setLoading(false);
  };

  return (
    <div>
      <h1>Generate Course Description</h1>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter course title"
      />
      <button onClick={handleGenerateDescription} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Description'}
      </button>
      {description && <p>{description}</p>}
    </div>
  );
}
