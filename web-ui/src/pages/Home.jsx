import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to SlideSearch
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Search through your presentation slides with AI-powered semantic search
        </p>
        <div className="space-x-4">
          <Link
            to="/search"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            Start Searching
          </Link>
          <Link
            to="/upload"
            className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Upload Slides
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home; 