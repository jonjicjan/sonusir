import React, { useState } from 'react';
import { supabase } from '../lib/supabase';
import { LogOut, LogIn } from 'lucide-react';
import { FaGraduationCap } from 'react-icons/fa'; // Importing the graduation cap icon
import AuthForm from './AuthForm';

interface NavbarProps {
  user: any;
}

export default function Navbar({ user }: NavbarProps) {
  const [isModalOpen, setIsModalOpen] = useState(false); // State to control modal visibility

  const handleSignOut = async () => {
    await supabase.auth.signOut();
  };

  const handleSignIn = () => {
    setIsModalOpen(true); // Show the modal when Sign In is clicked
  };

  const closeModal = () => {
    setIsModalOpen(false); // Close the modal
  };

  return (
    <nav className="bg-black shadow-lg fixed top-0 left-0 w-full z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <FaGraduationCap className="w-8 h-8 text-purple-600" /> {/* Using react-icons */}
            <span className="ml-2 text-xl font-bold text-white">Learning Hub</span>
          </div>
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-white">Welcome, {user.email}</span>
                <button
                  onClick={handleSignOut}
                  className="flex items-center text-white hover:text-purple-700"
                >
                  <LogOut className="w-4 h-4 mr-1" />
                  Sign Out
                </button>
              </>
            ) : (
              <button
                onClick={handleSignIn}
                className="flex items-center text-white hover:text-purple-700"
              >
                <LogIn className="w-4 h-4 mr-2" /> Sign In
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Sliding Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="w-full max-w-lg bg-white p-6 rounded-lg transform transition-all duration-300 ease-in-out">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Sign In</h2>
            <p className="text-gray-600 mb-4">Please log in to access the platform.</p>
            {/* Pass closeModal as prop to AuthForm */}
            <AuthForm closeModal={closeModal} />
            <div className="flex justify-end mt-4">
              <button
                onClick={closeModal}
                className="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
