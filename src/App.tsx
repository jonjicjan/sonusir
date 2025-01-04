import React, { useEffect, useState } from 'react';
import { supabase } from './lib/supabase';
import Navbar from './components/Navbar';
import AuthForm from './components/AuthForm';
import Course from './components/Course';
import { ReactTyped } from 'react-typed'; // Import ReactTyped
import Footer from './components/Footer'; // Import the Footer component
import  './Course.css';



function App() {
  const [user, setUser] = useState<any>(null);
  const [courses, setCourses] = useState<any[]>([]);



  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (user) {
      fetchCourses();

      const subscription = supabase
        .channel('courses')
        .on('postgres_changes', { event: '*', schema: 'public', table: 'courses' }, () => {
          fetchCourses();
        })
        .subscribe();

      return () => {
        subscription.unsubscribe();
      };
    }
  }, [user]);

  const fetchCourses = async () => {
    const { data, error } = await supabase
      .from('courses')
      .select(`
        *,
        profiles:instructor_id (
          full_name
        )
      `)
      .order('created_at', { ascending: false });

    if (!error && data) {
      setCourses(data);
    }
  };

  const handleViewAllCoursesClick = () => {
    if (!user) {
      alert('Please logged in to explore more');
    } else {
      // Redirect to courses page or load more courses
      console.log('Redirecting to courses page...');
    }
  };

  return (
    
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        {!user ? (
          <div className="flex flex-col items-center justify-center min-h-screen">
            <section className="py-12 bg-white text-center" id="courses">
              <h2 className="text-3xl font-bold text-purple-900 mb-6">Welcome to Learning Hub! AI-Powered Learning, Crafted for Your Success. </h2>
              <p className="text-lg text-gray-600 mb-8">
                Check out some of our most popular courses available now.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://www.simplilearn.com/ice9/free_resources_article_thumb/is_web_development_good_career.jpg"
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">Web Development</h3>
                  <p className="text-gray-600">Learn the fundamentals of web development, from building responsive and interactive websites to creating dynamic web applications. </p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>
                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://media.istockphoto.com/id/1452604857/photo/businessman-touching-the-brain-working-of-artificial-intelligence-automation-predictive.jpg?s=612x612&w=0&k=20&c=GkAOxzduJbUKpS2-LX_l6jSKtyhdKlnPMo2ito4xpR4="
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">AI & ML</h3>
                  <p className="text-gray-600">Learn the fundamentals of AI and Machine Learning to build smart, data-driven applications and systems that can think, learn, and make decisions.</p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>
                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://www.simplilearn.com/ice9/free_resources_article_thumb/what_is_aws.jpg"
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">AWS</h3>
                  <p className="text-gray-600">Master cloud computing with AWS and gain hands-on experience in deploying and managing applications and services on the world’s most widely used cloud platform.</p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>
                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://miro.medium.com/v2/resize:fit:1076/1*Q8kco_pkEiBHa59rNxVlkQ.png"
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">DevOPs</h3>
                  <p className="text-gray-600">Learn the essential practices of DevOps to streamline software development and operations, enabling faster releases through automation and collaboration.</p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>

                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://www.careerpower.in/blog/wp-content/uploads/sites/2/2023/07/21160517/Computer-Network.png"
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">Networking</h3>
                  <p className="text-gray-600">Understand the core principles of networking, from setting up networks to troubleshooting and ensuring seamless communication between devices and systems across the globe.</p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>

                <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
                  <img
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrzbgya8qpotyQsbDnuw6hno1nUeShpC_A-SyHaMTEGRcpFoO7DcVO0P89_DGVh5egbtg&usqp=CAU"
                    alt="Course"
                    className="w-full h-56 object-cover rounded-t-lg"
                  />
                  <h3 className="text-xl font-semibold mt-4">Cyber Security</h3>
                  <p className="text-gray-600">Dive into the world of cybersecurity and learn how to protect systems, networks, and data from malicious attacks, ensuring the safety and privacy of digital assets.</p>
                  <a href="#"  onClick={handleViewAllCoursesClick} className="text-purple-700 font-semibold">Learn More</a>
                </div>
              </div>
              
              <a
                href="#course"
                onClick={handleViewAllCoursesClick} // Handle the view all click event
                className="mt-6 inline-block text-xl text-purple-700 font-semibold"
              >
                View All Courses
              </a>
            </section>
            <AuthForm />
          </div>
        ) : (
          <div>
            <div className="headingtext flex justify-center items-center mb-8">
              <div className="min-h-[3rem] flex items-center">
                <ReactTyped
                  strings={[
                    'Available Courses', 'Learn New Skills', 'Advance Your Career', 'Join Our Community'
                  ]}
                  typeSpeed={60}
                  backSpeed={40}
                  backDelay={2000}
                  loop
                  className="text-3xl font-bold text-purple-800 text-center"
                />
              </div>
            </div>
            <Course />
          </div>
        )}
      </main>

      <Footer /> {/* Footer stays fixed at the bottom */}
    </div>
  );
}

export default App;
