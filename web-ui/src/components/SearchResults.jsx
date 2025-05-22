import React from 'react';

const SearchResults = ({ results, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
        <p className="mt-4 text-gray-600">Searching...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        Error loading search results. Please try again.
      </div>
    );
  }

  if (!results?.length) {
    return (
      <div className="text-center py-12 text-gray-600">
        No results found. Try different search terms.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {results.map((result) => (
        <div
          key={result.id}
          className="bg-white shadow rounded-lg overflow-hidden"
        >
          <div className="p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">
                Slide {result.slideNumber}
              </h3>
              <span className="text-sm text-gray-500">
                Presentation: {result.presentationId}
              </span>
            </div>
            <p className="mt-2 text-gray-600">{result.content}</p>
            {result.imageUrl && (
              <img
                src={result.imageUrl}
                alt={`Slide ${result.slideNumber}`}
                className="mt-4 rounded-lg max-w-full h-auto"
              />
            )}
            {result.topics?.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {result.topics.map((topic) => (
                  <span
                    key={topic}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default SearchResults; 