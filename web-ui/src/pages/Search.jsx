import React, { useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import SearchResults from '../components/SearchResults';
import SearchFilters from '../components/SearchFilters';

const Search = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({});

  const { data: results, isLoading, error } = useQuery(
    ['search', query, filters],
    async () => {
      if (!query) return [];
      const response = await axios.get('/api/search', {
        params: { query, ...filters }
      });
      return response.data;
    },
    {
      enabled: !!query,
    }
  );

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <div className="mt-1 relative rounded-md shadow-sm">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="focus:ring-primary-500 focus:border-primary-500 block w-full pl-4 pr-12 sm:text-sm border-gray-300 rounded-md"
            placeholder="Search slides..."
          />
        </div>
      </div>

      <div className="flex gap-8">
        <div className="w-64">
          <SearchFilters filters={filters} onFilterChange={setFilters} />
        </div>
        <div className="flex-1">
          <SearchResults results={results} isLoading={isLoading} error={error} />
        </div>
      </div>
    </div>
  );
};

export default Search; 