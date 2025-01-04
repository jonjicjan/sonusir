import React, { useState } from 'react';
import Loader from './Loader'; // Import the loader component
import AIChatModal from './AIChatModal';

interface AIAssistantProps {
  onDescriptionGenerated: (description: string) => void;
  courseTitle: string;
}

export default function AIAssistant({ onDescriptionGenerated, courseTitle }: AIAssistantProps) {
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="mt-2 relative">
      <button
        onClick={() => setShowChat(true)}
        className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 relative z-10"
      >
        Generate AI Description
      </button>

      {/* Display the loader behind the button */}
      {showChat && (
        <div className="absolute inset-0 flex items-center justify-center z-0">
          <Loader />
        </div>
      )}

      {showChat && (
        <AIChatModal
          onClose={() => setShowChat(false)}
          onDescriptionGenerated={(desc) => {
            onDescriptionGenerated(desc);
            setShowChat(false);
          }}
          courseTitle={courseTitle}
        />
      )}
    </div>
  );
}
